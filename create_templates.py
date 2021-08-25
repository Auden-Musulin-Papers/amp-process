import os
from utils import gsheet_to_df, create_templates

SHEET_ID = os.environ.get('SHEETID')
df = gsheet_to_df(SHEET_ID)
create_templates(df.query('status=="zugeordnet"'))