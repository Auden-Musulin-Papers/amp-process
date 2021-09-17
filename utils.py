import pandas as pd
import requests
import jinja2
from io import BytesIO
from datetime import date
from dateutil.parser import parse, ParserError
from slugify import slugify


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
    doc_title = row['document_title']
    if "Letter Signed W. H" in doc_title:
        is_letter = True
    else:
        is_letter = False
    written_date = row['document_date']
    try:
        parsed_date = parse(written_date)
    except ParserError:
        parsed_date = None
    item = {
        "id": row['image_id'],
        "file_name": f"amp-transkript__{row['image_id']:04}.xml",
        "title": row['document_title'],
        "sender": row['document_author'],
        "sender_id": f"{slugify(row['document_author'])}",
        "receiver": "Musulin, Stella",
        "receiver_id": f"{slugify('Musulin, Stella')}",
        "lang_code": 'en',
        "language": "English",
        "written_date": written_date,
        "parsed_date": parsed_date,
        "idno": row['container'],
        "pages": [],
        "current_date": f"{date.today()}",
        "is_letter": is_letter
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
