import requests, json
user = input('Введите имя пользователя: ')
main = requests.get(f'https://api.github.com/users/{user}/repos')
repos = json.loads(main.text)
print(f'Список репозиториев пользователя {user}')
with open('repos.json', 'w') as repos_json:
    for repo in repos:
        print(repo['name'])
        json.dump(repo['name'], repos_json)