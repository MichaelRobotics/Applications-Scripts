from Filters.log_generator import LogGenerator
from Filters.log_comparer import Comparer
import pytest

def test_check_text_in_file():
    with open(LogGenerator._log_filter("/home/laptopdev/logo_robotthree.txt"), 'r') as file:  # replace 'output_file' with your file path
        data = file.read()
    with open('fleetlogbuffile.txt', 'r') as file:  # replace 'specific_file' with the path to the file containing the text you want to check
        specific_text = file.read()
    assert specific_text == data


