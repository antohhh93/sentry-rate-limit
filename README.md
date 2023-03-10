# Sentry Rate Limit

Приложение обеспечивает гибкий способ управления количеством ошибок на организацию/проект/ключ.

### Минимальные требования

* Python >= 3.9
* PostgreSQL >= 11.8
* Sentry API [auth token](https://docs.sentry.io/api/auth/#auth-tokens)
    > Authentication token permissions: `org:read` `project:read` `project:write`

## Запуск приложения

1. Скопировать файл конфигурации `ratelimit/config.example.py` в `ratelimit/config.py`
2. Изменить настройки в файле конфигурации `ratelimit/config.py`, если это необходимо
3. Установить необходимые зависимости `pip install -r requirements.txt`
4. Собрать приложение `python setup.py install`
5. Запустить приложение `sentry-rate-limit`


## Запуск приложения в виртуальном окружение Python

1. Создать виртуально окружение `python3 -m venv .venv`
2. Активировать виртуальное окружение:
   *  `source .venv/bin/activate` - для Linux и MacOS
   *  `.venv\Scripts\activate.bat` - для Windows
   *  `deactivate` - для завершения работы в виртуальном окружении
3. Скопировать файл конфигурации `ratelimit/config.example.py` в `ratelimit/config.py`
4. Изменить настройки в файле конфигурации `ratelimit/config.py`, если это необходимо
5. Установить необходимые зависимости `pip install -r requirements.txt`
6. Собрать приложение `python setup.py install`
7. Запустить приложение `sentry-rate-limit`

## Запуск приложения в Docker

1. Собрать образ

```sh
docker build --file ./docker/Dockerfile --tag YOUR_IMAGE_NAME . --no-cache
```

2. Запустить приложение

```sh
docker run --name YOUR_NAME --rm -it YOUR_IMAGE_NAME
```

### Пример запуска с переменными окружения в Docker

```sh
docker run --name YOUR_NAME \
  -e "SENTRY_BEARER_TOKEN=00000000000000000000000000000000" \
  -e "LOGGING_ENABLE=True" \
  -e "LOGGING_LEVEL=info" \
  --rm -it YOUR_IMAGE_NAME
```

## Environment variables

### Sentry

* `SENTRY_URL`: URL адрес для подключения к Sentry (example `https://sentry.io`)
* `SENTRY_BEARER_TOKEN`: Токен авторизации ([подробнее](#минимальные-требования))

### PostgreSQL

* `POSTGRES_DB_NAME`: Название базы данных (default `postgres`)
* `POSTGRES_DB_USER`: Имя пользователя (default `postgres`)
* `POSTGRES_DB_PASSWORD`: Пароль пользователя
* `POSTGRES_HOST`: Имя хоста (default `localhost`)
* `POSTGRES_PORT`: Порт подключения (default `5432`)

### Логирование

* `LOGGING_ENABLE`: Активация логирования (default `False`)
* `LOGGING_LEVEL`: Уровень логирования (default `debug`)
* `LOGGING_FILE_NAME`: Название файла для логов

### Другие

* `DEFAULT_LIMIT_COUNT`: Количество ошибок (default `300`)
* `DEFAULT_LIMIT_WINDOW`: Временной интервал в секундах (default `60`)
* `MIN_LIMIT_COUNT`: Минимальное количество ошибок, допускаемых за 1 минуту (default `60`)

## Список команд

Приложение может работать в нескольких режимов команд:
  * [управления](#команды-управления)
  * [исполнения](#команды-исполнения)

```sh
Usage: sentry-rate-limit [OPTIONS] COMMAND [ARGS]...

  Sentry Rate Limit this is a utility for setting limits in.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  add       Add data to the database.
  cleanup   Delete data without dependencies.
  delete    Delete data from the database.
  describe  DESCRIBE.
  get       GET.
  help      Show this message and exit.
  init      Initialize the tables in the database.
  set       Set the speed limit in sentry.
  sync      Syncs data from Sentry.
  update    Update the data in the database.
```
### Команды управления

#### Команда - init

```sh
Usage: sentry-rate-limit init [OPTIONS]

  Initialize the tables in the database.

Options:
  --help  Show this message and exit.
```

#### Команда - add

Добавляет организацию в базу данных.

> Нельзя добавить организацию, которой нет в Sentry

* `--limit-count` - установить лимит на всю организацию
  > Eсли лимит не указан, будет использоваться дефолтный лимит:
  >
  > `default_limit_count` в файле `ratelimit/config.py`
* `--desc` - добавить описание для лимита

```sh
Usage: sentry-rate-limit add [OPTIONS]

  Add data to the database.

  Examples:

      $ sentry-rate-limit add --organization-name test --limit-count 300 --desc "Testing."
      $ sentry-rate-limit add --organization-name test --limit-count 300
      $ sentry-rate-limit add --organization-name test

Options:
  -o, --organization-name TEXT  Organization name. Not display name.
  -l, --limit-count INTEGER     Limit count.
  -d, --desc TEXT               Description.
  --help                        Show this message and exit.
```

#### Команда - delete

Удаляет организацию из базы данных.

```sh
Usage: sentry-rate-limit delete [OPTIONS]

  Delete data from the database.

  Examples:

      $ sentry-rate-limit delete --organization-name test

Options:
  -o, --organization-name TEXT  Organization name. Not display name.
  --help                        Show this message and exit.
```

#### Команда - describe

- [ ]  в разработке

#### Команда - get

- [ ]  в разработке

#### Команда - update

Обновляет лимиты на организацию/проект/ключ в базе данных.

```sh
Usage: sentry-rate-limit update [OPTIONS] COMMAND [ARGS]...

  Update the data in the database.

Options:
  --help  Show this message and exit.

Commands:
  limit  Update limit.
```

```sh
Usage: sentry-rate-limit update limit [OPTIONS]

  Update limit.      
  
  Examples:

      $ sentry-rate-limit update limit --organization-name test --limit-count 500 --desc "Testing."
      $ sentry-rate-limit update limit --organization-name test --project-name LoadTest --limit-count 100
      $ sentry-rate-limit update limit --organization-name test --project-name LoadTest --public-key cec9dfceb0b74c1c9a5e3c135585f364 --limit-count 50

Options:
  -o, --organization-name TEXT  Organization name. Not display name.
  -p, --project-name TEXT       Project name.
  -k, --public-key TEXT         Public key.
  -l, --limit-count INTEGER     Limit count.  [required]
  -d, --desc TEXT               Description.
  --help                        Show this message and exit.
```

### Команды исполнения

#### Команда cleanup

Запускает удаление данных без зависимостей из базы данных.

```sh
Usage: sentry-rate-limit cleanup [OPTIONS]

  Delete data without dependencies.

Options:
  --help  Show this message and exit.
```

#### Команда set

Устанавливает лимиты в sentry.

```sh
Usage: sentry-rate-limit set [OPTIONS]

  Set the speed limit in sentry.

Options:
  --help  Show this message and exit.
```

#### Команда sync

Синхронизирует данные между sentry и базы данных.

```sh
Usage: sentry-rate-limit sync [OPTIONS]

  Syncs data from Sentry.

Options:
  -L, --limit-only  Sync only limits.
  -N, --no-limit    Sync all except limits.
  --help            Show this message and exit.
```