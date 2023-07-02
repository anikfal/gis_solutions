#code to merge two TIF files with nan values
#Author: Amirhossein Nikfal

import rioxarray as rio # for the extension to load
from rioxarray.merge import merge_arrays

# Replace the filesnames below with the names of your TIF files
################################
tif1 = "S2-band10.tif"
tif2 = "S3-band10.tif"
################################
f1 = rio.open_rasterio(tif1)
f2 = rio.open_rasterio(tif2)
f1 = f1.fillna(0)
f2 = f2.fillna(0)
merged = merge_arrays([f1, f2])

merged.rio.to_raster("final_merged.tif")
print("final_merged.tif as the merge of", tif1, "and", tif2, "has been created!")
