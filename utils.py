from datetime import datetime
from collections import deque


class DequeIterator:
    def __init__(self, ringpuffer:deque):
        self.ringpuffer:deque = ringpuffer
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.ringpuffer) == 0:
            raise StopIteration
        element = self.ringpuffer[self.index]
        self.index = (self.index + 1) % len(self.ringpuffer)
        return element

def debug_arguments(attrs:list[str]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f'{func.__name__}')
            print(f'Expected: {','.join(attrs)}')
            print(f'Got {args} and {kwargs}')
            #return func(*args, **kwargs)
        return wrapper
    return decorator




def print_duration(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        endtime = datetime.now()
        hours, remainder = divmod((endtime-start).seconds, 3600)
        minutes, seconds = divmod(remainder, 60)  
        if hours < 24:
            print(f'{hours}:{minutes:02}:{seconds:02}')      
        else:
            days, hours = divmod(hours,24)
            print(f'{days}:{hours:02}:{minutes:02}:{seconds:02}')          
        return result
    return wrapper