    def on_rss_feeds_remove_selected_clicked(self):
        if len(self.window().edit_channel_rss_feeds_list.selectedItems()) == 0:
            ConfirmationDialog.show_message(self, "Remove RSS Feeds",
                                            "Selection is empty. Please select the feeds to remove.", "OK")
            return
        self.dialog = ConfirmationDialog(self, "Remove RSS feed",
                                         "Are you sure you want to remove the selected RSS feed?",
                                         [('REMOVE', BUTTON_TYPE_NORMAL), ('CANCEL', BUTTON_TYPE_CONFIRM)])
        self.dialog.button_clicked.connect(self.on_rss_feed_dialog_removed)
        self.dialog.show()