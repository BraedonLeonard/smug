import re

''' Various helper functions used by the bot '''

def static_vars(**kwargs):
    ''' Decorator for assigning static variables to a function '''
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def markdownCodeBlock(text: str, language: str=''):
    ''' formats text as a markdown code block '''
    return f'```{language}\n' + text + '```'

NdN = re.compile(r'\d+d\d+')
