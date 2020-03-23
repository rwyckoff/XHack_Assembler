"""
Robert Wyckoff
CS 4100
UCCS
Project One -- XHASM (Extended Hack Assembler)

The main XHack Assembler module drives the translation process from one XHAL file to one .hack pseudo-binary machine
language file.
"""

from sys import argv

from code_module import Code
from error_checker import *
from parser_module import Parser
from symbol_table_module import SymbolTable


# ************************************************************************************************
# Helper functions

# Idea from
# https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
def represents_int(string):
    """Return true if the given string is translatable into an integer and false otherwise."""
    try:
        int(string)
        return True
    except ValueError:
        return False

# ************************************************************************************************
# Main functions


def first_pass(current_line, current_ROM_address):
    """Conduct the first pass through the assembler, mostly adding symbols to the symbol table."""
    while parser.has_more_commands():
        current_line += 1
        parser.advance()
        check_comment_formatting_warning(parser.current_command, current_line)
        parser.command_type()
        if parser.current_command_type == "EQU":
            check_illegal_equ_format_error(parser.current_command, current_line)

            parser.symbol(current_line)
            # If a binary or hex format error was detected, record the error and skip the line.
            if parser.current_command_content == "ERROR":
                continue
            # If the EQU symbol name is illegal, record the error and skip the current line.
            if check_illegal_symbol_error(parser.current_command_equ_label, current_line):
                continue

            # If the EQU symbol redefines a previously defined symbol, record either an error or a warning.
            if symbol_table.contains(parser.current_command_equ_label):
                try:
                    prev_label_add = symbol_table.get_address(parser.current_command_content)
                except KeyError:
                    try:
                        prev_label_add = symbol_table.get_address(parser.current_command_equ_label)
                    except KeyError:
                        record_symbol_key_error(parser.current_command, current_line)
                        continue
                # If the EQU symbol redefines a previously defined symbol with a different address, record the error
                # and skip the current line.
                if prev_label_add != parser.current_command_equ_label:
                    record_symbol_redefinition_error(parser.current_command_content,
                                                     current_line, prev_label_add)
                    continue
                # Otherwise, the original and new symbol addresses are the same, so technically no harm done. Thus,
                # record a warning and continue as normal.
                else:
                    record_symbol_redefinition_warning(parser.current_command_content, current_line,
                                                       parser.current_command_equ_label)
            # If no label-related errors, add the EQU symbol to the symbol table.
            symbol_table.add_entry(parser.current_command_equ_label, parser.current_command_content, "EQU",
                                   current_line)

        elif parser.current_command_type == "C" or parser.current_command_type == "A":
            current_ROM_address += 1
            print(f"\nCURRENT ROM ADDRESS: {current_ROM_address}, instr: {parser.current_command}")
        elif parser.current_command_type == "L":
            if check_l_type_text_after_paren_error(parser.current_command, current_line):
                continue
            else:
                parser.symbol(current_line)

            # If the label name is illegal, record the error and skip the current line.
            if check_illegal_symbol_error(parser.current_command_content, current_line):
                continue

            # If the label redefines a previously defined label, record either an error or a warning.
            if symbol_table.contains(parser.current_command_content):
                prev_label_add = symbol_table.get_address(parser.current_command_content)
                # If the label redefines a previously defined label with a different ROM address, record the error
                # and skip the current line.
                if prev_label_add != current_ROM_address:
                    record_symbol_redefinition_error(parser.current_command_content,
                                                     current_line, prev_label_add)
                    continue
                # Otherwise, the original and new label ROM addresses are the same, so technically no harm done. Thus,
                # record a warning and continue as normal.
                else:
                    record_symbol_redefinition_warning(parser.current_command_content, current_line,
                                                       current_ROM_address)
            # If no label-related errors, add the label to the symbol table.
            symbol_table.add_entry(parser.current_command_content, current_ROM_address, "ROM",
                                   current_line)

        elif parser.current_command_type == "ILLEGAL" or parser.current_command_type == "COMMENT" or \
                parser.current_command_type == "BLANK":
            continue

    # Return the current ROM address to save it for the second pass.
    return current_ROM_address


def second_pass(current_line, current_RAM_address):
    """Conduct the second pass through the assembler, translating commands and handling symbols."""
    while parser.has_more_commands():
        current_line += 1
        current_word = ""
        parser.advance()
        print(f"\nCurrent command: {parser.current_command}")
        parser.command_type()
        print(f"Current command type: {parser.current_command_type}")
        # If the current line starts with a //, consider it a comment and ignore it.
        if parser.current_command_type == "COMMENT" or parser.current_command_type == "EQU" or \
                parser.current_command_type == "BLANK":
            continue
        elif parser.current_command_type == "A" or parser.current_command_type == "L":
            parser.strip_comments()
            parser.symbol(program_line)
            print(f"Current command content: {parser.current_command_content}")
            if parser.current_command_type == "A":
                # If the current A-command content is not a positive integer, it is a symbol, so check the symbol table.
                if not represents_int(parser.current_command_content):
                    # If the symbol table contains the A-command symbol, retrieve the integer address associated with
                    # that symbol and make it the address.
                    if symbol_table.contains(parser.current_command_content):
                        address = symbol_table.get_address(parser.current_command_content)
                    # Otherwise the symbol table does not yet contain the current symbol, so add it and make it the
                    # address.
                    else:
                        symbol_table.add_entry(parser.current_command_content, current_RAM_address, "RAM",
                                               program_line)
                        current_RAM_address += 1
                        address = symbol_table.get_address(parser.current_command_content)

                # If an error is found with the current non-symbolic A-Type command, record the error and skip the line.
                elif check_a_type_int_command(parser.current_command_content, program_line):
                    continue
                else:
                    address = parser.current_command_content
                # If an error is found with translating the address field into binary or the binary code is too long,
                # record the error and skip the line.
                if check_a_type_bin_command(address, program_line):
                    continue
                # Otherwise, everything appears fine with the address field, so translate as usual.
                else:
                    address_code = bin(int(address)).replace("0b", "")
                    current_word = "0" + address_code.zfill(15)

            # If the current command type is an L-type, skip over it.
            elif parser.current_command_type == "L":
                continue

        # If the current command is a C-type, parse it to get all its fields.
        elif parser.current_command_type == "C":
            parser.strip_comments()
            parser.dest()
            print(f"Current command dest: {parser.current_command_dest}")
            try:
                dest_code = code_translator.dest(dest_mnemonic=parser.current_command_dest)
            except KeyError:
                record_c_type_dest_error(program_line)
                continue
            print(f"Dest binary code: {dest_code}")
            parser.comp()
            print(f"Current command comp: {parser.current_command_comp}")
            try:
                comp_code = code_translator.comp(comp_mnemonic=parser.current_command_comp)
            except KeyError:
                record_c_type_comp_error(program_line)
                continue
            print(f"Comp binary code: {comp_code}")
            if parser.current_command_subtype == "COMP":
                current_word = "111" + comp_code + dest_code + "000"
            elif parser.current_command_subtype == "JUMP":
                parser.jump()
                print(f"Current command jump: {parser.current_command_jump}")
                try:
                    jump_code = code_translator.jump(jump_mnemonic=parser.current_command_jump)
                except KeyError:
                    record_c_type_jump_error(program_line)
                    continue
                print(f"Jump binary code: {jump_code}")
                current_word = "111" + comp_code + dest_code + jump_code

        # If no errors have occurred thus far, write the current binary word to the output file.
        print(f"Current word: {current_word}")
        output_file.write(current_word + "\n")

# ************************************************************************************************
# Program begins here:


# Open a .hack file for writing binary text to.
# Relative file location code from
# https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
file_path = os.path.abspath(__file__)
file_dir = os.path.split(file_path)[0]
relative_path = r"binary_output/" + argv[2] + ".hack"  # The output file name (minus the .hack) is arg 2.
output_file_path = os.path.join(file_dir, relative_path)
print(output_file_path)
output_file = open(output_file_path, "w")

# Create and open an error file if the option to is set.
error_file = None
if config.WRITE_ERRORS_TO_LOG:
    error_file = open(create_error_file(argv[2]), "w")

parser = Parser(argv[1])  # Initialize the parser with the input file as the first command-line argument.
code_translator = Code()  # Initialize the code module, responsible for translation from XHAL to binary codes.
symbol_table = SymbolTable()  # Initialize the symbol table, including filling in the predefined symbols.

# Initialize program line and memory addresses.
program_line = 0
ROM_address = 0
RAM_address = 16

# Conduct the first pass through the assembly program and build the symbol table without generating any code.
print("\nBeginning the first pass of the assembly program....\n\n")
ROM_address = first_pass(program_line, ROM_address)

# Reset parser so it starts from the beginning of the assembly code again.
parser.reset_parser()

# Print the symbol table at this point for reference.
print(f"\n\n\n\n\n*************************\n\n\nSymbol Table:\n{symbol_table.symbol_table}\n\n\n***************\n\n\n")

# Conduct the second pass through the assembly program, parsing each line and generating the binary code line by line.
print("\nBeginning the second pass of the assembly program....\n\n")
second_pass(program_line, RAM_address)

# Print the final symbol table for reference.
print(f"\n\n\n\n\n*************************\n\n\nSymbol Table:\n{symbol_table.symbol_table}\n\n\n***************\n\n\n")

# Export symbol tables.
if config.EXPORT_SYMBOL_TABLES:
    symbol_table.export_symbol_tables(argv[2])

# Close files.
if error_file is not None:
    error_file.close()
output_file.close()
