    def on_rss_feeds_refreshed(self, json_result):
        if not json_result:
            return
        if json_result["rechecked"]:
            self.window().edit_channel_details_rss_refresh_button.setEnabled(True)