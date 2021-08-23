# импорт основных модулей
import json
import os
import subprocess

# импорт дополнительных модулей
import aiofiles.os
import speech_recognition as sr  # импорт модуля для распознавания аудио в текст с дпльнейшим именем "sr"


# создаем класс для работы с файлом
class AudioSave:
    def __init__(self, filename, language="ru-Ru"):
        self.filename = filename
        self.language = language
        self.curr_path = os.path.dirname(__file__)
        self.new_file = (self.filename[:-3] + "wav")

    # метод для конвертации файла из .oga в .wav
    def convert_file(self):
        # запуск конвертера вне интерпретатора
        if os.path.exists(os.path.abspath(self.filename)) and os.path.exists(self.new_file):
            pass
        else:
            process = subprocess.run(["ffmpeg", "-hide_banner", "-i", (os.path.abspath(self.filename)), self.new_file])
            if process.returncode != 0:
                raise Exception("Something went wrong")

    # запуск распознавания файла с помошью google speech recognition
    async def recognize_file(self):
        try:
            tlg_audio = sr.AudioFile(os.path.abspath(self.new_file))
            r = sr.Recognizer()
            with tlg_audio as source:
                audio = r.listen(source)
                if self.language is None:
                    self.language = "ru-Ru"
                    text = r.recognize_google(audio, language=self.language)
                    return f"<i>Вы добавили:</i>\n\n<b>{text}</b>"
                else:
                    text = r.recognize_google(audio, language=self.language)
                    return f"<i>Вы добавили:</i>\n\n<b>{text}</b>"
        except sr.UnknownValueError:
            return "<i>Я тебя не слышу!\n🙉</i>"

    # статический метод удаления файлов при достижении в папке колличества больше 100
    @staticmethod
    async def delete_file():
        count = len([i for i in os.scandir("files_voice")])
        if count > 100:
            try:
                for items in [i for i in os.scandir("files_voice")]:
                    await aiofiles.os.remove(items)
                print("")
                return "<i>Кэш вычищен👾</i>"
            except FileExistsError:
                raise print("Пора почистить кэш")
        else:
            return "<i>Нечего удалять бл👾</i>"


# создаем класс для работы с языками
class LanguageClass:
    def __init__(self, user_id=0, language="ru-Ru"):
        self._language: str = language
        self.user_id: int = user_id
        self.lang_state: dict = {}

    # сохраняем в json словарь ключ = ид пользователя, значение = язык выбран пользователем
    def set_language(self, user_id: int, lang_types: str):
        self.user_id = user_id
        self._language = lang_types
        self.lang_state[user_id] = lang_types
        try:
            with open("states.json", "a+") as file:
                dictionary: dict = json.load(file)
                dictionary[user_id] = lang_types
                json.dump(dictionary, file)
        except json.decoder.JSONDecodeError:
            with open("states.json", "w") as file:
                data = self.lang_state
                json.dump(data, file)

    # метод возвращения переменной языка из словаря заданног ранее
    @staticmethod
    def get_language(user_id: int):
        try:
            with open("states.json", "r") as file:
                state: dict = json.load(file)
                lang = state.get(str(user_id))
                return lang
        except FileNotFoundError:
            with open("states.json", "w") as file:
                data = {1: "ru-Ru"}
                json.dump(data, file)
