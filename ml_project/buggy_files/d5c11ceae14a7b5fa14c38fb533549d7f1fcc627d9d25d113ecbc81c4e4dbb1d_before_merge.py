    def on_finished(self, reply, capture_errors):
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        if not reply.isOpen() or not status_code:
            self.received_json.emit(None, reply.error())
            return

        performed_requests[self.request_id][4] = status_code

        data = reply.readAll()
        try:
            json_result = json.loads(str(data), encoding='latin_1')

            if 'error' in json_result and capture_errors:
                self.show_error(TriblerRequestManager.get_message_from_error(json_result))
            else:
                self.received_json.emit(json_result, reply.error())
        except ValueError:
            self.received_json.emit(None, reply.error())
            logging.error("No json object could be decoded from data: %s" % data)

        # We disconnect the slot since we want the finished only to be emitted once. This allows us to reuse the
        # request manager.
        try:
            self.finished.disconnect()
            self.received_json.disconnect()
        except TypeError:
            pass  # We probably didn't have any connected slots.