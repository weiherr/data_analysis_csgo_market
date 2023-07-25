### -------------------- INITIALIZATION -------------------- ###
import pandas as pd
import numpy as np
df = pd.read_csv("./data/item_list/20230725_0741_item_list.csv")

### ----------------- FUNCTIONS --------------------- ###
def get_skin_name(input_string) -> str:
    skin_wear_list = [" (Factory New)", " (Minimal Wear)", " (Field-Tested)", " (Well-Worn)", " (Battle-Scarred)"]
    for skin_wear in skin_wear_list:
        if input_string.find(skin_wear) >= 0:
            slice_end = input_string.find(skin_wear)
            skin_name = input_string[0:slice_end]
            break
        else:
            skin_name = input_string
    return skin_name

def get_skin_type_category(input_string) -> str:
    string_word_list = input_string.split(" ")
    if "Music" in string_word_list:
        skin_type_category = " ".join(string_word_list[-2:])
    elif "Sniper" in string_word_list:
        skin_type_category = " ".join(string_word_list[-2:])
    else:    
        skin_type_category = string_word_list[-1]
    return skin_type_category

def get_totally_new_skin_type_cat(input_string) -> str:
    rifle = ["AUG","FAMAS","AK-47","M4A4","SG 553","Galil AR","M4A1-S"]
    machinegun = ["M249","Negev"]
    sniperrifle = ["SSG 08","G3SG1","SCAR-20","AWP"]
    shotgun = ["Sawed-Off","MAG-7","Nova","XM1014"]
    smg = ["P90","MP7","MP9","MP5-SD","UMP-45","MAC-10","PP-Bizon"]
    pistol = ["USP-S","Glock-18","P250","R8 Revolver","Dual Berettas","Five-SeveN","CZ75-Auto","Desert Eagle","Tec-9","P2000"]

    if input_string in rifle:
        return "Rifle"
    elif input_string in machinegun:
        return "Machinegun"
    elif input_string in sniperrifle:
        return "Sniper Rifle"
    elif input_string in shotgun:
        return "Shotgun"
    elif input_string in smg:
        return "SMG"
    elif input_string in pistol:
        return "Pistol"

def get_analysis_type(input_string) -> bool:
    analysis_type = ["Sniper Rifle", "Rifle", "SMG", "Shotgun", "Pistol", "Machinegun", "Knife", "Gloves"]
    if input_string in analysis_type:
        return True
    else:
        return False

def get_skin_grade(input_string) -> str:
    string_word_list = input_string.split(" ")
    if "StatTrak™" in string_word_list and "★" in string_word_list:
        skin_grade = " ".join(string_word_list[2:(len(string_word_list)-1)])
    elif ("StatTrak™" in string_word_list or "Souvenir" in string_word_list) and ("Sniper" in string_word_list or "Music" in string_word_list):
        skin_grade = " ".join(string_word_list[1:(len(string_word_list)-2)])
    elif "★" in string_word_list:
        skin_grade = " ".join(string_word_list[1:(len(string_word_list)-1)])
    elif "Souvenir" in string_word_list:
        skin_grade = " ".join(string_word_list[1:(len(string_word_list)-1)])
    elif "StatTrak™" in string_word_list:
        skin_grade = " ".join(string_word_list[1:(len(string_word_list)-1)])
    elif "Sniper" in input_string:
        skin_grade = " ".join(string_word_list[0:(len(string_word_list)-2)])
    elif "Music" in string_word_list:
        skin_grade = " ".join(string_word_list[0:(len(string_word_list)-2)])
    else:
        skin_grade = " ".join(string_word_list[0:(len(string_word_list)-1)])
    return skin_grade

def get_weapon_type(input_string) -> str:
    slice_end = input_string.find("|")
    if slice_end != -1:
        weapon_type = input_string[0:slice_end-1]
        if "★ StatTrak™" in input_string:
            weapon_type = weapon_type.replace("★ StatTrak™", "").strip()
        elif "StatTrak™" in input_string:
            weapon_type = weapon_type.replace("StatTrak™", "").strip()
        elif "Souvenir" in input_string:
            weapon_type = weapon_type.replace("Souvenir", "").strip()
        elif "★" in input_string:
            weapon_type = weapon_type.replace("★", "").strip()
    else:
        weapon_type = input_string
        if "★ StatTrak™" in input_string:
            weapon_type = weapon_type.replace("★ StatTrak™", "").strip()
        elif "StatTrak™" in input_string:
            weapon_type = weapon_type.replace("StatTrak™", "").strip()
        elif "Souvenir" in input_string:
            weapon_type = weapon_type.replace("Souvenir", "").strip()
        elif "★" in input_string:
            weapon_type = weapon_type.replace("★", "").strip()
    return weapon_type

def get_skin_wear(input_string) -> str:
    slice_start = input_string.rfind("(")
    slice_end = input_string.rfind(")")
    if slice_end != -1:
        if slice_start == slice_end:
            wear = "No Wear"
        else:
            wear = input_string[(slice_start+1):slice_end]
    else:
        wear = "No Skin Wear"
    return wear
    
def get_skin_quality(input_string) -> str:
    string_word_list = input_string.split(" ")
    if "Souvenir" in string_word_list:
        skin_type_category = string_word_list[0]
    elif "StatTrak™" in string_word_list and "Knife" in string_word_list:
        skin_type_category = string_word_list[1]
    elif "StatTrak™" in string_word_list:
        skin_type_category = string_word_list[0]
    else: 
        skin_type_category = "Regular"
    return skin_type_category

### ------------------ -DATA TRANSFORMATION ------------------- ###
### df.apply method
df["skin_name"] = df["market_hash_name"].apply(get_skin_name)
df["skin_grade"] = df["skin_type"].apply(get_skin_grade)
df["skin_type_category"] = df["skin_type"].apply(get_skin_type_category)
df["skin_quality"] = df["skin_type"].apply(get_skin_quality)
df["analysis_type"] = df["skin_type_category"].apply(get_analysis_type)

### list comprehension method
analysis_list = df["analysis_type"].to_list()
market_name_list = df["market_hash_name"].to_list()

weapon_type_list = [get_weapon_type(market_name_list[iter]) if value == True else "Not Weapon" for iter, value in enumerate(analysis_list)]
df["weapon_type"] = pd.Series(weapon_type_list)

skin_wear_list = [get_skin_wear(market_name_list[iter]) if value == True else "No Skin Wear" for iter, value in enumerate(analysis_list)]
df["skin_wear"] = pd.Series(skin_wear_list)
df = df.drop(columns="analysis_type")
# print(df.info())

### -------------------- GET SKIN NAME COUNT -------------------- ###
skin_name_count_df = df.groupby(["skin_name"])["skin_name"].count().rename("skin_name_count").reset_index()
df = df.merge(skin_name_count_df, how="left", on="skin_name", right_index=False)

incomplete_items_df = df[(df["skin_name_count"] < 5)&(df["skin_wear"]!="No Skin Wear")]
incomplete_items_df = incomplete_items_df.sort_values(["market_hash_name"])

### ----------- CREATE DF FOR NON-DOWNLOADED ITEMS ------------ ###
start_index_for_merge = len(df)

skin_wear_list = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]
missing_skin_list = list(incomplete_items_df["skin_name"].unique())

sample_list = [skin + " (" + skin_wear + ")" for skin_wear in skin_wear_list for skin in missing_skin_list]
full_incomplete_skin_name_df = pd.DataFrame(sample_list, columns=["skin_name_total"])

missing_item_df = pd.DataFrame(incomplete_items_df.merge(full_incomplete_skin_name_df, how="right", left_on="market_hash_name", right_on="skin_name_total", right_index=False, indicator=True).query('_merge=="right_only"')["skin_name_total"].rename("market_hash_name")).reset_index(drop=True)
missing_item_df["data_start_value"] = pd.Series([start_index_for_merge+iter for iter, value in enumerate(list(missing_item_df["market_hash_name"].unique()))])
missing_item_df["skin_name"] = missing_item_df["market_hash_name"].apply(get_skin_name)

merged_df = pd.concat([df, missing_item_df], ignore_index=True)

merged_df = merged_df.sort_values(["skin_name", "skin_type"])
merged_df["tradable"] = merged_df["tradable"].fillna(1)
merged_df["skin_type"] = merged_df["skin_type"].ffill(axis=0)
merged_df["skin_grade"] = merged_df["skin_grade"].ffill(axis=0)
merged_df = merged_df.sort_values(["data_start_value"])

merged_df["skin_type_category"] = merged_df["skin_type"].apply(get_skin_type_category)
merged_df["skin_quality"] = merged_df["skin_type"].apply(get_skin_quality)
merged_df["analysis_type"] = merged_df["skin_type_category"].apply(get_analysis_type)
merged_df["market_name"] = merged_df["market_hash_name"]
merged_df["timestamp"] = merged_df["timestamp"].fillna(pd.Timestamp.now())

analysis_list = merged_df["analysis_type"].to_list()
market_name_list = merged_df["market_hash_name"].to_list()

weapon_type_list = [get_weapon_type(market_name_list[iter]) if value == True else "Not Weapon" for iter, value in enumerate(analysis_list)]
merged_df["weapon_type"] = pd.Series(weapon_type_list)

skin_wear_list = [get_skin_wear(market_name_list[iter]) if value == True else "No Skin Wear" for iter, value in enumerate(analysis_list)]
merged_df["skin_wear"] = pd.Series(skin_wear_list)
merged_df = merged_df.drop(columns="analysis_type")

merged_df.to_csv("./data/item_list/20230725_0741_item_list_full.csv", index=False)

### --------------- GET TOTALLY EMPTY FROM CSGO WIKI ------------------ ###
df = pd.read_csv("./data/item_list/20230725_0741_item_list_full.csv")
csgo_wiki_df = pd.read_excel("./data/CSGO Wiki Table/Skin_Collections.xlsx", sheet_name="Case_Weapons", header = 0, index_col=None)
merge = csgo_wiki_df.merge(right=df, how="left", left_on="Market Hash Name", right_on="market_hash_name")

empty_df = merge[merge["market_hash_name"].isna()].reset_index(drop=True)
empty_df["market_hash_name"] = empty_df["Market Hash Name"]

data_last_value = df["data_start_value"].iloc[-1] + 1
# empty_df

empty_df["data_start_value"] = pd.Series([data_last_value + iter for iter, value in enumerate(list(empty_df["market_hash_name"]))])
empty_df["skin_name"] = empty_df["market_hash_name"].apply(get_skin_name)
empty_df["weapon_type"] = empty_df["market_hash_name"].apply(get_weapon_type)
empty_df["skin_type_category"] = empty_df["weapon_type"].apply(get_totally_new_skin_type_cat)
empty_df["skin_type"] = empty_df.apply(lambda row: row["Quality"] + " Grade " + row["skin_type_category"] if row["Quality"]=="Mil-Spec" else row["Quality"] + " " +row["skin_type_category"], axis=1)
empty_df["skin_grade"] = empty_df["skin_type"].apply(get_skin_grade)
empty_df["skin_quality"] = empty_df["skin_type"].apply(get_skin_quality)
empty_df["tradable"] = empty_df["tradable"].fillna(1)
empty_df["market_name"] = empty_df["market_hash_name"]
empty_df["timestamp"] = empty_df["timestamp"].fillna(pd.Timestamp.now())
empty_df["analysis_type"] = empty_df["skin_type_category"].apply(get_analysis_type)

analysis_list = empty_df["analysis_type"].to_list()
market_name_list = empty_df["market_hash_name"].to_list()

skin_wear_list = [get_skin_wear(market_name_list[iter]) if value == True else "No Skin Wear" for iter, value in enumerate(analysis_list)]
empty_df["skin_wear"] = pd.Series(skin_wear_list)

empty_df = empty_df.drop(columns="analysis_type")
empty_df = empty_df[list(df.columns)]

full_df = pd.concat([df, empty_df], ignore_index=True)

full_df.to_csv("./data/item_list/20230725_0741_item_list_full_with_wiki_data.csv", index=False)