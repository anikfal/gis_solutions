#Author Amirhossein Nikfal <https://github.com/anikfal>
import rioxarray as rio
from rioxarray.merge import merge_arrays
import numpy as np
#Sentinel-2 NDWI = (B03 - B08) / (B03 + B08)

b3 = rio.open_rasterio("T38SNG_20230814T074619_B03_10m.jp2")
b8 = rio.open_rasterio("T38SNG_20230814T074619_B08_10m.jp2")
print("Writing wi ...")
wi111 = ((b3.astype(np.float32)-b8)/(b3.astype(np.int32)+b8.astype(np.int32)))[0]
print("Other half ...")
b3 = rio.open_rasterio("T38SNH_20230814T074619_B03_10m.jp2")
b8 = rio.open_rasterio("T38SNH_20230814T074619_B08_10m.jp2")
print("Writing wi ...")
wi222 = ((b3.astype(np.float32)-b8)/(b3.astype(np.int32)+b8.astype(np.int32)))[0]
print("Merging ...")
merged = merge_arrays([wi111, wi222])
del(b3)
del(b8)
del(wi111)
del(wi222)
merged.rio.to_raster("water_index.tif")
