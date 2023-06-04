class NotIsotope(Exception):

    """
    type: exception class
    explanation: this error raises when two atoms are not isotpes
    output: an error raises NotIsotope
    """
    def __init__(self,proton_number1, proton_number2):
        self.proton_number1 = proton_number1
        self.proton_number2 = proton_number2
        super().__init__()

    def __str__(self) -> str:
        return f"The atoms with proton numbers {self.proton_number1} and {self.proton_number2} are not isotopes."

class NotAtomObject(Exception):

    """
    type: exception class
    explanation: this error raises when a variable is not Atom class object
    """
    def __init__(self, variable):
        super().__init__()
        self.variable = variable



    def __str__(self):
        return f"the input value {self.variable} is not an Atom object"   