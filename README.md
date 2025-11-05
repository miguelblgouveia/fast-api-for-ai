# Para iniciar o servidor de testes
py -m uvicorn app.main:app --reload

# Exemplo de utilização
curl.exe -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"prompt\": \"Como posso fazer uma pizza?\"}"

# Exermplo de utilização com token de autorização
curl.exe -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsIm5hbWUiOiJNaWd1ZWwgR291dmVpYSIsImlhdCI6MTUxNjIzOTAyMn0.UmcYi6TMBbhkOJhGdqTCm6gScqBZz2Nqb_LZ37e_vqU" -d "{\"prompt\": \"Como posso fazer uma pizza?\"}"

# Para obter jwt tokens
https://www.jwt.io/

header:
{
    "alg": "HS256",
    "typ": "JWT"
}

playload: 
{
    "sub": "testuser"
    "name": "Miguel Gouveia"
    "iat": 1516239022
}

secret:
a-string-secret-at-least-256-bits-long

token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsIm5hbWUiOiJNaWd1ZWwgR291dmVpYSIsImlhdCI6MTUxNjIzOTAyMn0.UmcYi6TMBbhkOJhGdqTCm6gScqBZz2Nqb_LZ37e_vqU