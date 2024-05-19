from Filters.log_generator import LogGenerator
import os

# Specify the filename
log_name = 'fleetlogbuffile.txt'

current_script_directory = os.path.dirname(os.path.abspath(__file__))
full_file_path = os.path.join(current_script_directory, log_name)


def test_check_text_in_file():
    with open(LogGenerator._log_filter('/home/laptopdev/logo_robotthree.txt'), 'r') as file:  # replace 'output_file' with your file path
        data = file.read()
    with open(full_file_path, 'r') as file:  # replace 'specific_file' with the path to the file containing the text you want to check
        specific_text = file.read()
    assert specific_text == data


