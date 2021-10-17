from nonebot import on_command
from nonebot.adapters.cqhttp.permission import GROUP, PRIVATE
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.typing import T_State
import httpx
from httpx import Response
from ....nonebot_plugin_ff14 import config


search = on_command("search", permission=GROUP | PRIVATE, priority=5, aliases={"搜索"})
# TODO:精准搜索


@search.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        args = args.split(" ")
        if len(args) == 1:
            if not args[0] == "道具":
                state['name'] = args[0]
            state['type'] = "道具"
        if len(args) == 2:
            state['type'] = args[0]
            state['name'] = args[1]


@search.got("type", prompt="想搜索什么？请输入道具名称或搜索类型（道具, 成就）")
async def _get(bot: Bot, event: Event, state: T_State):
    _type = state["type"]
    if _type in ['道具', '成就']:
        state['type'] = _type
    else:
        state['type'] = '道具'


@search.got("name", prompt="名称是什么？")
async def _get(bot: Bot, event: Event, state: T_State):
    search_result = await get_result(state['type'], state['name'])
    await search.finish(search_result)


async def get_result(_type: str, name: str):
    async with httpx.AsyncClient() as client:
        search_type = {"道具": "Item", "成就": "Achievement"}
        url = "{}/search/?indexes={}&string={}&limit=10".format(config.kafeapi, search_type[_type], name)
        response: Response = await client.get(url)
        if not response.status_code == 200:
            return "请求失败！"
        else:
            _json = response.json()
            if _json['Results']:
                return make_message(_json['Results'], _type)
            else:
                return "未搜到任何内容！"


def make_message(results, _type):
    message = ""
    for item in results:
        message += "{}  {}\n".format(item["ID"], item["Name"])
    message += "请输入'/{} ID' 查询对应内容的详细信息".format(_type)
    return message
