

def make_callback(func):
    print(func)
    def modified_hello(*args, **kwargs):
        print('Saying Hello to: ', end='')
        func(*args, **kwargs)
    return modified_hello

@make_callback
def hello(a, b, c, d, cls=None):
    print(a, b, c, d)


hello(1,2,3,4)

class Printer:
    def p(self, k):
        print(k)

