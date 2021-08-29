import os
import glob
import json

from PIL import Image

IIIF_SERVER_URL = "https://iiif.acdh.oeaw.ac.at/amp/"
PROJECT_URI = "https://auden-musulin"
PROJECT_MD = {
    "@context": "http://iiif.io/api/presentation/3/context.json",
    "id": f"{PROJECT_URI}/manifest.json",
    "type": "Manifest",
    "label": {
        "en": [
            "Scans from Auden Musulin Project"
        ]
    },
    "behavior": [
        "non-paged"
    ],
    "items": []
}
IMG_DIR = os.environ.get('IMG', '')
glob_pattern = f"{IMG_DIR}/*.jpg"
print(glob_pattern)
images = sorted(glob.glob(glob_pattern))


def yield_img_dict(images):
    for x in images:
        item = {}
        item['id'] = os.path.basename(x).split('.')[0]
        with Image.open(x) as image:
            item['width'], item['height'] = image.width, image.height
        yield item


for x in yield_img_dict(images):
    item = {
        "id": f"{PROJECT_URI}/canvas/{x['id']}",
        "type": "Canvas",
        "label": {
            "en": [
                f"ID: {x['id']}"
            ]
        },
        "height": x['height'],
        "width": x['width'],
        "items": [
            {
                "id": f"{PROJECT_URI}/",
                "type": "AnnotationPage",
                "items": [
                    {
                        "id": f"{PROJECT_URI}/{x['id']}",
                        "type": "Annotation",
                        "motivation": "painting",
                        "body": {
                            "id": f"{IIIF_SERVER_URL}{x['id']}/full/max/0/default.jpg",
                            "type": "Image",
                            "format": "image/jpeg",
                            "height": x['height'],
                            "width": x['width'],
                            "service": [
                                {
                                    "id": f"{IIIF_SERVER_URL}{x['id']}",
                                    "type": "ImageService3",
                                    "profile": "level1"
                                }
                            ]
                        },
                        "target": f"{PROJECT_URI}/canvas/{x['id']}"
                    }
                ]
            }
        ]
    }
    PROJECT_MD['items'].append(item)

with open('manifest.json', 'w') as f:
    f.write(json.dumps(PROJECT_MD))
