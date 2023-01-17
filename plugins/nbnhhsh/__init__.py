import re

import aiohttp
from alicebot import Plugin
from alicebot.adapter.cqhttp.event import GroupMessageEvent


class Test(Plugin[GroupMessageEvent, int, None]):
    def __post_init__(self):
        self.res = None

    async def handle(self) -> None:
        msg = await query(self.res['text'])
        if msg:
            await self.event.reply(msg)

    async def rule(self) -> bool:
        self.res = re.search(r'^\s*(?P<text>[a-zA-Z0-9]+)是(什么|甚么|啥|？|\?)', str(self.event.message))
        return (
                self.event.adapter.name == "cqhttp"
                and self.event.type == "message"
                and self.res
        )


async def query(text: str) -> str:
    # 防止文本过长。
    if len(text) > 50:
        return '太、太长了8…'
    if not re.match(r'^[a-zA-Z0-9]+$', text):
        return '只能包含字母'
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.post('https://lab.magiconch.com/api/nbnhhsh/guess', data={'text': text}) as resp:
            ret = await resp.json()
    result = []
    for item in ret:
        prefix = '[%s]: ' % item.get('name')
        trans = item.get('trans')
        if trans is None:
            inputting = ', '.join(item.get('inputting', []))
            if inputting == '':
                ans = '优质解答：我不知道'
            else:
                ans = '有可能是：' + inputting
        else:
            ans = ', '.join(trans)
        result.append(prefix + ans)
    return '\n'.join(result)
