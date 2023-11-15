    def handle_timedout_limit_buy(self, trade: Trade, order: Dict) -> bool:
        """
        Buy timeout - cancel order
        :return: True if order was fully cancelled
        """
        if order['status'] != 'canceled':
            reason = "cancelled due to timeout"
            try:
                corder = self.exchange.cancel_order(trade.open_order_id, trade.pair)
                # Some exchanges don't return a dict here.
                if not isinstance(corder, dict):
                    corder = {}
                logger.info('Buy order %s for %s.', reason, trade)
            except InvalidOrderException:
                corder = {}
                logger.exception(
                    f"Could not cancel buy order {trade.open_order_id} for pair {trade.pair}")
        else:
            # Order was cancelled already, so we can reuse the existing dict
            corder = order
            reason = "cancelled on exchange"
            logger.info('Buy order %s for %s.', reason, trade)

        if safe_value_fallback(corder, order, 'remaining', 'remaining') == order['amount']:
            logger.info('Buy order fully cancelled. Removing %s from database.', trade)
            # if trade is not partially completed, just delete the trade
            Trade.session.delete(trade)
            Trade.session.flush()
            return True

        # if trade is partially complete, edit the stake details for the trade
        # and close the order
        # cancel_order may not contain the full order dict, so we need to fallback
        # to the order dict aquired before cancelling.
        # we need to fall back to the values from order if corder does not contain these keys.
        trade.amount = order['amount'] - safe_value_fallback(corder, order,
                                                             'remaining', 'remaining')
        trade.stake_amount = trade.amount * trade.open_rate
        self.update_trade_state(trade, corder if 'fee' in corder else order, trade.amount)

        trade.open_order_id = None
        logger.info('Partial buy order timeout for %s.', trade)
        self.rpc.send_msg({
            'type': RPCMessageType.STATUS_NOTIFICATION,
            'status': f'Remaining buy order for {trade.pair} cancelled due to timeout'
        })
        return False