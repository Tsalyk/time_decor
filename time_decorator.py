from time import time, sleep

class DecorTimeCrit:
    def __init__(self, critical_time):
        self.critical_time = critical_time

    @staticmethod
    def check_time(func, critical_time):
        def helper(*args, **kwargs):
            start = time()
            func(*args, **kwargs)
            end = time() - start

            if end > critical_time:
                print(f"WARNING! {func.__name__} slow. Time = "
                      f"{round(end, 3)} sec.")
            return end
        return helper

    def __call__(self, cls):
        return self.wrap_all_methods(cls, self.critical_time)

    @staticmethod
    def wrap_all_methods(obj, critical_time):
        class NewClass:
            def __init__(cls, *args, **kwargs):
                cls.__obj = obj(*args, **kwargs)

            def __getattribute__(cls, item):
                try:
                    attr = super().__getattribute__(item)
                except AttributeError:
                    pass
                else:
                    return attr

                attr = cls.__obj.__getattribute__(item)

                if callable(attr):
                    return DecorTimeCrit.check_time(attr, critical_time)
                else:
                    return attr

        return NewClass



@DecorTimeCrit(critical_time=0.45)
class Test:
    def method_1(self):
        print('slow method start')
        sleep(1)
        print('slow method finish')

    def method_2(self):
        print('fast method start')
        sleep(0.1)
        print('fast method finish')


t = Test()

t.method_1()
t.method_2()


# slow method start
# slow method finish
# WARNING! method_1 slow. Time = ??? sec.
# fast method start
# fast method finish