from __future__ import division, print_function
import pandas as pd
import numpy as np


class DataFrame(object):  # wrapper around a pandas data frame:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self._pd_df = pd.read_csv(csv_file)
        self._column_names = self.get_column_names()
        self._colnames_map = {}
        self._colnames_old_new_map = {}

    def get_dataframe(self):
        return self._pd_df

    def add_derived_column(self, expression):
        self._pd_df.eval(expression, inplace=True)

    def get_column_names(self):
        return list(self._pd_df.columns)

    def map_columns(self, column_names_map):
        self._colnames_map = column_names_map
        self._remap_colnames(self._pd_df, self._colnames_map)
        for new_col, orig_col in column_names_map.items():
            self._colnames_old_new_map[orig_col] = new_col
        self._pd_df.rename(columns=self._colnames_old_new_map, inplace=True)
        self._column_names = self.get_column_names()

    def _remap_colnames(self, df, colnames_map):
        df = pd.DataFrame(dict([
            (orig_col, np.array(df[orig_col]))
            for new_col, orig_col in colnames_map.items()]))
        return df

    def resolve_columnname(self, name):
        if name in self._colnames_old_new_map:
            return self._colnames_old_new_map[name]
        # if name in self._colnames_map:
        #     return self._colnames_map[name]
        return name
