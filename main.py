# utf-8

###################
# IMPORTS
###################

from fractions import Fraction


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
        self.tab_ln = []

    def gen_ln(self):
        self.tab_ln.append(self.func + self.e_top)
        for i in range(len(self.constraints)):
            self.tab_ln.append(self.constraints[i] + self.e_inside[i])

    def gen_tab(self):
        if str(self.values[0]).startswith('-') or self.values[0] == 0:
            value_z = self.values[0] * -1
            sign = '-'
        else:
            value_z = self.values[0]
            sign = '+'

        for ln in range(len(self.tab_ln)):
            for cl in range(len(self.tab_ln[ln])):
                float_current_number = float(self.tab_ln[ln][cl])
                if str(float_current_number).endswith('.0'):
                    self.tab_ln[ln][cl] = int(self.tab_ln[ln][cl])

        space = f'%-10s'
        line_tab = '────────────' * (len(self.above) + 2) + '────'
        tab = [
            [space % ''],
            [space % '', '', f'Z{sign}{value_z}', self.lines[0]],
            [line_tab]
        ]
        for i in range(len(self.tab_ln[0])):
            tab[1][1] += space % str(self.tab_ln[0][i]) + '│'

        tab[0] += [space % self.above[i] for i in range(len(self.above))]

        for i in range(len(self.inside)):
            tab.append([self.inside[i], '', self.values[i + 1], self.lines[i + 1]])
            for val in range(len(self.tab_ln[i+1])):
                tab[i+3][1] += space % str(self.tab_ln[i+1][val]) + '│'

        for ln in range(len(tab)):
            for cl in range(len(tab[ln])):
                print(space % tab[ln][cl], end='│')
            print()

    def test_next_tab(self):
        self.gen_tab()

        for i in range(len(self.lines)):
            self.lines[i] = f'l{i}'

        max_value = max(self.tab_ln[0])
        idx = self.tab_ln[0].index(max_value)

        if max_value > 0:
            self.calc_next_tab(max_value, idx)
        else:
            print('\n----- FIN DES CALCULS -----\n')
            tab_final = [['z0', self.values[0]]]

            for i in range(len(self.above)):
                if self.above[i] in self.inside:
                    value_final = self.values[self.inside.index(self.above[i]) + 1]
                else:
                    value_final = 0

                tab_final.append([self.above[i], value_final])
            tab_final[0][1] *= -1

            space = '%-8s'
            for i in range(len(tab_final)):
                tab_final[i][1] = str(tab_final[i][1])
                print(space % tab_final[i][0], end='│')
            print()
            for i in range(len(tab_final)):
                tab_final[i][1] = str(tab_final[i][1])
                print(space % tab_final[i][1], end='│')

            input('\n\nAppuyer sur une touche pour quitter...')

    def calc_next_tab(self, val_top, idx):
        cl = [val_top]
        for i in range(1, len(self.tab_ln)):
            cl.append(self.tab_ln[i][idx])

        tab_value = []
        for i in range(1, len(cl)):
            if cl[i] > 0:
                tab_value.append(self.values[i] / cl[i])
                tab_value_after_point = str(float(tab_value[i-1])).split('.')[1]
                if any(tab_value_after_point.count(x) > 1 for x in tab_value_after_point):
                    tab_value[i-1] = Fraction(self.values[i], cl[i])
                else:
                    tab_value[i-1] = round(float(tab_value[i-1]), 2)
            else:
                tab_value.append(100000000)

        min_value = min(tab_value)
        idx_min = tab_value.index(min_value)
        current_ln = self.tab_ln[idx_min + 1]
        current_number = cl[idx_min + 1]
        current_number_idx = current_ln.index(current_number)

        print('\n~~~~~~~~~~~~~~~ TABLEAU SUIVANT ~~~~~~~~~~~~~~~\n')
        print("Element choisi :", current_number)
        print("Ligne entrante :", self.above[current_number_idx])
        print("Ligne sortante :", self.inside[idx_min], '\n')

        self.inside[idx_min] = self.above[current_number_idx]

        self.calc_new_lines(current_ln, current_number_idx)

    def calc_new_lines(self, current_ln, idx):
        new_current_ln = []
        new_value = -1
        current_name_ln = self.lines[self.tab_ln.index(current_ln)]
        current_val_ln = current_ln

        for i in range(len(self.tab_ln)):
            if (self.tab_ln[i][idx] != 0 and current_val_ln != self.tab_ln[i]) or \
                    (current_val_ln == self.tab_ln[i] and current_val_ln[idx] != 1):

                if self.tab_ln[i][idx] != 0 and current_val_ln != self.tab_ln[i]:
                    factor = float(self.tab_ln[i][idx]) / current_val_ln[idx]

                    if any(str(float(factor)).split('.')[1].count(x) > 1 for x in str(float(factor)).split('.')[1]):
                        if type(self.tab_ln[i][idx]) != Fraction and type(current_val_ln[idx]) != Fraction:
                            if type(self.tab_ln[i][idx]) == float:
                                self.tab_ln[i][idx] = Fraction(self.tab_ln[i][idx])
                            if type(current_val_ln[idx]) == float:
                                current_val_ln[idx] = Fraction(current_val_ln[idx])

                            factor = Fraction(self.tab_ln[i][idx], current_val_ln[idx])
                    else:
                        factor = float(factor)

                else:
                    factor = 1 / current_val_ln[idx]

                    if any(str(float(factor)).split('.')[1].count(x) > 1 for x in str(float(factor)).split('.')[1]):
                        if type(current_val_ln[idx]) != Fraction:
                            if type(current_val_ln[idx]) == float:
                                current_val_ln[idx] = Fraction(current_val_ln[idx])

                            factor = Fraction(1, current_val_ln[idx])
                    else:
                        factor = float(factor)

                if str(factor).endswith('.0'):
                    factor = int(factor)

                elif '.' in str(factor) and len(str(factor).split('.')[1]) > 2:
                    factor = round(factor, 2)

                current_ln_with_factor = [i * abs(factor) for i in current_val_ln]

                if self.tab_ln[i][idx] > 0 and current_val_ln != self.tab_ln[i]:
                    for val in range(len(self.tab_ln[i])):
                        self.tab_ln[i][val] -= current_ln_with_factor[val]

                elif self.tab_ln[i][idx] < 0 and current_val_ln != self.tab_ln[i]:
                    for val in range(len(self.tab_ln[i])):
                        self.tab_ln[i][val] += current_ln_with_factor[val]

                else:
                    for val in range(len(self.tab_ln[i])):
                        new_current_ln.append(current_ln_with_factor[val])

                for val in range(len(self.tab_ln[i])):
                    if str(self.tab_ln[i][val]).endswith('.0'):
                        self.tab_ln[i][val] = int(self.tab_ln[i][val])

                    elif '.' in str(self.tab_ln[i][val]) and len(str(self.tab_ln[i][val]).split('.')[1]) > 2:
                        self.tab_ln[i][val] = round(self.tab_ln[i][val], 2)

                if str(factor).startswith('-'):
                    sign = '+'
                else:
                    sign = '-'

                if factor != 1 and factor != -1 and self.tab_ln[i] != current_val_ln:
                    self.lines[i] += f' {sign}{abs(factor)} {current_name_ln}'
                elif self.tab_ln[i] != current_val_ln:
                    self.lines[i] += f' {sign}{current_name_ln}'
                else:
                    self.lines[i] = f'{abs(factor)} {current_name_ln}'

                if self.tab_ln[i] != current_val_ln:
                    self.values[i] -= (factor * self.values[self.tab_ln.index(current_val_ln)])
                else:
                    new_value = factor * self.values[self.tab_ln.index(current_val_ln)]

                if str(self.values[i]).endswith('.0'):
                    self.values[i] = int(self.values[i])

                elif '.' in str(self.values[i]) and len(str(self.values[i]).split('.')[1]) > 2:
                    self.values[i] = round(self.values[i], 2)

            else:
                continue

        if new_value != -1:
            if str(new_value).endswith('.0'):
                new_value = int(new_value)

            elif '.' in str(new_value) and len(str(new_value).split('.')[1]) > 2:
                new_value = round(new_value, 2)

            self.values[self.tab_ln.index(current_ln)] = new_value

        if len(new_current_ln) > 0:
            for i in range(len(new_current_ln)):
                if str(new_current_ln[i]).endswith('.0'):
                    new_current_ln[i] = int(new_current_ln[i])

                elif '.' in str(new_current_ln[i]) and len(str(new_current_ln[i]).split('.')[1]) > 2:
                    new_current_ln[i] = round(new_current_ln[i], 2)

            self.tab_ln[self.tab_ln.index(current_ln)] = new_current_ln

        self.test_next_tab()


###################
# RUN
###################

if __name__ == "__main__":
    function = []
    contraintes = []
    e_top = []
    e_inside = []
    inside = []
    value = [0]

    nb_function = int(input('Combien il y a-t-il de x dans la fonction ? '))
    above = [f'x{i + 1}' for i in range(nb_function)]

    print()
    for i in range(nb_function):
        function.append(float(input(f'Combien vaut x{i + 1} ? ')))
        if str(function[i]).endswith('.0'):
            function[i] = int(function[i])

    nb_contraintes = int(input('\nCombien il y a-t-il de contraintes (hors x1, x2, ..., xn >= 0) ? '))
    line = [f'l{i}' for i in range(nb_contraintes + 1)]

    for i in range(nb_contraintes):
        print()
        new_contraintes = []
        for j in range(nb_function):
            new_contraintes.append(float(input(f'Combien vaut x{j + 1} dans la contrainte {i + 1} ? ')))
            if str(new_contraintes[j]).endswith('.0'):
                new_contraintes[j] = int(new_contraintes[j])

        contraintes.append(new_contraintes)

        value.append(float(input(f'Combien vaut la contrainte {i + 1} ? ')))
        if str(value[i + 1]).endswith('.0'):
            value[i + 1] = int(value[i + 1])

    for i in range(len(contraintes)):
        above.append(f'e{i + 1}')
        inside.append(f'e{i + 1}')
        e_top.append(0)

        new_e_inside = []
        for j in range(len(contraintes)):
            if j != i:
                new_e_inside.append(0)
            else:
                new_e_inside.append(1)
        e_inside.append(new_e_inside)

    print('\n----- DEBUT DES CALCULS -----\n')

    simplex = Simplex(function, contraintes, value, e_top, e_inside, above, inside, line)
    simplex.gen_ln()
    simplex.test_next_tab()
