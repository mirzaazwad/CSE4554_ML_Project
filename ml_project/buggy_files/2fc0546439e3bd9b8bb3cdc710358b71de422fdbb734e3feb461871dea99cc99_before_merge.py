    def _walk(b_path, b_top_level_dir):
        is_root = b_path == b_top_level_dir

        for b_item in os.listdir(b_path):
            b_abs_path = os.path.join(b_path, b_item)
            b_rel_base_dir = b'' if b_path == b_top_level_dir else b_path[len(b_top_level_dir) + 1:]
            rel_path = to_text(os.path.join(b_rel_base_dir, b_item), errors='surrogate_or_strict')

            if os.path.isdir(b_abs_path):
                if any(b_item == b_path for b_path, root_only in b_ignore_dirs
                       if not root_only or root_only == is_root):
                    display.vvv("Skipping '%s' for collection build" % to_text(b_abs_path))
                    continue

                if os.path.islink(b_abs_path):
                    b_link_target = os.path.realpath(b_abs_path)

                    if not b_link_target.startswith(b_top_level_dir):
                        display.warning("Skipping '%s' as it is a symbolic link to a directory outside the collection"
                                        % to_text(b_abs_path))
                        continue

                manifest_entry = entry_template.copy()
                manifest_entry['name'] = rel_path
                manifest_entry['ftype'] = 'dir'

                manifest['files'].append(manifest_entry)

                _walk(b_abs_path, b_top_level_dir)
            else:
                if b_item == b'galaxy.yml':
                    continue
                elif any(fnmatch.fnmatch(b_item, b_pattern) for b_pattern, root_only in b_ignore_files
                         if not root_only or root_only == is_root):
                    display.vvv("Skipping '%s' for collection build" % to_text(b_abs_path))
                    continue

                manifest_entry = entry_template.copy()
                manifest_entry['name'] = rel_path
                manifest_entry['ftype'] = 'file'
                manifest_entry['chksum_type'] = 'sha256'
                manifest_entry['chksum_sha256'] = secure_hash(b_abs_path, hash_func=sha256)

                manifest['files'].append(manifest_entry)