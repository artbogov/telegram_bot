"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from core.core import Cities
from aiogram import Bot, Dispatcher, executor, types
import os


API_TOKEN = os.environ.get('TELEGRAM_API')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
chat = Cities()

@dp.message_handler(commands=['startgame'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    chat.set_cities_to_start_the_game()
    await message.reply(f"Игра началась. Назовите город.")

@dp.message_handler(commands=['gameover'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    chat.game_over()
    await message.reply(f"Игра завершена. Чтобы начать игру нажмите /startgame")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    await message.reply("Привет!\nДавай сыграем в города!\nНачать игру "
                        "/startgame\nСписок доступных команд /help")

@dp.message_handler(commands=['how'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    await message.reply("Каждый участник игры называет реально существующий "
                        "город России, название которого начинается на ту "
                        "букву, которой оканчивается название предыдущего "
                        "города.\n/startgame - начать игру")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    await message.reply("/how - как играть\n/startgame - начать игру\n"
                        "\n/already - названные города"
                        "\n/gameover - завершить игру")

@dp.message_handler(commands=['already'])
async def send_welcome(message: types.Message):
    chat.chat_id = message.chat.id
    await message.reply(f"Уже называли:\n {chat.get_cities_already()}")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    chat.chat_id = message.chat.id
    await message.answer(f'{chat.make_a_bot_move(message.text)}')
