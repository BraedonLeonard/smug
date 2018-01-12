import re

'''Various helper functions used by the bot'''

def static_vars(**kwargs):
    '''Decorator for assigning static variables to a function'''
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

NdN = re.compile(r'\d+d\d+')
