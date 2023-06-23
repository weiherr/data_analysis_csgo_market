<a id="top"></a>
CS:GO Steam Market Analaysis
============================

## Python/Data Analytics Journey Content: ##
- [0 Sample](#sample)
- [1 Get All Item](#item-one)
- [2 Examine Item Data](#item-two)

<!-- headings -->
<a id="sample"></a>

## 0 Sample ##

<h3 style="font-size:18px">0.1 Skills Showcased</h3>
#Skill1 &ensp; #Skill2

<h3 style="font-size:18px">0.2 Coding Journey</h3>
<details>
<summary>[Expand]</summary>

First paragraph.

- Challenge 1 - Sample Challenge
    Sample para
    
    **Solution and Other Interesting Find**
    
    Sample para.
    - <a href="https://www.google.com">Google</a>
    - <a href="https://www.yahoo.com">Yahoo</a>

    Sample para. `CODE`

    Sample para.

    **EMPHASIS!**
    
    <details>
    <summary>[Expand for code]</summary>

    ```python
    print("Hello world!")
    ```
    </details>
<br>

- ​Challenge 2 - Sample Challenge
    Sample para

    1. Sample para. <br>
    **Solution:** `CODE` sample.

    2. Sample para. <br>
    **Solution:** `CODE` sample.

    Sample para.

    <details>
    <summary>[Expand for code]</summary>

    ```python
    print("Hello World Again!")
    ```
    </details>

[[back to top]](#top)
</details>

<a id="get-all-item"></a>

## 1 Get All Item ##

<h3 style="font-size:18px">1.1 Skills Showcased</h3>
#API &ensp; #HTML &ensp; #Python &ensp; #TryExceptionErrorHandling &ensp; #pandas &ensp; #urllib

<h3 style="font-size:18px">1.2 Coding Journey</h3>
<details>
<summary>[Expand]</summary>

As this is the start of my "bigger" personal coding/data analytics project, I will be documenting the challenges that I have faced whilst coding.

- Challenge 1 - No Official Guideline on Steam Market API
    
    While Steam provided an official guideline for its API, it does not contain the documentation on the APIs to extract steam community market data.
    
    **Solution and other interesting find:**<br>Google is my best friend. The answer to this problem is based on the 2 links below.
    - <a href="https://steamcommunity.com/discussions/forum/7/1327844097128704472/?l=english">Steam Community Discussion Forum Link</a>
    - <a href="https://stackoverflow.com/questions/26170185/steam-market-api#">StackOverflow (Steam Market API) Link</a>

    While the links are sufficient to continue my project, the answers only pointed out the correct API links. It does not tell us how these links were discovered. There were many queries online but there were no satisfactory replies. So after spending a hefty amount of time searching for answers, I decided to test my searching skills in the Chrome's inspect panel despite not having too much knowledge in Javascript. Coding logics are not too different between each language.

    So after digging through the multiple tabs, I managed to stumble across the application tab where you can find multiple Javascript files that contain many functions involving `'GET'` HTTP request methods, which is how API works. `Pricehistory` (which is used to pull individual item's sales history) is one of the many methods that you can find by searching for `https://steamcommunity.com/market/` in the `.js` pages. However, I have yet to explore further on this. These links might enable you to get data on your own without going through 3rd party API applications if you are into cost savings.

    **CURIOSITY POTENTIALLY SAVED OUR WALLET!**

    <details>
    <summary>[Expand for code]</summary>

    ```python
    ### ------------------------------ INITIALIZATION ------------------------------ ###
    BASE_URL = "https://steamcommunity.com/market/search/render/"
    url_values = {
        "appid": 730,
        "search_descriptions": 0,
        "sort_column": "name",
        "sort_dir": "asc",
        "norender": 1,
        "count": 100, # maximum data returned is cap at 100
        "start": 0,
        "currency": 11, # unused parameter as Steam PAI does not accept this
    }
    full_url = BASE_URL + "?" + urllib.parse.urlencode(url_values) 
    # print(full_url) # can print to see what is the link printed

    INCLUSION_LIST = ["classid", "instanceid", "tradable", "type", "market_name", "market_hash_name", "commodity"] # create a list for get_data function to determine which information to keep from the data retrieved

    DIR = "./data/item_list/" # directory to save the file
    now = dt.datetime.now() # get datetime information as file name
    extraction_start = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+"T"+str(now.hour).zfill(2)+""+str(now.minute).zfill(2)
    filename = extraction_start + "_trial_v3.csv"
    filedir = DIR + filename
    # print(filedir) # can print to see what is the file directory + name

    def get_data(json_response) -> list:
        '''
        Extract the data of json object (json key specific to this Steam API only) and returns a list of dictionary with the following keys:
        [data_start_value, classid, instanceid, tradable, skin_type, market_name, market_hash_name, commodity, timestamp]

        :json_response: json object from request.get(any_url).json()
        '''
        extracted_list = []
        try:
            json_length = len(json_response["results"])
        except TypeError:
            raise TypeError("There is no response from link although response.status_code == 200.") # occasionally the link returns no data eventhough status code is 200. this is catch the exception to the error
        else:
            for count, dict_item in enumerate(json_response["results"]):
                breakdown_item = {}
                breakdown_item["data_start_value"] = url_values["start"] + count
                for key in dict_item:
                    if key == "asset_description":
                        for internal_key in dict_item[key]:
                            if internal_key in INCLUSION_LIST:
                                if internal_key == "type":
                                    breakdown_item["skin_type"] = dict_item[key][internal_key]
                                else:
                                    breakdown_item[internal_key] = dict_item[key][internal_key]
                            else:
                                continue
                breakdown_item["timestamp"] = dt.datetime.now()
                extracted_list.append(breakdown_item)
            return extracted_list
    ```
    </details>
<br>

- ​Challenge 2 - Dealing with Error Codes due to HTTP Status Code and Nature of Data Requested

    There are 2 scenarios that arose from the retrieval of data across multiple get requests:

    1. HTTP status code of 429 as there were too many requests to the server. Steam has its own limitation to requests over time. <br>
    **Solution:**<br>`time.sleep` function to delay calls to the API, circumventing the limitation.

    2. There could be 0 data retrieved while HTTP status code is 200, either all data has been accessed or that the server just returned nothing (happens occasionally). As my code checks for len of the json data, with no data, the function will throw an error. <br>
    **Solution:** `try-exception` error handling to allow another set of code to be run when the error is met, circumventing interruption to runs.

    With the problems addressed, it allowed me to complete the code to extract data from the Steam's market API.

    <details>
    <summary>[Expand for code]</summary>

    ```python
    ### ---------------------- WHILE LOOP TO GET ALL DATA ---------------------- ###
    run_continues = True # for while loop
    non_processed_values = [] # capture url parameter's "start" value that had errors in processing
    data_list = [] # empty list to encapsulate all dictionaries of each item 
    extracted_data_empty_count = 0 # to count the number of times request returned as empty
    
    while run_continues:
        print(f"ITER START: {url_values['start']}") # track progress
        full_url = BASE_URL + "?" + urllib.parse.urlencode(url_values) # get new full url as url_value["start"] increases per iteration
        request = requests.get(full_url)
        print(f"Request status code: {request.status_code}") # track status code of requests.get
        if request.status_code == 200:
            response = request.json()
            try:
                extracted_data = get_data(response)
            except TypeError:
                non_processed_values.append(url_values["start"])
                print(f"Value {url_values['start']} not-processed. Total non-processed start values: {len(non_processed_values)}")
                url_values["start"] += 100
            else:
                if len(extracted_data) == 100: # check whether data is at its extraction max value, hence determining whether there are more data to be extracted
                    data_list = data_list + extracted_data
                    print(f"Data list has {len(data_list)} items. Wait 5 seconds for the next request.")
                    time.sleep(5)
                    extracted_data_empty_count = 0 # reset extracted_data_empty_count if the next try gets 100 data.
                    url_values["start"] += 100 # add value for next iteration
                elif len(extracted_data) == 0: # if no data is extracted, try 3 times before giving up. Pause 1 minute in between each try
                    extracted_data_empty_count += 1
                    print(f"There is no data from url_values['start'] = {url_values['start']}. Could be the end.\nTrying again in 1 minute.\nCurrent try: {extracted_data_empty_count}.")
                    time.sleep(60)
                    if extracted_data_empty_count == 3:
                        run_continues = False
                        print(f"Have tried {extracted_data_empty_count} times. Will stop now.")
                        print(f"Non-processed:\n{non_processed_values}")
                elif len(extracted_data) < 100: # if data is less than 100, might indicate that there is no more data to be extracted
                    data_list = data_list + extracted_data
                    print(f"Extracted data has < 100 items. Might be the end. Try the next 100.")
                    url_values["start"] += 100
        elif request.status_code != 200: # due various reasons, rest for 5 minutes to try to run again
            sleep_timer = 300
            print(f"Pause for {sleep_timer/60} minutes. Continue later.")
            time.sleep(sleep_timer)

    ### ---------------------- SAVE DATA TO A CSV FILE ---------------------- ###
    df = pd.DataFrame(data_list)
    df["duplicated"] = df["market_hash_name"].duplicated() # mark only duplicated ones as True
    df = df[df["duplicated"]==False]
    df = df.drop(columns=["duplicated"])
    df.to_csv(filedir, index=False)

    ### ----------- SAVE NON-PROCESSED URL_VALUE["start"] DATA TO A CSV FILE ----------- ###
    now = dt.datetime.now()
    extraction_end = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+"T"+str(now.hour).zfill(2)+""+str(now.minute).zfill(2)
    with open(DIR+"log/"+extraction_end+"_non_processed.txt", "w") as file:
        writer = csv.writer(file)
        writer.writerow(non_processed_values)
    ```
    </details>

- Challenge 3 - Limitations of API

    CS:GO skins has 5 skin properties which determined the quality of their appearances. They are categorized as Factory New, Minimal Wear, Field-Tested, Well Worn, and Battle-Scarred, in the order from best to worst. As the API only returns items that currently has listings on the market, not all the weapon skins' propeties are included. For example, "AK-47 | Fire Serpent" only comprises Battle-Scarred, Field-Tested and Well-Worn. 

[[back to top]](#top)
</details>

<a id="item_two"></a>

## 2 Examine Item Data ##

<h3 style="font-size:18px">2.1 Skills Showcased</h3>
#Skill1 &ensp; #Skill2

<h3 style="font-size:18px">2.2 Coding Journey</h3>
<details>
<summary>[Expand]</summary>
<p>
Before we proceed to extract the price history of all the necessary items, it is important to examine the dataset that was retrieved. I will attempt to summarize the important categorizations of skins below, but if you require further information, it can be found in the wiki page [here](https://counterstrike.fandom.com/wiki/Skins). Feel free to skip if you have some background on this.

<details>
<summary><b>2.2.1 CS:GO Skin Categorizations</b> [Expand]</summary>

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
    While exploring the data with `df.iloc[x:y]`, I realized that some skins contained less than 5 of its skin properties. As mentioned, CS:GO skins has 5 skin properties. For example, "AK-47 | Fire Serpent" only comprises Field-Tested, Well-Worn, and Battle-Scarred. After further Google searches, I found out that the API only returns items that currently has listings on the market, hence not all the weapon skins' properties are included.

    This made me realized 2 limitations of the data:<br>
    1.&ensp;There will be more than 1 item without the their full set of skin properties.<br> 
    2.&ensp;There will be missing items, with all 5 skin properties not currently in market.

    **Solution**<br>
    For limitation 1, it is possible to get the the data with data transformation. It will allow us to find out which are the missing data and fill them up (see 2.2.3). 

    However, for limitation 2, while it's possible to scrape data online, it is not the main purpose of this current project, thus I will be skipping to retrieve the items that do not even have 1 skin properties.

**2.2.3 Data Transformation**<br>
</p>

[[back to top]](#top)
</details>
