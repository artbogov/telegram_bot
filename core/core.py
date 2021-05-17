"""Логика игры в Города"""


from collections import defaultdict


class Cities:
    """Игра в Города.

    Атрибуты:
        cities(dict) - Список городов, которые игрок может назвать, хранится
        для каждой игры
        cities_already(dict) - Список названных городов, хранится для
        каждой игры
        last_letter_of_the_city(dict) - Последняя буква названного города
        first_letter_of_the_city(dict) - Первые буквы городов
        chat_id(int) - ID игры (телеграм чата)

    Методы:
        checking_city() - проверяет входит ли введенный пользователем город в
        перечень доступных городов
        get_cities_already() - выводит список названных городов
        set_cities_to_start_the_game() - задает список городов вначале игры
        make_a_bot_move() - ход бота и подсказка пользователю на какую букву
        ему требуется назвать город
    """

    cities = defaultdict(list)
    cities_already = defaultdict(list)
    last_letter_of_the_city = defaultdict(list)
    first_letter_of_the_city = defaultdict(list)
    chat_id = None

    def __init__(self):
        pass

    def game_over(self):
        """Очищаем словари по id чата при завершении игры пользователем"""
        try:
            del self.cities[self.chat_id]
            del self.first_letter_of_the_city[self.chat_id]
            del self.cities_already[self.chat_id]
            del self.last_letter_of_the_city[self.chat_id]
        except KeyError:
            pass

    def checking_city(self, city):
        """Проверка введенного пользователем города на наличие в списке
        городов и уже названных городов.
        Аргумент:
        city(str) - город введенный пользователем
        :return True - если город есть в списке и False если указан
        некорректный город или город назывался ранее
        :rtype Boolean
        """
        city = city.lower()
        if self.last_letter_of_the_city[self.chat_id] and \
                self.last_letter_of_the_city[self.chat_id] != city[0]:
            return False
        if city in self.cities[self.chat_id]:
            self.cities[self.chat_id].remove(city)
            self.cities_already[self.chat_id].append(city.title())
            for letter in reversed(city):
                if self.first_letter_of_the_city[self.chat_id][letter] > 0:
                    self.last_letter_of_the_city[self.chat_id] = letter
                    break
            return True
        else:
            return False

    def get_cities_already(self):
        """Получаем строку с названными городами.
        :return Строка с названными городами
        :rtype str
        """
        return ', '.join(self.cities_already[self.chat_id])

    def set_cities_to_start_the_game(self):
        """Задает начальный список городов, которые можно называть в игре
        из файла cities.txt если список еще не установлен.
        """
        if self.chat_id is not None:
            self.cities[self.chat_id].clear()
            self.cities_already[self.chat_id].clear()
            self.last_letter_of_the_city[self.chat_id].clear()
            self.first_letter_of_the_city[self.chat_id].clear()
            with open('cities.txt', 'r', encoding='utf-8') as f:
                temp = []
                first_letter = defaultdict(int)
                for line in f:
                    temp.append(line.replace('\n', ''))
                    first_letter[line[0]] += 1
                self.cities[self.chat_id] = temp.copy()
                self.first_letter_of_the_city[self.chat_id] = \
                    first_letter.copy()

    def make_a_bot_move(self, city):
        """Ответ бота на ход пользователя. Если указан неверный город или город,
        который уже назывался - просьба назвать город на указанную букву.
        Если пользователь указал корректный город - бот делает ход (называет
        город).
        Аргумент:
        city(str) - город введенный пользователем
        :return Строка с ответом бота
        :rtype str
        """
        if self.checking_city(city):
            say_bot_city = ''
            for current_city in self.cities[self.chat_id]:
                if current_city[0] == \
                        self.last_letter_of_the_city[self.chat_id]:
                    say_bot_city = current_city
                    self.checking_city(current_city)
                    break
            return f'{say_bot_city.title()}\nНазовите город на букву ' \
                   f'{self.last_letter_of_the_city[self.chat_id].title()}'
        else:
            if self.last_letter_of_the_city[self.chat_id]:
                return f'Назовите город на букву ' \
                       f'{self.last_letter_of_the_city[self.chat_id].title()}' \
                       f'\n' \
                   f'Список названных городов доступен по команде /already'
            else:
                return 'Такого города нет. Назовите правильное название города'
