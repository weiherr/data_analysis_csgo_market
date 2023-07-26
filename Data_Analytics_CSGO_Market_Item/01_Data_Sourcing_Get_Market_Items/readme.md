## 1. Get All Item ##

<h3 style="font-size:18px">1.1 Summary</h3>

Sourced data from STEAM Market's API using `urllib` and `requests` library, along with `time` to limit put pause to the code if it reaches the API call threshold set by STEAM. Data is then processed through accessing different data types (e.g. `JSON`, `dictionary`, `list`), using `pandas`' DataFrame to save as a csv file.

<h3 style="font-size:18px">1.2 Code/Notebook Link</h3>

The github depository link for the code related to this section is located [here](https://github.com/weiherr/data_analysis_csgo_market/blob/main/Data_Analytics_CSGO_Market_Item/01_Data_Sourcing_Get_Market_Items/01%20get_item_list.py).

<h3 style="font-size:18px">1.3 Coding Reflection</h3>

As this is the start of my "bigger" personal coding/data analytics project, I will be documenting the challenges that I have faced whilst coding.

- Challenge 1 - No Official Guideline on Steam Market API
    
    While Steam provided an official guideline for its API, it does not contain the documentation on the APIs to extract steam community market data.
    
    **Solution and other interesting find:**<br>Google is my best friend. The answer to this problem is based on the 2 links below.
    - <a href="https://steamcommunity.com/discussions/forum/7/1327844097128704472/?l=english">Steam Community Discussion Forum Link</a>
    - <a href="https://stackoverflow.com/questions/26170185/steam-market-api#">StackOverflow (Steam Market API) Link</a>

    While the links are sufficient to continue my project, the answers only pointed out the correct API links. It does not tell us how these links were discovered. There were many queries online but there were no satisfactory replies. So after spending a hefty amount of time searching for answers, I decided to test my searching skills in the Chrome's inspect panel despite not having too much knowledge in Javascript. Coding logics are not too different between each language.

    So after digging through the multiple tabs, I managed to stumble across the application tab where you can find multiple Javascript files that contain many functions involving `'GET'` HTTP request methods, which is how API works. `Pricehistory` (which is used to pull individual item's sales history) is one of the many methods that you can find by searching for `https://steamcommunity.com/market/` in the `.js` pages. However, I have yet to explore further on this. These links might enable you to get data on your own without going through 3rd party API applications if you are into cost savings.

    CURIOSITY POTENTIALLY SAVED OUR WALLET!

- ​Challenge 2 - Dealing with Error Codes due to HTTP Status Code and Nature of Data Requested

    There are 2 scenarios that arose from the retrieval of data across multiple get requests:

    1. HTTP status code of 429 as there were too many requests to the server. Steam has its own limitation to requests over time. <br>
    **Solution:**<br>`time.sleep` function to delay calls to the API, circumventing the limitation.

    2. There could be 0 data retrieved while HTTP status code is 200, either all data has been accessed or that the server just returned nothing (happens occasionally). As my code checks for len of the json data, with no data, the function will throw an error. <br>
    **Solution:** `try-exception` error handling to allow another set of code to be run when the error is met, circumventing interruption to runs.

    With the problems addressed, it allowed me to complete the code to extract data from the Steam's market API.