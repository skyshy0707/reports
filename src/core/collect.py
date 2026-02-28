"""
Collect from csv-objects represented as csv.DictReader data and apply
passed mathmatical function
"""

import tabulate

from core.common_types import Callable, Dict, Iterator
from core.logger import setup_logger
from core.operations import average, cumulative, maximum, minimum


logger = setup_logger(__name__)

location_key = "country"


def aggregate_result(collect_func: Callable) -> Dict:
    """
    EN: Applies a function `function` to `results` grouped by country

    RU: Применяет функцию `function` к сгруппированным результатам `results` по странам
    """

    def _aggregate(results: Iterator, parameter: str=None, function: str="average"):

        aggregator = globals().get(function)
        results = collect_func(results, parameter)

        for result in results:
            results.update({
                result: aggregator(results.get(result))
            })
        return results
    
    return _aggregate


@aggregate_result
def collect_results(data: Iterator, parameter: str=None, function: str="average") -> Dict:
    """
    EN: Groups the given list of dictionaries results `data` by `parameter` into lists of countries 
    and applies the function `function` to them 
    the `function`.
    
    RU: Группирует переданные в виде списка словарей результаты `data` по `parameter` в списки по
    странам и применяет к ним функцию `function`.
    """
    results = {}
    for row in data:
        if not parameter and isinstance(row, dict):
            for prop, value in row.items():
                if prop not in results:
                    results[prop] = []
                results[prop].append(value)
            continue

        location = row.get(location_key)

        if location not in results:
            results[location] = []
        
        try:
            raw = row.get(parameter)
            value = float(raw)
        except ValueError:
            pass
        else:
            results[location].append(value)

    return results


def get_results(file: str, parameter: str, function: str="average") -> Dict:
    """ 
    EN: Gets the computed results for a `parameter` related to the single csv-file, taking into
    account the applied `function`.

    RU: Получает результаты вычислений по параметру `parameter` относящиеся к одному CSV-файлу 
    с учётом применения функции `function`.
    """
    try:
        results = collect_results(file, parameter, function)
    except Exception as e:
        message = f"Something went wrong. Details: {e}"
        logger.warning(message)
        raise Exception(message)
    return results


def represent_results(results: Dict, parameter: str) -> None:
    """
    EN: Outputs to the console the `results` for each country sorted in 
    descending order.

    RU: Выводит в консоль отсортированные в убывающем порядке результаты `results` 
    по каждой стране
    """

    results = sorted(results.items(), key=lambda result: 0 if str(result[1]) == 'nan' else result[1], reverse=True)
    print(tabulate.tabulate(
        results,
        headers=[location_key, parameter], 
        showindex=range(1, results.__len__() + 1)
    ))