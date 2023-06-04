from Molecule import Molecule
from Atom import Atom

class Chloroplast():

    def __init__(self):
        self.H2O = 0
        self.CO2 = 0
        self.C6H12O6 = 0
        self.O2 = 0
    
    def __str__(self):
        return f'H2O molecule number: {self.H2O}\nCO2 molecule number: {self.CO2}'

    def add_molecule(self, molecule):

        try:
            attribute = getattr(self, str(molecule))
            attribute += 1
            setattr(self, str(molecule), attribute)

            if self.H2O >= 12 and self.CO2 >= 6 :
                return self.photosyntheses()
            else:
                return []

        except AttributeError:
            print('the input value is not H2O or CO2')
        
    def photosyntheses(self):
        self.H2O -= 12
        self.CO2 -= 6
        self.C6H12O6 += 1
        self.O2 += 6
        return [('C6H12O6', self.C6H12O6), ('O2', self.O2)]

if __name__ == "__main__":

    hydrogen = Atom('H', 1, 1)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)
    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    demo = Chloroplast()
    els = [water, co2]

    while (True):
        print ('\nWhat molecule would you like to add?')
        print ('[1] Water')
        print ('[2] carbondioxyde')
        print ('Please enter your choice: ', end='')
        try:
            choice = int(input())
            print(els[choice-1])
            res = demo.add_molecule(els[choice-1])
            #print(demo)

            if (len(res)==0):
                print (demo)
            else:
                print ('\n=== Photosynthesis!')
                print (res)
                print (demo)

        except Exception:
            print ('\n=== That is not a valid choice.')
