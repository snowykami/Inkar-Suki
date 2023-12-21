from src.tools.dep import *
from src.tools.config import Config
from src.tools.utils import checknumber
from src.tools.file import read, write
from src.tools.permission import checker, error
import json
import sys
import nonebot

from nonebot import on_command, on_message
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg


def in_it(qq: str):
    for i in json.loads(read(TOOLS + "/ban.json")):
        if i == qq:
            return True
    return False


ban = on_command("ban", priority=5)  # 封禁，≥10的用户无视封禁。


@ban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    sb = args.extract_plain_text()
    self_protection = False
    if sb in Config.owner:
        await ban.send("不能封禁机器人主人，这么玩就不好了，所以我先把你ban了QwQ")
        sb = str(event.user_id)
        self_protection = True
    x = Permission(event.user_id).judge(10, '拉黑用户')
    if not x.success:
        if self_protection == False:
            return await ban.finish(x.description)
    if sb == False:
        return await ban.finish("您输入了什么？")
    if checknumber(sb) == False:
        return await ban.finish("不能全域封禁不是纯数字的QQ哦~")
    info = await bot.call_api("get_stranger_info", user_id=int(sb))
    if info["user_id"] == 0:
        return await ban.finish("唔……全域封禁失败，没有这个人哦~")
    elif in_it(sb):
        return ban.finish("唔……全域封禁失败，这个人已经被封禁了。")
    else:
        now = json.loads(read(TOOLS + "/ban.json"))
        now.append(sb)
        write(TOOLS + "/ban.json", json.dumps(now))
        sb_name = info["nickname"]
        if self_protection:
            return
        return await ban.finish(f"好的，已经全域封禁{sb_name}({sb})。")

unban = on_command("unban", priority=5)  # 解封


@unban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    x = Permission(event.user_id).judge(10, '解除拉黑用户')
    if not x.success:
        return await ban.finish(x.description)
    sb = args.extract_plain_text()
    if checknumber(sb) == False:
        return await ban.finish("不能全域封禁不是纯数字的QQ哦~")
    info = await bot.call_api("get_stranger_info", user_id=int(sb))
    sb_name = info["nickname"]
    if sb == False:
        return await unban.finish("您输入了什么？")
    if in_it(sb) == False:
        return await unban.finish("全域解封失败，并没有封禁此人哦~")
    now = json.loads(read(TOOLS + "/ban.json"))
    for i in now:
        if i == sb:
            now.remove(i)
    write(TOOLS + "/ban.json", json.dumps(now))
    return await ban.finish(f"好的，已经全域解封{sb_name}({sb})。")


@matcher_common_run.handle()
async def common_match_ban_user(matcher: Matcher, event: Event):
    info = json.loads(read(TOOLS + "/ban.json"))
    if not str(event.user_id) in info:
        return

    permit = Permission(event.user_id).judge(10, '黑名单用户免除封禁')
    if permit.success:
        return
        
    matcher.stop_propagation()
