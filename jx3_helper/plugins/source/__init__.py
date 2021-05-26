import sys
from motor.motor_asyncio import AsyncIOMotorClient
import nonebot


driver = nonebot.get_driver()
db = None


@driver.on_startup
async def init_db():
    nonebot.logger.info("init db")
    global db
    db = AsyncIOMotorClient('localhost', 27017, serverSelectionTimeoutMS=3)['jx3_helper']



