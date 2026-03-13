import requests


URLS = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]


def checkUrlStatur(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            statusMessage = "доступен"
        elif response.status_code == 403:
            statusMessage = "вход запрещен"
        elif response.status_code == 404:
            statusMessage = "не найден"
        elif response.status_code >= 500:
            statusMessage = "ошибка сервера"
        else:
            statusMessage = "неизвестный статус"
        return statusMessage, response.status_code
    except requests.exceptions.RequestException as e:
        return "не доступен (ошибка соединения)", None
    except requests.exceptions.Timeout:
        return "не доступен (таймаут)", None
    except Exception as e:
        return f"ошибка ({e})", None


def main():
    print("Проверка доступности веб-сайтов")
    for url in URLS:
        statusMessage, statusCode = checkUrlStatur(url)
        if statusCode:
            print(f"{url} - {statusMessage} - {statusCode}")
        else:
            print(f"{url} - {statusMessage}")


if __name__ == "__main__":
    main()