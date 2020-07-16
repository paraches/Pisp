class Cell:
    @staticmethod
    def append_cell_at_last(s_list, cell):
        if s_list is None:
            return cell
        p = s_list
        while True:
            if not isinstance(p, Cell):
                return None
            if p.cdr is None:
                p.cdr = cell
                return s_list
            else:
                p = p.cdr

    def __init__(self, car_value=None, cdr_value=None):
        self.car = car_value
        self.cdr = cdr_value

    def __str__(self):
        if isinstance(self.car, self.__class__):
            if self.cdr is None:
                return '(%s)' % self.car
            elif not isinstance(self.cdr, self.__class__):
                return '(%s).%s' % (self.car, self.cdr)
            else:
                return '(%s) %s' % (self.car, self.cdr)
        elif self.cdr is None:
            return '%s' % self.car
        elif not isinstance(self.cdr, self.__class__):
            return '%s.%s' % (self.car, self.cdr)
        else:
            return '%s %s' % (self.car, self.cdr)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.car == other.car and self.cdr == other.cdr

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        if self.car is None and self.cdr is None:
            return 0
        length = 1
        next_cell = self.cdr
        while next_cell is not None:
            length = length + 1
            next_cell = next_cell.cdr
        return length

    def cell_string(self):
        return '(%s)' % self
