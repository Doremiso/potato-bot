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

        if await self.table.find_one({"qq_group_id": qq_group_id}):
            try:
                await self.table.update_one({"qq_group_id": qq_group_id}, {"$set": {'server': server}})
            except Exception as e:
                return str(e)
            return True
        else:
            try:
                config = {"qq_group_id": qq_group_id, "server": server}
                await self.table.insert_one(config)
            except Exception as e:
                return str(e)
            return True

    async def get_server(self, qq_group_id):
        """
        查询区服
        :param qq_group_id:
        :return:
        """
        return await self.table.find_one({"qq_group_id": qq_group_id})
