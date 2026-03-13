import requests
import json

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = 'resource/save.json'


class CurrencyMonitor:
    def __init__(self):
        self.currencies = {}
        self.group = {}

    def fetchCurrencies(self):
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            self.currencies = data['Valute']

    def displayCurrencies(self):
        if not self.currencies:
            print('сначала загрузите днные о валютах')
            return

        for code, data in self.currencies.items():
            name = data['Name']
            nominal = data['Nominal']
            value = data['Value']


            print(f"{code:<6} {name:<50} {nominal:<8} {value:.4f}₽")

    def displayCurrincyByCode(self, code):
        if not self.currencies:
            print('сначала загрузите днные о валютах')
            return

        code = code.upper()
        if code in self.currencies:
            data = self.currencies[code]
            print(f"\n{'=' * 50}")
            print(f"Информация о валюте {code}:")
            print(f"{'=' * 50}")
            print(f"Название: {data['Name']}")
            print(f"Номинал: {data['Nominal']}")
            print(f"Курс: {data['Value']:.4f} ₽ за {data['Nominal']} {data['CharCode']}")
            print(f"Предыдущий курс: {data['Previous']:.4f}₽")

    def createGroup(self):
        if not self.currencies:
            print('сначала загрузите днные о валютах')
            return

        groupName = input("Введите название группы: ")

        if not groupName:
            print("Имя не может быть пустым")
            return

        if groupName in self.group:
            print("Такое имя уже существует")

        self.group[groupName] = []

    def addCurrencyToGroup(self, groupName, code):
        if groupName not in self.group:
            print(f"Группа {groupName} не найдена")
            return

        code = code.upper()
        if code in self.group[groupName]:
            print(f"Валюта {code} уже в группе")
            return

        if code not in self.currencies:
            print(f"Валюта {code} не найдена")
            return

        self.group[groupName].append(code)

    def removeCurrencyFromGroup(self, groupName, code):
        if groupName not in self.group:
            print(f"Группа {groupName} не найдена")
            return

        code = code.upper()
        if code not in self.group[groupName]:
            print(f"Валюты {code} нет в группе")
            return

        self.group[groupName].remove(code)

    def displayGroups(self):
        if not self.group:
            print("У вас нет групп")

        for groupName, currencies in self.group.items():
            print(groupName)
            for code in currencies:
                if code in self.currencies:
                    data = self.currencies[code]
                    name = data['Name']
                    value = data['Value']
                    nominal = data['Nominal']
                    print(f"{code:<6} {name:<50} {nominal:<8} {value:.4f}₽")

    def seveGroups(self):
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.group, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'ERROR: {e}')

    def loadGroups(self):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                self.group = json.load(f)
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {SAVE_FILE}. Файл поврежден.")
        except Exception as e:
            print(f'ERROR: {e}')


def main():
    currinces = CurrencyMonitor()
    while True:
        print("Выберете действие")
        print("1 - Посмотреть все валюты")
        print("2 - Посмотреть валюту по коду")
        print("3 - создать группу валют")
        print("4 - добавить валюту в группу")
        print("5 - удалить валюту из группы")
        print("6 - посмотреть все группы")
        print("7 - сохранить группы в json")
        print("8 - считать созданные группы из json")
        print("0 - выход")

        choice = input("Выберете что хотите сделать: ")

        match choice:
            case "1":
                currinces.displayCurrencies()
            case "2":
                code = input("Введите код валюты: ")
                currinces.displayCurrincyByCode(code)
            case "3":
                currinces.createGroup()
            case "4":
                groupName = input("Введите имя группы: ")
                code = input("Введите код валюты: ")
                currinces.addCurrencyToGroup(groupName, code)
            case "5":
                groupName = input("Введите имя группы: ")
                code = input("Введите код валюты: ")
                currinces.removeCurrencyFromGroup(groupName, code)
            case "6":
                currinces.displayGroups()
            case "7":
                currinces.seveGroups()
            case "8":
                currinces.loadGroups()
            case "9":
                currinces.fetchCurrencies()
            case "0":
                break
            case _:
                print("Неверное действие")


if __name__ == "__main__":
    main()