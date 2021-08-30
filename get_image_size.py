import glob
import os

import pandas as pd

from make_iiif import yield_img_dict


IMG_DIR = os.environ.get('IMG', '')
images = sorted(glob.glob(f"{IMG_DIR}/*.jpg"))

df = pd.DataFrame(yield_img_dict(images), columns=['id', 'width', 'height'])
df.to_csv('out.csv', index=False)
