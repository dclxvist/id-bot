from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Вспомогательная Функция ---

async def send_ids_for_copy(message: types.Message, main_file_id: str, file_type: str, thumb_file_id: str = None):
    response_text = f"ID {file_type}:\n`{main_file_id}`"

    if thumb_file_id:
        response_text += f"\n\nID миниатюры:\n`{thumb_file_id}`"

    await message.answer(
        response_text,
        parse_mode="Markdown"
    )

# --- Хендлеры Команд и Медиафайлов ---

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Приве́тствую!\n\nЭтот бот предназначен для мгновенного получения ID различных медиафайлов и их миниатюр в Telegram.\n\n"
        "Просто отправьте в чат любой из следующих типов файлов:\n\n"
        "      📸 Фото\n"
        "      📹 Видео\n"
        "      🎵 Аудио\n"
        "      📄 Документ\n"
        "      🌠 Стикер\n"
        "      🎙️ Голосовое сообщение\n"
        "      🎥 Видеосообщение\n"
        "      🎇 GIF-анимацию\n\n"
        "upd: бот не собирает и не хранит никакие ваши данные и информацию о файлах. Код доступен на <a href='https://github.com/dclxvist/id-bot.git'>GitHub</a>.",
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    main_file_id = message.photo[-1].file_id # большая версия фото
    thumb_file_id = message.photo[0].file_id # миниатюра
    await send_ids_for_copy(message, main_file_id, "картинки", thumb_file_id)

@dp.message(F.audio)
async def handle_audio(message: types.Message):
    main_file_id = message.audio.file_id
    thumb_file_id = message.audio.thumbnail.file_id if message.audio.thumbnail else None
    await send_ids_for_copy(message, main_file_id, "аудио", thumb_file_id)

@dp.message(F.document)
async def handle_document(message: types.Message):
    main_file_id = message.document.file_id
    thumb_file_id = message.document.thumbnail.file_id if message.document.thumbnail else None
    await send_ids_for_copy(message, main_file_id, "документа", thumb_file_id)

@dp.message(F.video)
async def handle_video(message: types.Message):
    main_file_id = message.video.file_id
    thumb_file_id = message.video.thumbnail.file_id if message.video.thumbnail else None
    await send_ids_for_copy(message, main_file_id, "видео", thumb_file_id)

@dp.message(F.animation)
async def handle_animation(message: types.Message):
    main_file_id = message.animation.file_id
    thumb_file_id = message.animation.thumbnail.file_id if message.animation.thumbnail else None
    await send_ids_for_copy(message, main_file_id, "анимации (GIF)")

@dp.message(F.voice)
async def handle_voice(message: types.Message):
    main_file_id = message.voice.file_id
    await send_ids_for_copy(message, main_file_id, "голосового сообщения")

@dp.message(F.video_note)
async def handle_video_note(message: types.Message):
    main_file_id = message.video_note.file_id
    await send_ids_for_copy(message, main_file_id, "видеосообщения")

@dp.message(F.sticker)
async def handle_sticker(message: types.Message):
    main_file_id = message.sticker.file_id
    await send_ids_for_copy(message, main_file_id, "стикера")

# --- Запуск Бота ---

async def main():
    print("Бот запущен!")

    commands_for_bot = [
        BotCommand(command="start", description="Получить информацию"),
    ]
    await bot.set_my_commands(commands_for_bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())