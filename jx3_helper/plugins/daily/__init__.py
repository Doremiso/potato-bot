from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import httpx
from ..source.model import QQGroupConfig

daily = on_command("日常", priority=5)
weekly = on_command("周常", priority=5)


@daily.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    group_id = event.dict()['group_id']
    msg = await get_daily(group_id)
    await daily.finish(msg)


async def get_daily(group_id):
    async with httpx.AsyncClient() as client:
        qq_group_config = QQGroupConfig()
        # 根据群号获取服务器
        server = await qq_group_config.get_server(group_id)
        if server:
            res = await client.get(f"https://jx3api.com/app/daily?server={server}")
        else:
            res = await client.get("https://jx3api.com/app/daily")
        _json = res.json()
        if _json['msg'] == 'success':
            data = _json['data']
            msg = f"日常：{data['DayWar']}\n战场：{data['DayBattle']}\n矿车：{data['DayCamp']}"
            try:
                # 判断是否有美人图
                msg += f"\n美人图：{data['DayDraw']}"
            except KeyError:
                pass
        else:
            msg = "获取失败！"
        return msg


@weekly.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = await get_weekly()
    await weekly.finish(msg)


async def get_weekly():
    async with httpx.AsyncClient() as client:
        res = await client.get("https://jx3api.com/app/daily")
        _json = res.json()
        if _json['msg'] == 'success':
            data = _json['data']
            msg = f"周常公共：\n{data['WeekCommon']}\n周常5人：\n{data['WeekFive']}\n周常10人：\n{data['WeekTeam']}"
        else:
            msg = "获取失败！"
        return msg
