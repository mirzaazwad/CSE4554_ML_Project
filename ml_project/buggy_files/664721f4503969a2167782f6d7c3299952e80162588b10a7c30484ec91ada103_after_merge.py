    def on_wallets(self, wallets):
        if not wallets:
            return
        wallets = wallets["wallets"]
        self.received_wallets.emit(wallets)

        created_wallets = [wallet_id for wallet_id, wallet_info in wallets.items() if wallet_info['created']]
        if len(created_wallets) < 2:
            self.window().market_create_wallet_button.show()
        else:
            self.window().create_ask_button.show()
            self.window().create_bid_button.show()

        self.wallets = wallets
        if self.chosen_wallets is None and len(self.wallets.keys()) >= 2:
            self.chosen_wallets = sorted(self.wallets.keys())[0], sorted(self.wallets.keys())[1]
            self.update_button_texts()

        for wallet_id, wallet in wallets.iteritems():
            if not wallet['created'] or not wallet['unlocked']:
                continue

            if wallet_id not in self.wallet_widgets:
                wallet_widget = MarketCurrencyBox(self.window().market_header_widget, wallets[wallet_id]['name'])
                self.window().market_header_widget.layout().insertWidget(4, wallet_widget)
                wallet_widget.setFixedWidth(100)
                wallet_widget.setFixedHeight(34)
                wallet_widget.show()
                self.wallet_widgets[wallet_id] = wallet_widget

                spacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
                self.window().market_header_widget.layout().insertSpacerItem(5, spacer)

            balance_amount = prec_div(wallet['balance']['available'], wallet['precision'])
            balance_currency = None

            self.wallet_widgets[wallet_id].update_with_amount(balance_amount, balance_currency)

        self.load_asks()
        self.load_bids()