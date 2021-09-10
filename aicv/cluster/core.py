from __future__ import division
from __future__ import print_function
import numpy as np
import sklearn.impute

import aicv.cluster.core
# import aicv.cluster.AbstractClusterAlg
import aicv.cluster.leiden


def normalize_features(raw_features):
    # for clustering purposes, we standardize each feature by subtracting mean and
    # dividing by standard deviation
    normalized_features = (raw_features - np.nanmean(raw_features, axis=0)) / np.nanstd(raw_features, axis=0)
    return normalized_features


def impute_features(normalized_features):
    #  for completing missing values using k-Nearest Neighbors
    imputed_features = np.array(sklearn.impute.KNNImputer(
        missing_values=np.nan,
        n_neighbors=5,
        weights='distance').fit_transform(normalized_features))  # .transpose((1, 0))
    return imputed_features


def normalize_and_impute_features(raw_features):
    normalized_features = normalize_features(raw_features=raw_features)
    imputed_features = impute_features(normalized_features=normalized_features)
    return imputed_features


class BaseClusterAlg(object):

    def __init__(self, cols_to_cluster, data_frame):
        self.cols_to_cluster = [data_frame.resolve_columnname(c) for c in cols_to_cluster]
        self.data_frame = data_frame.get_dataframe()
        raw_features = np.array(self.data_frame[self.cols_to_cluster])
        self.normalized_and_imputed_features = aicv.cluster.core.normalize_and_impute_features(
            raw_features=raw_features)

    def get_clusters(self, **kwargs):
        clusters = self(features=self.normalized_and_imputed_features,
                        **kwargs)
        return clusters
        # return self.normalized_and_imputed_features

    def add_tsne_to_df(self, tsne_perplexity, ax1_name="tsne_ax1",
                              ax2_name="tsne_ax2"):
        if "tsne_ax1" not in list(self.data_frame.columns):
            embeddings = sklearn.manifold.TSNE(perplexity=tsne_perplexity,
                                               random_state=123).fit_transform(self.normalized_and_imputed_features)
            self.data_frame[ax1_name] = embeddings[:, 0]
            self.data_frame[ax2_name] = embeddings[:, 1]

    # data_frame is an instance of
    # aicv.core.DataFrame
    # cols_to_cluster is a list of columns that you're going to cluster
    # new_col_name is the new column in the data frame that you will store
    # the clustering results to
    def add_clusters_to_df(self, new_col_name="clusters"):
        clusters = self.get_clusters()
        self.data_frame[new_col_name] = clusters

    # features is a numpy array of dims num_examples x num_features
    # returns the integer clusters
    def __call__(self, features, **kwargs):
        raise NotImplementedError()
