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