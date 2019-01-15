def debug(func):
    def wrapper():
        print("[DEBUG]:enter {}()".format(func.__name__))
        return func()
    return wrapper
def say_hello():
    print("hello!")

say_hello = debug(say_hello)
say_hello()
