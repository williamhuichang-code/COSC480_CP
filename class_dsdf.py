"""This module is designed for a super class DSDf, means Data Science dataframe.
   The DSDf class inherit from pandas dataframe, and controls features for its subclass, CrashDf, ..., etc.
   Author: William Hui Chang
   Date: Sat May 24 09:59:08 2025
"""

import pandas as pd
from pyproj import CRS, Transformer
from module_helper import print_divider, pause


class DSDf(pd.DataFrame):
    """ 
    A data science df class that can operate itself, 
    like enrich itself, wrangle itself etc. 
    """
    # preserve my custom class type after manipulations
    @property
    def _constructor(self):
        # after slicing or dicing, make it return a DSDf instead of a pd df
        return DSDf
    # initializer based upon super class pandas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # instances method
    def _xy_mutate_lonlat(self, x_col: str = 'X', y_col: str = 'Y') -> pd.DataFrame:
        """ A data science dataframe can 
        transforms meter-based X and Y coordinates (e.g., EPSG:2193) 
        into geographic coordinates (longitude, latitude) using CRS conversion. 
        """
        print_divider()
        print("[Data Enriching] (automatic) New columns 'lon', 'lat' mutated from 'X', 'Y' and added to the crash dataset.")
        pause()
        transformer = Transformer.from_crs("EPSG:2193", "EPSG:4326", always_xy=True)
        x_vals = self[x_col].values
        y_vals = self[y_col].values
        lon_vals, lat_vals = transformer.transform(x_vals, y_vals)
        self['lon'] = lon_vals
        self['lat'] = lat_vals
        return self
    
    def divider_in_chain(self):
        """ Prints a divider in class method chain. """
        print_divider()
        return self
    def pause_in_chain(self):
        """ Supports pause in class method chain. """
        pause()
        return self
    
    def print_in_chain(self):
        """ Supports print ds df itself in class method chain. """
        print_divider()
        print(self)
        return self

    def print_columns_in_chain(self):
        """ Supports print columns in class method chain. """
        print_divider()
        print(self.columns)
        return self

    def print_type_in_chain(self):
        """ Supports print type in class method chain. """
        print_divider()
        print(type(self))
        return self
    
    def print_head_in_chain(self,n=5):
        """ Supports print head in class method chain. """
        print_divider()
        print(self.head(n))
        return self

    def print_tail_in_chain(self,n=5):
        """ Supports print head in class method chain. """
        print_divider()
        print(self.tail(n))
        return self
    
    def general_bug_test(self):
        """ bug test purpose """
        self.print_columns_in_chain().print_type_in_chain().print_tail_in_chain()
        return self
    
    # class method

    # static method
    @staticmethod
    def meterbounds_for_projected_country(countryname: str) -> dict:
        """ Transforms and returns a dictionary of meter-based bounds for a country, 
        intended for geometry bounds data wrangling. 
            what is pyproj
        a python interface for the PROJ library
        what is PROJ library
            a standard tool used in GIS for converting geographic coordinates between different coordinate reference systems
        what is what is EPSG
            European Petroleum Survey Group, a standardized coding system for CRS
        what is CRS and .from_epsg(2193)
            CRS is the class name for Coordinate Reference Systems
            .from_epsg() is a class method that looks up the official definition of an EPSG code (e.g. 2193) from its internal database.
        what is wgs84
            the global standard coordinate system, World Geodetic System 1984, used by GPS, Google Maps, and most modern location-based services
        degrees (EPSG:4326) vs meters (projected CRS)
            Rule of Thumb: 
                use degrees for location, use meters for measurement.
            degrees (EPSG:4326) is better for 
                a broad region (continent/world); 
                compatibility with Google Maps, Leaflet, Foliumm; 
                interactive maps on the web.
            meters (projected CRS) is better for 
                accurate area, distance, or spatial analysis;
                plotting a local region (like NZ, a country, etc.);
                using matplotlib, cartopy, or precise overlays.
        """
        country_epsg_dict = {
            "New Zealand": 2193,
            "Eastern Australia": 28355,
            "Western Australia": 28350,
            "Central US": 26915,
            "China": 4490
        }
        epsg_num = country_epsg_dict.get(countryname)
        degreed_country_crs = CRS.from_epsg(epsg_num)
        min_lon, min_lat, max_lon, max_lat = degreed_country_crs.area_of_use.bounds
        degreed_global_wgs84 = CRS.from_epsg(4326)
        transformer = Transformer.from_crs(degreed_global_wgs84, degreed_country_crs, always_xy=True)
        x_min, y_min = transformer.transform(min_lon, min_lat)
        x_max, y_max = transformer.transform(max_lon, max_lat)
        meter_bound_dict = {
            "x_bounds" :(x_min, x_max), 
            "y_bounds": (y_min, y_max)
            }
        return meter_bound_dict



if __name__ == "__main__":
    mtcars_source = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mtcars.csv")
    print(type(mtcars_source))
    mtcars_df = DSDf(mtcars_source)
    print(type(mtcars_df))
    mtcars_df.head()
    # test for geometry meter bounds
    print("TEST FOR GEOMETRY METER BOUNDS")
    """
    what is pyproj
        a python interface for the PROJ library
    what is PROJ library
        a standard tool used in GIS for converting geographic coordinates between different coordinate reference systems
    what is what is EPSG
        European Petroleum Survey Group, a standardized coding system for CRS
    what is CRS and .from_epsg(2193)
        CRS is the class name for Coordinate Reference Systems
        .from_epsg() is a class method that looks up the official definition of an EPSG code (e.g. 2193) from its internal database.
    what is wgs84
        the global standard coordinate system, World Geodetic System 1984, used by GPS, Google Maps, and most modern location-based services
    degrees (EPSG:4326) vs meters (projected CRS)
        Rule of Thumb: 
            use degrees for location, use meters for measurement.
        degrees (EPSG:4326) is better for 
            a broad region (continent/world); 
            compatibility with Google Maps, Leaflet, Foliumm; 
            interactive maps on the web.
        meters (projected CRS) is better for 
            accurate area, distance, or spatial analysis;
            plotting a local region (like NZ, a country, etc.);
            using matplotlib, cartopy, or precise overlays.
    """
    epsg_dict = {
        "New Zealand": 2193,
        "China": 4490
    }
    print(f"\nthese country name keys are munnually stored in this dictionary for future use: \n")
    for key in epsg_dict.keys():
        print(" ", key)
    # test 'New Zealand'
    print("\nwhen input is 'New Zealand'\n")
    # name a country
    country_name = "New Zealand"
    # epsg_num from dictionary
    epsg_num = epsg_dict.get(country_name)
    print(" ", f"its epsg_num from the manual dictionary looks like {epsg_num}, and")
    # crs info, EPSG:2193, NZTM2000 (projected CRS in meters for New Zealand local coordinates)
    crs_from_epsg = CRS.from_epsg(epsg_num)
    print(" ", f"the projected CRS in degrees for New Zealand local lat/lon looks like {crs_from_epsg}\n")
    # crs name and bounds
    crs_name = crs_from_epsg.area_of_use.name
    print(" ", " ", f"this crs info has this name info: {crs_name}")
    crs_bounds = crs_from_epsg.area_of_use.bounds
    print(" ", " ", f"this crs info has this lon/lat bounds info: {crs_bounds}\n")
    # Bound box/corners in lon/lat (from EPSG:2193 definition)
    min_lon, min_lat, max_lon, max_lat = crs_from_epsg.area_of_use.bounds
    print(" ", " ", " ", f"lower bound for longitude: {min_lon}")
    print(" ", " ", " ", f"lower bound for latitude: {min_lat}")
    print(" ", " ", " ", f"upper bound for longitude: {max_lon}")
    print(" ", " ", " ", f"upper bound for latitude: {max_lat}\n")
    # crs info, EPSG:4326, WGS 84 (geographic CRS in degrees for global lat/lon)
    wgs84 = CRS.from_epsg(4326)
    print(" ", f"the projected CRS in degrees for global lat/lon looks like {wgs84}\n")
    # convert from wgs84 (lat/lon in degrees) to crs (meters in NZTM2000)
    # always_xy=True ensures the order is (lon, lat), not (lat, lon)
    transformer = Transformer.from_crs(wgs84, crs_from_epsg, always_xy=True)
    print(" ", " ", f"transformer is the meters alternative for lon/lat bound box: ")
    print(" ", " ", f"{transformer}\n")
    # the meters alternative for lon/lat bound box
    x_min, y_min = transformer.transform(min_lon, min_lat)
    x_max, y_max = transformer.transform(max_lon, max_lat)
    print(" ", " ", " ", f"lower x in meters: {x_min}")
    print(" ", " ", " ", f"lower y in meters: {y_min}")
    print(" ", " ", " ", f"upper x in meters: {x_max}")
    print(" ", " ", " ", f"upper y in meters: {y_max}\n")

    meter_bounds = DSDf.meterbounds_for_projected_country(country_name)
    print(" ", f"compared with func 'meterbounds_for_projected_country', func returns: ")
    print(" ", meter_bounds)
    print("-"*100)