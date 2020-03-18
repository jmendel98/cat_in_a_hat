# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:09:17 2020

@author: kkapr
"""
import numpy as np
import pickle

from scipy.stats import kurtosis,skew,iqr
from scipy.linalg import norm

def extract_minfeatures(df_full,model_in = False):
    bad_cols = df_full.isna().any()
    bad_cols = bad_cols[bad_cols]

    df_full= df_full.drop(bad_cols.index,axis=1)
    y = df_full['gesture_num']
    df_full = df_full.drop(['gesture_num','MAGzs','MAGys','MAGxs'],axis=1)
    top_inputs = np.load("top_inputs.npy")
    top_inputs = top_inputs.tolist()
    # print(list(top_inputs))
    # print(list(df_full))
    for label,content in df_full.items():
        mean_label = label+"_mean"
        std_label = label+"_std"
        # norm_label = label+"_norm"
        # kurtosis_label = label+"_kurtosis"
        # max_label = label+"_max"
        # min_label = label+"_min"
        # skew_label = label+"_skew"
        # iqr_label = label+"_iqr"
        df_full[mean_label]=df_full[label].map(lambda x: np.mean(np.asarray(x,dtype=np.float)))
        df_full[std_label]=df_full[label].map(lambda x: np.std(np.asarray(x,dtype=np.float)))
        # df_full[norm_label]=df_full[label].map(lambda x: norm(np.asarray(x,dtype=np.float)))
        # df_full[kurtosis_label]=df_full[label].map(lambda x: kurtosis(np.asarray(x,dtype=np.float)))
        # df_full[max_label]=df_full[label].map(lambda x: np.max(np.asarray(x,dtype=np.float)))
        # df_full[min_label]=df_full[label].map(lambda x: np.min(np.asarray(x,dtype=np.float)))
        # # df_full[skew_label]=df_full[label].map(lambda x: skew(np.asarray(x,dtype=np.float)))
        # df_full[iqr_label]=df_full[label].map(lambda x: iqr(np.asarray(x,dtype=np.float)))
             


    df_stats = df_full.select_dtypes(include=[np.number])
   # df_drop = df_stats.drop(['gesture_num','gesture_num_mean','gesture_num_std'],axis=1)
    df_drop = df_stats
    if(model_in):
        use_index = list(df_drop)
        pickle.dump(use_index,open("use_index.pkl",'wb'))
    if(model_in==False):
        use_index = pickle.load(open("use_index.pkl",'rb'))
        df_drop = df_drop[use_index]
    df_drop = df_drop[top_inputs]
    x = np.array(df_drop)
    y= np.array(y)
    return x,y



def extract_features(df_full,model_in = False):
    bad_cols = df_full.isna().any()
    bad_cols = bad_cols[bad_cols]

    df_full= df_full.drop(bad_cols.index,axis=1)
    y = df_full['gesture_num']
    df_full = df_full.drop(['gesture_num'],axis=1)
    df_full = df_full.drop(['MAGzs','MAGys','MAGxs'],axis=1)
    for label,content in df_full.items():
        mean_label = label+"_mean"
        std_label = label+"_std"
        # norm_label = label+"_norm"
        # kurtosis_label = label+"_kurtosis"
        # max_label = label+"_max"
        # min_label = label+"_min"
        # skew_label = label+"_skew"
        # iqr_label = label+"_iqr"
        df_full[mean_label]=df_full[label].map(lambda x: np.mean(np.asarray(x,dtype=np.float)))
        df_full[std_label]=df_full[label].map(lambda x: np.std(np.asarray(x,dtype=np.float)))
        # df_full[norm_label]=df_full[label].map(lambda x: norm(np.asarray(x,dtype=np.float)))
        # df_full[kurtosis_label]=df_full[label].map(lambda x: kurtosis(np.asarray(x,dtype=np.float)))
        # df_full[max_label]=df_full[label].map(lambda x: np.max(np.asarray(x,dtype=np.float)))
        # df_full[min_label]=df_full[label].map(lambda x: np.min(np.asarray(x,dtype=np.float)))
        # df_full[skew_label]=df_full[label].map(lambda x: skew(np.asarray(x,dtype=np.float)))
        # df_full[iqr_label]=df_full[label].map(lambda x: iqr(np.asarray(x,dtype=np.float)))
             


    df_stats = df_full.select_dtypes(include=[np.number])
   # df_drop = df_stats.drop(['gesture_num','gesture_num_mean','gesture_num_std'],axis=1)
    df_drop = df_stats
    if(model_in):
        use_index = list(df_drop)
        pickle.dump(use_index,open("use_index.pkl",'wb'))
    if(model_in==False):
        use_index = pickle.load(open("use_index.pkl",'rb'))
        df_drop = df_drop[use_index]
    
    x = np.array(df_drop)
    y= np.array(y)
    return x,y