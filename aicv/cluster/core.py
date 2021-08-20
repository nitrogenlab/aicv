from __future__ import division
from __future__ import print_function
import numpy as np


def normalize_features(raw_features):
    #TODO
    return normalized_features


def impute_feature(normalized_features):
    #TODO
    return imputed_features 


def normalize_and_impute_features(raw_features):
    normalized_features = normalize_features(raw_features=raw_features) 
    imputed_features = impute_features(normalized_features=normalized_features) 
    return imputed_features


class BaseClusterAlg(object):

    def __init__(self, cols_to_cluster, data_frame, tsne_perplexity=None):
        self.cols_to_cluster = cols_to_cluster
        self.data_frame = data_frame
        raw_features = np.array(data_frame._pd_df[self.cols_to_cluster]) 
        self.normalized_and_imputed_features = normalize_and_impute_features(
            raw_features=raw_features) 
        self.tsne_perplexity = tsne_perplexity

    def get_clusters(self):
        clusters = self(features=self.normalize_and_impute_features)
        return clusters

    def add_tsne_to_df(self, ax1_name="tsne_ax1",
                             ax2_name="tsne_ax2"):
        embeddings = sklearn.manifold.TSNE(perplexity=self.tsne_perplexity,
                      random_state=123).fit_transform(
                       self.normalized_and_imputed_features) 
        self.data_frame._pd_df[ax1_name] = embeddings[:,0]
        self.data_frame._pd_df[ax2_name] = embeddings[:,1]

    #data_frame is an instance of
    # aicv.core.DataFrame
    # cols_to_cluster is a list of columns that you're going to cluster
    # new_col_name is the new column in the data frame that you will store
    # the clustering results to
    def add_clusters_to_df(self, new_col_name="cluster"):
        clusters = self.get_clusters() 
        self.data_frame._pd_df[new_col_name] = clusters

    #features is a numpy array of dims num_examples x num_features
    #returns the integer clusters
    def __call__(self, features):
        raise NotImplementedError()
