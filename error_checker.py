"""
The error_checker module exports the ErrorChecker class.

ErrorChecker class: Checks for various types of errors in the original XHAL code. Has options to report them to the
console and/or a generated error log, stored in the error_logs file.
"""
import datetime as dt
import re
import config
import os

# TODO: A warning about how floating-point-style symbols probably aren't meant to be symbols and may instead mean to be
#  non-symbol address values.

# TODO: Currently only checks if jump portion is invalid OR blank. Should separate the two into two errors, ideally. Meh

# Initialize a global variable to hold the error file name.
FILENAME = "default_filename.txt"

# Initialize dictionary of illegal (reserved) labels.
illegal_labels = {
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


def create_error_file(io_file):
    # Below lines generate a random error file name based on the current date and time.
    # Date-time formatting idea from
    # https://stackoverflow.com/questions/10501247/best-way-to-generate-random-file-names-in-python
    # and relative file directory code from
    # https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python

    base_filename = "error_log"
    file_name_suffix = dt.datetime.now().strftime("%y%m%d_%H%M%S") + ".txt"

    file_path = os.path.abspath(__file__)
    file_dir = os.path.split(file_path)[0] + '/' 'error_logs' + '/' + base_filename + '_' \
        + io_file + '_' + file_name_suffix

    # Set the module-scope error output filename
    global FILENAME
    FILENAME = file_dir
    return FILENAME


def write_error(error_line, error_content):
    if config.PRINT_ERRORS_TO_CONSOLE:
        print(f"\n##########\n\nERROR, line {error_line}: {error_content}\n\n##########\n")
    if config.WRITE_ERRORS_TO_LOG:
        error_file = open(FILENAME, "a")
        error_file.write(f"\n##########\n\nERROR, line {error_line}: {error_content}\n\n##########\n")


def write_warning(warning_line, warning_content):
    if config.PRINT_ERRORS_TO_CONSOLE:
        print(f"\n!!!!!!!!!!\n\nWARNING, line {warning_line}: {warning_content}\n\n!!!!!!!!!!\n")
    if config.WRITE_ERRORS_TO_LOG:
        error_file = open(FILENAME, "a")
        error_file.write(f"\n!!!!!!!!!!\n\nWarning, line {warning_line}: {warning_content}\n\n!!!!!!!!!!\n")


def check_a_type_int_command(command, line):
    print(f"Error=checking address: {command}")
    if len(command) == 0:
        write_error(line, "Missing value for address field in A-Type instruction.")
        return True

    if command[0] == "-":
        write_error(line, "Address field in A-Type instruction is negative. A-Type instructions "
                          "require non-negative 15-bit integers.")
        return True
    # If the function does not find an error, return false.
    return False


def check_a_type_bin_command(command, line):
    try:
        # String to binary translation from https://www.geeksforgeeks.org/python-convert-string-to-binary/
        binary_code = bin(int(command)).replace("0b", "")
        print(f"Error-checker binary code: {binary_code}")

        if len(binary_code) > 15:
            write_error(line, "Address field in A-Type instruction is over 15 bits long. A-Type instructions "
                              "require non-negative 15-bit integers.")
            return True
    except ValueError:
        write_error(line, "Address field in A-Type instruction is not translatable to binary. A-Type "
                          "instructions require non-negative 15-bit integers.")
        return True

    # If the function does not find an error, return false.
    return False


def record_c_type_dest_error(line):
    write_error(line, "A destination for C-Type instruction was detected, but it is not one of the supported "
                      "mnemonics.")


def record_c_type_comp_error(line):
    write_error(line, "The computation portion of C-Type instruction is either missing or is not one of the "
                      "supported mnemonics.")


def record_c_type_jump_error(line):
    write_error(line, "A jump for C-Type instruction was detected, but it is not one of the supported "
                      "mnemonics.")


def check_illegal_symbol_error(label_content, line):
    if label_content in illegal_labels:
        write_error(line, f"{label_content} is an illegal symbol name; label is in the reserved labels list.")
        return True
    else:
        return False


def check_l_type_text_after_paren_error(label_command, line):
    # Idea for detecting comments from
    # https://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
    regex_post_paren = re.compile(r'(\)[\S]+)')
    post_paren_text = regex_post_paren.search(label_command.replace(" ", ""))

    # If what is matched is anything but '//' to indicate the start of a comment, record the error and return True.
    if post_paren_text is not None:
        head, sep, tail = post_paren_text[0].partition('//')
        if tail is "" and "//" not in post_paren_text[0]:
            write_error(line, f"{label_command} has non-comment, non-blank text after the closing parenthesis.")
            return True
    else:
        return False


def record_symbol_redefinition_error(symbol, line, original_label_ROM_add):
    write_error(line, f"{symbol} redefines a previously defined symbol as a different ROM location. The "
                      f"original symbol's ROM address is {original_label_ROM_add}.")


def record_symbol_redefinition_warning(symbol, line, ROM_add):
    write_warning(line, f"{symbol} redefines a previously defined symbol. The ROM locations are the "
                        f"same, but this was likely unintended. The ROM address for both symbols is "
                        f"{ROM_add}.")
