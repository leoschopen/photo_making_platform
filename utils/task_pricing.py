import numpy as np
import pandas as pd
from keras.models import Sequential,load_model

model = load_model('my_model.h5')
print(model.summary())