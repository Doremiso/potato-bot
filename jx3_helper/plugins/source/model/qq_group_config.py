import nonebot


class QQGroupConfig:
    def __init__(self):
        from ...source import db
        if db:
            self.table = db['QQGroupConfig']
        else:
            nonebot.logger.error("数据库未初始化！")

    async def set_server(self, qq_group_id, server):
        """
        设置区服
        :param qq_group_id:群号
        :param server:服务器名
        :return:
        """

        return await self.update_db(qq_group_id, 'server', server)

    async def get_server(self, qq_group_id):
        """
        查询区服
        :param qq_group_id:
        :return:
        """
        res = await self.table.find_one({"qq_group_id": qq_group_id})
        return res['server']

    async def set_add_msg(self, qq_group_id, msg):
        """
        设置新人进群欢迎语
        :param qq_group_id:
        :param msg:
        :return:
        """
        return await self.update_db(qq_group_id, 'msg', msg)

    async def get_add_msg(self, qq_group_id):
        """
        获取新人进群欢迎语
        :param qq_group_id:
        :return:
        """
        res = await self.table.find_one({"qq_group_id": qq_group_id})
        return res['msg']

    async def update_db(self, qq_group_id, key, value):
        """
        修改数据库
        :param qq_group_id:群号
        :param key:
        :param value:
        :return:
        """
        if await self.table.find_one({"qq_group_id": qq_group_id}):
            try:
                await self.table.update_one({"qq_group_id": qq_group_id}, {"$set": {key: value}})
            except Exception as e:
                return str(e)
            return True
        else:
            try:
                config = {"qq_group_id": qq_group_id, key: value}
                await self.table.insert_one(config)
            except Exception as e:
                return str(e)
            return True
