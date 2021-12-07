import numpy as np
from sklearn.metrics import precision_recall_curve

__precision, __recall, __thresholds = precision_recall_curve(__y_true, __probas_pred, pos_label=__pos_label, sample_weight=__sample_weight)

print("Precision Recall Execution OK")

