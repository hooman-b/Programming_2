from Atom import Atom
from exceptions import NotAtomObject

class Molecule(list):

    def __init__(self, atom_list):
        super().__init__(atom_list)
        self.object_validation_checker()
        self.chemical_formula = self.chemical_formula_maker()
    
    def __str__(self):
        return self.chemical_formula
    
    def __add__(self, other):
        formula = self.chemical_formula + other.chemical_formula
        return formula

    def object_validation_checker(self):
        for tuple_pair in self:
            assert isinstance(tuple_pair, tuple), ValueError('the input value is not a tuple')
            assert len(tuple_pair) == 2, ValueError('the atom tuple contains more than two values')
            assert isinstance(tuple_pair[1], int), ValueError('the number of atoms is not inserted correctly')
            assert isinstance(tuple_pair[0], Atom), NotAtomObject(tuple_pair[0])

    def chemical_formula_maker(self):
        chemical_formula = ''

        for tuple_pair in self:

            if tuple_pair[1] != 1:
                chemical_formula += tuple_pair[0].atomic_symbol + str(tuple_pair[1])

            else:
                chemical_formula += tuple_pair[0].atomic_symbol

        return chemical_formula

if __name__ == "__main__":
    hydrogen = Atom('H', 1, 1)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)

    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    print (water) # H2O
    print (co2) # CO2
    print (water + co2) # H2OCO2

    