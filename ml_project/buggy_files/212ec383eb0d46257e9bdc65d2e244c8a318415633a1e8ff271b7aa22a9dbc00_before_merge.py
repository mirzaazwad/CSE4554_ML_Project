    async def start_bot(bot, logger, catch=False):
        try:
            loop = asyncio.get_event_loop()
            # try to init
            await bot.create_services()
            await bot.create_exchange_traders()
            bot.create_evaluation_tasks()

            # try to start
            await bot.start_tasks()

            # join threads in a not loop blocking executor
            # TODO remove this when no thread anymore
            await loop.run_in_executor(None, bot.join_threads)

        except Exception as e:
            logger.exception(f"OctoBot Exception : {e}")
            if not catch:
                raise e
            Commands.stop_bot(bot)