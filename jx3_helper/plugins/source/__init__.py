import sys
from motor.motor_asyncio import AsyncIOMotorClient
import nonebot


driver = nonebot.get_driver()
db = None


@driver.on_startup
async def init_db():
    nonebot.logger.info("init db")
    global db
    db = AsyncIOMotorClient("mongodb://flypotato:tudou123@test.xsvcm.mongodb.net/test", serverSelectionTimeoutMS=3)['jx3_helper']

