from aiogram.utils.callback_data import CallbackData

# задаем обьект lang класса CallbackData с параметрами нашей клавиатуры
lang = CallbackData("use", "language")
lang.filter()

trans_lang = CallbackData("translate_lang", "tlang")
trans_lang.filter()
