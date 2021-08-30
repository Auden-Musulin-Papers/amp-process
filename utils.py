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
        "id": row['id'],
        "file_name": f"amp-transkript__{row['id']:04}.xml",
        "title": row['has_title'],
        # "sender": row['author'],
        "sender": "H. W. Auden",
        "sender_id": "hwa",
        "receiver": "Stella Musulin",
        "receiver_id": "sm",
        "lang_code": 'en',
        "language": "english",
        "date": row['has_created_start_date_original'],
        "idno": row['archive_folder'],
        "pages": [],
        "current_date": f"{date.today()}"
    }
    return item


def create_templates(done, prefix="amp-transkript__"):
    for gr, df in done.groupby('document'):
        file_name = f"{prefix}{int(gr):04}.xml"
        print(file_name)
        item = row_to_dict(df)
        with open(file_name, 'w') as f:
            for i, row in df.iterrows():
                scan_id = row["id"]
                scan_id_padd = f"amp-scan__{scan_id:04}.tif"
                item['pages'].append(
                    {
                        "id": scan_id_padd,
                        "p_type": row['document_type'],
                        "width": row['width'],
                        "height": row['height'],
                        "url": f"https://iiif.acdh.oeaw.ac.at/amp/amp_{scan_id:04}/"
                    }
                )
            f.write(template.render(**item))
    return done
