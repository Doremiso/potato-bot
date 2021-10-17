from nonebot import on_command
from nonebot.adapters import MessageTemplate
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP, PRIVATE
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import MessageSegment
import httpx
from ....nonebot_plugin_ff14 import config

items = on_command("item", permission=GROUP | PRIVATE, priority=5, aliases={"道具"})


@items.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["id"] = args


@items.got("id", prompt="想要查询的道具ID是多少？")
async def _get(bot: Bot, event: Event, state: T_State):
    item_info = await get_item_info(state["id"])
    await items.finish(item_info)


async def get_item_info(_id):
    MessageTemplate
    print("search")
    async with httpx.AsyncClient() as client:
        response = await client.get("{}/item/{}".format(config.kafeapi, _id))
        if not response.status_code == 200:
            return "请求失败！"
        else:
            _json = response.json()
            for key in _json:
                print(f"{key}: {_json[key]}")
            return "https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:%E5%A5%B3%E7%8E%8B%E4%B9%8B%E8%8D%A3%E8%80%80"

def make_message():

