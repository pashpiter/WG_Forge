# WG_Forge

##### Стек: Python, aiohttp, Postgresql, asyncpg, Docker, nginx. pytest
***

### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/WG_Forge
```
* Перейти в папку WG_Forge


* Запустить проект используя docker-compose
```
sudo docker-compose up -d
```

### Примеры команд API
* Проверка работы серверв
```
GET http://localhost/ping
```
```
curl -X http://localhost/ping
```
* Получение списка котов
```
GET http://localhost/cats
```
```
curl -X GET http://localhost/cats
```
* Получение списка котов с сортировкой по заданному атрибуту, по возрастанию или убыванию. Также можно добавить параметры offset и limit
```
GET http://localhost/cats?attribute=tail_length&order=desc
```
```
curl -X GET http://localhost/cats?attribute=tail_length&order=desc
```
```
curl -X GET http://localhost/cats?attribute=color&order=asc&offset=5&limit=2
```
* Добавление нового кота
```
POST http://localhost:8080/cat
{
  "name": "str",
  "color": "str",
  "tail_length": int,
  "whiskers_length": int
}
```
```
curl -X POST http://localhost/cat \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
```


#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
