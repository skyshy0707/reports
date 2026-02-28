import argparse
import csv
import re

from core import operations
from core.common_types import Tuple
from core.logger import setup_logger


logger = setup_logger(__name__)

class DEFAULT:

    report = "average-gdp"

def clean_column(column: str):
    i = 0
    for s in column:
        if re.match(r'^[\S]', s) and not re.match(r'^[A-Za-z0-9]', s):
            i += 1
        else:
            break
    column = column[i:]
    return column

def files(value: str) -> str:
    
    if not value.endswith("csv"):
        raise argparse.ArgumentTypeError(f"Invalid file format: {value}")
    
    reader = argparse.FileType('r')
    try:
        return reader(value)
    except argparse.ArgumentTypeError as e:
        raise argparse.ArgumentTypeError(e)

def report(value: str) -> Tuple[str]:
    try:
        function, parameter  = value.split("-")
    except AttributeError:
        raise argparse.ArgumentTypeError(
            f"Incorrect value: {value}. "
            "You should pass report parameter as template: function-parameter. "
            f"For example: {DEFAULT.report}"
        )
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Incorrect value: {value}. "
            "Parameter report should fit template: `function-parameter` and have correct separator `-`. "
            f"For example: {DEFAULT.report}"
        )
    
    if function not in operations.__all__:
        raise argparse.ArgumentTypeError(
            f"Incorrect parameter report: {value}. "
            f"Fuction {function} is not allowed. Allowed functions: {list(operations.__all__.keys())}"
        )
    

    if not all((function, parameter)):
        raise argparse.ArgumentTypeError(f"Incorrect parameter report: {value}. Missed part after or before separator `-`")

    return function, parameter

def cross_validation(parser: argparse.ArgumentParser) -> Tuple[str]:
    args = parser.parse_args()
    files = args.files
    function, parameter = args.report

    files_ = []
    for file in files: 
        reader = csv.DictReader(file, dialect='excel', skipinitialspace=True, quotechar='"')

        reader.fieldnames = [clean_column(field) for field in reader.fieldnames]
        if "country" not in reader.fieldnames:
            parser.error("Location key `country` not found in csv. Invalid csv report")
        if parameter not in reader.fieldnames:
            parser.error( 
                f"Parameter {parameter} not found in csv. "\
                f"Try another parameter for report `{function}-[parameter]` from: {reader.fieldnames}"
            )
        files_.append(reader)
            
    return files_, (function, parameter)