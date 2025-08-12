import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Create 64x32 synthetic temperature anomaly data
lat_len, lon_len = 32, 64
data = np.random.normal(loc=0.5, scale=0.2, size=(lat_len, lon_len))

# Coordinate arrays
lons = np.linspace(-180, 180, lon_len)
lats = np.linspace(-90, 90, lat_len)
lon2d, lat2d = np.meshgrid(lons, lats)

# Plotting
fig = plt.figure(figsize=(10, 5))
proj = ccrs.Robinson()
ax = plt.axes(projection=proj)
ax.set_global()

# Add coastlines and borders
ax.coastlines(linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.4)

# Pixelated pcolormesh with no interpolation
mesh = ax.pcolormesh(
    lon2d, lat2d, data,
    transform=ccrs.PlateCarree(),
    cmap='inferno',
    shading='auto'  # Ensures square pixels (no smoothing)
)

# Colorbar
cbar = plt.colorbar(mesh, orientation='horizontal', pad=0.05, shrink=0.7)
cbar.set_label("Temperature (°C)")

# Add RMSE text overlay
plt.text(0.01, 1.02, r"$\mathrm{RMSE_{LaMa}} = 0.64^\circ C$", transform=ax.transAxes,
         fontsize=12, ha='left')

plt.tight_layout()
plt.show()