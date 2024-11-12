from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from config import dp, BaseStates
from main import run_main

router = Router(name="router")


@router.message(StateFilter(None), Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Введи API_ID из <a href='https://my.telegram.org/apps'>telegram apps</a>")
    await state.set_data({})
    await state.set_state(BaseStates.api_id_writing)


@dp.message(BaseStates.api_id_writing)
async def api_id_handler(message: Message, state: FSMContext):
    await message.answer("Введи API_HASH из <a href='https://my.telegram.org/apps'>telegram apps</a>")
    await state.set_data({"APP_API_ID": message.text})
    await state.set_state(BaseStates.api_hash_writing)


@dp.message(BaseStates.api_hash_writing)
async def api_id_handler(message: Message, state: FSMContext):
    await message.answer("Отлично, теперь можешь вводить тег канала(без @), я буду отправлять в ответ базу юзеров\n\n"
                         "Важно, чтобы этот бот был админом и мог смотреть пользователей в канале")
    await state.update_data({"APP_API_HASH": message.text})
    await state.set_state(BaseStates.ready_accept)


@dp.message(BaseStates.ready_accept)
async def api_id_handler(message: Message, state: FSMContext):
    await message.answer("Сбор начат")
    data = await state.get_data()
    APP_API_ID = data["APP_API_ID"]
    APP_API_HASH = data["APP_API_HASH"]
    exc, res = await run_main(message.text, "SESSION_" + message.text[:10], APP_API_ID, APP_API_HASH)
    if exc == 1:
        await message.answer("ОШИБКА: " + res)
    else:
        await message.answer_document(
            BufferedInputFile(str(res).encode('utf-8'), filename=f'{message.text}.txt'))
