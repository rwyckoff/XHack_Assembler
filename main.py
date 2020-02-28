"""
The main XHack Assembler module drives the translation process from one XHAL file to one .hack pseudo-binary machine
language file.
"""

from sys import argv
from parser_module import Parser


parser = Parser(argv[1])
