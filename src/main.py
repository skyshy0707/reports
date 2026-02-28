import argparse

from core import validators
from core.collect import get_results, represent_results, collect_results
from core.common_types import Tuple
from core.logger import setup_logger


logger = setup_logger(__file__)
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--files', nargs="*", help="file list", type=validators.files)
parser.add_argument('--report', help="report type", type=validators.report, default=validators.DEFAULT.report)


def main(files: str, report: Tuple[str]) -> None:
    function, parameter = report
    if files:
        represent_results(
            collect_results(
                [get_results(file, parameter, function) for file in files], 
                function=function
            ),
            parameter
        )

if __name__ == "__main__":
    files, report = validators.cross_validation(parser)
    main(files, report)