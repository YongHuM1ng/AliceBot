from alicebot import Bot

from decode_str_cqcode import Tools


bot = Bot(hot_reload=True)


# @bot.event_preprocessor_hook
# async def hook_func(_event: "T_Event"):
#     _event.message = Tools.cq_text_decode(_event.message)


if __name__ == "__main__":
    bot.run()
