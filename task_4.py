import requests

URL = "https://api.github.com"


def getUserProfile(username):
    url = f"{URL}/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("\n" + "=" * 50)
        print(f"Профиль пользователя: {data.get('login')}")
        print("=" * 50)
        print(f"Имя: {data.get('name', 'Не указано')}")
        print(f"Ссылка на профиль: {data.get('html_url')}")
        print(f"Количество репозиториев: {data.get('public_repos')}")
        print(f"Количество подписчиков: {data.get('followers')}")
        print(f"Количество подписок: {data.get('following')}")
        print("=" * 50 + "\n")
    else:
        print(f"Ошибка: пользователь {username} не найден (код {response.status_code})")


def getUserRepos(username):
    url = f"{URL}/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()
        if repos:
            print(f"\nРепозитории пользователя {username}:")
            print("=" * 50)
            for i, repo in enumerate(repos, 1):
                print(f"{i}. {repo['name']}")
                print(f"   Ссылка: {repo['html_url']}")
                print(f"   Язык: {repo.get('language', 'Не указан')}")
                print(f"   Видимость: {'Публичный' if not repo['private'] else 'Приватный'}")
                print(f"   Ветка по умолчанию: {repo.get('default_branch')}")
                print("-" * 30)
        else:
            print(f"У пользователя {username} нет публичных репозиториев")
    else:
        print(f"Ошибка при получении репозиториев (код {response.status_code})")


def searchRepositories(query):
    url = f"{URL}/search/repositories"
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        total = data['total_count']
        items = data['items']

        print(f"\nНайдено репозиториев по запросу '{query}': {total}")
        print("=" * 50)

        if items:
            for i, repo in enumerate(items, 1):
                print(f"{i}. {repo['full_name']}")
                print(f" - Ссылка: {repo['html_url']}")
                print(f" - Язык: {repo.get('language', 'Не указан')}")
                print(f" - Видимость: {'Публичный' if not repo.get('private', False) else 'Приватный'}")
                print(f" - Ветка по умолчанию: {repo.get('default_branch', 'main')}")
                print(f" - Дата создания: {repo.get('created_at', 'Не указано')[:10] if repo.get('created_at') else 'Не указано'}")
                print(f" - Последнее обновление: {repo.get('updated_at', 'Не указано')[:10] if repo.get('updated_at') else 'Не указано'}")

                description = repo.get('description')
                if description is None:
                    description_text = "Нет описания"
                else:
                    description_text = description

                print(f"   Описание: {description_text}")
                print("-" * 30)
        else:
            print("Репозитории не найдены")
    else:
        print(f"Ошибка при поиске (код {response.status_code})")


def main():
    while True:
        print("Меню")
        print("1 - посмотреть профиль")
        print("2 - получить все репозитории пользователя")
        print("3 - поиск репозиториев по названию")
        print("0 - выход")

        choice = input("Выберите действие: ")

        match choice:
            case "0":
                break
            case "1":
                name = input("Введите имя пользователя: ")
                getUserProfile(name)
            case "2":
                name = input("Введите имя пользователя: ")
                getUserRepos(name)
            case "3":
                name = input("Введите название репозитория: ")
                searchRepositories(name)


if __name__ == "__main__":
    main()