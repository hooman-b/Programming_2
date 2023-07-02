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

            # refactoring this for-loop into list comprehension may not be the
            # best choice here since these operations are not used to make a list,
            # they are implementing some modifications. This kind of in-place modification
            # of objects is more suitable for a loop rather than a list comprehension.
            for number, ax in enumerate(axes):

                if number%num_cols != 0:
                    ax.get_yaxis().set_visible(False)

                if number/num_cols < num_rows-1:
                    ax.get_xaxis().set_visible(False)

        # Hide unused subplots
        # The above reasoning is also correct for this loop.
        for i in range(self.plot_number, len(axes)):
            fig.delaxes(axes[i])

        line_colors = self.color_maker()

        return fig, axes, line_colors

    def data_initializer(self):
        # in this case, it seems that dictionary comprehension is a better approach.
        # Because, not only we want to make a dictionary, but also we can reduce the number of code lines.
        data_dict = {'xdata': [], **{f'y{number}data': [] for number in range(len(self.axes))}}

        return data_dict

    def update(self, data):

        try:
            self.titles_list = data[1].index
            self.data_dict['xdata'].append(data[0])

            # refactoring the following for-loop may not be the best choice
            # since this loop does not make a list. It is true that it appends
            # values to different lists in the dictionary. But by using list
            # comprehension we can make complexity.
            for  counter in range(self.plot_number):
                self.data_dict[f'y{counter}data'].append(data[1][counter])

            self.animation_luncher()

        except IndexError:
            plt.show()

    def animation_luncher(self):

        # Here again the for-loop is doing some operations that can be better to do them
        # with a loop rather than list comprehension.
        for counter in range(self.plot_number):
            self.axes[counter].clear()
            self.axes[counter].plot(self.data_dict['xdata'], self.data_dict[f'y{counter}data'],
                                    color=self.line_colors[counter])
            self.axes[counter].title.set_text(self.titles_list[counter])

        plt.pause(0.01)
        self.fig.canvas.draw()

    def color_maker(self):

        colors= list(mcolors.TABLEAU_COLORS.keys())

        # Here list comprehension can be a better choice as we 
        # are making a list, but I believe for loop is more readable.
        color_list = [colors[randint(0, len(colors)-1)] for _ in range(self.plot_number)]

        return color_list
