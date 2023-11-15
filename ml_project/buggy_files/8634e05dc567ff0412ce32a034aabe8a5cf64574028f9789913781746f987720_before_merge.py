    def perform_request(self, req_id, method, params):
        response = None
        if method in self.sender_registry:
            logger.debug('Perform request {0} with id {1}'.format(
                method, req_id))
            handler_name = self.sender_registry[method]
            handler = getattr(self, handler_name)
            response = handler(params)
            if method in self.handler_registry:
                converter_name = self.handler_registry[method]
                converter = getattr(self, converter_name)
                if response is not None:
                    response = converter(response)
        self.sig_response_ready.emit(req_id, response or {})