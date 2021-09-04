import hashlib

# AGiraldo 27-06/2020
# Este método genera un HASH sobre una frase, utilizando SHA512 con un salted value
def hash(phrase):
    if not phrase or phrase == "":
        return ""

    # DiBanka1.0 was made for CASUR, and written by Migue and Daniel. At the end of the project, Juan, Edwin, Hugo and Andrés joined the team. Now we are a firefighters team.
    salt = "RGlCYW5rYTEuMCB3YXMgbWFkZSBmb3IgQ0FTVVIsIGFuZCB3cml0dGVuIGJ5IE1pZ3VlIGFuZCBEYW5pZWwuIEF0IHRoZSBlbmQgb2YgdGhlIHByb2plY3QsIEp1YW4sIEVkd2luLCBIdWdvIGFuZCBBbmRyw6lzIGpvaW5lZCB0aGUgdGVhbS4gTm93IHdlIGFyZSBhIGZpcmVmaWdodGVycyB0ZWFtLg=="

    encodedPhrase = str(phrase + salt).encode('utf-8')

    hashedPhrase = hashlib.sha512(encodedPhrase).hexdigest()

    return hashedPhrase
