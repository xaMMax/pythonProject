# импорт классов клавиатур из основной библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# импортируем обьект lang
from application.callback_datas import lang

# инлайн клавиатура для выбора языка с заранее задаными параметрами
lang_keyboard = InlineKeyboardMarkup()  # обьявление обьекта класса InlineKeyboardMarkup
russian = InlineKeyboardButton("Русский", callback_data=lang.new(language="ru-Ru"))  # кнопка для русского языка
english = InlineKeyboardButton("English", callback_data=lang.new(language="en-En"))  # кнопка для английского языка
lang_keyboard.add(russian, english)  # добавление кнопок в ранее созданный обьект

# клавиатура для смены языка и выдачи инфосообщения
change_lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = "Изменить язык распознавания"
button1 = "Информация"
change_lang_keyboard.add(button, button1)

# клавиатура для смены выдачи инфосообщения во время старта
info = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = "Информация"
info.add(button)
