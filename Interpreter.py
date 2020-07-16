from Cell import Cell


class Interpreter:
    class Env(dict):
        def __init__(self, params=(), args=(), before=None):
            super(dict, self).__init__()
            self.update(zip(params, args))
            self.before = before

        def find(self, var):
            return self if var in self else self.before.find(var)

    def __init__(self):
        self.env = Interpreter.Env(params=('T', 'nil'), args=(True, None))
        self.env = self.add_globals(self.env)

    def add_globals(self, env):
        import math
        import operator as op
        env.update(vars(math))
        env.update({
            '+': op.add, '-': op.sub, '*': op.mul, '/': op.floordiv, 'not': op.not_,
            '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq, 'equal?': op.eq,
            'eq?': op.is_, 'abs': op.abs, 'quit': lambda: '__quit',
        })

        self.load_functions(env)

        return env

    def load_functions(self, env):
        import Functions as pl_functions
        pl_f_vars = vars(pl_functions)
        pl_f_dict = {key[3:len(key)]: pl_f_vars[key] for key in pl_f_vars if key[:3] == 'pl_'}
        env.update(pl_f_dict)
        print('Read following functions:\n%s\n' % pl_f_dict.keys())

    @staticmethod
    def print_cells(cells):
        if isinstance(cells, Cell):
            print('(%s)' % cells)
        else:
            print('%s' % cells)

    @staticmethod
    def atom(a):
        try:
            return int(a)
        except ValueError:
            try:
                return float(a)
            except ValueError:
                return a

    def args_list(self, s):
        args = []
        if s is None or not isinstance(s, Cell):
            return args
        while s.cdr is not None:
            args.append(s.car)
            s = s.cdr
        args.append(s.car)
        return args

    def evaluated_args_list(self, s, env):
        args = []
        if s is None:
            return args
        while s.cdr is not None:
            v = self.eval_(s.car, env)
            args.append(v)
            s = s.cdr
        v = self.eval_(s.car, env)
        args.append(v)
        return args

    def eval_(self, s, env=None):
        if env is None:
            env = self.env
        if not isinstance(s, Cell):
            if isinstance(s, float) or isinstance(s, int):
                return s
            else:
                return env.find(s)[s]
        else:
            if isinstance(s.car, Cell):
                return self.apply_(Cell(self.eval_(s.car, env), s.cdr), env)
            else:
                return self.apply_(s, env)

    def apply_(self, s, env):
        if s.car == 'quote':
            return s.cdr.car
        elif s.car == 'if':
            test = s.cdr.car
            conseq = s.cdr.cdr.car
            alt = s.cdr.cdr.cdr.car if isinstance(s.cdr.cdr.cdr, Cell) else None
            if alt is None:
                if self.eval_(test, env):
                    return self.eval_(conseq, env)
                else:
                    return None
            else:
                return self.eval_((conseq if self.eval_(test, env) else alt), env)
        elif s.car == 'set!':
            var = s.cdr.car
            if s.cdr.cdr.cdr is None:
                env.find(var)[var] = self.eval_(s.cdr.cdr.car, env)
            else:
                env.find(var)[var] = self.eval_(s.cdr.cdr, env)
            return var
        elif s.car == 'define':
            var = s.cdr.car
            value = s.cdr.cdr
            if isinstance(value, Cell) and value.cdr is None:
                env[var] = self.eval_(value.car, env)
            else:
                env[var] = self.eval_(value, env)
            return var
        elif s.car == 'lambda':
            lambda_vars = self.args_list(s.cdr.car)
            exp = s.cdr.cdr.car
            return lambda *args: self.eval_(exp, Interpreter.Env(lambda_vars, args, env))
        elif s.car == 'begin':
            s = s.cdr
            while s.cdr is not None:
                self.eval_(s.car, env)
                s = s.cdr
            return self.eval_(s.car, env)
        elif s.car == 'cond':
            next_cell = s.cdr
            while next_cell is not None and isinstance(next_cell, Cell):
                exp = next_cell.car.car
                clause = next_cell.car.cdr.car
                if self.eval_(exp, env) is True:
                    return self.eval_(clause, env)
                next_cell = next_cell.cdr
        elif callable(s.car):
            proc = s.car
            exps = self.evaluated_args_list(s.cdr, env)
            return proc(*exps)
        else:
            proc = s.car
            exps = self.evaluated_args_list(s.cdr, env)
            return env.find(proc)[proc](*exps)
