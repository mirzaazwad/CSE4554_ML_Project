    def run(self):
        loop = asyncio.get_event_loop()
        self.run_loop(loop.run_forever)