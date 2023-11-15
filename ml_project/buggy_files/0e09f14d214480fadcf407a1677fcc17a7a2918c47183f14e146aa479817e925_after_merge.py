def _prepare_config_scope(
    scope, author: Union[discord.abc.User, int] = None, guild: Union[discord.Guild, int] = None
):
    scope = standardize_scope(scope)

    if scope == PlaylistScope.GLOBAL.value:
        config_scope = [PlaylistScope.GLOBAL.value, _bot.user.id]
    elif scope == PlaylistScope.USER.value:
        if author is None:
            raise MissingAuthor("Invalid author for user scope.")
        config_scope = [PlaylistScope.USER.value, int(getattr(author, "id", author))]
    else:
        if guild is None:
            raise MissingGuild("Invalid guild for guild scope.")
        config_scope = [PlaylistScope.GUILD.value, int(getattr(guild, "id", guild))]
    return config_scope