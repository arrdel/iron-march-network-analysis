"""
Data preprocessing utilities for Iron March dataset.

This module contains functions for loading, cleaning, and preparing 
the Iron March dataset for analysis.
"""

import pandas as pd
from datetime import datetime
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handle data loading and preprocessing operations."""
    
    def __init__(self, data_path: str):
        """
        Initialize the data preprocessor.
        
        Args:
            data_path: Path to the data file (CSV or XLSX)
        """
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV or XLSX file.
        
        Returns:
            Loaded DataFrame
        """
        try:
            if self.data_path.endswith('.csv'):
                self.df = pd.read_csv(self.data_path)
            elif self.data_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.data_path)
            else:
                raise ValueError(f"Unsupported file format: {self.data_path}")
            
            logger.info(f"Successfully loaded data from {self.data_path}")
            logger.info(f"Dataset shape: {self.df.shape}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def convert_unix_timestamp(self, timestamp_col: str = 'msg_date') -> pd.DataFrame:
        """
        Convert UNIX timestamp to datetime and readable UTC format.
        
        Args:
            timestamp_col: Name of the timestamp column
            
        Returns:
            DataFrame with converted timestamps
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Convert to datetime
        self.df[timestamp_col] = pd.to_datetime(self.df[timestamp_col], unit='s')
        
        # Create readable UTC format
        self.df[f'{timestamp_col}_UTC'] = self.df[timestamp_col].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"Converted {timestamp_col} to datetime format")
        return self.df
    
    def get_dataset_summary(self) -> dict:
        """
        Get summary statistics about the dataset.
        
        Returns:
            Dictionary containing summary statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'total_messages': len(self.df),
            'unique_authors': self.df['msg_author_id'].nunique() if 'msg_author_id' in self.df.columns else 0,
            'unique_topics': self.df['msg_topic_id'].nunique() if 'msg_topic_id' in self.df.columns else 0,
            'unique_ips': self.df['msg_ip_address'].nunique() if 'msg_ip_address' in self.df.columns else 0,
            'columns': list(self.df.columns),
            'date_range': (self.df['msg_date'].min(), self.df['msg_date'].max()) if 'msg_date' in self.df.columns else None
        }
        
        return summary
    
    def filter_columns(self, columns_to_keep: list) -> pd.DataFrame:
        """
        Filter dataframe to keep only specified columns.
        
        Args:
            columns_to_keep: List of column names to keep
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        missing_cols = [col for col in columns_to_keep if col not in self.df.columns]
        if missing_cols:
            logger.warning(f"Columns not found in dataset: {missing_cols}")
        
        available_cols = [col for col in columns_to_keep if col in self.df.columns]
        self.df = self.df[available_cols]
        
        logger.info(f"Filtered dataset to {len(available_cols)} columns")
        return self.df
    
    def save_processed_data(self, output_path: str) -> None:
        """
        Save processed data to file.
        
        Args:
            output_path: Path to save the processed data
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        if output_path.endswith('.csv'):
            self.df.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx'):
            self.df.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {output_path}")
        
        logger.info(f"Saved processed data to {output_path}")


def xlsx_to_csv(xlsx_file: str, csv_file: str) -> None:
    """
    Convert XLSX file to CSV format.
    
    Args:
        xlsx_file: Path to input XLSX file
        csv_file: Path to output CSV file
    """
    try:
        df = pd.read_excel(xlsx_file)
        df.to_csv(csv_file, index=False)
        logger.info(f"Successfully converted {xlsx_file} to {csv_file}")
    except Exception as e:
        logger.error(f"Error converting file: {e}")
        raise
