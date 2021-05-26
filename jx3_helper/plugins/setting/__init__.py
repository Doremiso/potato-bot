from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.permission import GROUP
from ..source.model import QQGroupConfig

set_server = on_command("设置区服", permission=GROUP, priority=5)


@set_server.handle()
async def handle_set_server_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["server"] = args


@set_server.got("server", prompt="要设置哪个服为默认服务器？")
async def handle_set_server_server(bot: Bot, event: Event, state: T_State):
    server = state["server"]
    group_id = event.dict()['group_id']
    await set_server_event(group_id, server)


async def set_server_event(group_id, server):
    setting = QQGroupConfig()
    res = await setting.set_server(group_id, server)
    if isinstance(res, str):
        msg = "设置失败！{}".format(res)
    else:
        msg = "设置成功！"
    await set_server.finish(msg)
