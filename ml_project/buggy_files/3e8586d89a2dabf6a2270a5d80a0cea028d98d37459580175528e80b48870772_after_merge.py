    def _match_manifests(self, read_manifest, expected_manifest, reference):
        if read_manifest is None or read_manifest != expected_manifest:
            raise ConanException("%s local cache package is corrupted: "
                                 "some file hash doesn't match manifest"
                                 % (str(reference)))