import shlex
import subprocess
import sys, os

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.logger import setup_logger


logger = setup_logger(__name__)
test_cases = [
    (
        "--files economic1.csv economic2.csv",
        "    country               gdp\n"\
        "--  --------------  ---------\n"\
        " 1  United States   23923.7\n"\
        " 2  China           17810.3\n"
        " 3  Japan            4467\n"\
        " 4  Germany          4138.33\n"\
        " 5  India            3423.67\n"\
        " 6  United Kingdom   3113.33\n"\
        " 7  France           2834.67\n"\
        " 8  Canada           2096.33\n"\
        " 9  Russia           2077.67\n"\
        "10  Italy            2042\n"\
        "11  Brazil           1900.67\n"\
        "12  South Korea      1727.33\n"\
        "13  Australia        1637\n"\
        "14  Spain            1409.33\n"\
        "15  Mexico           1392.67\n"\
        "16  Indonesia        1274.33\n"\
        "17  Saudi Arabia     1016.33\n"\
        "18  Netherlands      1006\n"\
        "19  Turkey            927.333\n"\
        "20  Switzerland       845"
    ),
    (
        "--files economic1.csv economic2.csv --report average-unemployment",
        "    country           unemployment\n"\
        "--  --------------  --------------\n"\
        " 1  Spain                 13.2\n"\
        " 2  Turkey                10.6\n"\
        " 3  Brazil                10.3333\n"\
        " 4  Italy                  8.43333\n"\
        " 5  India                  7.73333\n"\
        " 6  France                 7.46667\n"\
        " 7  Canada                 6.03333\n"\
        " 8  Saudi Arabia           5.83333\n"\
        " 9  Indonesia              5.7\n"\
        "10  China                  5.3\n"\
        "11  Switzerland            4.46667\n"\
        "12  Russia                 4.36667\n"\
        "13  United States          4.2\n"\
        "14  United Kingdom         4.2\n"\
        "15  Australia              4.16667\n"\
        "16  Netherlands            3.63333\n"\
        "17  Mexico                 3.43333\n"\
        "18  Germany                3.23333\n"\
        "19  South Korea            3.2\n"\
        "20  Japan                  2.6"
    ),
    (
        "--report average-unemployment", ""
    ),
    (
        "--files economic1.csv economic2.csv --report dispersion-gdp",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: argument --report: Incorrect parameter report: dispersion-gdp. Fuction dispersion is not allowed. Allowed functions: ['average', 'cumulative', 'maximum', 'minimum']"
    ),
    (
        "--files \"Life expectancy.csv\" --report average-gdp",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: Parameter gdp not found in csv. Try another parameter for report `average-[parameter]` from: ['country', 'Year', 'Life expectancy']"
    ),
    (
        "--files \"Life expectancy.csv\" --report average-",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: argument --report: Incorrect parameter report: average-. Missed part after or before separator `-`"
    ),
    (
        "--files \"Life expectance.csv\" --report \"average-Life expectancy\"",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: argument --files: can't open 'Life expectance.csv': [Errno 2] No such file or directory: 'Life expectance.csv'"
    ),
    (
        "--files economic1.csv economic3.txt --report average-gdp",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: argument --files: Invalid file format: economic3.txt"
    ),
    #NB! Create `economic4.csv` and remove read rights from current user, otherwise this next test will be fail:
    (
        "--files economic4.csv --report average-gdp",
        "usage: main.py [-h] [--files [FILES ...]] [--report REPORT]\n"\
        "main.py: error: argument --files: can't open 'economic4.csv': [Errno 13] Permission denied: 'economic4.csv'"
    )
]


@pytest.fixture
def user_inputs(request):
    files = filter(lambda x: x, [
        file.removesuffix(",").rstrip()
            for file in request.config.getoption("--files").split(" ")
        ]) if request.config.getoption("--files") \
    else None

    report = request.config.getoption("--report")
    return files, report


def test_unbroken_main(user_inputs):
    """
    Test crash the tool
    """
    files, report = user_inputs
    python_path = "\\".join((os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "venv\\Scripts\\python.exe"))
    command = [python_path, "./src/main.py"]

    if files:
        command.append("--files")
        command.extend(files)

    if report:
        command.append("--report")
        command.append(report)

    process = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    expected_output = process.stdout
    if files:
        assert expected_output, Exception(process.stderr)


@pytest.mark.parametrize("command_params, expected_output", test_cases)
def test_report_output(capsys, command_params: str, expected_output: str):
    """
    Test cases
    """
    python_path = "\\".join((os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "venv\\Scripts\\python.exe"))
    command = [python_path, "./src/main.py"]

    process = subprocess.run(
        command + shlex.split(command_params),
        capture_output=True,
        text=True
    )
    output = process.stdout + " " + process.stderr
    assert expected_output in output