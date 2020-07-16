from Interpreter import Interpreter
from Cell import Cell


class Reader:
    def read_next_cell(self, token, tokens):
        s_list = None
        if token != '(':
            return Interpreter.atom(token)
        while True:
            try:
                token = tokens.pop(0)
            except IndexError:
                print('Error ) is missing.')
                return None
            if token == ')':
                return s_list
            cell_car = self.read_next_cell(token, tokens)
            s_list = Cell.append_cell_at_last(s_list, Cell(cell_car, None))

    def read_cells(self, tokens):
        token = tokens.pop(0)
        return self.read_next_cell(token, tokens)
