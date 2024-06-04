import pandas as pd
import numpy as np
from PIL import Image
root = r'F:\datasets\driving\driving\ann\train\0.png'
image = np.array(Image.open(root))
print(image)
pd.DataFrame(image).to_excel('test.xlsx')