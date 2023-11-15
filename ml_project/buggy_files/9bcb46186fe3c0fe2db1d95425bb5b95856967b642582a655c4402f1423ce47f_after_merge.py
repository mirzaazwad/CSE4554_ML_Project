    async def convert(self, ctx: commands.Context, arg: str) -> MutableMapping:
        global_matches = await get_all_playlist_converter(
            PlaylistScope.GLOBAL.value, _bot, arg, guild=ctx.guild, author=ctx.author
        )
        guild_matches = await get_all_playlist_converter(
            PlaylistScope.GUILD.value, _bot, arg, guild=ctx.guild, author=ctx.author
        )
        user_matches = await get_all_playlist_converter(
            PlaylistScope.USER.value, _bot, arg, guild=ctx.guild, author=ctx.author
        )
        if not user_matches and not guild_matches and not global_matches:
            raise commands.BadArgument(_("Could not match '{}' to a playlist.").format(arg))
        return {
            PlaylistScope.GLOBAL.value: global_matches,
            PlaylistScope.GUILD.value: guild_matches,
            PlaylistScope.USER.value: user_matches,
            "arg": arg,
        }