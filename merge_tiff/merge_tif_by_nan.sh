#!/bin/bash
# Code to merge two TIFF files by avoiding nan values
#Author: Amirhossein Nikfal
if [ -z "$1" ]
  then
    echo "Error: Argument 1 is empty"
    echo "Provide 2 arguments as TIFF files and run again"
    exit
fi
if [ -z "$2" ]
  then
    echo "Error: Argument 2 is empty"
    echo "Provide 2 arguments as TIFF files and run again"
    exit
fi
tif11=$1
tif22=$2
name11=${tif11%.*}
name22=${tif22%.*}
nonull11=$name11"_no_null.tif"
nonull22=$name22"_no_null.tif"
echo Start ...
echo Removing nan values for $tif11
gdal_calc.py -A $tif11 --outfile=$nonull11 --calc="nan_to_num(A)" 1>/dev/null
echo Removing nan values for $tif22
gdal_calc.py -A $tif22 --outfile=$nonull22 --calc="nan_to_num(A)" 1>/dev/null
echo Make bounding box
gdal_merge.py -ot Float32 -of GTiff -o mergedbox.tif $nonull11 $nonull22
echo All values of the bouding box to zero
gdal_calc.py --calc "A*0" --format GTiff --type Float32 -A mergedbox.tif --A_band 1 --outfile mergedbox000.tif 1>/dev/null
echo Put $tif11 to bounding box
gdal_merge.py -ot Float32 -of GTiff -o tif11_to_mergedbox.tif mergedbox000.tif $nonull11
echo Put $tif22 to bounding box
gdal_merge.py -ot Float32 -of GTiff -o tif22_to_mergedbox.tif mergedbox000.tif $nonull22
echo Final merging
gdal_calc.py --calc "A+B" --format GTiff -A tif11_to_mergedbox.tif -B tif22_to_mergedbox.tif  --A_band 1 --B_band 1 --outfile final_merged.tif 1>/dev/null
echo --- final_merged.tif has been generated! ---
echo removing pre-processed files ...
rm mergedbox*.tif *no_null.tif *_to_mergedbox.tif
echo End
