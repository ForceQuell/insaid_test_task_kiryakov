# Тестовое задание Кирьяков П.А.

### Требования
* python3.10
* pipenv
* postgresql

  (тестировалось на ubuntu20.04)

### Как развернуть:

0) Склонировать проект
1) Создать виртуальное окружение: выполнять команду из корня проекта:
```bash
pipenv install
```
2) Создать две базы данных (основная и тестовая):

от имени юзера postgres выполнить:
```bash
psql
CREATE ROLE <username> WITH '<password>';
CREATE DATABASE <main db name>;
CREATE DATABASE <test db name>;
GRANT ALL PRIVILEGES ON DATABASE <main db name> TO <username>;
GRANT ALL PRIVILEGES ON DATABASE <test db name> TO <username>;
ALTER ROLE "<username>" WITH LOGIN;
```

3) В корне проекта создать файл .env, заполнить его подобно файлу .env.example

4) Активировать виртуальное окружение:
из корня проекта выполнить команду:
```bash
pipenv shell
```
5) Создать таблицы в БД:
```bash
cd src
alembic upgrade head
```

### Запуск
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


### Тестирование
0) В файле test.sh изменить переменную PROJECT_PATH, указав в ней путь до проекта
1) Сделать start.sh запускаемым:
```bash
chmod +x test.sh
```
2) Запустить:
```bash
./test.sh
```
