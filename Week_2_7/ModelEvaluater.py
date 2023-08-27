
# Metric modules
from sklearn.metrics import precision_score, recall_score, confusion_matrix, roc_curve, auc

class ModelEvaluater():

    def __init__(self, y_raw, y_pred, metric_names):
        self.y_actual = self.y_transformer(y_raw)
        self.y_pred = y_pred
        self.metric_names = metric_names

    def y_transformer(self, y_raw):
       y_trans = [1 if element=='NORMAL' else -1 for element in y_raw.iloc[:,-1]]
       return y_trans

    def precision(self):
        return precision_score(self.y_actual, self.y_pred)

    def recall(self):
        return recall_score(self.y_actual, self.y_pred)
  
    def f_score(self):

        pre = self.precision(self.y_actual, self.y_pred)
        rec = self.recall(self.y_actual, self.y_pred)

        f_score = (2.0 * pre * rec) / (pre + rec)

        return f_score

    def confusion(self):
        return confusion_matrix(self.y_actual, self.y_pred)

    def accuracy(self):

        cm = confusion_matrix(self.y_actual, self.y_pred)

        acc = (cm[0,0] + cm[1,1]) / (cm[0,0] + cm[0,1] + cm[1,0] + cm[1,1])

        return acc

    def auc_roc(self):
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

        evaluation_dict = {}
        for name in self.metric_names:
            evaluation_method = getattr(self, name)
            evaluation_dict[name] = evaluation_method()
        #evaluation_dict = {name:getattr(self, method_name)() for name in metric_names}
        # return the evaluation dictionary
        return evaluation_dict