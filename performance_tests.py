import requests
import time
import string
import random
import hashlib
import psutil

cpu = []
ram = []

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_time(f, *args, **xargs):
    start = time.time()
    r = f(*args, **xargs)
    end = time.time()
    return end - start, r


def create_user():
    user_data = {
        "email": f'{id_generator()}@test.com',
        "password": id_generator(),
        "user_type": 1,
        "phone": "99999999",
        "address": "Anything",
        "professional_email": f'{id_generator()}@test.com',
        "professional_title": "Test"
    }
    r = requests.post('http://localhost/api/users', json=user_data)
    return r.json()

def accept_user(request_id):
    login_data = {
        "email": "admin@amts.com",
        "password": encrypt_string("admin@amts.com12345")
    }
    r = requests.post("http://localhost/api/login", json=login_data).json()
    token = r.get('access_token')
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.put(f"http://localhost/api/requests/{request_id}", headers=headers, json={ "action": "approve" }).json()

def get_users():
    return requests.get('http://localhost/api/users').json()

def test_create_and_accept_users(n):
    total_create = 0
    total_accept = 0
    for _ in range(n):
        cpu.append(psutil.cpu_percent())
        ram.append(psutil.virtual_memory().percent)
        t_create, r = get_time(create_user)
        request_id = r.get('id')
        t_accept, r = get_time(accept_user, request_id)
        total_create += t_create
        total_accept += t_accept
    print("total_create", total_create)
    print("total_accept", total_accept)

def test_get_users():
    t, r = get_time(get_users)
    print("total get time", t)

c = 50
cc = 0
for _ in range(20):
    cc += c
    print(cc)
    test_create_and_accept_users(c)
    test_get_users()
print(cpu)
print(ram)