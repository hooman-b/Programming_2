"""
problems: 1- 
Explanation: This module contains a class (Molecule) that makes an Molecule object and returns
             its chemical formula and adds two chemical formula to each other.
"""

from Atom import Atom
from exceptions import NotAtomObject

# Nice that you extend from list

class Molecule(list):
    """
    type: list-like class
    explanation: this class contains two attributes, one initializer, two dunder methods,
                 and two instance methods. its instance methods are responsible for validating
                 the input list and making chemical formula.
    """

    def __init__(self, atom_list):
        """
        input: 1- atom_list (list): contains a list of tuples, each tuple consists of an Atom object
                                    and the number of them.
        explanation: this initializer get the above input, check the validity of the it, and make
                     the chemical formula of the object.
        """
        super().__init__(atom_list)
        self.object_validation_checker()
        self.chemical_formula = self.chemical_formula_maker()

    def __str__(self):
        """
        explanation: returns the chemical formula of the molecule.
        """
        return self.chemical_formula

    def __add__(self, other):
        """
        explanation: it adds two chemical formula strings to each other.
        output: 1- formula: this is a chemical formula of a compound.
        """
        # This is incorrect (***THIS RETURNS A MOLECULE OBJECT***)
        # The add-method shoud return a new Molecule. In your realisation you
        # just return a string. 
        combined_atoms = self.copy()
        combined_atoms.extend(other)
        return Molecule(combined_atoms)

    def object_validation_checker(self):
        """
        explanation: this function checks the validity of the atom list. It checks whether the list 
                     values are tuples, their lenghts are equeal to two, the first tuple component 
                     is an Atom object, and the second component is an integer.
        """
        for tuple_pair in self:

            #  check whether the list values are tuples
            assert isinstance(tuple_pair, tuple), ValueError('the input value is not a tuple')

            # check whether their lenghts are equeal to two
            assert len(tuple_pair) == 2, ValueError('the atom tuple contains more than two values')

            # check whether the first tuple component is an Atom object
            assert isinstance(tuple_pair[1], int), \
                              ValueError('the number of atoms is not inserted correctly')

            # check whether the second component is an integer
            assert isinstance(tuple_pair[0], Atom), NotAtomObject(tuple_pair[0])

    def chemical_formula_maker(self):
        """
        explanation: this function creates a chemical formula for a group of Atom objects and
                     their abundance.
        output: 1- chemical_formula: this is a formula based on the Mendeleev symbols.
        """
        # add tuples to the chemical_formula string
        # Could also be done in a list-comprehension... (***USING LIST COMPREHENSION***)
        chemical_formula = ''.join([
            f'{atom.atomic_symbol}{num}' if num != 1 else atom.atomic_symbol
            for atom, num in self
            ])

        return chemical_formula

if __name__ == "__main__":

    # Evaluation part
    hydrogen = Atom('H', 1, 1)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)

    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    print (water) # H2O
    print (co2) # CO2
    print (water + co2) # H2OCO2
