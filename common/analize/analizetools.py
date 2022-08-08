from pprint import pprint
import inspect
from inspect import (
    isclass,
    isfunction,
    isgenerator,
    ismethod,
    ismodule,
)
import sys
import builtins
from collections.abc import Mapping


# # for import
# from analizetools.analize import (
#     p_dir, p_mro, p_glob, p_loc, p_type,
#     delimiter, p_content, show_builtins,
#     show_doc, console, console_compose,
# )

# p_dir, p_mro, p_glob, p_loc, p_content, show_builtins, show_doc, delimiter

def p_dir(obj):
    return pprint(dir(obj))


# старая версия p_mro
# def p_mro(obj):
#     if isinstance(obj, type):
#         return pprint(obj.mro())
#     return pprint(type(obj).mro())

def p_mro(obj):
    if hasattr(obj, 'mro') or inspect.isclass(obj):
        return pprint(obj.mro())
    return pprint(type(obj).mro())


def p_glob():
    return pprint(globals())


def p_loc():
    return pprint(locals())


def p_content(obj):
    if hasattr(obj, '__iter__'):
        return pprint(obj)
    return pprint("Can't show elements of obj")


def show_builtins():
    # import builtins
    # pp(dir(builtins) == dir(globals()['__builtins__'])) # True
    # pp(builtins == globals()['__builtins__']) # True
    # pp(type(builtins)) # <class 'module'>
    # pp(type(builtins).mro()) # [<class 'module'>, <class 'object'>]
    key_builtins = globals().get('__builtins__')
    if key_builtins:
        if isinstance(key_builtins, dict):
            return pprint(key_builtins)
        return pprint(dir(key_builtins))
    else:
        return pprint("Can't show builtins")


def show_doc(obj):
    return print(obj.__doc__)


def delimiter(sym='-+', quant=50):
    return print('\n', sym * quant, end='\n')


def p_type(obj):
    return print(type(obj))


# потом можно улучшить чтобы передавался также **kwargs, и тогда выводился
# также имя переменной и её значенте
# поможет setattr
def console(*args, delimetr='- ', length=50, sdict=False):
    print('\n', '=' * 100)
    for elem in args:
        if issubclass(type(elem), (Mapping, dict)) or sdict:
            pprint(dict(elem))
        else:
            pprint(elem)
        print(delimetr * length)
    print('=' * 100, '\n')


def console_compose(
        obj,
        stype=False,
        smro=False,
        sdir=False,
        delimiter=delimiter,
        start=delimiter,
        end=delimiter
):
    params = (
        (stype, p_type, 'type:\n'),
        (smro, p_mro, 'mro:\n'),
        (sdir, p_dir, 'dir:\n'),

    )
    for action, func, view in params:
        if action:
            if params.index((action, func, view)) == 0:
                start()
            else:
                delimiter()
            print(view)
            func(obj)
    end()


def console_compose2(
        *args,
        stype=False,
        smro=False,
        sdir=False,
        delimiter=delimiter,
        **kwargs):
    params = (
        (stype, p_type, 'type:\n'),
        (smro, p_mro, 'mro:\n'),
        (sdir, p_dir, 'dir:\n'),

    )
    value_delimiter = '-'
    delimiter(value_delimiter)
    print()
    for obj in args:
        # ------ пытаемся вывести имя переменной, которою нам дали.
        # Если не получается - выводим имя её класса
        if any([
            inspect.isclass(obj),
            inspect.isfunction(obj),
            inspect.isgenerator(obj),
            inspect.ismethod(obj),
            inspect.ismodule(obj),
        ]) and hasattr(obj, '__name__'):
            print(f'{obj.__name__}:')
        else:
            print(f'{obj} - instance of the {type(obj).__name__}:')
        print()
        try:
            pprint(dict(obj))
        except (ValueError, TypeError):
            pprint(obj)
        print()
        for action, func, view in params:
            if action:
                print(f'{view}')
                func(obj)
                print()
        delimiter(value_delimiter)
        print()
    for k, v in kwargs.items():
        print(f'{k}:')
        print()
        try:
            pprint(dict(v))
        except (ValueError, TypeError):
            pprint(v)
        print()
        for action, func, view in params:
            if action:
                print(f'{view}')
                func(v)
                print()

        delimiter(value_delimiter)
        print()


class Console:
    def __init__(self, *args,
                 stype=False,
                 smro=False,
                 sdir=False,
                 sdoc=False,
                 shelp=False,
                 delimiter='- ',
                 **kwargs):
        self.args = args
        self.kwargs = kwargs
        params = (
            (stype, self.p_type, 'type:\n'),
            (smro, self.p_mro, 'mro:\n'),
            (sdir, self.p_dir, 'dir:\n'),
            (sdoc, self.p_doc, 'doc:\n'),
            (shelp, self.p_help, 'help:\n'),
        )
        self.params = {item[1]: item[-1] for item in filter(lambda x: x[0], params)}
        self.sign = delimiter

    def get_action(self, obj):

        for action, func, view in self.params:
            if action:
                print(f'{view}')
                func(obj)
                print()
        delimiter(self.sign)


    def get_value(self):
        pass

    @staticmethod
    def p_type(obj):
        return print(type(obj))

    @staticmethod
    def p_mro(obj):
        if isinstance(obj, type):
            return pprint(obj.mro())
        return pprint(type(obj).mro())

    @staticmethod
    def p_dir(obj):
        return pprint(dir(obj))

    @staticmethod
    def p_doc(obj):
        return print(obj.__doc__)

    @staticmethod
    def p_help(obj):
        pass

    def delimiter(self, sign='-+', quant=50):

        print('\n\n', sign * quant, end='\n\n')


    def output(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass


"""
isclass,
    isfunction,
    isgenerator,
    ismethod,
    ismodule,
    
    def p_dir(obj):
    return pprint(dir(obj))


# старая версия p_mro
# def p_mro(obj):
#     if isinstance(obj, type):
#         return pprint(obj.mro())
#     return pprint(type(obj).mro())

def p_mro(obj):
    if hasattr(obj, 'mro') or inspect.isclass(obj):
        return pprint(obj.mro())
    return pprint(type(obj).mro())
"""
