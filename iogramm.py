import asyncio
import logging
from XML import process_xml
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6183086192:AAHhL9dQjHia65PMgGbL6HkChzz-K9CXWYo"

# All handlers should be attached to the Router (or Dispatcher)
router = Router()
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


@dp.message(F.document)
async def handle_xml_file(message: types.Message, bot: Bot):
    # Перевіряємо, чи це файл XML
    xml_type = ['application/xml', 'text/xml', 'xml']
    if message.document.mime_type in xml_type:
        # Отримуємо файл XML
        xml_file = await bot.get_file(message.document.file_id)
        await bot.download_file(xml_file.file_path, 'score.xml')
        # Викликаємо функцію для обробки XML
        result = process_xml('score.xml')

        # Відправляємо результат повернення функції користувачеві
        await message.answer(str(result))
    else:
        await message.reply("Будь ласка, надішліть файл XML.")

async def main() -> None:
    # Dispatcher is a root router
    # ... and all other routers should be attached to Dispatcher


    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())