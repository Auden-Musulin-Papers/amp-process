# amp-process
repo for processing scripts

## install

* install requirements `pip install -r requirements.txt`
* set environemt variables, e.g. copy `.dumm-env` to `.env` modify it and run e.g `source .env`


## copy_process.sh

copies images from resource-share to local disc and converts and compresses them

```shell
source .env
./copy_process.sh
```


## create_templates.py

simple script to create XML-TEI templates for each document

```shell
source .env
python create_templates.py
```

## create manifest.json

simple script which parses an image directory (set via env-variable `$IMG`) and creates a IIIF Manifest-JSON

```shell
source .env
python make_iiif.py
```

## get image size

script reading image size from binaries and writes them into a csv

```shell
source .env
python get_image_size.py
```