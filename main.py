"""
The main XHack Assembler module drives the translation process from one XHAL file to one .hack pseudo-binary machine
language file.
"""

from sys import argv
from parser_module import Parser
from code_module import Code

# TODO: Encapsulate what's inside the loop into a few functions. Probably Parse(), Translate_Code(), and others?
# TODO: Make output file also an arg?

# Open a .hack file for writing binary text to.
output_file = open(r"C:/Users/Robert Sirois/Dropbox/Shpob Storage/School/Compiler Design/Projects/Project One/"
                   r"Robert_Wyckoff_PJ01_XHack/test_output_data/test.hack", "w")

# Initialize the parser with the input file as the first command-line argument.
parser = Parser(argv[1])

code_translator = Code()

# TODO: Track the current ROM address for the symbol table in the two loops, outside of functions and objects.

while parser.has_more_commands():
    current_word = ""
    parser.advance()
    print(f"\nCurrent command: {parser.current_command}")
    parser.command_type()
    print(f"Current command type: {parser.current_command_type}")
    if parser.current_command_type == "A" or parser.current_command_type == "L":
        parser.symbol()
        print(f"Current command content: {parser.current_command_content}")

        if parser.current_command_type == "A":
            # String to binary translation from https://www.geeksforgeeks.org/python-convert-string-to-binary/
            # address_code = ''.join(format(ord(i), 'b') for i in parser.current_command_content)

            address_code = bin(int(parser.current_command_content)).replace("0b", "")
            current_word = "0" + address_code.zfill(15)

    elif parser.current_command_type == "C":
        parser.dest()
        print(f"Current command dest: {parser.current_command_dest}")
        dest_code = code_translator.dest(dest_mnemonic=parser.current_command_dest)
        print(f"Dest binary code: {dest_code}")
        parser.comp()
        print(f"Current command comp: {parser.current_command_comp}")
        comp_code = code_translator.comp(comp_mnemonic=parser.current_command_comp)
        print(f"Comp binary code: {comp_code}")
        if parser.current_command_subtype == "COMP":
            current_word = "111" + comp_code + dest_code + "000"
        elif parser.current_command_subtype == "JUMP":
            parser.jump()
            print(f"Current command jump: {parser.current_command_jump}")
            jump_code = code_translator.jump(jump_mnemonic=parser.current_command_jump)
            print(f"Jump binary code: {jump_code}")
            current_word = "111" + comp_code + dest_code + jump_code

    # If the current line starts with a //, consider it a comment and ignore it.
    elif parser.current_command_type == "COMMENT":
        continue

    print(f"Current word: {current_word}")
    output_file.write(current_word + "\n")
