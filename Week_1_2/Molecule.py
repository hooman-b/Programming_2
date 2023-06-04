"""
Date of final revision: ....
Explanation: This module contains a class (Molecule) that makes an Molecule object and returns
             its chemical formula and adds two chemical formula to each other.
"""

from Atom import Atom
from exceptions import NotAtomObject

class Molecule(list):
    """
    type: list-like class
    explanation: this class contains two attributes, one initializer, two dunder methods,
                 and two instance methods. its instance methods are responsible for validating
                 the input list and making chemical formula.
    """

    def __init__(self, atom_list):
        """
        type: initializer method
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
        type: dunder method
        explanation: returns the chemical formula of the molecule.
        output: 1- chemical_formula: is the chemical formula of an Molecule object.
        """

        return self.chemical_formula

    def __add__(self, other):
        """
        type: dunder method
        explanation: it adds two chemical formula strings to each other.
        output: 1- formula: this is a chemical formula of a compound.
        """

        formula = self.chemical_formula + other.chemical_formula
        return formula

    def object_validation_checker(self):
        """
        type: instance method
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
        type: instance method
        explanation: this function creates a chemical formula for a group of Atom objects and
                     their abundance.
        output: 1- chemical_formula: this is a formula based on the Mendeleev symbols.
        """
        chemical_formula = ''

        # add tuples to the chemical_formula string
        for tuple_pair in self:

            # if the number of atom is not equal to one add its number
            if tuple_pair[1] != 1:
                chemical_formula += tuple_pair[0].atomic_symbol + str(tuple_pair[1])

            else:
                chemical_formula += tuple_pair[0].atomic_symbol

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
    