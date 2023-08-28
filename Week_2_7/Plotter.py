import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Plotter():

    def sensor_anomalies_plotter(self, df, sensor_names, column_name='machine_status',
                                  anomaly_method_name=None):
        """
        This plot sketch the plot performance, recovery part,
        broken part, and the prediction part
        """
        # seperate Broken and Recovering values
        broken_rows = df[df[column_name] == 'BROKEN']
        recovery_rows = df[df[column_name] == 'RECOVERING']

        # make the figure
        fig, axes = plt.subplots(nrows=len(sensor_names), ncols=1,
                                  figsize=(25, 3*len(sensor_names)))

        # Flatten the axes array if it's not already 1D
        if len(sensor_names) == 1:
            axes = [axes]

        else:
            axes = axes.flatten()

        # sketch the plot for each sensor in the list
        for number, ax in enumerate(axes):

            # plot the main line plot
            ax.plot(df[sensor_names[number]], color='grey')

            # assign the recovery parts as yellow
            ax.plot(recovery_rows[sensor_names[number]], linestyle='none', marker='o',
                    color='yellow', markersize=5, label='recovering', alpha=0.5)

            # Assign the broken parts as red
            ax.plot(broken_rows[sensor_names[number]], linestyle='none', marker='X',
                    color='red', markersize=20, label='broken')

            # sketch the anomaly prediction
            if anomaly_method_name is not None:
                anomaly_rows = df[df[anomaly_method_name] == -1]
                ax.plot(anomaly_rows[sensor_names[number]], linestyle='none', marker='X',
                        color='blue', markersize=7, label='anomaly predicted', alpha=0.2)

            ax.set_title(sensor_names[number])
            ax.legend()
        return fig

    def cm_plotter(self, cm, logarithm=False):
        """
        This function draws the confusion matrix in a heatmap
        """
        # use logarithm of confusion matrix if it is large
        if logarithm:
            cm = np.log(cm)

        # sketch the plot
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5), layout='constrained')

        # Create a heatmap of the confusion matrix
        sns.heatmap(cm, annot=True, cmap='Blues', ax=ax)
        ax.set(aspect='equal',
            xlabel='Predicted Labels',
            ylabel='$True Labels$')

        ax.set_title('Confusion Matrix')
        return fig

    def auc_roc_plotter(self, auc_dict):
        """
        This function draws the auc_roc curve
        """
        auc = auc_dict['auc']

        # Plot the ROC curve
        fig, ax = plt.subplots(figsize=(5, 5))  
        ax.plot(auc_dict['false_positive'], auc_dict['true_positive'], color='red',
                lw=2, label=f'ROC curve (AUC = {auc:.2f})')  
        ax.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Receiver Operating Characteristic')  
        ax.legend(loc="lower right")

        return fig
    