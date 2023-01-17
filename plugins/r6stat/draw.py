from PIL import Image, ImageDraw, ImageFont
import os
import time
from io import BytesIO
import base64

file_path = f'{os.path.dirname(__file__)}/'
font_bold = f'{file_path}ScoutCond-BoldItalic.otf'
font_regular = f'{file_path}ScoutCond-RegularItalic.otf'


async def draw_img(data: dict, season1: dict, season2: dict,
                   avatar: Image.Image, casual_img: Image.Image, rank_img: Image.Image):
    back = Image.open(f'{file_path}back.png')
    draw = ImageDraw.Draw(back)

    draw.text((515, 105), f'SEASON{data["currentSeason"]}', fill="#FFFFFF",
              font=ImageFont.truetype(font_bold, size=24))
    back.paste(avatar, (78, 184), mask=avatar)
    draw.text((256, 192), f'LEVEL {data["level"]}', fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=36))
    draw.text((256, 230), data['name'], fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=96))

    back.paste(casual_img, (125, 412), mask=casual_img)
    draw.text((181 - ImageFont.truetype(font_bold, size=16).getlength('THX UBI') / 2, 518),
              'THX UBI', fill="#FFFFFF", font=ImageFont.truetype(font_bold, size=16))
    draw.text((181 - ImageFont.truetype(font_bold, size=48).getlength('?') / 2, 530),
              '?', fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    draw.text((262, 446), str(round(season1['kd'], 2)), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))
    draw.text((384, 446), str(season1['kills']), fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))
    draw.text((491, 446),
              str(round(season1['kills'] / season1['kd'])) if season1['kd'] != 0 else '0',
              fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    draw.text((262, 521), str(season1['winPct']), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))
    draw.text((384, 521), str(season1['wins']), fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    if season1['winPct'] != 0:
        draw.text((491, 521), str(round(season1['wins'] / (season1['winPct'] / 100) - season1['wins'])),
                  fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))
    else:
        draw.text((491, 521), '0',
                  fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    back.paste(rank_img, (125, 676), mask=rank_img)
    draw.text((181 - ImageFont.truetype(font_bold, size=16).getlength(season2['rankName']) / 2, 782),
              season2['rankName'], fill="#FFFFFF", font=ImageFont.truetype(font_bold, size=16))
    draw.text((181 - ImageFont.truetype(font_bold, size=48).getlength(str(season2['rankPoints'])) / 2, 794),
              str(season2['rankPoints']), fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    draw.text((262, 674), str(round(season2['kd'], 2)), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))
    draw.text((384, 674), str(season2['kills']), fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))
    draw.text((491, 674),
              str(round(season2['kills'] / season2['kd'])) if season2['kd'] != 0 else '0',
              fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    draw.text((262, 749), str(season2['winPct']), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))
    draw.text((384, 749), str(season2['wins']), fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    if season2['winPct'] != 0:
        draw.text((491, 749), str(round(season2['wins'] / (season2['winPct'] / 100) - season2['wins'])),
                  fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))
    else:
        draw.text((491, 749), '0',
                  fill="#FFFFFF", font=ImageFont.truetype(font_regular, size=48))

    draw.text((262, 824), season2['maxRank']['rankName'], fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))
    draw.text((491, 824), str(season2['maxRankPoints']), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=48))

    draw.text((629, 925), time.strftime("%Y-%m-%d %H:%M", time.localtime()), fill="#FFFFFF",
              font=ImageFont.truetype(font_regular, size=24))

    bio = BytesIO()
    back.save(bio, format='PNG')
    return f'base64://{base64.b64encode(bio.getvalue()).decode()}'
