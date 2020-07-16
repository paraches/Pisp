from Cell import Cell
from functools import reduce


def pl_cons(car, cdr):
    return Cell(car, cdr)


def pl_car(s):
    return s.car


def pl_cdr(s):
    return s.cdr


def pl_length(s):
    #   args "()" is [None]
    return len(s) if s is not None else 0


def pl_plus(*args):
    return reduce((lambda x, y: x + y), args)


def pl_difference(*args):
    return reduce((lambda x, y: x - y), args)


def pl_numberp(arg):
    return type(arg) is int or type(arg) is float


def pl_atom(arg):
    return not pl_listp(arg)


def pl_null(arg):
    return arg == Cell(None, None) or arg is None


def pl_stringp(arg):
    return type(arg) is str


def pl_listp(arg):
    return isinstance(arg, Cell)


def pl_fixp(arg):
    return type(arg) is int


def pl_floatp(arg):
    return type(arg) is float


def pl_append(x, y):
    if pl_atom(x):
        return y
    else:
        return pl_cons(x.car, pl_append(x.cdr, y))


def pl_reverse(x):
    if pl_atom(x):
        return x
    else:
        return pl_append(pl_reverse(x.cdr), pl_cons(x.car, None))


def pl_last(x):
    if pl_atom(x.cdr):
        return x.car
    else:
        return pl_last(x.cdr)


def pl_member(x, y):
    if x is None:
        return None
    if x.car == y:
        return x
    else:
        return pl_member(x.cdr, y)


def pl_list(*args):
    index = len(args) - 1
    s_list = None
    while index >= 0:
        item = args[index]
        s_list = Cell(item, s_list)
        index = index - 1
    return s_list


def pl_fprint(format_string, *args):
    print(format_string % tuple(args))


def pl_print(arg):
    print(arg)


def pl_or(*args):
    for arg in args:
        if arg is not None and arg is not False:
            return True
    return None


def pl_and(*args):
    for arg in args:
        if arg is None or arg is False:
            return None
    return True
