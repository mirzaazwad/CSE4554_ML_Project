def checkout(
    self,
    targets=None,
    with_deps=False,
    force=False,
    relink=False,
    recursive=False,
    allow_missing=False,
):
    from dvc.stage.exceptions import (
        StageFileBadNameError,
        StageFileDoesNotExistError,
    )

    unused = []
    stats = {
        "added": [],
        "deleted": [],
        "modified": [],
        "failed": [],
    }
    if not targets:
        targets = [None]
        unused = _get_unused_links(self)

    stats["deleted"] = [_fspath_dir(u) for u in unused]
    self.state.remove_links(unused)

    if isinstance(targets, str):
        targets = [targets]

    pairs = set()
    for target in targets:
        try:
            pairs.update(
                self.collect_granular(
                    target, with_deps=with_deps, recursive=recursive
                )
            )
        except (
            StageFileDoesNotExistError,
            StageFileBadNameError,
            NoOutputOrStageError,
        ) as exc:
            if not target:
                raise
            raise CheckoutErrorSuggestGit(target) from exc

    total = get_all_files_numbers(pairs)
    with Tqdm(
        total=total, unit="file", desc="Checkout", disable=total == 0
    ) as pbar:
        for stage, filter_info in pairs:
            result = stage.checkout(
                force=force,
                progress_callback=pbar.update_msg,
                relink=relink,
                filter_info=filter_info,
                allow_missing=allow_missing,
            )
            for key, items in result.items():
                stats[key].extend(_fspath_dir(path) for path in items)

    if stats.get("failed"):
        raise CheckoutError(stats["failed"], stats)

    del stats["failed"]
    return stats