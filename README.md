# Айки — Django REST API

## Описание

Этот проект — серверная часть на Django для управления пользователями, ролями и заявками на зачисление учеников. Используется Django REST Framework и JWT-аутентификация.

## Основные возможности
- Регистрация и аутентификация пользователей (JWT)
- Роли пользователей: ученик, тренер, руководитель, администратор
- Управление заявками на зачисление учеников
- Разграничение прав доступа по ролям

## Установка

1. **Клонируйте репозиторий:**
   ```sh
   git clone <адрес_репозитория>
   cd <папка_проекта>
   ```

2. **Создайте и активируйте виртуальное окружение:**
   - Windows (cmd):
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```sh
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Примените миграции:**
   ```sh
   cd app
   python manage.py migrate
   ```

5. **Создайте суперпользователя (администратора):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Запустите сервер разработки:**
   ```sh
   python manage.py runserver
   ```

## Использование

- Админ-панель: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/

## Переменные окружения

Создайте файл `.env` в папке `app/app/` и добавьте переменные из `.env.example`:

## Структура проекта

- `app/` — основной Django-проект
  - `registration/` — приложение регистрации и управления пользователями
    - `models/` — модели пользователей, заявок и JWT
    - `views.py` — основные API-вьюхи
    - `permissions.py` — кастомные права доступа
    - `serializers.py` — сериализаторы для моделей

## Роуты API

### Аутентификация и регистрация

- **POST /api/token/** — Получение JWT access/refresh токенов
  - Тело запроса:
    ```json
    {
      "username": "логин",
      "password": "пароль"
    }
    ```
  - Ответ:
    ```json
    {
      "access": "JWT access token"
    }
    ```
  - Refresh-токен возвращается только в httpOnly cookie.

- **POST /api/token/refresh/** — Обновление access-токена по refresh-токену (refresh берётся из cookie)
  - Тело запроса:
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
  - Ответ:
    ```json
    {
      "access": "новый access token"
    }
    ```

- **POST /api/register/** — Регистрация нового пользователя (может только тренер/руководитель/админ)
  - Тело запроса:
    ```json
    {
      "username": "логин",
      "password": "пароль",
      "first_name": "...",
      "last_name": "...",
      "birth_date": "YYYY-MM-DD",
      "phone": "...",
      "email": "...",
      "role": "student",
      "city": "...",
      "parent_name": "...",
      "parent_phone": "...",
      "rank": "...",
      "rank_date": "YYYY-MM-DD"
    }
    ```
  - Ответ: данные созданного пользователя.

- **POST /api/logout/** — Выход из системы, refresh-токен заносится в blacklist и cookie удаляется.

---

### Пользовательский профиль

- **GET /api/profile/** — Получение профиля текущего пользователя (по access-токену)
- **PUT /api/profile/** — Полное обновление профиля текущего пользователя
- **PATCH /api/profile/** — Частичное обновление профиля текущего пользователя

---

### Пользователи (только для тренеров/руководителей)

- **GET /api/users/** — Получить список всех пользователей
- **POST /api/users/** — Создать пользователя (аналогично /register/)
- **GET /api/users/{id}/** — Получить пользователя по id
- **PUT /api/users/{id}/** — Полностью обновить пользователя по id
- **PATCH /api/users/{id}/** — Частично обновить пользователя по id
- **DELETE /api/users/{id}/** — Удалить пользователя по id


#### Примечания
- Для большинства запросов требуется JWT access-токен в заголовке Authorization:
  ```
  Authorization: Bearer <access_token>
  ```
- Refresh-токен хранится только в httpOnly cookie.
- Роуты пользователей и заявок используют стандартные методы Django REST Framework (list, retrieve, create, update, destroy).

## Зависимости
См. `requirements.txt`.
