This tool allows you to output summary information to stdout in tabular form for a specific column [`parameter`] contained 
in the `source` by applying a `mathematical operation` to the data collected for each country. CSV files serve as the data source.

The `mathematical operation` [`function`] can be set to one of the following: [`average`, `cumulative`, `maximum`, `minimum`]

> [!WARNING]
>> The tool only works with csv files that require sufficient rights for the user running the tool to open them.

>> Column names should start with latin alphabet symbols or arabic numbers only. Double quotes are allowed. Otherwise, take note of other 
characters when setting the parameter `parameter` and omit them.

>> Required columns in every csv-file are `country`, [`parameter`]. Where `parameter` is the name of the column whose data will be applied 
to the mathematical operation `function`. Default value for `parameter` is `gdp`. If you want to set the another one you should make sure
that desirable `parameter` is exist as column name is in the file passed to the command. Default value for `function` is `average`. Above,
you have seen allowed values for `function`.

>> Data type for the `parameter` column should be a decimal number. Otherwise, the tool will skip these data. If you receive a nan value in
your result for a country, this means the data have type that cannot be converted to a decimal number.


Example:

python ./src/main.py --files csv_file_1.csv csv_file_2.csv ... --report [function]-[parameter]

To play with this tool, you can use the sample CSV files located in the root of the project:
![alt text](https://github.com/skyshy0707/reports/blob/master/images/csv-files-list.PNG?raw=true)


A more live example:

You have csv-file named `economic1.csv` with next content:

```text
country,year,gdp,gdp_growth,inflation,unemployment,population,continent
United States,2023,25462,2.1,3.4,3.7,339,North America
United States,2022,23315,2.1,8.0,3.6,338,North America
...
Australia,2023,1693,2.1,5.2,3.7,26,Oceania
Australia,2022,1675,3.7,6.6,3.7,26,Oceania
Australia,2021,1543,1.6,2.9,5.1,26,Oceania
```

As you have seen, it have column `country`. You can use any column whose data can be converted to decimal numbers. And these columns are
`year`, `gdp`, `gdp_growwth`, `inflation`, `unemployment`, `population` in this csv-file.

So, let assume that you are interested in compute maximum unemployment for all estimated time of this csv. Then command for this purpose
will be as:


```bash
python.exe ./src/main.py --files economic1.csv --report maximum-unemployment
```

Then output will be look like:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-1-trial.PNG?raw=true)


Of course you can set few files in `files` parameter and then the tool unite all results:


```bash
python.exe ./src/main.py --files economic1.csv economic2.csv --report maximum-unemployment
```

Output:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-2-trial.PNG?raw=true)


If you try to set column with non-converted-to-decimal data as `parameter`, for example:


```bash
python.exe ./src/main.py --files economic1.csv economic2.csv --report average-country
```

Then you have received nan results as:

![alt text](https://github.com/skyshy0707/reports/blob/master/images/output-3-trial.PNG?raw=true)


> [!WARNING]
> You have to install python version 3.13.5 or later. Earlier versions may cause the tool to malfunction.
> Also, before you use, activate virtual environment and install dependencies:


Unix\*
------


```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

\*For POSIX platform, you can find specific command to activate virtual environment here:[https://docs.python.org/3/library/venv.html]


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

Of course, you can just install dependencies globaly:

```bash
pip install -r requirements.txt
```

-----
Tests
-----

These tests cover all possible outputs regarding their composition.

```bash
pytest --log-cli-level=INFO -v src/tests/tests.py --files=[FILES ...] --report=[average, cumulative, maximum, minimum]-parameter
```

Example:

```bash
pytest --log-cli-level=INFO -v src/tests/tests.py --files="economic1.csv economic2.csv"
```