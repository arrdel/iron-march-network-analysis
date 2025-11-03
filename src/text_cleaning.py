"""
Text cleaning and preprocessing utilities.

This module provides functions for cleaning and preprocessing text data,
including HTML tag removal, URL cleaning, and special character handling.
"""

import re
import logging
from typing import List, Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextCleaner:
    """Text cleaning and preprocessing utilities."""
    
    @staticmethod
    def clean_text_advanced(text: str) -> str:
        """
        Perform advanced text cleaning including HTML removal and normalization.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ""
        
        # Remove URLs
        text = re.sub(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            '',
            text
        )
        
        # Remove URL fragments
        text = re.sub(r'/index\.php[^\s"]+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove newlines and escaped quotes
        text = text.replace('\n', ' ').replace('\\\'', '\'')
        text = text.replace('Â\xa0', ' ').replace('&nbsp;', ' ')
        
        # Remove image paths and HTML-like attributes
        text = re.sub(r'/emoticons/[^\s"]+', '', text)
        text = re.sub(r'\"[^\"]*\"', '', text)
        
        # Remove non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        # Trim extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text: Input text with HTML tags
            
        Returns:
            Text without HTML tags
        """
        if not isinstance(text, str):
            return ""
        
        return re.sub(r'<.*?>', '', text)
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text.
        
        Args:
            text: Input text with URLs
            
        Returns:
            Text without URLs
        """
        if not isinstance(text, str):
            return ""
        
        # Remove standard URLs
        text = re.sub(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            '',
            text
        )
        
        # Remove www URLs
        text = re.sub(r'www\.[^\s]+', '', text)
        
        return text
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        if not isinstance(text, str):
            return ""
        
        # Replace multiple spaces with single space
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def remove_special_characters(text: str, keep_basic_punctuation: bool = True) -> str:
        """
        Remove special characters from text.
        
        Args:
            text: Input text
            keep_basic_punctuation: Whether to keep basic punctuation (.,!?)
            
        Returns:
            Text without special characters
        """
        if not isinstance(text, str):
            return ""
        
        if keep_basic_punctuation:
            # Keep alphanumeric and basic punctuation
            text = re.sub(r'[^a-zA-Z0-9\s.,!?\'-]', '', text)
        else:
            # Keep only alphanumeric and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        return text
    
    def clean_dataframe_column(
        self,
        df: pd.DataFrame,
        column_name: str,
        method: str = 'advanced'
    ) -> pd.DataFrame:
        """
        Clean a specific column in a DataFrame.
        
        Args:
            df: Input DataFrame
            column_name: Name of column to clean
            method: Cleaning method ('advanced', 'basic', 'html_only')
            
        Returns:
            DataFrame with cleaned column
        """
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame")
        
        logger.info(f"Cleaning column '{column_name}' using method '{method}'")
        
        if method == 'advanced':
            df[column_name] = df[column_name].apply(self.clean_text_advanced)
        elif method == 'basic':
            df[column_name] = df[column_name].apply(
                lambda x: self.normalize_whitespace(
                    self.remove_special_characters(x)
                )
            )
        elif method == 'html_only':
            df[column_name] = df[column_name].apply(self.remove_html_tags)
        else:
            raise ValueError(f"Unknown cleaning method: {method}")
        
        return df
    
    def clean_multiple_columns(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'advanced'
    ) -> pd.DataFrame:
        """
        Clean multiple columns in a DataFrame.
        
        Args:
            df: Input DataFrame
            columns: List of column names to clean
            method: Cleaning method to apply
            
        Returns:
            DataFrame with cleaned columns
        """
        for col in columns:
            df = self.clean_dataframe_column(df, col, method)
        
        return df
