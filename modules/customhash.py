import hashlib

# AGiraldo 27-06/2020
# Este método genera un HASH sobre una frase, utilizando SHA512 con un salted value
def hash(phrase):
    if not phrase or phrase == "":
        return ""

    # NapTrading es creada por Daniel Hoyos y Daniel Rodriguez. y fue creado para lo inversores y sus administradores. 
    salt = "TmFwVHJhZGluZyBlcyBjcmVhZGEgcG9yIERhbmllbCBIb3lvcyB5IERhbmllbCBSb2RyaWd1ZXouIHkgZnVlIGNyZWFkbyBwYXJhIGxvcyBpbnZlcnNvcmVzIHkgc3VzIGFkbWluaXN0cmFkb3Jlcy4g"

    encodedPhrase = str(phrase + salt).encode('utf-8')

    hashedPhrase = hashlib.sha512(encodedPhrase).hexdigest()

    return hashedPhrase
