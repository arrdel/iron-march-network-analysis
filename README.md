# Iron March Network Analysis

A comprehensive toolkit for analyzing far-right forum networks and activities using the Iron March dataset. This project provides tools for data preprocessing, network analysis, centrality measures, community detection, and visualization of forum interaction patterns.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Data](#data)
- [Modules](#modules)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

## 🔍 Overview

The Iron March forum was a web platform for far-right groups that operated from 2011 to 2016, facilitating communication among neo-fascist and neo-nazi followers. This project analyzes the network structure and interaction patterns within this forum to understand:

- **Key influencers** and their roles in the network
- **Information flow** and coordination between actors
- **Temporal dynamics** of forum activities
- **Community structures** and group formations
- **Communication patterns** and radicalization trends

### Importance of Network Analysis

Network analysis is crucial for understanding complex relationships in social systems. This project demonstrates how network analysis can:

- Identify hidden structures and patterns in online communities
- Track information flow and social interactions
- Detect potential threats and vulnerable points in extremist networks
- Monitor network dynamics and group evolution
- Support policymakers in combating far-right activities

## ✨ Features

- **Data Preprocessing**: Clean and prepare forum data for analysis
- **Text Cleaning**: Remove HTML tags, URLs, and normalize text content
- **Network Construction**: Build interaction networks from forum data
- **Centrality Analysis**: Calculate degree, betweenness, closeness, and eigenvector centrality
- **Community Detection**: Identify communities using Louvain and greedy algorithms
- **Temporal Analysis**: Track network evolution over time
- **Visualization**: Create network graphs, heatmaps, and word clouds
- **Configurable**: YAML-based configuration for easy customization

## 📁 Project Structure

```
knowledge_graph/
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── data_preprocessing.py     # Data loading and preprocessing
│   ├── text_cleaning.py          # Text cleaning utilities
│   ├── network_analysis.py       # Network analysis tools
│   └── visualization.py          # Visualization utilities
├── notebooks/                    # Jupyter notebooks
│   ├── a_play_with_Iron_march_dataset.ipynb
│   └── spacy_test_on_Iron_march_Content.ipynb
├── data/                         # Data directory
│   ├── raw/                      # Raw data files
│   └── processed/                # Processed data files
├── outputs/                      # Output directory
│   ├── images/                   # Generated plots and figures
│   ├── graphs/                   # Network graph visualizations
│   └── wordclouds/               # Word cloud images
├── config/                       # Configuration files
│   ├── __init__.py
│   └── config.yaml               # Main configuration
├── docs/                         # Documentation
├── tests/                        # Unit tests
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup configuration
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/knowledge_graph.git
cd knowledge_graph
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Step 4: Download Spacy Model (for NLP tasks)

```bash
python -m spacy download en_core_web_trf
```

## 🎯 Quick Start

### Example 1: Data Preprocessing

```python
from src.data_preprocessing import DataPreprocessor

# Initialize preprocessor
preprocessor = DataPreprocessor('data/raw/original_data.csv')

# Load and process data
df = preprocessor.load_data()
df = preprocessor.convert_unix_timestamp()

# Get dataset summary
summary = preprocessor.get_dataset_summary()
print(summary)

# Save processed data
preprocessor.save_processed_data('data/processed/cleaned_data.csv')
```

### Example 2: Text Cleaning

```python
from src.text_cleaning import TextCleaner
import pandas as pd

# Initialize cleaner
cleaner = TextCleaner()

# Load data
df = pd.read_csv('data/raw/original_data.csv')

# Clean text column
df = cleaner.clean_dataframe_column(df, 'orig_text', method='advanced')
```

### Example 3: Network Analysis

```python
from src.network_analysis import NetworkAnalyzer
import pandas as pd

# Initialize analyzer
analyzer = NetworkAnalyzer()

# Load data
df = pd.read_csv('data/processed/cleaned_data.csv')

# Build interaction network
graph = analyzer.build_interaction_graph(
    df,
    source_col='msg_author_id',
    target_col='msg_topic_id'
)

# Calculate centrality measures
centrality_df = analyzer.calculate_centrality_measures()
print(centrality_df.head(10))

# Get graph properties
properties = analyzer.get_graph_properties()
print(properties)
```

### Example 4: Visualization

```python
from src.visualization import NetworkVisualizer

# Initialize visualizer
visualizer = NetworkVisualizer(output_dir='outputs/images')

# Plot network
visualizer.plot_network(
    graph,
    title='Iron March Interaction Network',
    save_path='outputs/images/network_graph.png'
)

# Plot centrality distribution
visualizer.plot_centrality_distribution(
    centrality_df,
    metric='degree_centrality',
    save_path='outputs/images/centrality_distribution.png'
)
```

## 📊 Usage

### Working with Jupyter Notebooks

The project includes Jupyter notebooks in the `notebooks/` directory:

1. **a_play_with_Iron_march_dataset.ipynb**: Main analysis notebook with network analysis
2. **spacy_test_on_Iron_march_Content.ipynb**: NLP and text analysis experiments

To run the notebooks:

```bash
jupyter notebook notebooks/
```

### Configuration

Edit `config/config.yaml` to customize:

- Data paths
- Output directories
- Processing parameters
- Visualization settings
- Logging preferences

## 📦 Data

### Input Data Format

The project expects data with the following columns:

- `msg_id`: Unique message identifier
- `msg_author_id`: Author/user identifier
- `msg_topic_id`: Topic/thread identifier
- `msg_date`: Unix timestamp of message
- `msg_ip_address`: IP address (optional)
- `orig_text` or `text`: Message content

### Data Privacy

⚠️ **Important**: The Iron March dataset contains sensitive content. Ensure compliance with:
- Data protection regulations (GDPR, etc.)
- Ethical research guidelines
- Institutional review board (IRB) requirements
- Proper data anonymization practices

## 🔧 Modules

### data_preprocessing.py

- `DataPreprocessor`: Main class for data loading and preprocessing
- `xlsx_to_csv()`: Convert Excel files to CSV format

### text_cleaning.py

- `TextCleaner`: Utilities for text cleaning and normalization
- Methods for HTML removal, URL cleaning, and special character handling

### network_analysis.py

- `NetworkAnalyzer`: Network construction and analysis tools
- Centrality calculations
- Community detection
- Temporal graph analysis

### visualization.py

- `NetworkVisualizer`: Visualization utilities for networks and data
- Network plots
- Centrality distributions
- Temporal analysis plots
- Heatmaps and word clouds

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use this code in your research, please cite:

```bibtex
@software{iron_march_analysis,
  author = {Your Name},
  title = {Iron March Network Analysis Toolkit},
  year = {2024},
  url = {https://github.com/yourusername/knowledge_graph}
}
```

## 📧 Contact

For questions or collaborations, please contact:
- **Your Name** - your.email@example.com
- Project Link: [https://github.com/yourusername/knowledge_graph](https://github.com/yourusername/knowledge_graph)

## 🙏 Acknowledgments

- NetworkX team for the excellent graph analysis library
- The research community studying online extremism
- All contributors to this project

## ⚠️ Disclaimer

This research is conducted for academic and analytical purposes. The analysis of extremist content does not constitute endorsement of such views. Researchers should follow ethical guidelines and legal requirements when working with sensitive data.

---

**Built with ❤️ for understanding and combating online extremism through network science**
