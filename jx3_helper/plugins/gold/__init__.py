"""
金价
"""
import httpx
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import time
import json

gold = on_command("金价", rule=to_me(), priority=5)


@gold.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["server"] = args


@gold.got("server", prompt="要查询哪个服务器？")
async def handle_server(bot: Bot, event: Event, state: T_State):
    server = state["server"]
    gold_price = await get_gold_price(server)
    await gold.finish(gold_price)


async def get_gold_price(server: str):
    """
    获取指定服务器的金价信息
    """
    # TODO：其他平台的金价
    _time = int(time.time()*1000)  # 得到13位时间戳
    get_ways_url = "https://api-wanbaolou.xoyo.com/api/platform/setting/gateways?__ts__={}&callback=__xfe0".format(
        _time)
    async with httpx.AsyncClient() as client:
        res = await client.get(get_ways_url)
        text = res.text.replace("__xfe0(", "").replace(");", "")
        _json = json.loads(text)
        server_dict = dict()
        # 拿到服务器列表，得到大区ID和服务器ID
        if _json['code'] and _json['msg'] == 'SUCCESS':
            for server_list in _json['data']['list']:
                for s in server_list['servers']:
                    server_dict[s['server_name']] = dict(server_id=s['server_id'], zone_id=server_list['zone_id'])
        if server in server_dict.keys():
            gold_url = f"https://api-wanbaolou.xoyo.com/api/buyer/goods/list?req_id=&zone_id=" \
                  f"{server_dict[server]['zone_id']}&server_id={server_dict[server]['server_id']}" \
                  f"&sort%5Bsingle_count_price%5D=0&game=jx3&page=1&size=10&goods_type=1&__ts__={_time}&callback=__xfe6"
            res = await client.get(gold_url)
            text = res.text.replace("__xfe6(", "").replace(");", "")
            _json = json.loads(text)
            if _json['code'] and _json['msg'] == 'SUCCESS':
                num = len(_json['data']['list'])
                _sum = 0
                for price in _json['data']['list']:
                    _sum += price['single_count_price']
                return f"{server}的金价：{_sum/num}\n数据来源：万宝楼"
            return f"查询失败！\n{_json}"
        else:
            return f"服务器{server}未找到，请使用主服务器名称查询！"
