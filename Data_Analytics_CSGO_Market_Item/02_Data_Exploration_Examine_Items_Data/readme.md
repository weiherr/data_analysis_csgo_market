## 2. Examine Market Items Data ##

<h3 style="font-size:18px">2.1 Summary</h3>

Explored dataset with common `pandas` data exploration methods like `df.shape`, `df.info()`, `df.head()`, `df.describe(include="all")`. Drilled down data further through methods like `df.iloc`, `df.unique()`, conditional filtering and groupby to uncover details regarding the data to provide information for the next data cleaning/transformation step.

**Skills Showcased**: Python (pandas), Jupyter Notebook, Descriptive Statistics

<h3 style="font-size:18px">2.2 Code/Notebook Link</h3>

The github depository link for my code is located [here](https://github.com/weiherr/data_analysis_csgo_market/blob/main/Data_Analytics_CSGO_Market_Item/02_Data_Exploration_Examine_Items_Data/02%20data_exploration.ipynb). Please refer to the notebook for detailed analysis as the notebook tool is useful in explaining steps with visualization of data.

<h3 style="font-size:18px">2.3 Coding Reflection</h3>
<p>

1. **Nature of `df.describe()` Method**<br>
    While `df.descibe()` method is a very quick and useful way to get descriptive data from the dataframe, it is dependent on the datatype of each column. As we can see from the notebook, columns like "classid", as it is considered numeric datatype, we can see that the data behaves like an index/unique identifier for each item. Hence, it would be more useful to find out the unique values rather than its mean.

    While one can convert the datatype of classid to either string with `df["classid"].apply(lambda x: str(x))` or changing it to categorical by `pandas.Categorical()`, it will not be required if you are merely exploring data. It might be more useful to keep it numerical for easier sorting. 
     
    Hence, I chose to check for unique values of all columns in the next step instead.

2. **Limitation of API**<br>
    As discussed in the conclusion/findings section of the [jupyter notebook](https://github.com/weiherr/data_analysis_csgo_market/blob/main/Data_Analytics_CSGO_Market_Item/02_Data_Exploration_Examine_Items_Data/02%20data_exploration.ipynb), the API for this data's extraction only shows skins that are currently listed/available in the market. Hence, it will be important to generate all potential incomplete/missing skin names in the data cleaning/transformation section.

    If for any reason this data is required to be stored and kept updated, it will be helpful if a code could be written to take into account changes to existing skins' data and to append only new data.