""" Crash KDE Heatmap — Auto-adjusted Grid """
import pandas as pd
import geopandas as gpd
import plotly.express as px
from subclass_crashdf import CrashDf

# Load and clean data
raw_df = CrashDf.df_loaded_with_online_update(CrashDf._crash_csv_name).cleaned_crashdf_by_nz_bounds()
df = raw_df[
    (raw_df['crashSeverity'] == 'Fatal Crash')
    & (raw_df['tlaName'] == 'Christchurch City')
    # & (raw_df['tree'] > 0)
    ][['X', 'Y', 'crashSeverity']].dropna().tail(100000)

# Convert to lat/lon
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['X'], df['Y']), crs='EPSG:2193')
gdf = gdf.to_crs(epsg=4326)
df['lat'] = gdf.geometry.y
df['lon'] = gdf.geometry.x

# Plot density heatmap
fig = px.density_mapbox(
    df,
    lat='lat',
    lon='lon',
    z=None,  # optional: use 'crashSeverity' count if it's numeric
    radius=10,  # adjust for smoothness (in pixels)
    center=dict(lat=-43.53, lon=172.64),  # Christchurch area
    zoom=10,
    mapbox_style='open-street-map',  # Try: "carto-positron", "stamen-terrain"
    height=700,
    title='Fatal Crash Heatmap — Christchurch'
)

fig.show()
