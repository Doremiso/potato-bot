"""
花价

api：jx3box
"""
import httpx
import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import asyncio
import time
import json


flower_price = on_command("花价", priority=5)


@flower_price.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        if " " in args:  # 首先判断文本中间有没有空格
            arg_list = args.split(' ')
            if len(arg_list) == 2:  # 当参数为两个时，直接执行
                state["server"] = arg_list[0]
                state["flower"] = arg_list[1]
            else:
                await flower_price.finish("参数错误!")
        else:  # 没有空格的话就直接赋值给参数server
            state["server"] = args


@flower_price.got("server", prompt="要查询哪个服务器？")
async def handle_server(bot: Bot, event: Event, state: T_State):
    pass


@flower_price.got("flower", prompt="要查询什么花？")
async def handle_server(bot: Bot, event: Event, state: T_State):
    price = await get_flower_price(state["server"], state["flower"])
    await flower_price.finish(price)


async def get_flower_price(server, flower):
    map_list = ["广陵邑", "枫叶泊·天苑", "枫叶泊·乐苑"]
    res_text = ""

    async with httpx.AsyncClient() as client:
        for _map in map_list:
            get_price_url = f"https://spider.jx3box.com/flower?server={server}&map={_map}&type={flower}"
            res = await client.get(get_price_url)
            _json = res.json()
            if _json['msg'] == 'success':
                flower_list = _json['data']
                res_text += f"{_map}：\n"
                if flower_list:
                    for flower_info in flower_list:
                        lines = ''
                        for f_price in flower_info['branch']:
                            lines += f_price['number']+"线 "
                        res_text += f"{flower_info['name']} \n {lines}\n"
            else:
                return "查询失败！请检查服务器和花名是否正确！"
            await asyncio.sleep(0.5)
    return res_text
