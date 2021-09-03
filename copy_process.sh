# bin/bash

echo "copy images from $SOURCE/*.tif into $IMG_TIF"
cp $SOURCE/*.tif -n $IMG_TIF
echo "copy done"
echo $(ls $IMG_TIF | wc -l) "images in $IMG_TIF"
echo "start creating jpgs"
for f in $IMG_TIF/*.tif; do  echo "Converting $f to $IMG/$(basename "$f" .tif).jpg"; convert  -quality 50% "$f"  "$IMG/$(basename "$f" .tif).jpg"; done