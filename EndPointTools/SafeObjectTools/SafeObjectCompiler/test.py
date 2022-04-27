import pandas as pd
import numpy as np
import sys, pickle
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_curve
from typing import List, Tuple

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)

def read_csv(filename):
    df = pd.read_csv(filename)
    return df

def to_numpy(df):
    return df.to_numpy()

def Run(y_ture: np.ndarray, y_calc: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray, [True,True,True]):
    precision, recall, thresholds = precision_recall_curve(y_true, y_calc)
    return precision, recall, thresholds

def Run1(arg_0: float, arg_1: float) -> List[float]:
    return [arg_0, arg_1]

def Run2(arg_0: float, arg_1: float) -> Tuple[float, float]:
    '''
    Confidentiality: True, Ture
    '''
    return arg_0, arg_1
