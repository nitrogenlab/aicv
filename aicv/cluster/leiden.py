import leidenalg
import scipy
import sklearn.manifold
import numpy as np
from .core import BaseClusterAlg


class LeidenCluster(BaseClusterAlg):

    def __call__(self, features, perplexity):
        return run_leiden_using_tsneadapted_distances(
            features=features, perplexity=perplexity)


# From: https://github.com/theislab/scanpy/blob/8131b05b7a8729eae3d3a5e146292f377dd736f7/scanpy/_utils.py#L159
def get_igraph_from_adjacency(adjacency, directed=None):
    """Get igraph graph from adjacency matrix."""
    import igraph as ig
    sources, targets = adjacency.nonzero()
    weights = adjacency[sources, targets]
    if isinstance(weights, np.matrix):
        weights = weights.A1
    g = ig.Graph(directed=directed)
    g.add_vertices(adjacency.shape[0])  # this adds adjacency.shap[0] vertices
    g.add_edges(list(zip(sources, targets)))
    try:
        g.es['weight'] = weights
    except:
        pass
    if g.vcount() != adjacency.shape[0]:
        print('WARNING: The constructed graph has only '
              + str(g.vcount()) + ' nodes. '
                                  'Your adjacency matrix contained redundant nodes.')
    return g


def run_leiden_community_detection(affinity_matrix, seed):
    the_graph = get_igraph_from_adjacency(affinity_matrix)
    partition = leidenalg.find_partition(
        the_graph, leidenalg.ModularityVertexPartition,
        weights=(np.array(the_graph.es['weight'])
                 .astype(np.float64)),
        n_iterations=-1,
        seed=seed)
    return partition


def run_leiden_with_multiple_seeds_and_take_best(affinity_matrix, num_seeds):
    best_quality = None
    for seedidx in range(num_seeds):
        partition = run_leiden_community_detection(affinity_matrix, seedidx * 100)
        quality = partition.quality()
        if ((best_quality is None) or (quality > best_quality)):
            best_quality = quality
            best_clustering = np.array(partition.membership)
    return best_clustering


# This idea of running leiden on t-sne adapted distances is based on the
# approach used in the TF-MoDISco algorithm:
# https://arxiv.org/abs/1811.00416
def run_leiden_using_tsneadapted_distances(features, perplexity):
    pairwise_distances = scipy.spatial.distance.squareform(
        scipy.spatial.distance.pdist(X=features))
    affmat = sklearn.manifold._utils._binary_search_perplexity(
        pairwise_distances.astype("float32"), perplexity, False)
    # symmetrize affinity matrix by addition
    affmat = affmat + affmat.T
    # run louvain with 3 random seeds and take the best one
    leiden_clusters = run_leiden_with_multiple_seeds_and_take_best(
        affinity_matrix=affmat, num_seeds=3)
    return leiden_clusters
