import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import httpx
import json

role = on_command("角色", rule=to_me(), priority=5)


@role.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送时的参数
    if args:
        state['name'] = args


@role.got('name', prompt="请输入想查询的角色名称")
async def handle_name(bot: Bot, event: Event, state: T_State):
    name = state['name']
    code, info = await get_material(name)
    if code:
        for material_info in info:
            await role.send(material_info)
    else:
        await role.send(info)
    await role.finish()


async def get_material(name: str):
    async with httpx.AsyncClient() as client:
        driver = nonebot.get_driver()
        # https://wiki.biligame.com/pcr/%E9%95%9C%E5%8D%8E
        res = await client.get("https://wiki.biligame.com/pcr/%E9%95%9C%E5%8D%8E")
        print(res.text)
        # if _json['code']:
        #     for material_info in _json['materials']:
        #         material_list.append(f"名称:{material_info['name']}, 类型: {material_info['type']}, 地区:{material_info['addr']}")
        #     return 1, material_list
        # else:
        #     return 0, _json['info']
