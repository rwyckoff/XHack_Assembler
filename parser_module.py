"""
The parser module exports the Parser class.

Parser class: Opens XHAL .asm files and breaks XHAL assembly commands into their underlying fields and symbols.
"""
from error_checker import *


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
    strip_whitespace: Strips all whitespace out of a command.
    command_type: Sets the type of command (comment, blank, illegal, EQU, A, C, or L)
    translate_bin_hex: Translates binary and hexidecimal code and handles relevant errors.
    reset_parser: Resets the index of the commands to 0. Used between passes of the assembler.
    strip_comments: Removes comments from commands.
    """

    # Initialize all regular expressions for the parser. Done at the class level so they don't have to be initialized
    # more than once.
    regex_a_command = re.compile(r'^@', flags=re.MULTILINE)
    regex_c_command = re.compile(r'^.+=')
    regex_c_jump_command = re.compile(r'(^.*;)')
    regex_l_command = re.compile(r'(^\().*(\))')
    regex_post_dest = re.compile(r'=.*')
    regex_comp_pre_comp = re.compile(r'.*=')
    regex_jump_pre_comp = re.compile(r';.*')
    regex_pre_jump = re.compile(r'.*;')
    regex_comment = re.compile(r'//.*')
    regex_binary = re.compile(r'^0b|0B.*')
    regex_hex = re.compile(r'^0x|0X.*')
    regex_equ = re.compile(r'^.EQU\s.*\s.*')
    regex_post_equ_symbol = re.compile(r'\s.*')
    regex_pre_equ_address = re.compile(r'.*\s')

    def __init__(self, input_file):
        """Construct the Parser object and open the given XHAL .asm input file to enable parsing of it. Then save that
        file as a list of commands to easily iterate over.

        Arguments:
        input_file: The XHAL .asm file to be parsed and translated into a .hack pseudo-binary machine language file.
        """
        # Open the file for parsing, and save the text as a list where each element is a line.
        with open(input_file, 'r') as file:
            self.command_list = file.readlines()

        # Strip newlines from the command list. Does not remove blank lines at this time
        # so that line numbers in error-reporting are accurate.
        self.command_list = [line.strip() for line in self.command_list]

        # Initialize variables.
        self.command_idx = 0
        self.current_command = None
        self.current_command_type = None
        self.current_command_subtype = None
        self.current_command_content = None
        self.current_command_dest = None
        self.current_command_comp = None
        self.current_command_jump = None
        self.current_command_equ_label = None

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

    def strip_whitespace(self):
        """Edit the current command, stripping off any whitespace"""
        self.current_command = self.current_command.replace(" ", "")

    def command_type(self):
        """Set the type of the current command. There are three possible command types that could be returned:
        A_Command: @XXX-style Address commands where XXX is either a symbol or a decimal number.
        C_Command: Compute commands in the form of dest=comp;jump. Sub-types are jump and comp.
        L_Command: A pseudo-command in the form of (XXX), where XXX is a symbol.
        BLANK: A blank command, with no content. Will be skipped over by the assembler.
        EQU: An equate directive of the form .EQU symbol value
        COMMENT: A line with only a comment in it. Will be skipped over by the assembler.
        """
        # Detect the current command type and set it based on the class-level compiled regular expressions.
        if not self.current_command.strip():    # If command is blank
            self.current_command_type = "BLANK"
            return

        if self.regex_equ.match(self.current_command):
            self.current_command_type = "EQU"
            return
        else:
            self.strip_whitespace()     # Strip whitespace if the command type is not EQU, since we won't need it.

        if self.regex_comment.match(self.current_command):
            self.current_command_type = "COMMENT"
        elif self.regex_a_command.match(self.current_command):
            self.current_command_type = "A"
        elif self.regex_c_command.match(self.current_command):
            self.current_command_type = "C"
            self.current_command_subtype = "COMP"
        elif self.regex_c_jump_command.match(self.current_command):
            self.current_command_type = "C"
            self.current_command_subtype = "JUMP"
        elif self.regex_l_command.match(self.current_command):
            self.current_command_type = "L"
        else:
            self.current_command_type = "COMMAND TYPE NOT DETECTED"

    def translate_bin_hex(self, content, line):
        """Detect if the content of the command is written in binary or hexidecimal, then translate and redefine the
        content into decimal and return that value."""
        if self.regex_binary.match(content):
            print("Binary detected! Translating....")
            stripped_content = content.replace('0b', '').replace('0B', '')
            try:
                return str(int(stripped_content, 2))
            except ValueError:
                record_invalid_bin_error(stripped_content, line)    # Record error if binary content is invalid.
                return "ERROR"
        elif self.regex_hex.match(self.current_command_content):
            print("Hex detected! Translating....")
            stripped_content = self.current_command_content.replace('0x', '').replace('0X', '')
            try:
                return str(int(stripped_content, 16))
            except ValueError:
                record_invalid_hex_error(stripped_content, line)    # Record error if hex content is invalid.
                return "ERROR"

        # No binary or hexadecimal is detected, so return the content unchanged.
        else:
            return content

    def symbol(self, line):
        """Set the symbol or decimal XXX of the current command, where the command is either an A_Command of the form
        @XXX or an L_Command of the form (XXX). Or, if the command is an EQU directive, set both the symbol (label)
        and the address (content)."""
        # Gets the content (either a symbol or a decimal) of the current A L, or EQU command.
        if self.current_command_type == "EQU":
            stripped_of_equ = self.current_command.replace(".EQU ", "")
            self.current_command_equ_label = re.sub(self.regex_post_equ_symbol, "", stripped_of_equ)
            self.current_command_content = re.sub(self.regex_pre_equ_address, "", stripped_of_equ)
            self.current_command_content = self.translate_bin_hex(self.current_command_content, line)
        elif self.current_command_type == "A":
            self.current_command_content = self.current_command.replace("@", "")
            self.current_command_content = self.translate_bin_hex(self.current_command_content, line)
        elif self.current_command_type == "L":
            self.current_command_content = self.current_command.replace("(", "").replace(")", "")
            self.current_command_content = self.translate_bin_hex(self.current_command_content, line)
        else:
            print("ERROR!")

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
        """Reset the command index of the parser so that the assembler can run through the XHAL code multiple times."""
        self.command_idx = 0
        self.current_command = None

    def strip_comments(self):
        """Edit the current command, stripping off any inline comments."""
        comment_text = self.regex_comment.search(self.current_command)
        if comment_text is not None:
            self.current_command = self.current_command.replace(comment_text[0], "")
