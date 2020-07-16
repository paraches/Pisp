#!/usr/bin/env python
import argparse
from Interpreter import Interpreter
from Parser import Parser
from Reader import Reader
from Cell import Cell


class Pisp:
    def __init__(self):
        self.interpreter = Interpreter()
        self.parser = Parser()
        self.reader = Reader()

    def run(self, s_exp_list):
        result = None
        while len(s_exp_list) > 0:
            s = s_exp_list.pop(0)
            cells = self.reader.read_cells(s)
            result = self.interpreter.eval_(cells)
            print('%s' % result.cell_string() if isinstance(result, Cell) else result)
        return result

    def run_s(self, s):
        s_exps = self.parser.parse_text(s)
        return self.run(s_exps)

    def repl(self):
        prompt = 'pisp > '
        result = None
        while result != '__quit':
            t = input(prompt)
            result = self.run_s(t)

    def with_file(self, file_name):
        with open(file_name) as f:
            s = f.read()
        print('read "%s":\n%s' % (file_name, s))
        return self.run_s(s)


def main():
    psr = argparse.ArgumentParser()
    psr.add_argument('-f', '--file_name', type=str, help='File name to read.')
    args = psr.parse_args()

    pisp = Pisp()
    if args.file_name is not None:
        pisp.with_file(args.file_name)
    pisp.repl()


if __name__ == '__main__':
    main()
