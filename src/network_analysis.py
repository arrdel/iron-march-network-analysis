"""
Network analysis utilities for studying forum interaction networks.

This module provides functions for building and analyzing network graphs
from forum interaction data, including centrality measures and community detection.
"""

import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """Network analysis and graph construction utilities."""
    
    def __init__(self):
        """Initialize the network analyzer."""
        self.graph: Optional[nx.Graph] = None
        self.graphs: Dict[str, nx.Graph] = {}
        
    def build_interaction_graph(
        self,
        df: pd.DataFrame,
        source_col: str = 'msg_author_id',
        target_col: str = 'msg_topic_id',
        weight_col: Optional[str] = None
    ) -> nx.Graph:
        """
        Build an interaction network graph from DataFrame.
        
        Args:
            df: Input DataFrame with interaction data
            source_col: Column name for source nodes
            target_col: Column name for target nodes
            weight_col: Optional column for edge weights
            
        Returns:
            NetworkX graph object
        """
        G = nx.Graph()
        
        if weight_col:
            # Build weighted graph
            edge_weights = defaultdict(int)
            for _, row in df.iterrows():
                source = row[source_col]
                target = row[target_col]
                edge_weights[(source, target)] += row[weight_col]
            
            for (source, target), weight in edge_weights.items():
                G.add_edge(source, target, weight=weight)
        else:
            # Build unweighted graph (count interactions)
            edge_counts = defaultdict(int)
            for _, row in df.iterrows():
                source = row[source_col]
                target = row[target_col]
                edge_counts[(source, target)] += 1
            
            for (source, target), count in edge_counts.items():
                G.add_edge(source, target, weight=count)
        
        self.graph = G
        logger.info(f"Built graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        return G
    
    def build_temporal_graphs(
        self,
        df: pd.DataFrame,
        time_col: str = 'msg_date',
        time_window: str = 'M',  # Month
        source_col: str = 'msg_author_id',
        target_col: str = 'msg_topic_id'
    ) -> Dict[str, nx.Graph]:
        """
        Build temporal network graphs based on time windows.
        
        Args:
            df: Input DataFrame with temporal data
            time_col: Column name for timestamps
            time_window: Time window for grouping ('D', 'W', 'M', 'Y')
            source_col: Column name for source nodes
            target_col: Column name for target nodes
            
        Returns:
            Dictionary of graphs keyed by time period
        """
        # Ensure time column is datetime
        df[time_col] = pd.to_datetime(df[time_col])
        
        # Group by time window
        df['time_period'] = df[time_col].dt.to_period(time_window)
        
        graphs = {}
        for period, group_df in df.groupby('time_period'):
            G = self.build_interaction_graph(
                group_df,
                source_col=source_col,
                target_col=target_col
            )
            graphs[str(period)] = G
        
        self.graphs = graphs
        logger.info(f"Built {len(graphs)} temporal graphs")
        
        return graphs
    
    def calculate_centrality_measures(
        self,
        graph: Optional[nx.Graph] = None
    ) -> pd.DataFrame:
        """
        Calculate various centrality measures for nodes.
        
        Args:
            graph: NetworkX graph (uses self.graph if None)
            
        Returns:
            DataFrame with centrality measures for each node
        """
        if graph is None:
            graph = self.graph
        
        if graph is None:
            raise ValueError("No graph available. Build a graph first.")
        
        # Calculate centrality measures
        degree_cent = nx.degree_centrality(graph)
        betweenness_cent = nx.betweenness_centrality(graph)
        closeness_cent = nx.closeness_centrality(graph)
        eigenvector_cent = nx.eigenvector_centrality(graph, max_iter=1000)
        
        # Create DataFrame
        centrality_df = pd.DataFrame({
            'node': list(degree_cent.keys()),
            'degree_centrality': list(degree_cent.values()),
            'betweenness_centrality': list(betweenness_cent.values()),
            'closeness_centrality': list(closeness_cent.values()),
            'eigenvector_centrality': list(eigenvector_cent.values())
        })
        
        # Sort by degree centrality
        centrality_df = centrality_df.sort_values('degree_centrality', ascending=False)
        
        logger.info(f"Calculated centrality measures for {len(centrality_df)} nodes")
        
        return centrality_df
    
    def get_graph_properties(
        self,
        graph: Optional[nx.Graph] = None
    ) -> Dict[str, Union[int, float]]:
        """
        Calculate basic graph properties.
        
        Args:
            graph: NetworkX graph (uses self.graph if None)
            
        Returns:
            Dictionary of graph properties
        """
        if graph is None:
            graph = self.graph
        
        if graph is None:
            raise ValueError("No graph available. Build a graph first.")
        
        properties = {
            'num_nodes': graph.number_of_nodes(),
            'num_edges': graph.number_of_edges(),
            'density': nx.density(graph),
            'num_components': nx.number_connected_components(graph),
            'avg_degree': sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
        }
        
        # Add diameter for connected graphs
        if nx.is_connected(graph):
            properties['diameter'] = nx.diameter(graph)
            properties['avg_shortest_path'] = nx.average_shortest_path_length(graph)
        else:
            # Use largest component
            largest_cc = max(nx.connected_components(graph), key=len)
            subgraph = graph.subgraph(largest_cc)
            properties['diameter_largest_cc'] = nx.diameter(subgraph)
            properties['avg_shortest_path_largest_cc'] = nx.average_shortest_path_length(subgraph)
        
        return properties
    
    def detect_communities(
        self,
        graph: Optional[nx.Graph] = None,
        method: str = 'louvain'
    ) -> Dict[int, int]:
        """
        Detect communities in the network.
        
        Args:
            graph: NetworkX graph (uses self.graph if None)
            method: Community detection method ('louvain', 'greedy')
            
        Returns:
            Dictionary mapping nodes to community IDs
        """
        if graph is None:
            graph = self.graph
        
        if graph is None:
            raise ValueError("No graph available. Build a graph first.")
        
        if method == 'louvain':
            try:
                import community as community_louvain
                communities = community_louvain.best_partition(graph)
            except ImportError:
                logger.warning("python-louvain not installed, using greedy method")
                method = 'greedy'
        
        if method == 'greedy':
            communities_generator = nx.community.greedy_modularity_communities(graph)
            communities = {}
            for idx, comm in enumerate(communities_generator):
                for node in comm:
                    communities[node] = idx
        
        logger.info(f"Detected {len(set(communities.values()))} communities")
        
        return communities
    
    def get_top_nodes(
        self,
        graph: Optional[nx.Graph] = None,
        n: int = 10,
        metric: str = 'degree'
    ) -> List[Tuple[int, float]]:
        """
        Get top N nodes by specified metric.
        
        Args:
            graph: NetworkX graph (uses self.graph if None)
            n: Number of top nodes to return
            metric: Metric to use ('degree', 'betweenness', 'closeness', 'eigenvector')
            
        Returns:
            List of (node, score) tuples
        """
        if graph is None:
            graph = self.graph
        
        if graph is None:
            raise ValueError("No graph available. Build a graph first.")
        
        if metric == 'degree':
            scores = nx.degree_centrality(graph)
        elif metric == 'betweenness':
            scores = nx.betweenness_centrality(graph)
        elif metric == 'closeness':
            scores = nx.closeness_centrality(graph)
        elif metric == 'eigenvector':
            scores = nx.eigenvector_centrality(graph, max_iter=1000)
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        top_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        
        return top_nodes
