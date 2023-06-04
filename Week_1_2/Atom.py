"""
Date of final revision: ....
Explanation: This module contains a class (Atom) that makes an Atom object and returns some
             of its features, and using some rich comparison methods.
"""

from exceptions import NotIsotope

class Atom():
    """
    type: class
    explanation: this class contains three attributes and one initializer, three instance methods,
                 and five rich comparison methods. Each instance method returnsa feature of the 
                 object and each rich comparison method reintroduces the concept of each logical
                 statement.
    """

    def __init__(self, atomic_symbol, atomic_number, neutron_number):
        """
        type: initializer method
        input: 1- atomic_symbol (string): is the atomic symbol exists in Mendeleev table.
               2- atomic_number (integer): is the number of protons.
               3- neutron_number (integer): is the number of neutrons.
        explanation: this initializer get the above input and use them to make the initial object.
        """

        self.atomic_symbol = atomic_symbol
        self.atomic_number = atomic_number
        self.neutron_number = neutron_number

    def __lt__(self, other):
        """
        type: rich comparison method
        input: 1- other (Atom object): is the Atom object that one wants to compare with the current
                  object.
        explanation: this function check whether the current Atom object (self) is smaller than the
                          (other) Atom object.
        output: 1- True/False
        """

        # Check whether these two atom objects are isotopes
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number < other.neutron_number

    def __le__(self, other):
        """
        type: rich comparison method
        input: 1- other (Atom object): is the Atom object that one wants to compare with the current
                  object.
        explanation: this function check whether the current Atom object (self) is smaller and equal
                     than the (other) Atom object.
        output: 1- True/False
        """
        # Check whether these two atom objects are isotopes
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number <= other.neutron_number

    def __gt__(self, other):
        """
        type: rich comparison method
        input: 1- other (Atom object): is the Atom object that one wants to compare with the current
                  object.
        explanation: this function check whether the current Atom object (self) is larger than the
                          (other) Atom object.
        output: 1- True/False
        """

        # Check whether these two atom objects are isotopes
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number > other.neutron_number

    def __ge__(self, other):
        """
        type: rich comparison method
        input: 1- other (Atom object): is the Atom object that one wants to compare with the current
                  object.
        explanation: this function check whether the current Atom object (self) is larger and equal
                     than the (other) Atom object.
        output: 1- True/False
        """

        # Check whether these two atom objects are isotopes
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number >= other.neutron_number

    def __eq__(self, other):
        """
        type: rich comparison method
        input: 1- other (Atom object): is the Atom object that one wants to compare with the current
                  object.
        explanation: this function check whether the current Atom object (self) is equal to the 
                     (other) Atom object.
        output: 1- True/False
        """

        # Check whether these two atom objects are isotopes
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number == other.neutron_number

    def proton_number(self):
        """
        type: instance method
        explanation: this function returns the number of protons.
        output: 1- atomic_number: number of protons. 
        """

        return self.atomic_number

    def mass_number(self):
        """
        type: instance method
        explanation: this function returns the mass number.
        output: 1- number of protons plus number of neutrons. 
        """

        return self.atomic_number + self.neutron_number

    def isotope(self, new_number):
        """
        type: instance method
        input: 1- new_number: is a new number for neutrons in an atom.
        explanation: this function change the number of neutrons to make an isotope for that object.
        """

        self.neutron_number = new_number


    @staticmethod
    def isotope_checker(proton_number1, proton_number2):
        """
        type: instance method
        input: 1- proton_number1: is the proton number of the first Atom object
               2- proton_number2: is the proton number of the second Atom object
        explanation: this function check whether two Atom objects are isotope or raise NotIsotope
                     error.
        """
        if proton_number1 != proton_number2:
            raise NotIsotope(proton_number1, proton_number2)

if __name__ == "__main__":
    protium = Atom('H', 1, 1)
    deuterium = Atom('H', 1, 2)
    oxygen = Atom('O', 8, 8)
    tritium = Atom('H', 1, 2)
    tritium.isotope(3)

    assert tritium.neutron_number == 3
    assert tritium.mass_number() == 4

    assert protium < deuterium
    assert deuterium <= tritium
    assert tritium >= protium
    print (oxygen > tritium)
