# создаем класс для хранения конфигурационных данных
class Config:
    TOKEN = "TOKEN"  # токен полученный от ботфазера
    list_start_commands = ["start"]  # перечень команд для запуска бота
    languages_dictionary = {"ru-RU": "Russian", "en-GB": "English",
                            "uk-UA": "Ukrainian", "pl-PL": "Poland",
                            "de-DE": "Germany", "fr-FR": "France"}
    translate_language_dictionary = {"ru": "Russian", "en": "English",
                                     "uk": "Ukrainian", "pl": "Poland",
                                     "de": "Germany", "fr": "France"}
