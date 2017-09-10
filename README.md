# picorg
A set of scripts to organize my pictures. Tested with Python 3.6.0 on Windows 7 64-bit.

## settings.json
The settings for the scripts.

## rename.py
Renames all images in a folder. It tries to use the timestamp of when the image was taken.

## duplicates.py
Traverses all folders in the setting file and tries to find any duplicates (by filename).

## thumbs.py
Creates thumbnails of all images. Each thumbnail is stored in a subfolder called `.picorg_thumbs`.
