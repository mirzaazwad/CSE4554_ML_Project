    async def _list_global_alias(self, ctx: commands.Context):
        """List the available global aliases on this bot."""
        global_aliases = await self._aliases.get_global_aliases()
        if not global_aliases:
            return await ctx.send(_("There are no global aliases."))
        names = [_("Aliases:")] + sorted(["+ " + a.name for a in global_aliases])
        await ctx.send(box("\n".join(names), "diff"))