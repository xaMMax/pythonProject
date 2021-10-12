import json
import logging
import random
import time

import gtts
# импорт основных необходимых модулей из библиотеки "aiogram"
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text

# импорт дополнительных модулей и классов
from application.callback_datas import lang, trans_lang
from classes import AudioSave, LanguageClass, Translate
from config import Config
from markup import lang_keyboard, change_lang_keyboard, info, trans_markup

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
                           f"Hello {message.from_user.first_name}! I am a <i> Translator </i> Bot.\n"
                           "My task is to translate your voice message into the selected language.",
                           reply_markup=info)
    await bot.send_message(message.from_user.id, "Get start now!\n"
                                                 "<i>Choice language for recognition 😉</i>", reply_markup=lang_keyboard)


# Вызов "функции" изменения языка
@dp.message_handler(Text(equals="Change recognition language"))
async def call_another_keyboard(message: types.Message):
    await message.reply("Choice language", reply_markup=lang_keyboard)


# Показ инфо-сообщения
@dp.message_handler(Text(equals="Info"))
async def info_function(message: types.Message):
    await message.answer(f"Hello! I am a <i> Translator </i> Bot.\nMy task is to translate your voice message into "
                         f"the selected language. I support multiple languages, English, German, French, Polish, "
                         f"Russian, Ukrainian. Translation can be done between these languages\n"
                         f"For restart press start via keyboard <i>start</i>\n"
                         f"For feedback and wishes send email to my creator\n"
                         f"<b>petrolijuice@gmail.com</b>\n<i>PS: it is my early development stage.</i>"
                         f"Ypu can find open_code in GitHub...................",
                         reply_markup=change_lang_keyboard)


# Функция изменения языка
@dp.callback_query_handler(lang.filter(language="ru-RU"))
@dp.callback_query_handler(lang.filter(language="en-GB"))
@dp.callback_query_handler(lang.filter(language="uk-UA"))
@dp.callback_query_handler(lang.filter(language="pl-PL"))
@dp.callback_query_handler(lang.filter(language="de-DE"))
@dp.callback_query_handler(lang.filter(language="fr-FR"))
async def language_ru(call: types.CallbackQuery):
    recognition_language = call.data[-5:]
    await call.answer(cache_time=60)
    language.set_language(call.from_user.id, recognition_language)
    await call.message.answer(f"Your choice <b>{Config.languages_dictionary.get(recognition_language)}</b> !",
                              reply_markup=change_lang_keyboard)
    await message_delete(call.message, 0)


# Основная функция бота
@dp.message_handler(content_types=[types.ContentType.VOICE])
async def get_voice(message: types.Message):
    file_info = await bot.get_file(message.voice.file_id)  # вытаскиваем ид записанного аудиосообщения
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
    if recognition_file != "<i>I can`t hear you!\n🙉</i>":
        await bot.send_message(message.chat.id, f"You add:\n{recognition_file}", disable_notification=True,
                               reply_markup=trans_markup)
        await voice_file.delete_file()
    else:
        msg = await message.reply(f"<b>{recognition_file}</b>"
                                  f"\n<i>message will be delete after 5 seconds</i>")
        await message_delete(msg, 5)
        await message_delete(message, 1)
        await voice_file.delete_file()
    await save_text(message.from_user.id, recognition_file)


async def save_text(user_id: int, text: str):
    try:
        with open("Text.json", "r+") as file:
            json_decoded = json.load(file)
        json_decoded[user_id] = text
        with open("Text.json", "w+") as json_file:
            json.dump(json_decoded, json_file)

    except json.decoder.JSONDecodeError:
        with open("Text.json", "w") as file:
            data: dict = {user_id: text}
            json.dump(data, file)


# Захват колбэка с функцией перевода
@dp.callback_query_handler(trans_lang.filter(tlang="pl"))
@dp.callback_query_handler(trans_lang.filter(tlang="ru"))
@dp.callback_query_handler(trans_lang.filter(tlang="en"))
@dp.callback_query_handler(trans_lang.filter(tlang="uk"))
@dp.callback_query_handler(trans_lang.filter(tlang="fr"))
@dp.callback_query_handler(trans_lang.filter(tlang="de"))
async def translate_and_send(call: types.CallbackQuery):
    translate_language = call.data[-2:]
    await bot.send_message(call.message.chat.id, f"You choice {Config.translate_language_dictionary.get(translate_language)}")
    await call.answer(cache_time=60)
    with open("Text.json", "r") as file:
        data = json.loads(file.read())
        text = data.get(str(call.from_user.id))

    trans = Translate(user_id=call.from_user.id)
    trans_text = await trans.translate_text(translate_language, str(text))
    await bot.send_message(call.message.chat.id, trans_text, disable_notification=True)

    text_to_speech = gtts.gTTS(trans_text, lang=translate_language)
    namefile_random = random.randint(99, 9999)
    text_to_speech.save(f"files_voice/{namefile_random}.mp3")
    await bot.send_document(call.message.chat.id, open(f"files_voice/{namefile_random}.mp3", "rb"))


# Функция удаления сообщения с учетом времени
async def message_delete(name: types.message.Message, secs: int):
    time.sleep(secs)
    await name.delete()
    return


# Основной запуск бота
if __name__ == '__main__':
    def bot_start():
        print(f"The bot started at {time.strftime('%m/%d/%Y, %H:%M:%S')}")
        executor.start_polling(dp, skip_updates=False)
        print(f"The bot stopped at {time.strftime('%m/%d/%Y, %H:%M:%S')}")
    bot_start()
