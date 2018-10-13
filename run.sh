#!/bin/bash

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 0:9090


# curl -X POST \
#   http://0.0.0.0:9090/screens/ \
#   -H 'Cache-Control: no-cache' \
#   -H 'Postman-Token: 50afb113-0807-4038-a028-da86a9db4a8d' \
#   -d '{"name": "inox","seatInfo": {"A": {"numberOfSeats": 10,"aisleSeats": [0, 5, 6, 9]},"B": {"numberOfSeats": 15,"aisleSeats": [0, 5, 6, 9]},"D": {"numberOfSeats": 20,"aisleSeats": [0, 5, 6, 9]}}
# }'

# curl -X POST \
#   http://0.0.0.0:9090/screens/inox/reserve \
#   -H 'Cache-Control: no-cache' \
#   -H 'Postman-Token: 955494b2-ccd7-412e-85b0-094542a89791' \
#   -d '{ "seats": { "B": [1, 2], "D": [ 6, 7] } }'

# curl -X GET \
#   'http://localhost:9090/screens/inox/seats?status=unreserved' \
#   -H 'Cache-Control: no-cache' \
#   -H 'Postman-Token: 0edf7231-60df-4d6a-bdd5-9b2bb762545b'