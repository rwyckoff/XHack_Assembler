"""
The error_checker module exports the ErrorChecker class.

ErrorChecker class: Checks for various types of errors in the original XHAL code. Has options to report them to the
console and/or a generated error log, stored in the error_logs file.
"""
import re
import datetime as dt


class ErrorChecker:

    def __init__(self, print_to_console, write_to_log):
        self.print_to_console = print_to_console
        self.write_to_log = write_to_log

        # Date-time formatting idea from
        # https://stackoverflow.com/questions/10501247/best-way-to-generate-random-file-names-in-python
        error_log_path = r"C:/Users/Robert Sirois/Dropbox/Shpob Storage/School/Compiler Design/Projects/Project One/" \
                         r"Robert_Wyckoff_PJ01_XHack/error_logs/"
        base_filename = "error_log"
        file_name_suffix = dt.datetime.now().strftime("%y%m%d_%H%M%S")
        self.date_time_filename = "_".join([error_log_path, base_filename, file_name_suffix])

    def write_error(self, error_line, error_content):
        if self.print_to_console:
            print(f"\n##########\n\nERROR, line {error_line}: {error_content}\n\n##########\n")
        if self.write_to_log:
            error_file = open(self.date_time_filename, "a")
            error_file.write(f"\n##########\n\nERROR, line {error_line}: {error_content}\n\n##########\n")

    def check_a_type_command(self, command, line):
        print(f"Address: {command}")
        if len(command) == 0:
            self.write_error(line, "Missing value for address field in an A-Type instruction.")

        if len(command) > 15:
            pass
