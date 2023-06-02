from exceptions import NotIsotope

class Atom():

    def __init__(self, atomic_symbol, atomic_number, neutron_number):
        self.atomic_symbol = atomic_symbol
        self.atomic_number = atomic_number
        self.neutron_number = neutron_number

    def __lt__(self, other):
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number < other.neutron_number

    def __le__(self, other):
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number <= other.neutron_number
    
    def __gt__(self, other):
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number > other.neutron_number

    def __ge__(self, other):
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number >= other.neutron_number

    def __eq__(self, other):
        self.isotope_checker(self.atomic_number, other.atomic_number)
        return self.neutron_number == other.neutron_number
   
    def proton_number(self):
        return self.atomic_number
    
    def mass_number(self):
        return self.atomic_number + self.neutron_number
    
    def isotope(self, new_number):
        self.neutron_number = new_number


    @staticmethod
    def isotope_checker(proton_number1, proton_number2):

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

