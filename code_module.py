"""
The code module exports the Code class.

Code class: Translates XHAL mnemonics into binary codes.
"""
from error_checker import ErrorChecker


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
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",   # This code and above are when the a field = 0 (thus, all start with 0)
            "M": "1110000",     # This code and below are when the a field = 1 (thus, all start with 1)
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        self.jump_dict = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

    def dest(self, dest_mnemonic):
        """Looks up the XHAL dest mnemonic in the dest dictionary and returns the corresponding binary dest code."""
        return self.dest_dict[dest_mnemonic]

    def comp(self, comp_mnemonic):
        """Looks up the XHAL comp mnemonic in the comp dictionary and returns the corresponding binary comp code."""
        return self.comp_dict[comp_mnemonic]

    def jump(self, jump_mnemonic):
        """Looks up the XHAL jump mnemonic in the jump dictionary and returns the corresponding binary jump code."""
        return self.jump_dict[jump_mnemonic]