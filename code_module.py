"""
The code module exports the Code class.

Code class: Translates XHAL mnemonics into binary codes.
"""


class Code:
    """
    The Code class is responsible for taking the XHAL mnemonics gotten by the Parser class and translating them into
    .hack binary codes.

    Methods:
    __init__: Constructs the Code object, initializing the binary code dictionaries.
    dest: Takes a dest mnemonic string and returns its corresponding 3-bit binary code.
    comp: Takes a comp mnemonic string and returns its corresponding 7-bit binary code.
    jump: Takes a jump mnemonic string and returns its corresponding 3-bit binary code.
    """

    def __init__(self):
        """Construct the Code object and initialize the dictionaries that map XHAL mnemonics to .hack binary codes."""
        self.dest_dict = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }
        self.comp_dict = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
        }

    def dest(self, dest_mnemonic):
        """Looks up the XHAL dest mnemonic in the dest dictionary and returns the corresponding binary dest code."""
        return self.dest_dict[dest_mnemonic]

    def comp(self):
        """Looks up the XHAL comp mnemonic in the comp dictionary and returns the corresponding binary comp code."""
        pass

    def jump(self):
        """Looks up the XHAL jump mnemonic in the jump dictionary and returns the corresponding binary jump code."""
        pass