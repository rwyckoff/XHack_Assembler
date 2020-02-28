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
    print(parser.current_command)

