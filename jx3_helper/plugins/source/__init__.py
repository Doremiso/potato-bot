import sys
from motor.motor_asyncio import AsyncIOMotorClient
import nonebot


driver = nonebot.get_driver()
db = None


@driver.on_startup
async def init_db():
    nonebot.logger.info("init db")
    global db
    mongodb_uri = driver.config.mongodb_uri
    if mongodb_uri:
        db = AsyncIOMotorClient(mongodb_uri, serverSelectionTimeoutMS=3)['jx3_helper']
    else:
        nonebot.logger.error("mongodb_uri not found!")
        sys.exit()

