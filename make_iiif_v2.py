import os
import json

from utils import gsheet_to_df


IIIF_SERVER_URL = "https://iiif.acdh.oeaw.ac.at/amp/"
PROJECT_URI = "https://auden-musulin"
PROJECT_MD = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": "https://auden-musulin-papers.github.io/amp-process/manifest2.json",
    "@type": "Manifest",
    "label": {
        "en": [
            "Scans from Auden Musulin Project"
        ]
    },
    "description": "Stella Musulin (1915-1996), née Stella Lloyd-Philipps, was a Welsh-Austrian writer, translator, journalist and broadcaster. Resident at the Musulin family estate at Schloss Fridau, Ober-Grafendorf, and Vienna, she was one of the closest friends of the Anglo-American poet W. H. Auden (1907-1973), with whom she corresponded frequently from the early 1960s, when Auden had settled in Kirchstetten, Lower Austria, until his death. The letters and literary papers by Auden preserved in Musulin’s estate provide revealing insights into one of Auden’s most prolific creative periods and Austria’s complex political, social and cultural history in the 1960s and 70s.",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Austrian Centre for Digitial Humanities and Cultural Heritage",
    "logo": "https://shared.acdh.oeaw.ac.at/acdh-common-assets/images/acdh-ch-logo-with-text-grayscale.png",

    "viewingDirection": "left-to-right",
    "viewingHint": "paged",
    "navDate": "2020-05-18T12:18:43Z",
    "sequences": [
        {
            "@id": "https://iiifpresentation.acdh.oeaw.ac.at/margins/sequence/normal",
            "@type": "sc:Sequence",
            "label": "Current Page Order",
            "viewingDirection": "left-to-right",
            "viewingHint": "paged",
            "canvases": []
        }
    ]
}
SHEET_ID = os.environ.get('SHEETID')
df = gsheet_to_df(SHEET_ID)


for i, x in df[df['image_width'].notna()].iterrows():
    image_id = f"amp_{x['image_id']:04}"
    label = f"{x['document_title']} ({x['object_type']}); ID: {image_id}"
    item = {
        "@id": f"{PROJECT_URI}/canvas/{image_id}",
        "@type": "sc:Canvas",
        "label": image_id,
        "height": x['image_width'],
        "width": x['image_width'],
        "images": [
            {
                "@id": f"{PROJECT_URI}/{image_id}",
                "@type": "oa:Annotation",
                "motivation": "sc:painting",
                "resource": {
                    "@id": f"{IIIF_SERVER_URL}{image_id}/full/max/0/default.jpg",
                    "@type": "dctypes:Image",
                    "format": "image/jpeg",
                    "height": x['image_width'],
                    "width": x['image_width'],
                },
                "on": f"{PROJECT_URI}/canvas/{image_id}"
            }
        ]
    }
    PROJECT_MD['sequences'][0]['canvases'].append(item)

with open('manifestv2.json', 'w') as f:
    f.write(json.dumps(PROJECT_MD))
