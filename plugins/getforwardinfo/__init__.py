import time

from alicebot import Plugin
from alicebot.adapter.cqhttp.event import GroupMessageEvent


class GetForwardInfo(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        forward_msg = None
        for i in self.event.message:
            if i.type == 'reply':
                froward_id = (
                    await self.event.adapter.call_api('get_msg', message_id=i['id'])
                )['message'][0]['data']['id']
                forward_msg = await self.event.adapter.call_api('get_forward_msg', message_id=froward_id)
                break
        if not forward_msg:
            self.skip()
        msg_list = {}

        self.__data_handle(forward_msg['messages'], msg_list)

        msg_str = ''.join(f'{i}: {msg_list[i]}\n' for i in msg_list)
        msg_str = msg_str[:-1]
        group_id = forward_msg['messages'][0]['group_id']
        forward_time = [
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(forward_msg['messages'][0]['time'])),
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(forward_msg['messages'][-1]['time']))
        ]
        msg = f'群号: {group_id}\n' \
              f'(可能为二手转发群号)\n' \
              f'----------QQ号----------\n' \
              f'{msg_str}\n' \
              f'-------消息时间段-------\n' \
              f'{forward_time[0]}\n' \
              f'                |\n' \
              f'{forward_time[1]}'
        await self.event.reply(msg)

    async def rule(self) -> bool:
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and self.event.message.endswith('获取详细信息')
                and 'reply' in self.event.message
                and self.event.message_type == 'group'
        )

    @staticmethod
    def __data_handle(data: list, msg_list: dict):
        for i in data:
            for j in i['content']:
                if 'content' in j:
                    if i['sender']['user_id'] not in msg_list:
                        msg_list[i["sender"]["user_id"]] = i["sender"]["nickname"]
                    if j['sender']['user_id'] not in msg_list:
                        msg_list[j["sender"]["user_id"]] = j["sender"]["nickname"]
                    if len(i['content']) != 1:
                        GetForwardInfo.__data_handle(i['content'], msg_list)
