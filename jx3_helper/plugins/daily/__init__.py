from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import httpx

daily = on_command("日常", rule=to_me(), priority=5)


@daily.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = await get_daily()
    await daily.finish(msg)


async def get_daily():
    async with httpx.AsyncClient() as client:
        server = "绝代天骄"
        res = await client.get(f"https://jx3api.com/app/daily?server={server}")
        _json = res.json()
        if _json['msg'] == 'success':
            data = _json['data']
            msg = f"日常：{data['DayWar']}\n战场：{data['DayBattle']}\n矿车：{data['DayCamp']}"
            try:
                msg += f"\n美人图：{data['DayDraw']}"
            except KeyError:
                pass
        else:
            msg = "获取失败！"
        return msg
