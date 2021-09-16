import pandas as pd
import requests
import jinja2
from io import BytesIO
from datetime import date

TEMPLATE_FILE = "tei-template.xml"
GDRIVE_BASE_URL = "https://docs.google.com/spreadsheet/ccc?key="


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)


def gsheet_to_df(sheet_id):
    url = f"{GDRIVE_BASE_URL}{sheet_id}&output=csv"
    r = requests.get(url)
    print(r.status_code)
    data = r.content
    df = pd.read_csv(BytesIO(data))
    return df


def row_to_dict(df):
    row = df.iloc[0]
    item = {
        "id": row['image_id'],
        "file_name": f"amp-transkript__{row['image_id']:04}.xml",
        "title": row['document_title'],
        "sender": row['document_author'],
        "sender_id": "wha",
        "receiver": "Stella Musulin",
        "receiver_id": "sm",
        "lang_code": 'en',
        "language": "English",
        "date": row['document_date'],
        "idno": row['container'],
        "pages": [],
        "current_date": f"{date.today()}"
    }
    return item


def create_templates(done, prefix="amp-transcript__"):
    for gr, df in done.groupby('document_id'):
        file_name = f"{prefix}{int(gr):04}.xml"
        print(file_name)
        item = row_to_dict(df)
        with open(file_name, 'w') as f:
            for i, row in df.iterrows():
                scan_id = row["image_id"]
                scan_id_padd = f"amp-scan__{scan_id:04}.tif"
                item['pages'].append(
                    {
                        "id": scan_id_padd,
                        "p_type": row['object_type'],
                        "width": row['image_width'],
                        "height": row['image_height'],
                        "url": f"https://iiif.acdh.oeaw.ac.at/amp/amp_{scan_id:04}/"
                    }
                )
            f.write(template.render(**item))
    return done
