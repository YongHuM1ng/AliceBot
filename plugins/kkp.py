from alicebot import Plugin
from alicebot.adapter.cqhttp.event import GroupMessageEvent


class Kkp(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        await self.event.reply('不理你啦！バーカー')

    async def rule(self) -> bool:
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and str(self.event.message) == 'kkp'
                and self.event.message_type == 'group'
        )
