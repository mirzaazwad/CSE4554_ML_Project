    def get_free(self, currency) -> float:

        balance = self._wallets.get(currency)
        if balance and balance.free:
            return balance.free
        else:
            return 0