from aiogram import types


def start_button():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton("Сгенерувати QR код")
    )


def back_button():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton("Головне меню")
    )
