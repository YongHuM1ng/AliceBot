from alicebot import Plugin
from alicebot.adapter.cqhttp.event import GroupMessageEvent

group_id = [373912464, 963995600]


class SpecialTitle(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        special_title = ''
        split_msg = self.event.message.get_plain_text().split(' ')
        if len(split_msg) == 2:
            special_title = split_msg[1]
        elif self.event.message.get_plain_text() == '.头衔':
            ...
        else:
            self.skip()
        if len(special_title.encode('utf-8')) <= 18:
            await self.event.adapter.call_api('set_group_special_title',
                                              group_id=self.event.group_id,
                                              user_id=self.event.user_id,
                                              special_title=special_title)
        else:
            await self.event.reply(
                f'头衔最长为18字节 (汉字为3字节)\n您的输入为{len(special_title.encode("utf-8"))}字节')

    async def rule(self) -> bool:
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and self.event.message.startswith('.头衔')
                and self.event.group_id in group_id
                and self.event.message_type == 'group'
        )


class GroupName(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        split_msg = self.event.message.get_plain_text().split(' ')
        if len(split_msg) == 2:
            await self.event.adapter.call_api('set_group_name',
                                              group_id=self.event.group_id,
                                              group_name=split_msg[1])

    async def rule(self) -> bool:
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and self.event.message.startswith('.群名')
                and self.event.group_id in group_id
                and self.event.message_type == 'group'
        )


class GroupNotice(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        split_msg = self.event.message.get_plain_text().split(' ')
        if len(split_msg) == 2:
            await self.event.adapter.call_api('_send_group_notice',
                                              group_id=self.event.group_id,
                                              content=split_msg[1])

    async def rule(self) -> bool:
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and self.event.message.startswith('.公告')
                and self.event.group_id in group_id
                and self.event.message_type == 'group'
        )
