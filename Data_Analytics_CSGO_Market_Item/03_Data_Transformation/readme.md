## 3 Data Transformation ##

<h3 style="font-size:18px">3.1 Summary</h3>

Generated multiple categories through string manipulation of "market_hash_name", "skin_type" columns for future analysis purposes, and creating entries for skins that do not have their full skin wear in the market data extracted. This is achieved by utilizing `groupby`, `merge`, `sort`, `ffill` (front-fill), `fillna` then `concat` pandas methods.

Utilized Excel's Power Query to extract and transform the remaining skin data that were absent in the extracted list from [Counter Strike Fandom Website](https://counterstrike.fandom.com/wiki/Skins/List). This data is then merged with the original dataset. Similar string manipulation functions are then applied to this new data to obtain a comparatively more complete data.

**Skills Showcased**: Python (pandas, String Manipulation, List Comprehension, Functions), Power Query, M Language

<h3 style="font-size:18px">3.2 Code Link</h3>

The github depository link for my code is located [here](https://test.com).

<h3 style="font-size:18px">3.3 Coding Reflection</h3>

1. **Solutions to Problems Highlighted during Data Exploration**
    - Solution 1: To address the incomplete set of extracted data<br>
        Besides using the `apply` method to perform string manipulation through custom written functions, I decided to use the `groupby().count()` method to find out the skins that do not have their complete skin wear sets. I drew inspiration from `SQL` and found this method easiest to understand, as compared to the `iterrow`/`apply` method.
        
        Through similar string manipulation techniques, I filled up the necessary columns, along with other `pandas` methods like `sort`, `ffill` and `fillna`, which gave me easier options to handle missing data. The final result is then concatenated with the main table using `pd.concat`.

    - Solution 2: To address the missing skins <br>
        While it is possible to utilize `requests` and `pandas` to perform cross-join functions with the data from the [Fandom]() website, I chose Power Query to showcase my data extraction and transformation skills with it.

2. **Limitations of `.apply()` Method (Unexpected Discovery Whilst Doing Reflection)**

    In my data transformation section of the code, while I created a new column with both the `.apply()` method and List Comprehension (creating a list before turning it to a panda series) to showcase my knowledge and also applying a simpler solution, it dawned to me to actually find out which one is more effective in creating a new column.

    Another reason why list comprehension was used in this scenario was because it was easier to use an if-else clause through a list than the apply method. As seen in the code chunk below, the lambda function was required in addition to the `get_weapon_type` function for the apply method.

    A simple comparison would be to use the %time / %%time function inbuilt in Jupyter Notebook to measure time taken required for each of these different methods. The results as seen in my [Notebook]() is drastically favouring the list method. 
    
    So, through this little experimentation, I realized how `.apply()` method might be inferior to other solutions. While this method is taught in most courses, it is important to learn more about performance for real life big data situations. A [Medium article](https://towardsdatascience.com/avoiding-apply-ing-yourself-in-pandas-a6ade4569b7f) on this topic might be useful future reference. 

    ```python
    # creating "weapon_type" column with .apply method 
    df["weapon_type"] = df.apply(lambda row: "Not Weapon" if row["analysis_type"] == False else get_weapon_type(row["market_hash_name"]), axis=1)

    # with List Comprehension and converting list to Pandas Series
    analysis_list = df["analysis_type"].to_list()
    market_name_list = df["market_hash_name"].to_list()

    weapon_type_list = [get_weapon_type(market_name_list[iter]) if value == True else "Not Weapon" for iter, value in enumerate(analysis_list)]
    df["weapon_type"] = pd.Series(weapon_type_list)
    ```