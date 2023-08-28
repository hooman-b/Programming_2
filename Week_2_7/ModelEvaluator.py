import numpy as np
from sklearn.metrics import precision_score, recall_score, confusion_matrix, roc_curve, auc

class ModelEvaluator():
    """
    Type: A class for evaluating model predictions using various metrics.
    Explanation: This class provides methods to calculate precision, recall, F-score,
    confusion matrix, accuracy, and AUC-ROC metrics based on actual and predicted labels.
    Attributes: 1. y_actual (array-like): The transformed actual labels (binary format).
                2. y_pred (array-like): The predicted labels.
                3. metric_names (list): List of metric names to calculate.
    """

    def __init__(self, y_raw, y_pred, metric_names):
        """
        Input: 1. y_raw (array-like): The actual labels (ground truth).
               2. y_pred (array-like): The predicted labels.
               3. metric_names (list): List of metric names to calculate.
        Explanation: Initialize the Normalization object.
        """
        self.y_actual = self.y_transformer(y_raw)
        self.y_pred = y_pred
        print('1:',list(self.y_pred).count(1),'-1:',list( self.y_pred).count(-1), np.unique(self.y_pred))
        self.metric_names = metric_names

    def y_transformer(self, y_raw):
        """
        Input: 1. y_raw (array-like): The actual labels (ground truth).
        Explanation: Transform raw labels to binary format.     
        Output: 1. (array-like): Transformed labels in binary format.
        """
        y_trans = [1 if element=='NORMAL' else -1 for element in y_raw]
        return y_trans

    def precision(self):
        """
        Explanation: Calculate precision.
        Output: 1. (float): Precision score.
        """
        return precision_score(self.y_actual, self.y_pred)

    def recall(self):
        """
        Explanation: Calculate recall.
        Output: 1. (float): Recall score.
        """
        return recall_score(self.y_actual, self.y_pred)
  
    def f_score(self):
        """
        Explanation: Calculate F-score.
        Output: 1. (float): F-score.
        """
        pre = self.precision()
        rec = self.recall()

        f_score = (2.0 * pre * rec) / (pre + rec)

        return f_score

    def confusion(self):
        """
        Explanation: Calculate confusion matrix.
        Output: 1. (array-like): Confusion matrix.
        """
        return confusion_matrix(self.y_actual, self.y_pred)

    def accuracy(self):
        """
        Explanation: Calculate accuracy.
        Output: 1. (float): Accuracy score.
        """
        cm = confusion_matrix(self.y_actual, self.y_pred)

        acc = (cm[0,0] + cm[1,1]) / (cm[0,0] + cm[0,1] + cm[1,0] + cm[1,1])

        return acc

    def auc_roc(self):
        """
        Explanation: Calculate AUC-ROC.
        Output: 1. (dict): A dictionary containing false positive rates,
                   true positive rates, thresholds, and AUC score.
        """
        fp, tp, threshold = roc_curve(self.y_actual, self.y_pred)
        area = auc(fp, tp)

        auc_roc_dict = {
                        'false_positive': fp,
                        'true_positive': tp,
                        'threshold': threshold,
                        'auc': area
                        }
        return auc_roc_dict

    def evaluation_metrics_calculator(self):
        """
        Explanation: Calculate multiple evaluation metrics.

        
        Output: 1. (dict): A dictionary containing calculated evaluation metrics
                           based on metric names.

        """
        evaluation_dict = {name:getattr(self, name)() for name in self.metric_names}
        # return the evaluation dictionary
        return evaluation_dict