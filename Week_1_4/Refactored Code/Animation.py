# pylint: disable=E1101
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from random import randint
import math
from Subject import SecondLayerObserver

class Animation(SecondLayerObserver):
    def __init__(self, plot_num):
        SecondLayerObserver.__init__(self)
        self.plot_number = plot_num
        self.titles_list = []
        self.fig, self.axes, self.line_colors = self.subplot_maker()
        self.data_dict = self.data_initializer()
  
    def subplot_maker(self):
        num_rows = math.ceil(math.sqrt(self.plot_number))
        num_cols = math.ceil(self.plot_number / num_rows)
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10,7))
        fig.tight_layout()

        # Flatten the axes array if it's not already 1D
        if self.plot_number == 1:
            axes = [axes]

        else:
            axes = axes.flatten()

            for number, ax in enumerate(axes):

                if number%num_cols != 0:
                    ax.get_yaxis().set_visible(False)

                if number/num_cols < num_rows-1:
                    ax.get_xaxis().set_visible(False)

        # Hide unused subplots
        for i in range(self.plot_number, len(axes)):
            fig.delaxes(axes[i])

        line_colors = self.color_maker()

        return fig, axes, line_colors

    def data_initializer(self):
        data_dict = {}
        data_dict['xdata'] = []

        for number in range(len(self.axes)):
            data_dict[f'y{number}data'] = []

        return data_dict

    def update(self, data):

        try:
            self.titles_list = data[1].index
            self.data_dict['xdata'].append(data[0])

            for  counter in range(self.plot_number):
                self.data_dict[f'y{counter}data'].append(data[1][counter])

            self.animation_luncher()

        except IndexError:
            plt.show()

    def animation_luncher(self):

        for counter in range(self.plot_number):
            self.axes[counter].clear()
            self.axes[counter].plot(self.data_dict['xdata'], self.data_dict[f'y{counter}data'],
                                    color=self.line_colors[counter])
            self.axes[counter].title.set_text(self.titles_list[counter])

        plt.pause(0.01)
        self.fig.canvas.draw()

    def color_maker(self):
        color_list = []
        colors= list(mcolors.TABLEAU_COLORS.keys())

        for counter in range(self.plot_number):
            rand_int1 = randint(0, len(colors)-1)
            color_list.append(colors[rand_int1])

        return color_list
