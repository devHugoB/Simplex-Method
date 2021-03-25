# utf-8

###################
# IMPORTS
###################

from fractions import Fraction
from sys import exit


###################
# GLOBAL FUNCTION
###################

def which_number_types(result, number1, number2):
    reformat_result = str(round(float(result), 3)).split('.')[1]

    if str(float(result)).endswith('.0'):
        return int(result)
    elif any(reformat_result.count(x) > 1 for x in reformat_result):
        if type(number1) != Fraction and type(number2) != Fraction:
            if type(number1) == float:
                number1 = Fraction(number1)
            if type(number2) == float:
                number2 = Fraction(number2)

            return Fraction(number1, number2)

        return result
    else:
        return round(float(result), 2)


###################
# SIMPLEX DEUXIEME ESPECE
###################

class DoubleSimplex:
    def __init__(self, func, func_top, constraints, values, e_top, e_top2, e_in, f_top, f_top2, f_in, a_top, a_top2,
                 a_in, above, inside, lines):

        self.func = func
        self.func_top = func_top
        self.constraints = constraints
        self.values = values
        self.e_top = e_top
        self.e_top2 = e_top2
        self.e_inside = e_in
        self.f_top = f_top
        self.f_top2 = f_top2
        self.f_inside = f_in
        self.a_top = a_top
        self.a_top2 = a_top2
        self.a_inside = a_in
        self.above = above
        self.inside = inside
        self.lines = lines
        self.tab_ln = []
        self.phase = 1
        self.iterations = 0

    def gen_ln(self):
        self.tab_ln.append(self.func_top + self.e_top2 + self.f_top2 + self.a_top2)
        self.tab_ln.append(self.func + self.e_top + self.f_top + self.a_top)
        for i in range(len(self.constraints)):
            self.tab_ln.append(self.constraints[i] + self.e_inside[i] + self.f_inside[i] + self.a_inside[i])

    def gen_tab(self):
        if str(self.values[0]).startswith('-') or self.values[0] == 0:
            value_z_prime = self.values[0] * -1
            sign_prime = '+'
        else:
            value_z_prime = self.values[0]
            sign_prime = '-'

        if str(self.values[1]).startswith('-') or self.values[1] == 0:
            value_z = self.values[1] * -1
            sign = '-'
        else:
            value_z = self.values[1]
            sign = '+'

        for ln in range(len(self.tab_ln)):
            for cl in range(len(self.tab_ln[ln])):
                float_current_number = float(self.tab_ln[ln][cl])
                if str(float_current_number).endswith('.0'):
                    self.tab_ln[ln][cl] = int(self.tab_ln[ln][cl])

        space = f'%-10s'
        line_tab = '────────────' * (len(self.above) + 2)
        tab = [
            [space % ''],
            [space % '', '', f'-Z\'{sign_prime}{value_z_prime}', self.lines[0]],
            [space % '', '', f'Z{sign}{value_z}', self.lines[1]],
            [line_tab]
        ]

        for i in range(len(self.tab_ln[0])):
            tab[1][1] += space % str(self.tab_ln[0][i]) + '│'
        for i in range(len(self.tab_ln[0])):
            tab[2][1] += space % str(self.tab_ln[1][i]) + '│'

        tab[0] += [space % self.above[i] for i in range(len(self.above))]

        for i in range(len(self.inside)):
            tab.append([self.inside[i], '', self.values[i + 2], self.lines[i + 2]])
            for val in range(len(self.tab_ln[i + 1])):
                tab[i + 4][1] += space % str(self.tab_ln[i + 2][val]) + '│'

        for ln in range(len(tab)):
            for cl in range(len(tab[ln])):
                print(space % tab[ln][cl], end='│')
            print()

        input('\n\nAppuyer sur une touche pour quitter...')
        exit(0)


###################
# SIMPLEX PREMIERE ESPECE
###################

class SimpleSimplex:
    def __init__(self, func, constraints, values, e_top, e_in, above, inside, lines):
        self.func = func
        self.constraints = constraints
        self.values = values
        self.e_top = e_top
        self.e_inside = e_in
        self.above = above
        self.inside = inside
        self.lines = lines
        self.tab_ln = []
        self.iterations = 0

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

            print()

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
            for val in range(len(self.tab_ln[i + 1])):
                tab[i + 3][1] += space % str(self.tab_ln[i + 1][val]) + '│'

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
            exit(0)

    def calc_next_tab(self, val_top, idx):
        cl = [val_top]
        for i in range(1, len(self.tab_ln)):
            cl.append(self.tab_ln[i][idx])

        tab_value = []
        for i in range(1, len(cl)):
            if cl[i] > 0:
                tab_value.append(self.values[i] / cl[i])
                tab_value[i - 1] = which_number_types(tab_value[i - 1], self.values[i], cl[i])
            else:
                tab_value.append(100000000)

        min_value = min(tab_value)
        idx_min = tab_value.index(min_value)
        current_ln = self.tab_ln[idx_min + 1]
        current_number = cl[idx_min + 1]
        current_number_idx = current_ln.index(current_number)

        self.iterations += 1

        print('\n~~~~~~~~~~~~~~~ TABLEAU SUIVANT ~~~~~~~~~~~~~~~\n')
        print(f"Itérations n°{self.iterations}")
        print("────────────────────")
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
                    factor = self.tab_ln[i][idx] / current_val_ln[idx]

                    factor = which_number_types(factor, self.tab_ln[i][idx], current_val_ln[idx])

                else:
                    factor = 1 / current_val_ln[idx]

                    factor = which_number_types(factor, 1, current_val_ln[idx])

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
                    self.tab_ln[i][val] = which_number_types(self.tab_ln[i][val], self.tab_ln[i][val], 1)

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

                self.values[i] = which_number_types(self.values[i], self.values[i], 1)

            else:
                continue

        if new_value != -1:
            new_value = which_number_types(new_value, new_value, 1)

            self.values[self.tab_ln.index(current_ln)] = new_value

        if len(new_current_ln) > 0:
            for i in range(len(new_current_ln)):
                new_current_ln[i] = which_number_types(new_current_ln[i], new_current_ln[i], 1)

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

    witch_simplex = str(input('Simplex de première ou seconde espèce ? (1/2) '))

    nb_function = int(input('\nCombien il y a-t-il de x dans la fonction ? '))
    above = [f'x{i + 1}' for i in range(nb_function)]

    print()
    for i in range(nb_function):
        function.append(float(input(f'Combien vaut x{i + 1} ? ')))
        if str(function[i]).endswith('.0'):
            function[i] = int(function[i])

    nb_contraintes = int(input('\nCombien il y a-t-il de contraintes (hors x1, x2, ..., xn >= 0) ? '))

    if witch_simplex == '1':
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

        simplex = SimpleSimplex(function, contraintes, value, e_top, e_inside, above, inside, line)
        simplex.gen_ln()
        simplex.test_next_tab()

    elif witch_simplex == '2':
        value.append(0)
        function_top = []
        e_top2 = []
        f_top = []
        f_top2 = []
        f_inside = []
        a_top = []
        a_top2 = []
        a_inside = []

        contraintes_inf = 0
        contraintes_supp = 0

        line = [f'l{i}' for i in range(-1, nb_contraintes + 1)]

        for i in range(nb_function):
            function_top.append(0)

        for i in range(nb_contraintes):
            print()
            new_contraintes = []
            for j in range(nb_function):
                new_contraintes.append(float(input(f'Combien vaut x{j + 1} dans la contrainte {i + 1} ? ')))
                if str(new_contraintes[j]).endswith('.0'):
                    new_contraintes[j] = int(new_contraintes[j])

            contraintes.append(new_contraintes)
            contraintes_sign = str(input(f'La contrainte {i + 1} est composée du signe > ou < ? '))

            if contraintes_sign == '<':
                contraintes_inf += 1
            elif contraintes_sign == '>':
                contraintes_supp += 1
            else:
                print('ERREUR ! > ou < attendu')
                input()
                exit(-1)

            value.append(float(input(f'Combien vaut la contrainte {i + 1} ? ')))
            if str(value[i + 2]).endswith('.0'):
                value[i + 2] = int(value[i + 2])

        for i in range(contraintes_inf):
            new_a_inside = []
            new_f_inside = []
            for j in range(contraintes_supp):
                new_a_inside.append(0)
                new_f_inside.append(0)
            a_inside.append(new_a_inside)
            f_inside.append(new_f_inside)

            above.append(f'e{i + 1}')
            inside.append(f'e{i + 1}')
            e_top.append(0)
            e_top2.append(0)

            new_e_inside = []
            for j in range(contraintes_inf):
                if j != i:
                    new_e_inside.append(0)
                else:
                    new_e_inside.append(1)
            e_inside.append(new_e_inside)

        for i in range(contraintes_supp):
            new_e_inside = []
            for j in range(contraintes_inf):
                new_e_inside.append(0)
            e_inside.append(new_e_inside)

            above.append(f'f{i + 1}')
            inside.append(f'a{i + 1}')
            f_top.append(0)
            f_top2.append(0)
            a_top.append(0)
            a_top2.append(-1)

            new_f_inside = []
            new_a_inside = []
            for j in range(contraintes_supp):
                if j != i:
                    new_f_inside.append(0)
                    new_a_inside.append(0)
                else:
                    new_f_inside.append(-1)
                    new_a_inside.append(1)
            f_inside.append(new_f_inside)
            a_inside.append(new_a_inside)

        for i in range(contraintes_supp):
            above.append(f'a{i + 1}')

        print('\n----- DEBUT DES CALCULS -----\n')

        simplex = DoubleSimplex(function, function_top, contraintes, value, e_top, e_top2, e_inside, f_top, f_top2,
                                f_inside, a_top, a_top2, a_inside, above, inside, line)
        simplex.gen_ln()
        simplex.gen_tab()

    else:
        '\n\nERREUR ! 1 ou 2 attendu...'
        input()
        exit(-1)
