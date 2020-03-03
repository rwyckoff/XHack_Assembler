"""
The symbol table module exports the SymbolTable class.

SymbolTable class: Keeps a correspondence between symbolic labels and numeric addresses using a dictionary.
"""


class SymbolTable:
    """
    The SymbolTable class is responsible for managing a symbol table (implemented as a dictionary) of symbols that the
    assembler can use to resolve symbols in the XHAL code.

    Methods:
    __init__: Constructs the SymbolTable object and creates a symbol table empty except for predefined symbols.
    add_entry: Adds an entry consisting of a symol and an address to the table.
    contains: Determines if the symbol table contains a given symbol.
    get_address: Returns the address associated with a given symbol.
    """

    def __init__(self):
        """Construct the SymbolTable object and initialize a symbol table with only predefined symbols.
        """
        self.symbol_table = {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
            "SCREEN": "16384",
            "KBD": "24576"
        }

    def add_entry(self, symbol, address):
        """Adds the arguments symbol and address to the symbol table as a new entry."""
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        """Looks in the symbol table to determine if the symbol argument is inside it. Returns true if it is and false
        otherwise."""
        if symbol in self.symbol_table:
            return True
        else:
            return False

    def get_address(self, symbol):
        """Returns the int ROM address associated with the given symbol argument. Should only be called in contains()
        had just returned true."""
        return self.symbol_table[symbol]


