from .api import *

from nonebot import require, get_bots

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

jx3_cmd_daily = on_command("jx3_daily", aliases={"日常"}, force_whitespace=True, priority=5)
@jx3_cmd_daily.handle()
async def jx3_daily(event: GroupMessageEvent):
    """
    查询日常。

    Notice：每个服务器的日常相同，仅美人图有可能存在不同。

    Example：-日常
    Example：-周常
    """
    info = await daily_()
    await jx3_cmd_daily.finish(info)

@scheduler.scheduled_job("cron", hour="7", minute="40")
async def run_at_7_40():
    msg = await daily_()
    bots = get_bots()
    groups = os.listdir(DATA)
    group = {}
    for i in list(bots):
        single_groups = await bots[i].call_api("get_group_list")
        group_id_s = []
        for x in single_groups:
            group_id_s.append(x["group_id"])
        group[i] = group_id_s
    for group_id in groups:
        for x in list(group):
            if int(group_id) in group[x]:
                if "日常" in getGroupData(str(group_id), "subscribe"):
                    await bots[x].call_api("send_group_msg", group_id=int(group_id), message=msg)

import datetime

@scheduler.scheduled_job("cron", hour="19", minute="30")
async def run_at_19_30():
    if datetime.datetime.weekday() not in [2, 4]:
        return
    msg = "世界BOSS要开始啦，请提前前往对应地图等待吧！\n发送“日常”可获得今日世界BOSS名单（如有）。"
    bots = get_bots()
    groups = os.listdir(DATA)
    group = {}
    for i in list(bots):
        single_groups = await bots[i].call_api("get_group_list")
        group_id_s = []
        for x in single_groups:
            group_id_s.append(x["group_id"])
        group[i] = group_id_s
    for group_id in groups:
        for x in list(group):
            if int(group_id) in group[x]:
                if "首领" in getGroupData(str(group_id), "subscribe"):
                    await bots[x].call_api("send_group_msg", group_id=int(group_id), message=msg)