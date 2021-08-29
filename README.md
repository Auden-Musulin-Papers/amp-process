# amp-process
repo for processing scripts

## install

* install requirements `pip install -r requirements.txt`
* set environemt variables, e.g. copy `.dumm-env` to `.env` modify it and run e.g `source .env`


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