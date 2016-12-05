======================
zv test
======================

Тестовое задание

Окружение для разработки
=================================

Требования
----------

- [Docker](https://www.docker.io)
- [Python 2.7](https://www.python.org/)

Установка и запуск инфраструктуру
------------
Установка [Redis](https://www.redis.io/)
```bash 
  docker pull redis
```
Запуск [Redis](https://www.redis.org/)
```bash 
  docker run -p 6379:6379 --name redis -d redis
```

Сборка Docker образа приложения:
```bash
  docker build -t zvooq .
```

Запуск приложения:
```bash
  docker run -d -p 8000:8000 --link redis:redis --name zvooq zvooq
```

Запуск процессов для фоновой обработки запросов:
```bash
  docker exec -d zvooq /opt/zvooq/manage.py run_tasks_worker
```

