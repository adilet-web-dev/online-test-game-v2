# online-test-game-v2
Онлайн приложение для интерактивного, одновременного тестирования студентов.
Во время прохождения теста студенты (ученики) могут видеть рейтинг, что делает тест как игру.
За правильный ответ получает баллы.
Время на ответ ограничен, а также за оставшееся время даются дополнительные баллы
В конце игры выводятся 3 победителя

### Есть два роли:
1. Создатель. Он создает тесты и создает запускает тест (рекомендуется использовать ноутбук или компьютер и подключить к большому экрану).
2. Игрок. Он же проходит тест
### Немедленный запуск приложения
с начала выполните Установка -> Фронтенд - Vue -> 2 пункт

и запустите с помощью докера
```
docker-compose up --build
```
### Установка
#### Фронтенд - Vue (папка frontend-v2)
1. Установите зависимости с помощью
```
npm install
```
2. Смените домен в файле hosts.ts на домен вашего сервера
```
export const HOST: string = '127.0.0.1:8000';
```
3.1 Для разработки запустите с помощью
```
npm run serve
```
3.2 Для продакшена соберите приложение с помощью
```
npm run build
```
И можете использовать любой сервер для обслуживания статик файл в директории dist/
Например можете использовать http-server
```
npm install -g http-server
http-server dist
```

#### Бекенд - Python: Django (папка backend)
1. Установите зависимости
```
pipenv install
```
2. Войдите в виртуальное окружение
```
pipenv shell
```
3. У вас должен быть установлены PostgreSQL и Redis
(Лично у меня PostgreSQL стоит на Линуксе, а Redis запускаю с помощью докера `docker run -p 6379:6379 -d redis`)
4. Поставьте переменные окружение

В Windows создайте файл .env и пропишите как примере свои параметры
```
DEBUG=True
SECRET_KEY=jgidfsgsodfhfskdfjhsdd
DATABASE_URL=postgres://postgres_user:postgres_password21@your_postgres_host:5432/database
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```
В Линукс переменные выше пропишите в командной строке только поставив export перед. Например `export DEBUG=True`

5. Сделайте миграции и запустите
```
python manage.py migrate
daphne -p 8000 -d 0.0.0.0 config.asgi:application
```
### Проблемы? 
Пишите в Issues в этой же репозитории
### Дополнительные ссылки
Django сервер - https://www.djangoproject.com/

Django Channels (для вебсокетов) - https://channels.readthedocs.io/en/stable/

Daphne для запуска в продакшене - https://github.com/django/daphne

Vue-class-component Чтобы использовать TypeScript вместе с Vue - https://class-component.vuejs.org/

Bootstrap-vue тотже бутстрап чтобы красиво было :) - https://bootstrap-vue.org/
