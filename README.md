# Colpali Search Engine
 
![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat&logo=nginx&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-black?style=flat&logo=llama&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)

## 🌐 Демо

Приложение развёрнуто и доступно по адресу: [https://mvp.agicraft.ru/](https://mvp.agicraft.ru/)

## 🔧 Установка и запуск

1. Установите и запустите Colpali сервер:
```bash
git clone https://github.com/idashevskii/colpali-server.git
cd colpali-server
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.prod.yml
```

2. Клонируйте данный репозиторий:
```bash
git clone https://github.com/agicraft/colpali-search-engine.git
cd colpali-search-engine
```

3. Создайте файл с переменными окружения:
```bash
cp .env.example .env
```

Откройте файл `.env` и отредактируйте следующие параметры

```bash
# Адрес Colpali, доступные внутри докера
COLPALI_BASE_URL=https://192.168.0.100:9001/ 

# Мультимодальная модель LLM
LLM_MODEL=qwen-2-vl-7b-instruct

# Адрес Ollama или другого провайдера с интерфейсом OpenAI
LLM_API_BASE_URL=https://192.168.0.100:11434/api/v1

# API ключ, при необходимости
LLM_API_KEY=sk-oc-v1-my-ollama-key
```

4. Запустите проект с Помощью Docker Compose:
```bash
docker compose -f docker-compose.yml --build
```

5. Откройте браузер и перейдите по адресу:
```
http://localhost:8080
```

## 📦 Структура проекта

- `backend/` - бэкенд приложения
- `ui/` - фронтенд приложения
- `reverse-proxy/` - конфигурация обратного прокси
- `migrations/` - миграции для базы данных
- `db/` - конфигурация базы данных
- `vector-db/` - конфигурация векторной базы данных
- `scripts/` - вспомогательные скрипты

## 🛠 Архитектура и технологии

- **Nginx** - обратный прокси
- **VueJS (TypeScript)** - фронтенд
- **FastAPI (Python)** - бэкенд
- **Colpali Server** - сервис для инференса моделей ColPali
- **Ollama Server** - сервис для инференса моделей LLM
- **QDrant** - векторная база данных
- **PostgresSQL** - реляционная база данных
- **DBMate** - миграции базы данных
- **LibreOffice** - конвертирование документов
- **Docker** - контейнеры для всех компонентов

## 👏 Благодарности

* [@dafcoe/vue-file-uploader](https://github.com/dafcoe/vue-file-uploader): Multiple file uploader (License MIT)
* [FastAPI](https://github.com/fastapi/fastapi): Web framework for building APIs with Python (License MIT)

## 📝 Лицензия

Проект распространяется под лицензией GNU General Public License v3.0.
