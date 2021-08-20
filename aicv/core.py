from __future__ import division, print_function
import pandas as pd


class DataFrame(object): #wrapper around a pandas data frame:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self._pd_df = pd.read_csv(csv_file)

    def add_derived_column(self, expression):
        self._pd_df.eval(expression)
