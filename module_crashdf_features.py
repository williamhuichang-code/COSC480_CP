"""This module is for functions specific to crash report project.
   Author: William Hui Chang
   Date: Sat Apr 26 10:43:45 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
from class_helper_menu import Menu
from subclass_crashdf import CrashDf
import folium
from folium.plugins import HeatMapWithTime, Geocoder, MarkerCluster, BeautifyIcon
import webbrowser
import os
import urllib.parse

###### part 2 features consideration ######
# feature 2, crash report prioritizing temporarySpeedLimit, and using speedLimit as fallback
# (!!! obsoleted, already redesigned as class method in subclass_crashdf, keep 30 days just in case)
# def df_with_effective_speed(crash_df: pd.DataFrame) -> pd.DataFrame:
#    """ Return new crash df with effective speed limit. """
#    new_df = crash_df.assign(effectiveSpeedLimit = 
#          lambda crash_df: crash_df['temporarySpeedLimit'].combine_first(crash_df['speedLimit']))
#    return new_df


# core report table for year, speed, crash severity type
def core_crash_severity_data(enriched_df: pd.DataFrame) -> pd.DataFrame:
   """ Returns core dataframe for further reports and graphs. """
   core_df = CrashDf(enriched_df) \
      .loc[:,['crashYear', 'effectiveSpeedLimit', 'crashSeverity']] \
      .groupby(['crashYear', 'crashSeverity', 'effectiveSpeedLimit']) \
      .size() \
      .reset_index(name='count')
   return CrashDf(core_df)


# offer slicing and dicing choices for value selection (all value, range, point)
def enhanced_numeric_selection(core_df: pd.DataFrame, col_name: str) -> list:
   """ Offers choices for slicing, dicing. """
   # OOP chains
   options = [f"all {col_name}", f"{col_name} range", f"a specific {col_name}"]
   option_choice = None
   while option_choice == None:
      option_choice = Menu(options).display_with_index().custom_prompt(f"Your filter method for {col_name}: ").validate_with_index()
   all_col_values = Menu(core_df[col_name]).return_as_list()
   var1, var2, var3 = None, None, None
   if option_choice == f"all {col_name}":
      return all_col_values
   elif option_choice == f"{col_name} range":
      while var1 == None:
         var1 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"The start {col_name} of interest: ").validate_with_values()
      while var2 == None:
         var2 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"The end {col_name} of interest: ").validate_with_values()
         small_var = min(int(float(var1)), int(float(var2)))
         large_var = max(int(float(var1)), int(float(var2)))
      return [x for x in all_col_values if small_var <= x <= large_var]
   elif option_choice == f"a specific {col_name}":
      while var3 == None:
         var3 = Menu(core_df[col_name]).display_with_values().custom_prompt(f"For your {col_name} of interest: ").validate_with_values()
      return [int(float(var3))]


# offer slicing and dicing choices for value selection (all value, one to many)
def enhanced_text_selection(core_df: pd.DataFrame, col_name: str) -> list:
   """ Offers choices for slicing, dicing. """
   # OOP chains
   options = [f"all {col_name}", f"one to many {col_name}"]
   option_choice = None
   while option_choice == None:
      option_choice = Menu(options).display_with_index().custom_prompt(f"Your filter method for {col_name}: ").validate_with_index()
   all_col_values = Menu(core_df[col_name]).return_as_list()
   if option_choice == f"all {col_name}":
      return all_col_values
   elif option_choice == f"one to many {col_name}":
      split_str_index = Menu(core_df[col_name]).display_with_index().split_prompt().split_validation_with_index()
      split_int_index = Menu.list_items_as_int(split_str_index)
      split_col_values = [all_col_values[i] for i in split_int_index]
      return split_col_values


# enhanced crash_report with feature 1, 2, 3, 4
# feature 1 & 3, Validate user input
#     catch non-existing report years
#     give meaningful error msg feedback, no record, out of bound
#     provide valid year options in the dataset (unique, non-null year values)
# feature 4, add all possible years options to crash severity report
def crash_severity_report(core_df: pd.DataFrame) -> pd.DataFrame:
   """ Print crash report with specific year and effective speed limit. """
   # Rstudio report <- df %>% mutate %>% select %>% filter %>% group_by %>% summurize
   # offer choices for all possible years, year range, single year
   print("Choose your crash year of interest ↓↓↓")
   year_of_interest = enhanced_numeric_selection(core_df, 'crashYear')
   # offer choices for all possible speed, speed range, single speed
   print("Choose your speed limit of interest ↓↓↓")
   speed_of_interest = enhanced_numeric_selection(core_df, 'effectiveSpeedLimit')
   # offer choices for all possible crash severity type
   print("Choose your crash severity of interest ↓↓↓")
   crash_of_interest = enhanced_text_selection(core_df, 'crashSeverity')
   # reshaping crash_df to generate report
   row_conditions = (core_df['crashYear'].isin(year_of_interest) & 
                     core_df['effectiveSpeedLimit'].isin(speed_of_interest) & 
                     core_df['crashSeverity'].isin(crash_of_interest))
   col_conditions = ['crashYear', 'crashSeverity', 'effectiveSpeedLimit', 'count']
   report = core_df \
      .loc[row_conditions, col_conditions] \
      .groupby(['crashYear', 'crashSeverity']) \
      .agg({'count': 'sum'}) \
      .unstack('crashSeverity') \
      .reset_index()
   return report


# feature 5, generate over time graph based on report result
#     as an extention from crash severity report
def plot_crash_trends(plot_df: pd.DataFrame) -> None:
   """ Plot crash trends using matplotlib.pyplot. """
   # plot each severity as a line
   plot_df = plot_df.set_index('crashYear')
   plot_df.columns = plot_df.columns.get_level_values(-1)
   plot_df.plot(kind='line', marker='o')
   plt.title("Crash Trends by Year")
   plt.xlabel("Crash Year")
   plt.ylabel("Number of Crashes")
   plt.grid(True)
   plt.tight_layout()
   plt.legend(title='Crash Severity')
   plt.show()


def core_crash_heatmap_data(initialized_df: pd.DataFrame) -> pd.DataFrame:
   """ bla """
   core_heatmap_df = CrashDf(initialized_df) \
      .cleaned_crashdf_by_nz_bounds()\
      .loc[:,['OBJECTID', 'X', 'Y', 'lon', 'lat', 'tlaName', 'crashYear', 'light', 'weatherA', 'motorcycle', 'tree', 'crashSeverity']]
   return CrashDf(core_heatmap_df)




def auto_save_open(map, savename:str):
   """ Leverage os and webbrowser to save and open html file using different system. """
   # relative path
   relative_path = f"data/{savename}"
   # save html
   map.save(relative_path)
   # open using absolute path (on either system)
   absolute_path = os.path.abspath(relative_path)
   file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(absolute_path))
   webbrowser.open_new_tab(file_url)


# create a map background
def map_background(core_heatmap_df: pd.DataFrame):
   """ bla """
   # lat_mbound and lon_mbound decide where the map start to show
   lat_mbound = (core_heatmap_df['lat'].max() + core_heatmap_df['lat'].min())/2
   lon_mbound = (core_heatmap_df['lon'].max() + core_heatmap_df['lon'].min())/2
   # map
   mbackground = folium.Map(location=[lat_mbound, lon_mbound], zoom_start=6, tiles="OpenStreetMap")
   return mbackground


### timed_heatmap feature
def plot_crash_heatmap(core_heatmap_df: pd.DataFrame):
   """ bla """
   # timed_heatmap step 1: prepare map background
   m = map_background(core_heatmap_df)
   # timed_heatmap step 2: prepare heatmap data grouped by year
   years = sorted(core_heatmap_df['crashYear'].dropna().unique())
   heat_data = [
      core_heatmap_df[core_heatmap_df['crashYear'] == year][['lat', 'lon']].dropna().values.tolist()
      for year in years
   ]
   # timed_heatmap step 2: generate time index (just use year labels)
   time_index = [str(year) for year in years]
   # timed_heatmap Step 3: Create animated heatmap
   HeatMapWithTime(
      data=heat_data,
      index=time_index,
      auto_play=True,
      max_opacity=0.6,
      radius=10
   ).add_to(m)
   ### save and plot
   auto_save_open(m, "fatal_heatmap_with_year.html")


# create a dualmap background
def dualmap_background(core_heatmap_df: pd.DataFrame):
   """ bla """
   # lat_mbound and lon_mbound decide where the map start to show
   lat_mbound = (core_heatmap_df['lat'].max() + core_heatmap_df['lat'].min())/2
   lon_mbound = (core_heatmap_df['lon'].max() + core_heatmap_df['lon'].min())/2
   # map
   dmbackground = folium.plugins.DualMap(location=(lat_mbound, lon_mbound), zoom_start=6)
   folium.TileLayer("openstreetmap").add_to(dmbackground.m1)
   folium.TileLayer("Cartodb dark matter").add_to(dmbackground.m2)
   return dmbackground


### pin map feature
def plot_crash_pinmap(core_heatmap_df: pd.DataFrame, severity_of_interest=['Serious Crash', 'Fatal Crash']):
   """ bla """
   # limit pin map to serious and fatal to save memory
   core_heatmap_df = core_heatmap_df[core_heatmap_df['crashSeverity'].isin(severity_of_interest)]
   #create a dualmap background to compare dark theme and bright theme
   dm = dualmap_background(core_heatmap_df)
   # seperate map df into bright df and dark df
   df_bright = core_heatmap_df[core_heatmap_df['light'] == 'Bright sun']
   df_dark = core_heatmap_df[core_heatmap_df['light'] == 'Dark']
   # define pin color per crashSeverity
   colors = {
      'Fatal Crash': 'red',
      'Serious Crash': 'orange',
      'Minor Crash': 'beige',
      'Non-Injury Crash': 'green'
   }
   # create severity feature group for bright theme
   for severity in severity_of_interest:
      fg_bright = folium.FeatureGroup(name=severity)
      info_in_display = ['OBJECTID', 'lat', 'lon', 'crashYear', 'tlaName', 'light', 'weatherA', 'motorcycle', 'tree', 'crashSeverity']
      subset = df_bright[df_bright['crashSeverity'] == severity][info_in_display]
      for _, row in subset.iterrows():
         # use html to define what to demonstrate on crash pin
         html = row.to_frame().T.to_html(classes="table table-striped table-hover table-condensed table-responsive")
         folium.Marker(
               location=[row['lat'], row['lon']],
               popup=folium.Popup(html),
               icon=folium.Icon(color=colors[severity])
               ).add_to(fg_bright)
      # add bright feature group back to bright map
      fg_bright.add_to(dm.m1)
   # create severity feature group for dark theme
   for severity in severity_of_interest:
      fg_dark = folium.FeatureGroup(name=severity)
      info_in_display = ['OBJECTID', 'lat', 'lon', 'crashYear', 'tlaName', 'light', 'weatherA', 'motorcycle', 'tree', 'crashSeverity']
      subset = df_dark[df_dark['crashSeverity'] == severity][info_in_display]
      for _, row in subset.iterrows():
            # use html to define what to demonstrate on crash pin
            html = row.to_frame().T.to_html(classes="table table-striped table-hover table-condensed table-responsive")
            folium.Marker(
               location=[row['lat'], row['lon']],
               popup=folium.Popup(html),
               icon=folium.Icon(color=colors[severity])
               ).add_to(fg_dark)
      # add dark feature group back to dark map
      fg_dark.add_to(dm.m2)
   # add layer control to pinmap to support selecting
   folium.LayerControl(collapsed=False).add_to(dm)
   # add bar plugin to support location searching
   folium.plugins.Geocoder(position='topleft').add_to(dm.m1)
   ### save to html and open it automatically
   auto_save_open(dm, "pinmap_bright_dark.html")


### cluster map feature
def plot_crash_cluster_map(core_heatmap_df: pd.DataFrame, severity_of_interest=['Non-Injury Crash', 'Minor Crash', 'Serious Crash', 'Fatal Crash']):
   """ bla """
   # limit pin map to serious and fatal to save memory
   core_heatmap_df = core_heatmap_df[core_heatmap_df['crashSeverity'].isin(severity_of_interest)]
   #create a dualmap background to compare dark theme and bright theme
   cm = map_background(core_heatmap_df)
   # define marker icon per crashSeverity
   icon_lookup = {
   'Non-Injury Crash': 'smile-o', 
   'Minor Crash': 'wrench',
   'Serious Crash': 'exclamation-triangle',
   'Fatal Crash': 'skull'
   }
   # create marker cluster feature for each severity group
   for severity in ['Non-Injury Crash', 'Minor Crash', 'Serious Crash', 'Fatal Crash']:
      severity_cluster = MarkerCluster(name=severity)
      info_in_display = ['OBJECTID', 'lat', 'lon', 'crashYear', 'tlaName', 'light', 'weatherA', 'motorcycle', 'tree', 'crashSeverity']
      subset = core_heatmap_df[core_heatmap_df['crashSeverity'] == severity][info_in_display]
      # create different icon markers for each severity and add to cluster
      for _, row in subset.iterrows():
         # use html to define what to demonstrate on crash markers
         html = row.to_frame().T.to_html(classes="table table-striped table-hover table-condensed table-responsive")
         folium.Marker(
               location=[row['lat'], row['lon']],
               popup=folium.Popup(html),
               icon=BeautifyIcon(
                  icon=icon_lookup[severity],
                  icon_shape='marker',
                  border_color="#000",
                  text_color="#000",
                  background_color="#fff",
                  inner_icon_style="font-size:12px;margin-top:1px;"
                  )
         ).add_to(severity_cluster)
      # add each severity cluster to cluster map background
      severity_cluster.add_to(cm)
   # add layer control to cluster map to support selecting
   folium.LayerControl(collapsed=False).add_to(cm)
   # add bar plugin to support location searching
   folium.plugins.Geocoder(position='topleft').add_to(cm)
   ### save to html and open it automatically
   auto_save_open(cm, "cluster_map_for_severity.html")



# if main
if __name__ == '__main__':
   # load data
   print("testing for enhanced_text_selection")
   # test df
   initial_df = CrashDf.df_loaded_with_online_update(CrashDf._crash_csv_name).cleaned_crashdf_by_nz_bounds()
   # initial_df = CrashDf(pd.read_excel(r"D:\DS\Py code\crash sample.xlsx"))._df_with_effective_speed()._xy_mutate_lonlat().cleaned_crashdf_by_nz_bounds()
   crash_severity_core_df = core_crash_severity_data(initial_df)
   print()

   # enhanced_numeric_selection
   print("testing for enhanced_numeric_selection")   
   selection = enhanced_numeric_selection(crash_severity_core_df, "crashYear")
   print(selection)
   print()

   # enhanced_text_selection
   print("testing for enhanced_text_selection")
   selection = enhanced_text_selection(crash_severity_core_df, 'crashSeverity')
   print(selection)
   print()

   # crash severity report
   print("testing for crash severity report")
   report_for_plot = crash_severity_report(crash_severity_core_df)
   print(report_for_plot)
   print()

   # over time graph
   print("testing for crash over time graph")
   plot_crash_trends(report_for_plot)

   # testing for heatmap df
   print("testing for heatmap df")
   core_hm_df = core_crash_heatmap_data(initial_df).general_bug_test()
   core_hm_df = core_hm_df[core_hm_df['crashSeverity'] == 'Fatal Crash']

   # testing for heatmap
   core_pm_df = core_crash_heatmap_data(initial_df).tail(10000)
   print("testing for crash pinmap feature")
   plot_crash_pinmap(core_pm_df)

