"""
Visualization utilities for network analysis and data exploration.

This module provides functions for creating various visualizations including
network graphs, centrality plots, temporal analysis, and word clouds.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class NetworkVisualizer:
    """Network visualization utilities."""
    
    def __init__(self, output_dir: str = "outputs/images"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save output images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def plot_network(
        self,
        graph: nx.Graph,
        title: str = "Network Graph",
        node_size: int = 300,
        node_color: str = 'lightblue',
        with_labels: bool = False,
        layout: str = 'spring',
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot a network graph.
        
        Args:
            graph: NetworkX graph to plot
            title: Plot title
            node_size: Size of nodes
            node_color: Color of nodes
            with_labels: Whether to show node labels
            layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
            save_path: Path to save the figure
        """
        plt.figure(figsize=(15, 10))
        
        # Choose layout
        if layout == 'spring':
            pos = nx.spring_layout(graph, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(graph)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(graph)
        else:
            pos = nx.spring_layout(graph)
        
        # Draw network
        nx.draw(
            graph,
            pos,
            node_size=node_size,
            node_color=node_color,
            with_labels=with_labels,
            edge_color='gray',
            alpha=0.7
        )
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved network plot to {save_path}")
        
        plt.show()
        plt.close()
    
    def plot_centrality_distribution(
        self,
        centrality_df: pd.DataFrame,
        metric: str = 'degree_centrality',
        title: Optional[str] = None,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot centrality distribution.
        
        Args:
            centrality_df: DataFrame with centrality measures
            metric: Centrality metric to plot
            title: Plot title
            save_path: Path to save the figure
        """
        if metric not in centrality_df.columns:
            raise ValueError(f"Metric '{metric}' not found in DataFrame")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Distribution plot
        axes[0].hist(centrality_df[metric], bins=50, edgecolor='black', alpha=0.7)
        axes[0].set_xlabel(metric.replace('_', ' ').title(), fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].set_title(f'Distribution of {metric.replace("_", " ").title()}', fontsize=14)
        axes[0].grid(True, alpha=0.3)
        
        # Top nodes bar plot
        top_10 = centrality_df.nsmallest(10, metric) if len(centrality_df) > 10 else centrality_df
        axes[1].barh(range(len(top_10)), top_10[metric], color='steelblue')
        axes[1].set_yticks(range(len(top_10)))
        axes[1].set_yticklabels(top_10['node'])
        axes[1].set_xlabel(metric.replace('_', ' ').title(), fontsize=12)
        axes[1].set_ylabel('Node', fontsize=12)
        axes[1].set_title(f'Top 10 Nodes by {metric.replace("_", " ").title()}', fontsize=14)
        axes[1].grid(True, alpha=0.3, axis='x')
        
        if title:
            fig.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved centrality plot to {save_path}")
        
        plt.show()
        plt.close()
    
    def plot_temporal_graph_properties(
        self,
        properties_dict: Dict[str, Dict[str, float]],
        metrics: List[str] = ['num_nodes', 'num_edges', 'density', 'avg_degree'],
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot temporal evolution of graph properties.
        
        Args:
            properties_dict: Dictionary mapping time periods to property dictionaries
            metrics: List of metrics to plot
            save_path: Path to save the figure
        """
        # Prepare data
        df = pd.DataFrame(properties_dict).T
        df.index = pd.to_datetime(df.index.astype(str))
        df = df.sort_index()
        
        # Create subplots
        n_metrics = len(metrics)
        fig, axes = plt.subplots(n_metrics, 1, figsize=(14, 4 * n_metrics))
        
        if n_metrics == 1:
            axes = [axes]
        
        for idx, metric in enumerate(metrics):
            if metric in df.columns:
                axes[idx].plot(df.index, df[metric], marker='o', linewidth=2, markersize=6)
                axes[idx].set_xlabel('Time Period', fontsize=12)
                axes[idx].set_ylabel(metric.replace('_', ' ').title(), fontsize=12)
                axes[idx].set_title(f'{metric.replace("_", " ").title()} Over Time', fontsize=14)
                axes[idx].grid(True, alpha=0.3)
                axes[idx].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved temporal plot to {save_path}")
        
        plt.show()
        plt.close()
    
    def plot_degree_distribution(
        self,
        graph: nx.Graph,
        log_scale: bool = True,
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot degree distribution of the network.
        
        Args:
            graph: NetworkX graph
            log_scale: Whether to use log scale
            save_path: Path to save the figure
        """
        degrees = [d for n, d in graph.degree()]
        
        plt.figure(figsize=(12, 6))
        
        if log_scale:
            plt.subplot(1, 2, 1)
        
        plt.hist(degrees, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        plt.xlabel('Degree', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Degree Distribution', fontsize=14)
        plt.grid(True, alpha=0.3)
        
        if log_scale:
            plt.subplot(1, 2, 2)
            plt.hist(degrees, bins=50, edgecolor='black', alpha=0.7, color='coral')
            plt.xlabel('Degree', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.title('Degree Distribution (Log Scale)', fontsize=14)
            plt.yscale('log')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved degree distribution to {save_path}")
        
        plt.show()
        plt.close()
    
    def plot_heatmap(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        title: str = "Heatmap",
        xlabel: str = "X",
        ylabel: str = "Y",
        cmap: str = 'viridis',
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot a heatmap.
        
        Args:
            data: Data to plot (DataFrame or array)
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            cmap: Colormap
            save_path: Path to save the figure
        """
        plt.figure(figsize=(12, 10))
        
        sns.heatmap(
            data,
            cmap=cmap,
            annot=False,
            cbar=True,
            square=False
        )
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved heatmap to {save_path}")
        
        plt.show()
        plt.close()
    
    def create_wordcloud(
        self,
        text: str,
        title: str = "Word Cloud",
        max_words: int = 100,
        background_color: str = 'white',
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a word cloud from text.
        
        Args:
            text: Input text
            title: Plot title
            max_words: Maximum number of words
            background_color: Background color
            save_path: Path to save the figure
        """
        try:
            from wordcloud import WordCloud
        except ImportError:
            logger.error("wordcloud package not installed. Install with: pip install wordcloud")
            return
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            max_words=max_words,
            background_color=background_color,
            colormap='viridis'
        ).generate(text)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved word cloud to {save_path}")
        
        plt.show()
        plt.close()
