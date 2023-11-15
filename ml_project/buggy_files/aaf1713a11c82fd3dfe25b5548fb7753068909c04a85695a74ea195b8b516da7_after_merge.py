    def get_files_completion(self):
        """ Returns a list of filename, progress tuples indicating the progress
        for every file selected using set_selected_files. Progress is a float
        between 0 and 1
        """
        completion = []

        if self.lt_status and self.download.handle:
            files = self.download.get_def().get_files_with_length()
            progress = self.download.handle.file_progress(flags=1)
            for index, (path, size) in enumerate(files):
                completion_frac = (float(progress[index]) / size) if size > 0 else 1
                completion.append((path, completion_frac))

        return completion