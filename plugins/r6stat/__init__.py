import asyncio
import os
from io import BytesIO

import aiohttp
from PIL import Image
from alicebot import Plugin
from alicebot.adapter.cqhttp.event import GroupMessageEvent

from draw import draw_img

file_path = f'{os.path.dirname(__file__)}/'
empty_season = {
    'rankName': 'No Rank',
    'img': 'https://trackercdn.com/cdn/r6.tracker.network/ranks/s28/small/unranked.png',
    'rankPoints': 0,
    'maxRankPoints': 0,
    'winPct': 0.0,
    'wins': 0,
    'kd': 0,
    'kills': 0,
    'matches': 0,
    'maxRank': {
        'mmr': 0,
        'rankIcon': 'https://trackercdn.com/cdn/r6.tracker.network/ranks/s23/small/unranked.png',
        'rankName': 'No Rank'
    }
}


class R6Stat(Plugin[GroupMessageEvent, int, None]):
    async def handle(self) -> None:
        args = self.event.get_plain_text().split(' ')
        name = ''
        if 'at' in self.event.message:
            for i in self.event.message:
                if i.type == 'at':
                    member_info = await self.event.adapter.call_api('get_group_member_info',
                                                                    group_id=self.event.group_id, user_id=i['qq'])
                    name = member_info['card'] if member_info['card'] else member_info['nickname']
        elif len(args) == 2:
            name = args[1]
        else:
            name = self.event.sender.card if self.event.sender.card else self.event.sender.nickname

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://r6.tracker.network/api/v0/overwolf/player',
                                       params={'name': name}, timeout=10) as resp:
                    data = await resp.json()
        except asyncio.exceptions.TimeoutError:
            await self.event.reply('连接R6Tracker服务器超时')

        if not data['success']:
            if data['reason'] == 'InvalidName':
                await self.event.reply('没有这个游戏ID')
                return
            await self.event.reply(f"出现错误，错误原因：{data['reason']}")

        season1 = season2 = empty_season
        for i in range(len(data['seasons'])):
            if data['seasons'][i]['season'] == data['currentSeason']:
                if data['seasons'][i]['regionLabel'] == 'CASUAL':
                    season1 = data['seasons'][i]
                if data['seasons'][i]['regionLabel'] == 'RANKED':
                    season2 = data['seasons'][i]

        if os.path.exists(f'{file_path}cache/{data["name"]}.png'):
            avatar = Image.open(f'{file_path}cache/{data["name"]}.png')
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(data['avatar'], timeout=10) as resp:
                        avatar = Image.open(BytesIO(await resp.read())).resize((150, 150))
            except asyncio.exceptions.TimeoutError:
                avatar = Image.open(f'{file_path}default_avatar.png')
            else:
                avatar.save(f'{file_path}cache/{data["name"]}.png')

        casual_img = self.get_avatar(season1)
        rank_img = self.get_avatar(season2)

        await draw_img(data, season1, season2, avatar, casual_img, rank_img)



    async def rule(self) -> bool:
        return (
                self.event.adapter.name == 'cqhttp'
                and self.event.type == 'message'
                and self.event.message.startswith('R6')
        )

    @staticmethod
    def get_avatar(season: dict):
        if os.path.exists(f'{file_path}cache/{season["rankName"]}.png'):
            img = Image.open(f'{file_path}cache/{season["rankName"]}.png').convert('RGBA')
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(season['img'], timeout=10) as resp:
                        img = Image.open(BytesIO(await resp.read())).convert('RGBA')
            except asyncio.exceptions.TimeoutError:
                img = Image.new('RGBA', (0, 0))
            else:
                img.save(f'{file_path}cache/{season["rankName"]}.png')
        return img
