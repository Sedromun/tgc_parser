import os
import sqlite3
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import StatesGroup, State

load_dotenv()


TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
bot = Bot(str(TG_BOT_TOKEN), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


class BaseStates(StatesGroup):
    api_id_writing = State()
    api_hash_writing = State()
    ready_accept = State()
