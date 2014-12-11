__author__ = 'wan'


def log(f):
    def decorator(*args, **kwargs):
        print('debug log')
        return f(*args, **kwargs)

    return decorator


class TestLog():
    @log
    def say_hello(self):
        print('hahhahahah')

    @log
    def haode(self, name, hehe):
        print(name + hehe)


if __name__ == '__main__':
    t = TestLog().say_hello()
    print(None or {})


