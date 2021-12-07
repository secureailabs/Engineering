import numpy as np
from sklearn.metrics import average_precision_score

__avg_precision = average_precision_score(__y_true, __y_score, pos_label=__pos_label, average=__average, sample_weight= __sample_weight )

print("Avearage Precision Success")