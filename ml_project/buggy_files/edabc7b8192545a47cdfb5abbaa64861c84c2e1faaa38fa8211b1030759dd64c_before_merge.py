    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help()
        elif isinstance(error, commands.ConversionFailure):
            if error.args:
                await ctx.send(error.args[0])
            else:
                await ctx.send_help()
        elif isinstance(error, commands.BadArgument):
            await ctx.send_help()
        elif isinstance(error, commands.DisabledCommand):
            disabled_message = await bot.db.disabled_command_msg()
            if disabled_message:
                await ctx.send(disabled_message.replace("{command}", ctx.invoked_with))
        elif isinstance(error, commands.CommandInvokeError):
            # Need to test if the following still works
            """
            no_dms = "Cannot send messages to this user"
            is_help_cmd = ctx.command.qualified_name == "help"
            is_forbidden = isinstance(error.original, discord.Forbidden)
            if is_help_cmd and is_forbidden and error.original.text == no_dms:
                msg = ("I couldn't send the help message to you in DM. Either"
                       " you blocked me or you disabled DMs in this server.")
                await ctx.send(msg)
                return
            """
            log.exception(
                "Exception in command '{}'" "".format(ctx.command.qualified_name),
                exc_info=error.original,
            )
            if should_log_sentry(error):
                sentry_log.exception(
                    "Exception in command '{}'" "".format(ctx.command.qualified_name),
                    exc_info=error.original,
                )

            message = (
                "Error in command '{}'. Check your console or "
                "logs for details."
                "".format(ctx.command.qualified_name)
            )
            exception_log = "Exception in command '{}'\n" "".format(ctx.command.qualified_name)
            exception_log += "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            bot._last_exception = exception_log
            if not hasattr(ctx.cog, "_{0.command.cog_name}__error".format(ctx)):
                await ctx.send(inline(message))
        elif isinstance(error, commands.CommandNotFound):
            term = ctx.invoked_with + " "
            if len(ctx.args) > 1:
                term += " ".join(ctx.args[1:])
            fuzzy_result = await fuzzy_command_search(ctx, ctx.invoked_with)
            if fuzzy_result is not None:
                await ctx.maybe_send_embed(fuzzy_result)
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("That command is not available in DMs.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                "This command is on cooldown. Try again in {:.2f}s".format(error.retry_after)
            )
        else:
            log.exception(type(error).__name__, exc_info=error)
            try:
                sentry_error = error.original
            except AttributeError:
                sentry_error = error

            if should_log_sentry(sentry_error):
                sentry_log.exception("Unhandled command error.", exc_info=sentry_error)