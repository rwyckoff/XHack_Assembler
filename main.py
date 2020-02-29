"""
The main XHack Assembler module drives the translation process from one XHAL file to one .hack pseudo-binary machine
language file.
"""

from sys import argv
from parser_module import Parser

# Initializes the parser with the input file as the first command-line argument.
parser = Parser(argv[1])

while parser.has_more_commands():
    parser.advance()
    print(f"Current command: {parser.current_command}")
    parser.command_type()
    print(f"Current command type: {parser.current_command_type}")
    if parser.current_command_type == "A" or parser.current_command_type == "L":
        parser.symbol()
        print(f"Current command content: {parser.current_command_content}")
    elif parser.current_command_type == "C":
        if parser.current_command_subtype == "COMP":
            parser.dest()
            print(f"Current command dest: {parser.current_command_dest}")
            parser.comp()
            print(f"Current command comp: {parser.current_command_comp}")
        elif parser.current_command_subtype == "JUMP":
            parser.jump()
            print(f"Current command jump: {parser.current_command_jump}")
