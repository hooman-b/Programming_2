
class LenghtDiscripancy(Exception):

    """
    type: exception class
    explanation: this error raises when the number of keys is different from number of values
    output: an error raises NotIsotope
    """
    def __init__(self, keys_len, vals_len):
        self.keys_len = keys_len
        self.vals_len = vals_len
        super().__init__()

    def __str__(self) -> str:
        return f"keys number {self.keys_len} is different from vals number {self.vals_len}"
    