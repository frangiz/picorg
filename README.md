# picorg
A set of scripts to organize pictures. Tested with Python 3.6.0 on Windows 7 64-bit.

## Installation
Install dependencies with `pip3 install -r requirements.txt`.

## The src folder
You will find all you need in the src-folder.

* `rename.py` renames all images in the current working directory. It tries to use the timestamp of when the image was taken from the EXIF data. All renamed files will be moved to a folder called **OK**, and if the script cannot find a suitable name, the file will be moved to the **NOK** folder.
* `duplicates.py` traverses all folders listed in the settings.json file and lists all duplicated filenames and where to find them. Useful when using more than one root folder for your pictures.

## Configuration
A settings file is created in <USER_HOME>/.picorg that stores the users settings.