# pylint: disable=E1101
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
from matplotlib.widgets import Button
from random import randint
import math

class Animation():

    def __init__(self, consuming_class):

        self.consuming_class = consuming_class
        self.average_number = 0
#        self.titles = ''
        self.fig, self.axes, self.line = self.subplot_maker()

        self.data_dict = self.data_initializer()


        self.paused = False


    def animation_luncher(self):
        ani = animation.FuncAnimation(self.fig, self.run,
                                           self.consuming_class.update,
                                           init_func=self.animation_initializer,
                                            interval=300, repeat=False)
    
        self.pause_button_ax = plt.axes([0.95, 0.49, 0.05, 0.05])
        self.pause_button = Button(self.pause_button_ax, 'Pause')
        self.pause_button.on_clicked(self.toggle_pause)

        plt.show()
    

    def subplot_maker(self):
        plot_numbers = 1 #self.consuming_class.average_number
        titles_list = 'year' #self.consuming_class.reader.csv_converter.keys
        print(plot_numbers)
        num_rows = math.ceil(math.sqrt(plot_numbers))
        num_cols = math.ceil(plot_numbers / num_rows)
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10,7))
        fig.tight_layout()

        # Flatten the axes array if it's not already 1D
        if plot_numbers == 1:
            axes.title.set_text(titles_list[0])
            axes = [axes]

        else:
            axes = axes.flatten()

            for number, ax in enumerate(axes):
                ax.title.set_text(titles_list[number+1])

                if number%num_cols != 0:
                    ax.get_yaxis().set_visible(False)

                if number/num_cols < num_rows-1:
                    ax.get_xaxis().set_visible(False)

        # Hide unused subplots
        for i in range(plot_numbers, len(axes)):
            fig.delaxes(axes[i])

        line = []
        for ax in axes:
            sub_line, = ax.plot([], [], self.color_maker(), lw=2)
            line.append(sub_line)

        return fig, axes, line

    def data_initializer(self):
        data_dict = {}
        data_dict['xdata'] = []
        for number in range(len(self.axes)):
            data_dict[f'y{number}data'] = []

        return data_dict

    def animation_initializer(self):
        for ax in self.axes:
            ax.set_ylim(-1., 1.1)
            ax.set_xlim(1880, 1930)

    def run(self, data):
        if self.paused:
            # Return the line without updating the data
            return self.line,  
        x_axis, y_axis = data

        self.data_dict['xdata'].append(x_axis)

        for counter, y_i_data in enumerate(list(self.data_dict.values())[1:]):
            try:
                y_i_data.append(y_axis[counter])

            except IndexError:
                y_i_data.append(None)

        for ax in self.axes:
            xmin, xmax = ax.get_xlim()

            if x_axis >= xmax:
                ax.set_xlim(xmin, xmax + 50)
                ax.figure.canvas.draw()

        for counter, line_i in enumerate(self.line):
            line_i.set_data(self.data_dict['xdata'], self.data_dict[f'y{counter}data'])

        return self.line

    def toggle_pause(self, *args, **kwargs):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.label.set_text('Resume')
        else:
            self.pause_button.label.set_text('Pause')

    def color_maker(self):
        color_list= list(mcolors.TABLEAU_COLORS.keys())
        rand_int1 = randint(0, len(color_list)-1)
        return color_list[rand_int1]

