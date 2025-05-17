"""This module is designed to update dataset from opendata-nzta..
   Author: William Hui Chang
   Date: Fri May 16 10:12:48 2025
"""

import pandas as pd_update
import numpy as np_update
import requests as requests_update
from config_module import COMMON_URL_PART, CRASH_CSV


def df_of_entries_from_request(max_local_pk: int, nrows = 2000) -> pd_update.DataFrame:
    """ Returns single or max online entries from a request as pd df. """
    if nrows == 1:
        sorting = "desc"
    else:
        sorting = "asc"
    update_url = (
        f"{COMMON_URL_PART}/query"
        f"?where=OBJECTID>{max_local_pk}"
        f"&outFields=*"
        f"&orderByFields=OBJECTID {sorting}"
        f"&resultRecordCount={nrows}"
        f"&f=json"
        )
    # the HTTP response
    http_response = requests_update.get(update_url)
    # .json() converts the HTTP response into a nested Python list of dicts
    nested_attribute_list = http_response.json().get('features', [])
    all_attributes = []
    for attribute in nested_attribute_list:
        split_dict_of_geometry = attribute.pop('geometry')
        split_dict_of_geometry = {k: np_update.round(np_update.float64(v), 0) for k, v in split_dict_of_geometry.items()}
        x = split_dict_of_geometry.get('x')
        y = split_dict_of_geometry.get('y')
        attribute.get('attributes').update({"X": x, "Y": y})
        all_attributes.append(attribute.get('attributes'))
    entries_per_query = pd_update.DataFrame(all_attributes)
    return entries_per_query


def df_requested_from_url(existed_df: pd_update.DataFrame) -> pd_update.DataFrame:
    """ Compares with existed local df and collects updates and returns as df. """
    ### step 0, max local pk from local file and online pk from url, for comparison
    maxpk_existed = existed_df['OBJECTID'].max()
    maxpk_online = df_of_entries_from_request(maxpk_existed, nrows=1).loc[0,'OBJECTID']
    ### step 1, make requests until new entries are exhausted
    df_for_new_entries = pd_update.DataFrame()
    while maxpk_existed < maxpk_online:
        df_of_entries_per_request = df_of_entries_from_request(maxpk_existed)
        df_for_new_entries = pd_update.concat([df_for_new_entries, df_of_entries_per_request], axis=0)
        n_collected = df_for_new_entries.shape[0]
        maxpk_existed = df_for_new_entries['OBJECTID'].max()
        print(f"{n_collected} entries collected, OBJECTID progress: {maxpk_existed}/{maxpk_online}.\n")
    # step 2, returns the df of new entries
    return df_for_new_entries


def df_loaded_with_auto_update(csv_name) -> pd_update.DataFrame:
    """ Returns dataframe loaded with auto-update from API. """
    ### step 0, local parameters
    # pathed_csv = f"D:/Data4Code/{csv_name}"  # for local testing
    pathed_csv = f"data/{csv_name}"  # for git lauching
    ### refuse to update if local csv file not initialized
    try:
        ### step 1, load local df and get requested_df from online API
        local_df = pd_update.read_csv(pathed_csv)
        requested_df = df_requested_from_url(local_df)
        ### step 2, concat and return
        return pd_update.concat([local_df, requested_df], axis=0).reset_index(drop=True)
    except FileNotFoundError:
        print("\nLoading/Updating Request Refused:")
        print(f"    '{csv_name}' was not found in the expected path.\n")
        print("Recommendation:")
        print("    Please download the full dataset once and place it in the right path.")
        print("    Incremental updates will be applied automatically every time the project is launched.\n")
        return None


# out dated old function, put here just in case
# def df_loaded_from_file(filename: str) -> pd.DataFrame:
#     """ Returns dataframe loaded from a CSV file into a pandas DataFrame. """
#     print("Now loading ...\n...")
#     ready_df = pd.read_csv(filename)
#     print("Dataframe has been successfully loaded!")
#     return ready_df



if __name__ == "__main__":
    # "data/Crash_Analysis_System_(CAS)_data.csv"
    updated_df = df_loaded_with_auto_update(CRASH_CSV)
    if updated_df is not None:
        print(updated_df.head())
        print(updated_df.tail())
        print()
        print("(New updated entries will not be saved to local files for demonstrating this update feature.)")
    else:
        pass