import time
import math
import datetime
import os
import sys
import select
import pandas as pd
import os.path
import numpy as np
from os import path

from gesture_utils import extract_features,extract_minfeatures
df = pd.read_csv('gesture_data2.csv')

df_class = df.groupby(['gesture_num']).mean()

df_full = pd.read_pickle("gesture_data.pkl")


num_each = df_full["gesture_num"].value_counts()
  
# for label,content in df_full.items():
#     mean_label = label+"_mean"
#     std_label = label+"_std"
#     df_full[mean_label]=df_full[label].map(lambda x: np.mean(np.asarray(x,dtype=np.float)))
#     df_full[std_label]=df_full[label].map(lambda x: np.std(np.asarray(x,dtype=np.float)))

outputs = {
    'ACCxs': [[1,2]],
    'ACCys': [[2,3,4]],
    'ACCzs': [[5,6,7,8]],
    }

df_full_class = df_full.groupby(['gesture_num']).mean()
# df_test = pd.DataFrame.from_dict(outputs)
# #x = df_test['ACCxs'][0]


# df_test.to_pickle("df_test.pkl")

# df_test2 = pd.read_pickle("df_test.pkl")
# x2 = df_test2['ACCxs'][0]

# df_stats = df_full.select_dtypes(include=[np.number])

# y = df_stats['gesture_num'].to_numpy()

# test_x = df_stats.drop(['gesture_num','gesture_num_mean','gesture_num_std'],axis=1)


# x = test_x.to_numpy()
# x2 = np.array(test_x)
# df_stats_np= df_stats.to_numpy()
use_min = 1

if(use_min):
    x,y = extract_minfeatures(df_full,model_in=True)
    np.save("x_min.npy",x)
    np.save("y_min.npy",y)
else:
    x,y = extract_features(df_full,model_in=True)
np.save("x.npy",x)
np.save("y.npy",y)