from Filters.log_generator import LogGenerator
import os

# Specify the filename 1
log_name = 'fleetlogbuffile.txt'
current_script_directory = os.path.dirname(os.path.abspath(__file__))
full_file_path = os.path.join(current_script_directory, log_name)

# Specify the filename 2

log_name_two = 'logo_robotthree.txt'
current_script_directory_two = os.path.dirname(os.path.abspath(__file__))
full_file_path_two = os.path.join(current_script_directory_two, log_name_two)


def test_check_text_in_file():
    with open(LogGenerator._log_filter(full_file_path_two), 'r') as file:  # replace 'output_file' with your file path
        data = file.read()
    with open(full_file_path, 'r') as file:  # replace 'specific_file' with the path to the file containing the text you want to check
        specific_text = file.read()
    assert specific_text == data


