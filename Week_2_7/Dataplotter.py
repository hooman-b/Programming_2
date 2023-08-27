import pandas as pd
import matplotlib.pyplot as plt

class DataPlotter():

    def plot_sensor_anomalies(self, df, sensor_names, column_name='machine_status', anomaly_method_name=None):
        broken_rows = df[df[column_name] == 'BROKEN']
        recovery_rows = df[df[column_name] == 'RECOVERING']

        fig, axes = plt.subplots(nrows=len(sensor_names), ncols=1, figsize=(25, 3*len(sensor_names)))

        # Flatten the axes array if it's not already 1D
        if len(sensor_names) == 1:
            axes = [axes]

        else:
            axes = axes.flatten()

        for number, ax in enumerate(axes):
            
            ax.plot(df[sensor_names[number]], color='grey')
            ax.plot(recovery_rows[sensor_names[number]], linestyle='none', marker='o',
                    color='yellow', markersize=5, label='recovering', alpha=0.5)
            ax.plot(broken_rows[sensor_names[number]], linestyle='none', marker='X',
                    color='red', markersize=20, label='broken')

            if anomaly_method_name is not None:
                anomaly_rows = df[df[anomaly_method_name] == -1]
                ax.plot(anomaly_rows[sensor_names[number]], linestyle='none', marker='X',
                        color='blue', markersize=7, label='anomaly predicted', alpha=0.2)

            ax.set_title(sensor_names[number])
            ax.legend()
        return fig