## 3 Data Transformation ##

<h3 style="font-size:18px">3.1 Summary</h3>

Generated multiple categories through string manipulation of `market_hash_name` column for future analysis purposes, and creating entries for skins that do not have their full skin wear in the market data extracted. This is achieved by utilizing `groupby`, `merge`, `sort`, `ffill` (front-fill), `fillna` then `concat` pandas methods.

Utilized Excel's Power Query to extract and transform the remaining skin data that were absent in the extracted list from [Counter Strike Fandom Website](https://counterstrike.fandom.com/wiki/Skins/List). Made the assumption that each skin name should have 5 skin wear, and each skin name should have its StatTrak counterpart.

**Skills Showcased**: Python (pandas, String Manipulation), Power Query, M Language

<h3 style="font-size:18px">3.2 Code Link</h3>

The github depository link for my code is located [here](https://test.com).

<h3 style="font-size:18px">3.3 Coding Reflection</h3>

- Solution 1: To address the incomplete set of extracted data<br>
    Besides using the `apply` method to perform string manipulation through custom written functions, I decided to use the `groupby().count()` method to find out the skins that do not have their complete skin wear sets. I drew inspiration from `SQL` and found this method easiest to understand, as compared to the `iterrow`/`apply` method.
    
    Through similar string manipulation techniques, I filled up the necessary columns, along with other `pandas` methods like `sort`, `ffill` and `fillna`, which gave me easier options to handle missing data. The final result is then concatenated with the main table using `pd.concat`.

- Solution 2: To address the missing skins <br>
    While it is possible to utilize `requests` and `pandas` to perform cross-join functions with the data from the [Fandom]() website, I chose Power Query to showcase my data extraction and transformation skills with it. 