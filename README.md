# Тестовое задание Кирьяков П.А.

Тестовый проект, реализующий следующий функционал:
* регистрацию пользователей;
* отправку сообщения от авторизованных пользователей;
* вывод последних n сообщений;


## Требования
* python3.10
* pipenv
* postgresql 13

  (тестировалось на ubuntu20.04)

## Как развернуть

0) Склонировать проект
1) Создать виртуальное окружение. Выполнить команду из корня проекта:
```bash
pipenv install
```
2) Создать две базы данных (основная и тестовая)

3) В корне проекта создать файл .env, заполнить его подобно файлу .env.example

4) Активировать виртуальное окружение.
Из корня проекта выполнить команду:
```bash
pipenv shell
```
5) Создать таблицы в БД:
```bash
cd src
alembic upgrade head
```

## Запуск
0) В файле start.sh изменить переменную PROJECT_PATH, указав в ней путь до проекта
1) Сделать start.sh запускаемым:
```bash
chmod +x start.sh
```
2) Запустить:
```bash
./start.sh
```

После запуска будет доступен сваггер по эндпоинту /docs


## Тестирование
0) В файле test.sh изменить переменную PROJECT_PATH, указав в ней путь до проекта
1) Сделать start.sh запускаемым:
```bash
chmod +x test.sh
```
2) Запустить:
```bash
./test.sh
```


## Запуск из докера

### Требования
* docker 20.10
* docker-compose 1.29

0) Склонировать образ приложения
https://hub.docker.com/repository/docker/forcequell/insaid_test_task_kiryakov

1) Запустить
```bash
sudo docker-compose up
```

Приложен файл с примерами запросов: sample_requests.sh
