![Foodgram workflow](https://github.com/hydrospirt/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
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
Добавить в nginx ваш ip сервера:
```
server {
    listen 80;
    server_name ip адрес;
    server_tokens off;
    ...
```
Скопирвать папки 'docs/', 'fontend/' и файлы docker-compose.yml, nginx.conf (на вашем локальном компьютере) на ваш сервер:
```
scp -r docs/* <server user>@<server IP>:/home/<server user>/
```
Создать .env
```
touch .env
```
Заполнить .env данными:
```
echo SECRET_KEY=Ваш секретный ключ Django >> .env
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=имя вашей БД >> .env
echo POSTGRES_USER=имя пользователя БД >> .env
echo POSTGRES_PASSWORD=пароль от вашей БД >> .env
echo DB_HOST=хост >> .env
echo DB_PORT=порт по умолчанию 5432 >> .env
```
Изменить настройки в settings.py:
```
CSRF_TRUSTED_ORIGINS = [http://ip или сайт]
```
Запустить docker-compose:
```
sudo docker-compose up -d
```
Применить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
Собрать статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Создать супер пользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Заполнить базу данных ингредиентами:
```
sudo docker-compose exec backend python manage.py fill_db ingredients.csv
```

# Автор
Эдуард Гумен - GitHub: https://github.com/hydrospirt
