""" this is for test only """

from subclass_crashdf import CrashDf
from module_helper import print_divider
from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# Load data
raw_df = CrashDf.df_loaded_with_online_update(CrashDf._crash_csv_name).cleaned_crashdf_by_nz_bounds()
# Filter for Christchurch fatal crashes
df = raw_df[
    (raw_df['crashSeverity'] == 'Fatal Crash')
    # & (raw_df['tlaName'] == 'Christchurch City')
    # & (raw_df['tree'] > 0)
][['X', 'Y', 'crashSeverity']].dropna().tail(100000)


# Get coordinates
coords = df[['X', 'Y']].values

# Fit KDE
kde = KernelDensity(kernel='gaussian', bandwidth=10000).fit(coords)  # Tune bandwidth as needed

# Auto-adjust grid extent from crash areade
xmin, ymin = coords.min(axis=0) - 2000  # padding = 2000 meters
xmax, ymax = coords.max(axis=0) + 2000
xx, yy = np.meshgrid(np.linspace(xmin, xmax, 400), np.linspace(ymin, ymax, 400))
grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T

# KDE prediction
log_density = kde.score_samples(grid_coords)
density = np.exp(log_density).reshape(xx.shape)

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title("Crash KDE Heatmap — Christchurch (Fatal Crashes)", fontsize=14)

# Heatmap
ax.imshow(
    density,
    origin='lower',
    extent=[xmin, xmax, ymin, ymax],
    cmap='hot',
    alpha=0.7,
    zorder=2
)

plt.axis("off")
plt.tight_layout()
plt.show()
