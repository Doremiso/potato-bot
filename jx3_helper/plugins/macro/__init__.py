import random

import httpx
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


xinfa = ["冰心诀", "云裳心经", "花间游", "离经易道", "毒经", "补天诀", "莫问", "相知", "傲血战意", "铁牢律", "易筋经", "洗髓经",
         "焚影圣诀", "明尊琉璃体", "分山劲", "铁骨衣", "紫霞功", "太虚剑意", "天罗诡道", "惊羽诀", "问水诀", "笑尘诀", "北傲诀",
         "凌海诀", "隐龙诀", "太玄经"]


macro = on_command("宏", rule=to_me(), priority=5)


@macro.handle()
async def handle_set_server_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["xinfa"] = args


@macro.got("xinfa", prompt="要查找哪个心法的宏？")
async def handle_set_server_server(bot: Bot, event: Event, state: T_State):
    _xinfa = state["xinfa"]
    if _xinfa not in xinfa:
        await macro.reject("请重新输入！")
    res = await get_macro(_xinfa)
    await macro.finish(res)


async def get_macro(_xinfa):
    async with httpx.AsyncClient() as client:
        url = f"https://cms.jx3box.com/api/cms/posts?type=macro&per=18&page=1&subtype={_xinfa}&order=update&lang=cn&zlp=%E7%99%BD%E5%B8%9D%E9%A3%8E%E4%BA%91&client=std&sticky=1"
        try:
            res = await client.get(url)
        except Exception as e:
            return "查询失败！请反馈该错误\n{}".format(str(e))
        try:
            _json = res.json()
        except Exception as e:
            return "查询失败！请反馈该错误\n{}\n{}".format(str(e), res.text)
        if _json['msg'] == 'Success':
            # 取宏的总数
            num = len(_json['data']['list'])
            # 判断是否有宏
            if num:
                # 随机一个宏
                i = random.randint(0, num-1)
                # 取出随机宏的信息
                macro_info = _json['data']['list'][i]
                # 宏的id
                macro_id = macro_info['ID']
                # 作者
                macro_author = macro_info['author']
                # 标题
                macro_title = macro_info['post_title']
                macro_text = f"{macro_title}\n作者：{macro_author}\n云端宏：\n"
                for m in macro_info['post_meta']['data']:
                    macro_text += f"{macro_author}#{m['name']}\n"
                macro_text += f"链接：https://www.jx3box.com/macro/{macro_id}\n云端宏使用说明：https://www.jx3box.com/tool/18152"
                return macro_text
            else:
                return "未查找到当前心法的宏"
        return ''
