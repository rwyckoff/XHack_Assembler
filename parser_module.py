"""
The parser module exports the Parser class.

Parser class: Opens XHAL .asm files and breaks XHAL assembly commands into their underlying fields and symbols.
"""


class Parser:
    """
    The Parser class is responsible for providing access to the input XHAL assembly code. It reads an .asm file one
    line at time. For each assembly command, it parses it and provides access to the command's components (fields and
    symbols). Additionally, the parser module removes all white space and comments from the given .asm file.

    Methods:
    __init__: Constructs the parser object and opens the XHAL input file and gets ready to parse it.
    has_more_commands: Returns true if there are more commands (lines) in the input.
    advance: Reads the next command from the input and makes it the current command.
    command_type: Returns the type of the current command (the types being A_Command, C_Command, or L_Command).
    symbol: Returns the symbol or decimanl of the current command.
    dest: Returns the dest mnemonic in the current C_Command.
    comp: Returns the comp mnemonic in the current C_Command.
    jump: Returns the jump mnemonic in the current C_Command.
    """

    # TODO: May need to add arguments to some or all of the below methods.

    def __init__(self, input_file):
        """Construct the Parser object and open the given XHAL .asm input file to enable parsing of it.

        Arguments:
        input_file: The XHAL .asm file to be parsed and translated into a .hack psuedo-binary machine language file.
        """
        self.input_file = input_file

    def has_more_commands(self):
        """Detect if there are more commands in the XHAL .asm input file. Return true if there are, and false
        otherwise."""
        pass

    def advance(self):
        """Read the next command from the XHAL .asm input file and makes that the current command. Advance() will only
        be called if has_more_commands() has just returned True. Initially there is no current command."""
        pass

    def command_type(self):
        """Return the type of the current command. There are three possible command types that could be returned:
        A_Command: @XXX-style Address commands where XXX is either a symbol or a decimal number.
        C_Command: Compute commands in the form of dest=comp;jump
        L_Command: A pseudo-command in the form of (XXX), where XXX is a symbol.
        """
        pass

    def symbol(self):
        """Return the symbol or decimal XXX of the current command, where the command is either an A_Command of the form
        @XXX or an L_Command of the form (XXX)."""
        pass

    def dest(self):
        """Return the dest mnemonic string (one of 8 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        pass

    def comp(self):
        """Return the comp mnemonic string (one of 28 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        pass

    def jump(self):
        """Return the jump mnemonic string (one of 8 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        pass
