## 2. Examine Item Data ##

<h3 style="font-size:18px">2.1 Summary</h3>

<h3 style="font-size:18px">2.2 Coding Reflection</h3>
<p>

Before we proceed to extract the price history of all the necessary items, it is important to examine the dataset that was retrieved. I will attempt to summarize the important categorizations of skins below, but if you require further information, it can be found in the wiki page [here](https://counterstrike.fandom.com/wiki/Skins). Feel free to skip if you have some background on this.

<details>
<summary><b>2.2.1 CS:GO Skin Categorizations</b> <br>[Expand if required]</summary>

- Skin Grades - denotes rarity of skins with 7 main grade categories:
    |    Categories    |              Grades              |
    |------------------|----------------------------------|
    | Common           | Consumer Grade, Base Grade       |
    | Uncommon         | Industrial Grade                 |
    | Rare             | Mil-Spec, High Grade             |
    | Mythical         | Restricted, Remarkable           |
    | Legendary        | Classified, Exotic               |
    | Ancient          | Covert, Extraordinary            |
    | Exceedingly Rare | Rare Special (★), Knives, Gloves |

- Skin Quality - identification or modification to skin’s appearances:

    a.&ensp;Rare Special (★): extra identification on gloves and knives.<br>
    b.&ensp;StatTrak™: track and display number of kills secured with the weapon.<br>
    c.&ensp;Souvenir: items obtained from souvenir packages dropped during major events, often containing stickers related to the event.<br>

- Skin Properties - simulates randomized condition on the skin with 5 broad categories. Each categories contains a range of float value that denotes the worn level of the skin, with 0 being the best. This affects appearances:

    a.&ensp;Factory New (0.00-0.07)<br>
    b.&ensp;Minimal Wear (0.07-0.15)<br>
    c.&ensp;Field-Tested (0.15-0.37)<br>
    d.&ensp;Well Worn (0.37-0.44)<br>
    e.&ensp;Battle-Scarred (0.44-1.00)
</details>
<br>

**2.2.2 Data Exploration (Descriptive Statistics)**
<br>
When exploring data with pandas, there are a few functions/attributes that are useful. 

```python
df.shape # allows one to find out the size of the data
df.info() # allows one to check the column names, data types, and potential na values
df.head() # allows one to see the first 5 rows of data
df.iloc[x:y] # allows us to see rows of data specfied (x and y being the starting row and ending row respectively)
df.describe(include="all") # allows us to see a descriptive statistics for the whole data set, including non-numeric columns
```

- Challenge - Limitations of API<br>
    While exploring the data with `df.iloc[selected_rows:selected_columns]`, I realized that some skins contained less than 5 of its skin properties. As mentioned, CS:GO skins has 5 skin properties. For example, "AK-47 | Fire Serpent" only comprises Field-Tested, Well-Worn, and Battle-Scarred. After further Google searches, I found out that the API only returns items that currently has listings on the market, hence not all the weapon skins' properties are included.

    This made me realized 2 limitations of the data:<br>
    1.&ensp;There will be more than 1 item without the their full set of skin properties.<br> 
    2.&ensp;There will be missing items, with all 5 skin properties not currently in market.

    **Solutions**<br>
    For limitation 1, it is possible to get the the data with data transformation. 

    For limitation 2, I sourced the data from [Counter Strike Fandom Website](https://counterstrike.fandom.com/wiki/Skins/List). Excel's Power Query was utilized for data extraction and transformation.
