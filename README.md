# Домашнее задание 22 - Аутентификация по JWT токену

## Запуск:
Приложение FastAPI разворачивается в Docker  
Сборка образа выпоняется по команде: 
```bash
docker build . -t hw22:1
```
Запуск контейнера из созданного образа:
```bash
docker run --name 'hw22' -p 8100:8100 --rm hw22:1
```

## Проверка работоспособности по ключевым условиям задачи:
#### 1. Проверка того, что приложение в контейнере запущено:
```bash
curl -X GET 'http://127.0.0.1:8100/'
```
ответ на запрос:
```bash
{"message":"Добро пожаловать, Пользователь"}
```
#### 2. Проверка функционала регистрации пользователя:
Регистрируем пользователя user1
```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/auth/register' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "user1",
  "pwd": "123456"
}'
```
результат регистрации:
```
Code: 200, Response body: true
```

#### 3. Проверка аутентификации пользователя:
Пытаемся залогиниться под только что созданным пользователем, но с неверным паролем:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "user1",
  "pwd": "654321"
}'
```
Ответ приложения:
```http
Code: 401 Undocumented
Response body:
    {
    "detail": "Incorrect auth data"
    }
```
Формируем запрос с верными данными пользователя:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "user1",
  "pwd": "123456"
}'
```
Полученный ответ c токеном для дальнейшей работы:
```http
Code: 200
Response body:
    {
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJ1c2VyMSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzk0MTY0Nzg2fQ.lWoDtOdW4pFmTXiRLYksgm2mJVePOARTchjQxV0U_kQ",
    "jwt_eat": "2026-11-08T19:06:26.882794"
    }
```

#### 4. Проверка доступа к защищенным эндпоинтам:
4.1 Доступ к "/me" без данных для авторизации:
```bash
curl -X 'GET' 'http://127.0.0.1:8100/me/' -H 'accept: */*'
```
Ответ сервера:
```http
Code: 401 Undocumented
Response body:
    {
    "detail": "Not authenticated"
    }
```

Теперь запрос со значением Bearer в заголовке:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8100/me/' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJ1c2VyMSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzk0MTY0Nzg2fQ.lWoDtOdW4pFmTXiRLYksgm2mJVePOARTchjQxV0U_kQ'
```
Успешно получаем данные о пользователе с ролью user:
```http
Code: 200
Response body: 
    {
    "id": 3,
    "name": "user1",
    "pwd": "$2b$12$Ukma9Q0kJMXahPsolRqhRuxyHQFLfvJ3jz1FbLUVfWRz9WOaoWfc6",
    "role": "user"
    }
```

4.1 Доступ к "/predict":   
Без данных для авторизации:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/predict' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "Pregnancies": 2,
  "Glucose": 140,
  "BMI": 35.5,
  "Age": 32
}'
```
Ответ:
```http
Code: 401 Unauthorized
    {
    "detail": "Not authenticated"
    }
```
Тот же запрос, но с включением токена в заголовок:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/predict' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJ1c2VyMSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzk0MTY0Nzg2fQ.lWoDtOdW4pFmTXiRLYksgm2mJVePOARTchjQxV0U_kQ' \
  -H 'Content-Type: application/json' \
  -d '{
  "Pregnancies": 2,
  "Glucose": 140,
  "BMI": 35.5,
  "Age": 32
}'
```
Ответ модели ONNX:
```http
Code: 200 
Response body: 1
```
4.1 Доступ к админской части проекта "/admin/health":   
4.1.1 Из под пользователя "user1":
```bash
curl -X 'GET' \
  'http://127.0.0.1:8100/admin/health' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsIm5hbWUiOiJ1c2VyMSIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNzk0MTY0Nzg2fQ.lWoDtOdW4pFmTXiRLYksgm2mJVePOARTchjQxV0U_kQ'
```
Ответ:
```http
Code: 403 Forbidden
Response body:
    {
    "detail": "FORBIDDEN"
    }
```
Авторизуемся под пользоватем "admin" и получаем токен:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8100/auth/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "admin",
  "pwd": "qwerty"
}'
```
```http
Code: 200
Response body:
    {
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsIm5hbWUiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc5NDE2NTg5Nn0.KMtgx_ibesBCsPXHyO1IYLkixqkAno1WXZeJ7Ppn4Vo",
    "jwt_eat": "2026-11-08T19:24:56.220905"
    }
```
Подставляем полученый токен в запрос к эндпоинту:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8100/admin/health' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsIm5hbWUiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc5NDE2NTg5Nn0.KMtgx_ibesBCsPXHyO1IYLkixqkAno1WXZeJ7Ppn4Vo'
```

```http
Code: 200
Response body:
    {
    "value": 17
    }
```