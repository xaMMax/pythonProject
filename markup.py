# импорт классов клавиатур из основной библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# импортируем обьект lang
from application.callback_datas import lang, trans_lang

# инлайн клавиатура для выбора языка с заранее задаными параметрами
lang_keyboard = InlineKeyboardMarkup()  # обьявление обьекта класса InlineKeyboardMarkup
russian = InlineKeyboardButton("Ru 🇷🇺", callback_data=lang.new(language="ru-RU"))  # кнопка для русского языка
english = InlineKeyboardButton("En 🇬🇧", callback_data=lang.new(language="en-GB"))  # кнопка для английского языка
polish = InlineKeyboardButton("Pl 🇵🇱", callback_data=lang.new(language="pl-PL"))  # кнопка для английского языка
ukrainian = InlineKeyboardButton("Ua 🇺🇦", callback_data=lang.new(language="uk-UA"))  # кнопка для английского языка
german = InlineKeyboardButton("De 🇩🇪", callback_data=lang.new(language="de-DE"))  # кнопка для английского языка
french = InlineKeyboardButton("Fr 🇫🇷", callback_data=lang.new(language="fr-FR"))  # кнопка для английского языка
lang_keyboard.add(russian, english, polish, ukrainian, german, french)  # добавление кнопок в ранее созданный обьект

# клавиатура для смены языка и выдачи инфосообщения
change_lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = "Change recognition language"
button1 = "Info"
change_lang_keyboard.add(button, button1)

# клавиатура для смены выдачи инфосообщения во время старта
info = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = "Info"
info.add(button)


trans_markup = InlineKeyboardMarkup()
russian = InlineKeyboardButton("Ru 🇷🇺", callback_data=trans_lang.new(tlang="ru"))  # кнопка для русского языка
english = InlineKeyboardButton("En 🇬🇧", callback_data=trans_lang.new(tlang="en"))  # кнопка для английского языка
polish = InlineKeyboardButton("Pl 🇵🇱", callback_data=trans_lang.new(tlang="pl"))  # кнопка для английского языка
ukrainian = InlineKeyboardButton("Ua 🇺🇦", callback_data=trans_lang.new(tlang="uk"))  # кнопка для английского языка
german = InlineKeyboardButton("De 🇩🇪", callback_data=trans_lang.new(tlang="de"))  # кнопка для английского языка
french = InlineKeyboardButton("Fr 🇫🇷", callback_data=trans_lang.new(tlang="fr"))  # кнопка для английского языка
trans_markup.add(russian, english, polish, ukrainian, german, french)  # добавление кнопок в ранее созданный обьект
