Этот инструмент позволяет выводить сводную информацию в стандартный поток вывода в табличной форме для определенного столбца [`parameter`], 
содержащегося в `source`, путем применения математической операции к данным, собранным для каждой страны. В качестве источника данных 
используются CSV-файлы.

Математическая операция [`function`] может быть задана одним из следующих значений: [`average`, `cumulative`, `maximum`, `minimum`]

> [!WARNING]
> Данный инструмент работает только с CSV-файлами, для открытия которых пользователю, запускающему инструмент, требуются достаточные права
на чтение.
> Названия столбцов должны начинаться только с символов латинского алфавита или арабских цифр. Если это не так, следует учитывать это при 
установке параметра `parameter` и в этом случае пропускать эти символы.
> Обязательными столбцами в каждом CSV-файле являются `country` и [`parameter`]. Где `parameter` — это имя столбца, данные которого будут 
применяться к математической операции `function`. Значение по умолчанию для `parameter` — `gdp`. Если вы хотите установить другое значение, 
убедитесь, что желаемое значение `parameter` существует как название столбца в файле, который вы передаёте в команде. Значение по умолчанию 
для `function` — `average`. Выше вы можете посмотреть допустимые значения для `function`.
> Тип данных для столбца `parameter` должен быть десятичным числом. В противном случае инструмент пропустит эти данные. Если в результате 
поиска по стране вы получаете значение NaN, это означает, что данные имеют тип, который невозможно преобразовать в десятичное число.


Пример:

python ./src/main.py --files csv_file_1.csv csv_file_2.csv ... --report [function]-[parameter]

Для работы с этим инструментом вы можете использовать примеры CSV-файлов, расположенные в корне проекта:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/csv-files-list.PNG?raw=true)


Более наглядный пример:

У вас есть файл `economic1.csv` со слудующим содержимым:

```text
country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
United States,2022,23315,2.1,8.0,3.6,338,North America
...
Australia,2023,1693,2.1,5.2,3.7,26,Oceania
Australia,2022,1675,3.7,6.6,3.7,26,Oceania
Australia,2021,1543,1.6,2.9,5.1,26,Oceania
```

Как вы видите, он содержит столбец `country`. Вы можете передавать любое название стобца, чьи данные могут быть преобразованы в десятичное
число. И в этом файле это столбцы: `year`, `gdp`, `gdp_growwth`, `inflation`, `unemployment`, `population`.

Итак, предположим, что вас интересует вычисление максимального уровня безработицы за весь расчетный период времени, указанный в этом CSV-файле. 
Тогда, команда для этой цели будет выглядеть следующим образом:


```bash
python.exe ./src/main.py --files economic1.csv --report maximum-unemployment
```

Тогда вывод будет выглядеть так:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-1-trial.PNG?raw=true)


Безусловно, вы можете передавать несколько файлов в параметр`files`, и, тогда инструмент объединит
все результаты по совокупности всех переданных файлов:


```bash
python.exe ./src/main.py --files economic1.csv economic2.csv --report maximum-unemployment
```

Вывод:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-2-trial.PNG?raw=true)


Если вы попытаетесь запустить команду, указав параметр столбца `parameter`, содержащий данные, которые преобразовать в десятичное число будет
невозможно, например:


```bash
python.exe ./src/main.py --files economic1.csv economic2.csv --report average-country
```

То вы получите несопоставимые реузльтаты с NaN:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-3-trial.PNG?raw=true)


> [!WARNING]
> Для работы инструмента необходимо установить Python версии 3.13.5 или более поздней. Более ранние версии могут привести к сбоям в работе инструмента.
> Кроме того, перед использованием активируйте виртуальную среду и установите зависимости:


Unix\*
------


```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

\*Для платформы POSIX вы можете найти специальную команду для активации виртуальной среды здесь:[https://docs.python.org/3/library/venv.html]


```bash
pip install -r requirements.txt
```

Windows
-------

```bash
python -m venv venv
```

```bash
venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

Конечно, вы можете просто установить зависимости глобально:
-----------------------------------------------------------

```bash
pip install -r requirements.txt
```

-----
Тесты
-----

Эти тесты охватывают все возможные результаты в отношении их состава.

```bash
pytest --log-cli-level=INFO -v src/tests/tests.py --files=[FILES ...] --report=[average, cumulative, maximum, minimum]-parameter
```