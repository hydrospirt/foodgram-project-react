# Foodgram - Продуктовый помощник

Сервис создан для размещения рецептов различных блюд.

- Создание или редактирование рецептов
- Изучайте рецепты других пользователей, добавляйте их в избранное или корзину
- Подписыватся на пользователей и узнавайте о новых записях
- Скачать список ингредиентов, необходимых для приготовления блюд в корзине

### Технологии:
- Python 3.9
- Django 4.2
- djangorestframework 3.14.0
- PostgresSQL
- Nginx
- ReDoc
- Docker 20.10.24
- Docker-compose
- Yandex.oblako

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:hydrospirt/foodgram-project-react.git
```
Подключится к своему серверу:
```
ssh <server user>@<server IP>
```
Установить Docker на сервер:
```
sudo apt install docker.io
```
Установить docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:
```
sudo chmod +x /usr/local/bin/docker-compose
```
Запустить docker-compose:
```
sudo docker-compose up -d
```


# Автор
Эдуард Гумен - GitHub: https://github.com/hydrospirt