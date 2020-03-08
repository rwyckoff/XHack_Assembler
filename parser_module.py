"""
The parser module exports the Parser class.

Parser class: Opens XHAL .asm files and breaks XHAL assembly commands into their underlying fields and symbols.
"""
import re


# TODO: Currently setting instance variables instead of returning them. Cool? May want to change descriptions.
# TODO: When an error is encountered, report/log it and continue so that I can find all the errors in the file.


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
    symbol: Returns the symbol or decimal of the current command.
    dest: Returns the dest mnemonic in the current C_Command.
    comp: Returns the comp mnemonic in the current C_Command.
    jump: Returns the jump mnemonic in the current C_Command.
    """

    # Initialize all regular expressions for the parser.
    regex_a_command = re.compile(r'^@', flags=re.MULTILINE)

    # TODO: Below is too specific for error handling. Keep just in case.
    # regex_c_command = re.compile(r'(^[ADM]=)|(^MD=)|(^AM=)|(^AD=)|(^AMD=)|(^null=)', flags=re.MULTILINE)

    regex_c_command = re.compile(r'^.+=')
    regex_c_jump_command = re.compile(r'(^.*;)')
    regex_l_command = re.compile(r'(^\().*(\))')
    regex_post_dest = re.compile(r'=.*')
    regex_comp_pre_comp = re.compile(r'.*=')
    regex_jump_pre_comp = re.compile(r';.*')
    regex_pre_jump = re.compile(r'.*;')
    regex_comment = re.compile(r'//.*')

    def __init__(self, input_file):
        """Construct the Parser object and open the given XHAL .asm input file to enable parsing of it. Then save that
        file as a list of commands to easily iterate over.

        Arguments:
        input_file: The XHAL .asm file to be parsed and translated into a .hack pseudo-binary machine language file.
        """
        # Open the file for parsing, and save the text as a list where each element is a line.
        with open(input_file, 'r') as file:
            self.command_list = file.readlines()

        # Strip newlines from the command list and remove blank lines.
        self.command_list = [line.strip() for line in self.command_list if line.strip() != ""]

        # Initialize variables.
        self.command_idx = 0
        self.current_command = None
        self.current_command_type = None
        self.current_command_subtype = None
        self.current_command_content = None
        self.current_command_dest = None
        self.current_command_comp = None
        self.current_command_jump = None

    def has_more_commands(self):
        """Detect if there are more commands in the XHAL .asm input file. Return true if there are, and false
        otherwise."""
        if self.command_idx < len(self.command_list):
            return True
        else:
            return False

    def advance(self):
        """Read the next command from the XHAL .asm input file and makes that the current command. Advance() will only
        be called if has_more_commands() has just returned True. Initially there is no current command."""
        self.current_command = self.command_list[self.command_idx]
        self.command_idx += 1
        return self.current_command

    def command_type(self):
        """Return the type of the current command. There are three possible command types that could be returned:
        A_Command: @XXX-style Address commands where XXX is either a symbol or a decimal number.
        C_Command: Compute commands in the form of dest=comp;jump
        L_Command: A pseudo-command in the form of (XXX), where XXX is a symbol.
        """
        # Detect the current command type and set it based on the class-level compiled regular expressions.
        if self.regex_a_command.match(self.current_command):
            self.current_command_type = "A"
        elif self.regex_c_command.match(self.current_command):
            self.current_command_type = "C"
            self.current_command_subtype = "COMP"
        elif self.regex_c_jump_command.match(self.current_command):
            self.current_command_type = "C"
            self.current_command_subtype = "JUMP"
        elif self.regex_l_command.match(self.current_command):
            self.current_command_type = "L"
        elif self.regex_comment.match(self.current_command):
            self.current_command_type = "COMMENT"
        else:
            self.current_command_type = "COMMAND TYPE NOT DETECTED"  # TODO: Error detection here?

    def symbol(self):
        """Return the symbol or decimal XXX of the current command, where the command is either an A_Command of the form
        @XXX or an L_Command of the form (XXX)."""
        # Gets the content (either a symbol or a decimal) of the current A or L command.
        if self.current_command_type == "A":
            self.current_command_content = self.current_command.replace("@", "")
        elif self.current_command_type == "L":
            self.current_command_content = self.current_command.replace("(", "").replace(")", "")
        else:
            print("ERROR!")  # TODO: Make into a real error catch.

    def dest(self):
        """Return the dest mnemonic string (one of 8 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        # Use a class-level regex to remove everything following the dest portion of the command and set that to
        # the dest portion of the command.
        if self.current_command_subtype == "COMP":
            self.current_command_dest = re.sub(self.regex_post_dest, "", self.current_command)
        elif self.current_command_subtype == "JUMP":
            self.current_command_dest = "null"  # Dest fields for jumps are null and will translate to 000.

    def comp(self):
        """Return the comp mnemonic string (one of 28 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        # Use a class-level regex to remove everything before the comp portion of the command and set that to
        # the comp portion of the command.
        if self.current_command_subtype == "COMP":
            self.current_command_comp = re.sub(self.regex_comp_pre_comp, "", self.current_command)
        elif self.current_command_subtype == "JUMP":
            self.current_command_comp = re.sub(self.regex_jump_pre_comp, "", self.current_command)

    def jump(self):
        """Return the jump mnemonic string (one of 8 possible) in the current C_Command. Will only be called when
        command_type() returns a C_Command."""
        # Use a class-level regex to remove everything before the jump portion of the command and set that to
        # the jump portion of the command.
        self.current_command_jump = re.sub(self.regex_pre_jump, "", self.current_command)

    def reset_parser(self):
        """Resets the command index of the parser so that the assembler can run through the XHAL code multiple times."""
        self.command_idx = 0
        self.current_command = None
