import asyncio

import discord
from data.services.guild_service import guild_service

from utils.config import cfg


class BanCache:
    def __init__(self, bot):
        self.bot = bot
        self.cache = set()
        self.fetch_ban_cache()

    def fetch_ban_cache(self):
        asyncio.ensure_future(fetch_ban_cache(self.bot, self))

    def is_banned(self, user_id):
        return user_id in self.cache

    def ban(self, user_id):
        self.cache.add(user_id)

    def unban(self, user_id):
        self.cache.discard(user_id)


async def fetch_ban_cache(bot, ban_cache: BanCache):
    """Fetches ban cache

    Parameters
    ----------
    bot
        "Bot object"
    ban_cache : BanCahce
        "Ban cache"

    """
    guild = bot.get_guild(cfg.guild_id)
    the_list = await guild.bans()
    ban_cache.cache = {entry.user.id for entry in the_list}


class IssueCache():
    def __init__(self, bot):
        self.bot = bot
        self.fetch_issue_cache()

    def fetch_issue_cache(self):
        asyncio.ensure_future(fetch_issue_cache(self.bot, self))


async def fetch_issue_cache(bot, cache):
    cache.cache = {}
    guild: discord.TextChannel = bot.get_guild(cfg.guild_id)
    if not guild:
        return

    channel = guild.get_channel(
        guild_service.get_guild().channel_common_issues)

    async for message in channel.history(limit=None, oldest_first=True):
        if message.author.id != bot.user.id:
            continue

        if not message.embeds:
            continue

        embed = message.embeds[0]
        if not embed.footer.text:
            continue

        if embed.footer.text.startswith("Submitted by"):
            cache.cache[f"{embed.title}"] = message
        else:
            continue
