from aiofiles import os
import aiofiles as aiofiles
from aiogram import Dispatcher, executor, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from qr import create_qr_code
from bot_buttons import *
from db_users import insert_id
import config

storage = MemoryStorage()
bot = Bot(config.TG_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class QRInfo(StatesGroup):
    name = State()
    password = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    insert_id(message.from_user.username)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Вас вітає бот\n"
        "Я можу згенерувати QR код для вашого wi-fi."
        " Вам потрібно лише натиснути кнопку *Сгенерувати QR код* і дотримуватись інструкції",
        parse_mode="Markdown",
        reply_markup=start_button(),
    )


@dp.message_handler(Text(equals="Головне меню"), state=["*"])
async def back(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Ви повернулися в головне меню",
        reply_markup=start_button(),
    )
    await state.finish()


@dp.message_handler(Text(equals="Сгенерувати QR код"))
async def generate(message: types.Message):
    await QRInfo.name.set()
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Введіть назву свого WI-FI",
        reply_markup=back_button(),
    )


@dp.message_handler(state=QRInfo.name)
async def save_name(message: types.Message, state: FSMContext):
    if validate(message.text):
        async with state.proxy() as data:
            data["name"] = message.text
        await QRInfo.next()
        await bot.send_message(
            chat_id=message.from_user.id, text="А тепер введіть пароль від WI-FI"
        )
    else:
        cur_state = await state.get_state()
        if cur_state is None:
            return
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ви ввели забагато символів",
            reply_markup=start_button(),
        )
        await state.finish()

@dp.message_handler(state=QRInfo.password)
async def save_name(message: types.Message, state: FSMContext):
    if validate(message.text):
        async with state.proxy() as data:
            data["password"] = message.text
        await bot.send_message(chat_id=message.from_user.id, text="Вся інформація отримана")
        async with state.proxy() as data:
            create_qr_code(data["name"], data["password"], message.from_user.username)
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Назва вашого WI-FI: *{data['name']}*\nПароль вашого WI-FI: *{data['password']}*",
                parse_mode="Markdown",
                reply_markup=start_button(),
            )
        await state.finish()
        async with aiofiles.open(f"{message.from_user.username}.png", "rb") as photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await os.remove(f"{message.from_user.username}.png")
    else:
        cur_state = await state.get_state()
        if cur_state is None:
            return
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ви ввели забагато символів",
            reply_markup=start_button(),
        )
        await state.finish()

@dp.message_handler()
async def hello(message: types.Message):
    await message.answer("Оберіть дію", reply_markup=start_button())


def validate(message):
    if len(message) > 40:
        return False
    else:
        return True

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
