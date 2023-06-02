from Atom import Atom
from exceptions import NotAtomObject

class Molecule(list):

    def __init__(self, atom_list):
        super().__init__(atom_list)
        self.tuple_two_value_checker()
        self.atom_object_checker()
        self.atom_number_checker()

    def tuple_two_value_checker(self):
        # asking teacher which one is better raise or assert 
        for tuple_pair in self:
            if len(tuple_pair) != 2:
                raise ValueError ('the atom tuple contains more than two values')

    def atom_number_checker(self):
        for tuple_pair in self:
            if not isinstance(tuple_pair[1], int):
                raise ValueError ('the number of atoms is not inserted correctly')
    
    def atom_object_checker(self):
        for tuple_pair in self:
            if not isinstance(tuple_pair[0], Atom):
                raise NotAtomObject(tuple_pair[0])

if __name__ == "__main__":
    hydrogen = Atom('H', 1, 1)
    oxygen = Atom('O', 8, 8)
    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    print(water)
    