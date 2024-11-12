import asyncio

from config import dp, bot
from handlers import router

dp.include_router(router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



