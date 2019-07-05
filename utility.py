import discord


def has_role(ctx, item):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        return False

    if isinstance(item, int):
        role = discord.utils.get(ctx.author.roles, id=item)
    else:
        role = discord.utils.get(ctx.author.roles, name=item)
    return role is not None