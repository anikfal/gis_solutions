Merging two TIF files with nan values:


### Method 1:
open merge_tif_by_null.py and put the names of your TIF files. You need to install the python packages of xarray and rioxarray:
python merge_tif_by_null.py


### Method 2:
This is a shell script running gdal commands. However, it is mostly coorect, but it cannot avoid the sharing area between the 2 TIF files:


### Geotif 1:
![1](https://github.com/anikfal/GIS_solutions/assets/11738727/db583c95-b7b9-44b3-bff1-3dfbd3a075a9)


### Geotif 2:
![2](https://github.com/anikfal/GIS_solutions/assets/11738727/0d231a29-63e2-4141-b8a1-6da482d46585)


### Ordinary merging by gdal_merge.py:
![blank_space](https://github.com/anikfal/GIS_solutions/assets/11738727/afb8346e-adcc-4059-9b5a-79580505d234)


### Correct merging by merge_tif_by_nan.py:
![1](https://github.com/anikfal/GIS_solutions/assets/11738727/c769f966-38ae-4f41-ae4a-8fbb860f361b)

