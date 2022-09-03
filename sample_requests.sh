# запрос на регистрацию
curl --location --request POST 'http://localhost:80/register' --header 'Content-Type: application/json' --data-raw '{
    "name": "Johnny",
    "password": "Pass_pass12"
}'

# запрос на получение токена
curl --location --request POST 'http://localhost:80/auth' --header 'Content-Type: application/json' --data-raw '{
    "name": "Johnny",
    "password": "Pass_pass12"
}'


# запрос на отправку сообщения (токен поменять на свой)
curl --location --request POST 'http://localhost:80/send_message' --header 'auth: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiSm9obm55In0.dCaUdWeNDZfeICKEmmtUTf7CruhHYndrZYIfz9MYykI' --header 'Content-Type: application/json' --data-raw '{
    "name": "Johnny",
    "message": "some message"
}'


# запрос на получение последних 10 сообщений (токен поменять на свой)
curl --location --request POST 'http://localhost:80/send_message' --header 'auth: Bearer_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiSm9obm55In0.dCaUdWeNDZfeICKEmmtUTf7CruhHYndrZYIfz9MYykI' --header 'Content-Type: application/json' --data-raw '{
    "name": "Johnny",
    "message": "history 10"
}'