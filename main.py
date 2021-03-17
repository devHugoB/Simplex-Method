# utf-8

###################
# SIMPLEX
###################

class Simplex:
    def __init__(self, func, constraints, values, e_top, e_inside, above, inside, lines):
        self.func = func
        self.constraints = constraints
        self.values = values
        self.e_top = e_top
        self.e_inside = e_inside
        self.above = above
        self.inside = inside
        self.lines = lines

    def gen_ln(self):
        self.first_ln = self.func + self.e_top
        self.second_ln = self.constraints[0] + self.e_inside[0]
        self.third_ln = self.constraints[1] + self.e_inside[1]
        self.fourth_ln = self.constraints[2] + self.e_inside[2]

    def gen_tab(self):

        tab = [
            ['  ', self.above[0], self.above[1], self.above[2], self.above[3], self.above[4]],
            ['  ', self.first_ln, f'Z-{self.values[0]}', self.lines[0]],
            [self.inside[0], self.second_ln, self.values[1], self.lines[1]],
            [self.inside[1], self.third_ln, self.values[2], self.lines[2]],
            [self.inside[2], self.fourth_ln, self.values[3], self.lines[3]]
        ]

        for i in range(len(tab)):
            for j in range(len(tab[i])):
                print(tab[i][j], end=' ')
            print()

    def test_next_tab(self):
        self.gen_tab()

        max_value = max(self.first_ln)
        idx = self.first_ln.index(max_value)

        if max_value > 0:
            self.calc_next_tab(max_value, idx)
        else:
            print('\nFin de la simulation')
            tab_final = [['z0', self.values[0]]]

            for i in range(len(self.above)):
                if i > 2:
                    value_final = 0
                else:
                    value_final = self.values[i + 1]

                tab_final.append([self.above[i], value_final])

            for i in range(len(tab_final)):
                print(tab_final[i][0], end=' |')
            print()
            for j in range(len(tab_final)):
                print(tab_final[j][1], end='  |')

    def calc_next_tab(self, val_top, idx):
        cl = [val_top, self.second_ln[idx], self.third_ln[idx], self.fourth_ln[idx]]
        tab_value = []
        for i in range(1, len(cl)):
            tab_value.append(cl[i] / self.values[i])

        min_value = min(tab_value)
        idx_min = tab_value.index(min_value)

        if idx_min == 0:
            current_ln = self.second_ln
        elif idx_min == 1:
            current_ln = self.third_ln
        elif idx_min == 2:
            current_ln = self.fourth_ln



###################
# RUN
###################

if __name__ == "__main__":
    function = [-1, 0]
    contraintes = [[1, -1], [1, 0], [0, 1]]
    value = [0, 1, 2, 2]
    e_top = [0, 0, 0]
    e_inside = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    first_line = function + e_top
    above = ['x1', 'x2', 'e1', 'e2', 'e3']
    inside = ['e1', 'e2', 'e3']
    line = ['l0', 'l1', 'l2', 'l3']

    simplex = Simplex(function, contraintes, value, e_top, e_inside, above, inside, line)
    simplex.gen_ln()
    simplex.test_next_tab()
