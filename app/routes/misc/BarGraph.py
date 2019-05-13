import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class Bar:

    def __init__(self):

        self.x = None
        self.y = None
        self.fig = Bar.figure(self)[0]
        self.ax = Bar.figure(self)[1]

    def figure(self):

        fig, ax = plt.subplots()

        return fig, ax

    def setaxis(self, x, y):

        self.x = x
        self.y = y

    def graph(self):

        self.ax.bar(self.x, self.y)
        cd = os.getcwd()
        plt.savefig(cd.replace('\\', '/') + "/app/static/sample.png")


