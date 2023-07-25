import datetime as dt # get extraction start/end time for filename creation
import time # only use the sleep module to ensure that code rests before sending too many requests as Steam has a limit (occasionally returns http status code 429)
import requests # request from Steam API
import pandas as pd # create DataFrame
import urllib.parse #join and encode the API parameters to create a ASCII compliant url-link
import csv # use writerow function to write list into csv with each item as separate rows

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
extraction_start = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+"_"+str(now.hour).zfill(2)+""+str(now.minute).zfill(2)
filename = extraction_start + "_item_list.csv"
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
extraction_end = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+"_"+str(now.hour).zfill(2)+""+str(now.minute).zfill(2)
with open(DIR+"log/"+extraction_end+"_non_processed.txt", "w") as file:
    writer = csv.writer(file)
    writer.writerow(non_processed_values)