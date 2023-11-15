    def _init_i18n(self):
        """Load translated strings from the configured localedirs if enabled in
        the configuration.
        """
        if self.config.language is not None:
            self.info(bold('loading translations [%s]... ' %
                           self.config.language), nonl=True)
            locale_dirs = [None, path.join(package_dir, 'locale')] + \
                [path.join(self.srcdir, x) for x in self.config.locale_dirs]
        else:
            locale_dirs = []
        self.translator, has_translation = locale.init(locale_dirs,
                                                       self.config.language,
                                                       charset=self.config.source_encoding)
        if self.config.language is not None:
            if has_translation or self.config.language == 'en':
                # "en" never needs to be translated
                self.info('done')
            else:
                self.info('not available for built-in messages')