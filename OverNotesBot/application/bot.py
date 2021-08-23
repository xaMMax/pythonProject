import logging
import os
import time

# импорт основных необходимых модулей из библиотеки aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text

# импорт дополнительных модулей и классов
from application.callback_datas import lang
from classes import AudioSave, LanguageClass
from config import Config
from markup import lang_keyboard, change_lang_keyboard, info

# обьявление обьекта класса Бот
bot = Bot(token=Config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# ведение логов
logging.basicConfig(level=logging.INFO)
# обьявление обьекта класса LanguageClass
language = LanguageClass()


# стартовое приветствие
@dp.message_handler(Command(Config.list_start_commands))
async def welcome(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Приветствую, {0.first_name}!\n"
                           "Я бот для работы с Вашими голосовыми заметками.".format(message.from_user),
                           reply_markup=info)
    await bot.send_message(message.from_user.id, "Начните работу уже сейчас!\n"
                                                 "<i>Выберите язык заметки 😉</i>", reply_markup=lang_keyboard)


# Вызов "функции" изменения языка
@dp.message_handler(Text(equals="Изменить язык распознавания"))
async def call_another_keyboard(message: types.Message):
    await message.reply("Выберите язык", reply_markup=lang_keyboard)


# Показ инфо-сообщения
@dp.message_handler(Text(equals="Информация"))
async def info_function(message: types.Message):
    await message.answer(f"Здравствуйте! Я <i> OverNotes </i> бот.\nМоя задача преобразовать ваши заметки в текст, "
                         f"просто продиктуйте вашу заметку мне в головосом сообщении, не забыв вначале выбрать язык.\n"
                         f"<b>ВНИМАНИЕ: никогда не передавайте мне свои пароли.</b>\n"
                         f"Для перезапуска можно ввести одну из комманд <i>start, старт, поехали, go, пуск.</i>\n"
                         f"Для обратной связи и пожеланий пишите моему создателю на почту "
                         f"<b>petrolijuice@gmail.com</b>\n<i>PS: я нахожусь в ранней стадии разработки.</i>",
                         reply_markup=change_lang_keyboard)


# Функция изменения языка на русский
@dp.callback_query_handler(lang.filter(language="ru-Ru"))
async def language_ru(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    language.set_language(call.from_user.id, "ru-Ru")
    await call.message.answer(f"Вы выбрали <b>Русский</b> язык!", reply_markup=change_lang_keyboard)
    await message_delete(call.message, 0)


# Функция изменения языка на английский
@dp.callback_query_handler(lang.filter(language="en-En"))
async def language_en(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    language.set_language(call.from_user.id, "en-En")
    await call.message.answer(f"You choice <b>English</b> language!", reply_markup=change_lang_keyboard)
    await message_delete(call.message, 0)


# Основная функция бота
@dp.message_handler(content_types=[types.ContentType.VOICE])
async def get_voice(message: types.Message):
    file_info = await bot.get_file(message.voice.file_id)  # вытаскиваем ид записанного аудиосообщения
    if os.path.exists("files_voice"):
        pass
    else:
        os.mkdir("files_voice")
    filename = f"files_{file_info.file_path}"  # сохранение в переменную имени файла и пути
    await message.voice.download(filename)  # скачиваем файл на сервер с ботом
    # обьявление обьекта класса AudioSave с параметрами имя файла и языка выбранного ранее привязанного к ид
    # пользователя
    voice_file = AudioSave(filename=filename, language=language.get_language(message.from_user.id))
    # конвертация файла с помошью метода convert_file класса AudioSave
    voice_file.convert_file()
    # распознавание файла  с помошью метода recognize_file класса AudioSave
    recognition_file = await voice_file.recognize_file()
    # задаем условие если файл возможно распознать возвращаем текст распознаного файла и отправляем пользователю
    if recognition_file != "<i>Я тебя не слышу!\n🙉</i>":
        await bot.send_message(message.from_user.id, f"{recognition_file}", disable_notification=True)
        await voice_file.delete_file()
    # в противном случае (невозможно распознать): удаляем аудиофайл и информационное сообщение (через указанное время)
    else:
        msg = await message.reply(f"<b>{recognition_file}</b>"
                                  f"\n<i>Это сообщение удалиться через 5 секунд</i>")
        await message_delete(msg, 5)
        await message_delete(message, 1)
        await voice_file.delete_file()


# Функция удаления сообщения с учетом времени
async def message_delete(name: types.message.Message, secs: int):
    time.sleep(secs)
    await name.delete()
    return


# Основной запуск бота
if __name__ == '__main__':
    while True:  # Цикл запуска/перезапуска бота в случае непредвиденной ошибки
        try:
            executor.start_polling(dp, skip_updates=False)
        except Exception:
            print("Something went wrong, I go to restart myself")
            executor.start_polling(dp, skip_updates=False)
