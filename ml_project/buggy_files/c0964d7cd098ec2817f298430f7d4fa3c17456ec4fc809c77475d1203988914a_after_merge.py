def _make_repo(repo_url, rev=None):
    if not repo_url or os.path.exists(repo_url):
        assert rev is None, "Custom revision is not supported for local repo"
        yield Repo(repo_url)
    else:
        with external_repo(url=repo_url, rev=rev) as repo:
            yield repo