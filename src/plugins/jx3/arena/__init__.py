from .api import *

jx3_cmd_arena_records = on_regex(
    r"^(/)?(名剑|jjc|竞技场)?(战绩|记录|查询)",
    priority=5,
    description='获取玩家竞技场的战绩记录',
    catalog='jx3.pvx.property.horse.chitu',
    example=[Jx3Arg(Jx3ArgsType.server),
             Jx3Arg(Jx3ArgsType.user),
             Jx3Arg(Jx3ArgsType.default, default='22')],
    document='''战绩 玩家id 模式
    模式可以写22 33 55'''
)


@jx3_cmd_arena_records.handle()
async def jx3_arena_records(bot: Bot, event: GroupMessageEvent):
    template = [
        Jx3Arg(Jx3ArgsType.server),
        Jx3Arg(Jx3ArgsType.user),
        Jx3Arg(Jx3ArgsType.default, default='22')
    ]
    server, user, pvp_mode = get_args(template, event)
    if server is None:
        return await jx3_cmd_arena_records.finish(PROMPT_ServerNotExist)
    if user is None:
        return await jx3_cmd_arena_records.finish(PROMPT_UserNotExist)

    data = await arena_records(server=server, name=user, mode=pvp_mode)
    if type(data) == type([]):
        return await jx3_cmd_arena_records.finish(data[0])
    return await jx3_cmd_arena_records.send(ms.image(data))


jx3_cmd_arena_rank = on_regex(r"^(/)?(名剑|jjc|竞技场)?(排行|榜单|榜)", priority=5)


@jx3_cmd_arena_rank.handle()
async def jx3_arena_rank(bot: Bot, event: GroupMessageEvent):
    template = [Jx3Arg(Jx3ArgsType.default, default='22')]
    pvp_mode, = get_args(template, event)
    data = await arena_rank(mode=pvp_mode)
    if type(data) == type([]):
        return await jx3_cmd_arena_rank.finish(data[0])
    return await jx3_cmd_arena_rank.send(ms.image(data))

jx3_cmd_arena_statistics = on_regex(r"^(/)?(名剑|jjc|竞技场)?(统计|日志)", priority=5)


@jx3_cmd_arena_statistics.handle()
async def jx3_arena_statistics(bot: Bot, event: GroupMessageEvent):
    template = [
        Jx3Arg(Jx3ArgsType.default, default='22'),
        Jx3Arg(Jx3ArgsType.server),
    ]
    pvp_mode, = get_args(template, event)
    data = await arena_statistics(mode=pvp_mode)
    if type(data) == type([]):
        return await jx3_cmd_arena_statistics.finish(data[0])
    return await jx3_cmd_arena_statistics.send(ms.image(data))
