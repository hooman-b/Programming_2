"""
Problems with the code:
1-  (solved)    # This is incorrect.
            # You should have returned new sugar and oxygen molecules. In this case you
            # just return a list of tuples of strings and numbers.

2- (solved) # get the value of an attribute
            # This is a rather complex way to increase the 
            # corresponding value of self.H2O or self.CO2, but ok.
            # It's nice that you put this inside a try-catch block
            # so a wrong molecule gets caught directly. 
            # (**Yes it is complex but I did not use if clause here**)

            # However, with this method I could also increase self.C2H12O6
            # (**solve this problem**)

Explanation: This module contains a class (Chloroplast) that makes a Chloroplast object and returns
             a list of tuples from the products of the excersize's chemical reaction.
"""
from Molecule import Molecule
from Atom import Atom

class Chloroplast():
    """
    type: class
    explanation: this class contains four attributes, one initializer,
                 and two instance methods. its instance methods are responsible for doing
                 photosyntheses process when the number ofreactors reach to the required threshold.
    """

    def __init__(self):
        """
        attributes: 1- H2O (integer): number of H2O (water) molecules.
                    2- CO2 (integer): number of CO2 (Carbon Dyoxide) molecules.
        """
        self.H2O = 0
        self.CO2 = 0

    def __str__(self):
        """
        type: dunder method
        explanation: returns the the number of water and co2 molecules.
        output: 1- a string of the water and co2 numbers.
        """

        return f'H2O molecule number: {self.H2O}\nCO2 molecule number: {self.CO2}'

    def add_molecule(self, molecule):
        """
        input: 1- molecule: it is a Molecule object. 
        explanation: this method increments the number of water and co2, and when these numbers
                     reaches to the proper amount call photosyntheses process.
        output: 1- list of products: it contains the number of sugar and oxygen molecules producted
                   in the reaction.
                2- empty list: when the number of reactors do not meet the required amount an empty
                               list will be returned.
        """

        # try to find the proper attribute
        try:
            # nice to do it like this (could be a one-liner, though)
            attribute = getattr(self, str(molecule))
            attribute += 1

            # set the new value to the attribute
            setattr(self, str(molecule), attribute)

            # return the product list if some criteria are met
            if self.H2O >= 12 and self.CO2 >= 6 :
                return self.photosyntheses()

            # return empty list
            else:
                return []
         # if wrong attribute name is inserted, raise and error <-- you are not raising an error
        except AttributeError:
            # better to raise an exception here, I would argue
            print('the input value is not H2O or CO2')

    def photosyntheses(self):
        """
        explanation: this method emplements the chemical reation (photosyntheses).
        output: 1- list of products: it contains the number of sugar and oxygen molecules producted
                   in the reaction.
        """
        self.H2O -= 12
        self.CO2 -= 6
        C6H12O6 = Molecule([(Atom('C', 6, 6), 6), (Atom('H', 1, 1), 12), (Atom('O', 8, 8), 6)])
        O2 = Molecule([(Atom('O', 8, 8), 2)])

        return [(str(C6H12O6), 1), (str(O2), 6)]

if __name__ == "__main__":

    # Evaluation code
    hydrogen = Atom('H', 1, 1)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)
    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    demo = Chloroplast()
    els = [water, co2]

    while True:
        print ('\nWhat molecule would you like to add?')
        print ('[1] Water')
        print ('[2] carbondioxyde')
        print ('Please enter your choice: ', end='')
        try:
            choice = int(input())
            print(els[choice-1])
            res = demo.add_molecule(els[choice-1])
            #print(demo)

            if len(res) == 0:
                print (demo)
            else:
                print ('\n=== Photosynthesis!')
                print (res)
                print (demo)

        except ValueError:
            print ('\n=== That is not a valid choice.')
