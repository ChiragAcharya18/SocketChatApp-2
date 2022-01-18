import datetime
from aess import encrypt, decrypt
from nthprime import nthprime

def key():
    x = str(datetime.datetime.today()).split("-")
    x = int(x[0]) + int(x[1]) + int(x[2][0:1])
    x = str(nthprime(x))
    x = x + x[::-1]
    return x


if __name__ == "__main__":
    print("This is main!")