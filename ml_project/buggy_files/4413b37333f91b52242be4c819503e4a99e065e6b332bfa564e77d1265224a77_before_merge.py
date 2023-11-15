    def __call__(self, target, *args, **kwargs):
        @wraps(target)
        def wrapper(*args, **kwargs):
            try:
                result = target(*args, **kwargs)
            except self.catch as e:
                if self.image_api and not kwargs.get('lang'):
                    if args[1].lang != 'en':
                        logger.debug("Could not find the image on the indexer, re-trying to find it in english")
                        kwargs['lang'] = 'en'
                        return wrapper(*args, **kwargs)

                logger.debug("Could not find item on the indexer: (Indexer probably doesn't have this item) [{error}]".format(error=str(e)))
                result = self.default_return
            except RHTTPError as e:
                logger.debug("Could not find item on the indexer: (Indexer probably doesn't have this item) [{error}]".format(error=str(e)))
                result = self.default_return

            return result

        wrapper.__doc__ = target.__doc__
        return wrapper