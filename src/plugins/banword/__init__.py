import json
import sys
from pathlib import Path

from aiocqhttp import MessageSegment as ms
from nonebot import on_command
from nonebot import on_message
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Event
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

TOOLS = Path(__file__).resolve().parent.parent.parent / "tools"
sys.path.append(str(TOOLS))
from permission import checker, error
from file import read, write


def is_in(full_str, sub_str):
    try:
        full_str.index(sub_str)
        return True
    except ValueError:
        return False


global flag

bwa = on_command("banwordadd", aliases={"bwa", "addbanword"}, priority=5)


@bwa.handle()
async def __(matcher: Matcher, event: Event, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    if checker(str(event.user_id), 5) == False:
        await bwa.finish(error(5))
    if cmd:
        now = json.loads(read(TOOLS / "banword.json"))
        now.append(cmd)
        write(TOOLS / "banword.json", json.dumps(now, ensure_ascii=False))
        await bwa.finish("已成功封禁词语！")
    else:
        await bwa.finish("您封禁了什么？")

bwr = on_command("banwordremove",aliases={"removebanword","deletebanword","bwd","bwr"},priority=5)

@bwr.handle()
async def ___(matcher: Matcher, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),5) == False:
        await bwr.finish(error(5))
    cmd = args.extract_plain_text()
    if cmd:
        now = json.loads(read(TOOLS / "banword.json"))
        try:
            now.remove(cmd)
            write(TOOLS / "banword.json", json.dumps(now, ensure_ascii=False))
            await bwr.finish("成功解封词语！")
        except ValueError:
            await bwr.finish("您解封了什么？")
    else:
        await bwr.finish("您解封了什么？")

bw = on_message(priority=0, block=False)

@bw.handle()
async def _(matcher: Matcher,bot: Bot, event: MessageEvent):
    if checker(str(event.user_id),5):
        return
    flag = False
    banwordlist = read(TOOLS / "banword.json")
    msg = str(event.raw_message)
    id = str(event.message_id)
    for i in banwordlist:
        if is_in(msg,i):
            flag = True
    if flag:
        sb = str(event.user_id)
        try:
            group = event.group_id
            await bot.call_api("delete_msg",message_id=id)
            await bot.call_api("set_group_ban", group_id = group, user_id = sb, duration = 60)
            msg = ms.at(sb) + "唔……你触发了违禁词，已经给你喝了1分钟的红茶哦~"
            await bw.finish(msg)
        except:
            pass
    else:
        pass