import xgboost as xbg
import numpy as np

__X = __X.to_numpy()
data = xgb.DMatrix(np.asarray(__X))
__pred = __model.predict(data)
