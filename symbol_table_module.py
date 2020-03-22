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
        """Construct the SymbolTable object and initialize a symbol table with only predefined symbols and their pre-
        allocated RAM addresses. Then initialize three other symbol tables that will contain subsets of the main symbol
        table, for reporting purposes.
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

        # The below symbol tables also hold line numbers as the second number in each tuple.

        # Initialize the RAM symbol table to have the predefined symbols. Each will associated with the line number 0,
        # to indicate they're initialized before the assembly program is parsed.
        # Will later also hold copies of variables and associated RAM addresses and line numbers.
        self.ram_symbol_table = {
            "SP": ("0", "0"),
            "LCL": ("1", "0"),
            "ARG": ("2", "0"),
            "THIS": ("3", "0"),
            "THAT": ("4", "0"),
            "R0": ("0", "0"),
            "R1": ("1", "0"),
            "R2": ("2", "0"),
            "R3": ("3", "0"),
            "R4": ("4", "0"),
            "R5": ("5", "0"),
            "R6": ("6", "0"),
            "R7": ("7", "0"),
            "R8": ("8", "0"),
            "R9": ("9", "0"),
            "R10": ("10", "0"),
            "R11": ("11", "0"),
            "R12": ("12", "0"),
            "R13": ("13", "0"),
            "R14": ("14", "0"),
            "R15": ("15", "0"),
            "SCREEN": ("16384", "0"),
            "KBD": ("24576", "0")
        }

        # Initialize the ROM symbol table, which will hold copies of the labels and associated ROM addresses and line
        # numbers.
        self.rom_symbol_table = {}

        # Initialize the EQU symbol table
        self.equ_symbol_table = {}

    def add_entry(self, symbol, address, memory_type, line):
        """Adds the arguments symbol and address to the symbol table as a new entry."""
        self.symbol_table[symbol] = address
        if memory_type == "ROM":
            self.rom_symbol_table[symbol] = address, line
        elif memory_type == "RAM":
            self.ram_symbol_table[symbol] = address, line
        elif memory_type == "EQU":
            self.equ_symbol_table[symbol] = address, line

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

    def export_symbol_tables(self, io_file):
        # TODO: Change to relative path.
        with open(r"C:/Users/Robert Sirois/Dropbox/Shpob Storage/School/Compiler Design/Projects/"
                  r"Project One/Robert_Wyckoff_PJ01_XHack/symbol_tables/" + io_file + "_sym_tables.txt", "w") as file:
            h_titles = "Entry", "Address", "Line"
            header = f"RAM Symbol Table\n----------\n{h_titles[0]:<50}{h_titles[1]:<50}{h_titles[2]:<50}\n" \
                     f"------------------------------------------------------------------------------------------" \
                     f"----------------------\n"
            file.write(header)
            for entry in self.ram_symbol_table:
                file.write(f"{entry:<50}{self.ram_symbol_table[entry][0]:<50}{self.ram_symbol_table[entry][1]}\n")
            file.write("\n\n***********************************************************************************"
                       "***********************************\n\n\n\n")
            header = f"ROM Symbol Table\n----------\n{h_titles[0]:<50}{h_titles[1]:<50}{h_titles[2]:<50}\n" \
                     f"------------------------------------------------------------------------------------------" \
                     f"----------------------\n"
            file.write(header)
            for entry in self.rom_symbol_table:
                file.write(f"{entry:<50}{self.rom_symbol_table[entry][0]:<50}{self.rom_symbol_table[entry][1]}\n")
            file.write("\n\n***********************************************************************************"
                       "***********************************\n\n\n\n")
            header = f"EQU Symbol Table\n----------\n{h_titles[0]:<50}{h_titles[1]:<50}{h_titles[2]:<50}\n" \
                     f"-----------------------------------------------------------------------------------------" \
                     f"-----------------------\n"
            file.write(header)
            for entry in self.equ_symbol_table:
                file.write(f"{entry:<50}{self.equ_symbol_table[entry][0]:<50}{self.equ_symbol_table[entry][1]}\n")
