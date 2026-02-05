import random

def generate_token(lenght=16):
    x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    token=''
    for i in range(lenght):
        token+= x[random.randint(0,61)]
    return token