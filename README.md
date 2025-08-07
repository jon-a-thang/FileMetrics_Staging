# LongiEng

A collection of Python utilities for file processing, data analysis, and text manipulation. This repository contains three main tools designed to assist with various data processing tasks.

## 📋 Table of Contents

- [Overview](#overview)
- [Tools](#tools)
  - [File Size Aggregator](#file-size-aggregator)
  - [File Meta Metrics](#file-meta-metrics)
  - [Compound Words Finder](#compound-words-finder)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Author](#author)

## 🔍 Overview

LongiEng is a collection of Python utilities originally developed for data migration and analysis tasks. The tools help with file size calculations, CSV data analysis, and text processing operations.

## 🛠️ Tools

### File Size Aggregator (`filesize-aggregate.py`)

A comprehensive tool for calculating file sizes from CSV data and organizing files for migration processes.

**Features:**
- Calculate aggregate file sizes from CSV file paths
- Convert file sizes to human-readable formats (B, KB, MB, GB, TB, etc.)
- Stage and organize files for data migration
- Handle duplicate files with automatic renaming
- Support for both Docket and Document Index file processing

**Key Functions:**
- `get_filesize()` - Get file size in bytes
- `convert_size()` - Convert bytes to human-readable format
- `file_aggregate()` - Calculate total size from CSV file paths
- `stage_data()` - Organize files for migration
- `stage_data_di()` - Document Index specific file staging

### File Meta Metrics (`file-meta-metrics.py`)

Analyzes CSV exports to extract metadata and generate metrics for data migration planning.

**Features:**
- Process Document Index Export CSV files
- Analyze Docket CSV files
- Generate unique case ID lists
- Calculate file counts and metrics
- Export processed data to new CSV files

**Key Functions:**
- `get_meta_data()` - Extract metadata from CSV files
- Generates metrics for total files, unique case IDs, and unique file counts
- Supports TRLA CSV export format analysis

### Compound Words Finder (`compound_words.py`)

A text processing utility that identifies compound words within a given list of words.

**Features:**
- Find compound words formed by combining 2-3 words from input list
- Identify words that can be formed by concatenating other words in the list
- Useful for linguistic analysis and text processing tasks

**Key Functions:**
- `temp_func()` - Main compound word detection algorithm
- Supports detection of 2-word and 3-word compounds
- Returns list of identified compound words

## 📦 Requirements

```
pandas
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LongiEng.git
cd LongiEng
```

2. Install required dependencies:
```bash
pip install pandas
```

## 💻 Usage

### File Size Aggregator

**Command Line Usage:**
```bash
python filesize-aggregate.py
```

**Programmatic Usage:**
```python
# To use as a module, you'll need to import using importlib due to hyphens in filename
import importlib.util
import sys

# Load the module
spec = importlib.util.spec_from_file_location("filesize_aggregate", "filesize-aggregate.py")
filesize_aggregate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(filesize_aggregate)

# Use the functions
csv_file = 'path/to/your/file.csv'
output_file = 'path/to/output.txt'
column_name = 'filepath_column'

filesize_aggregate.file_aggregate(csv_file, output_file, column_name)
```

### File Meta Metrics

**Command Line Usage:**
```bash
python file-meta-metrics.py
```

**Programmatic Usage:**
```python
# To use as a module, you'll need to import using importlib due to hyphens in filename
import importlib.util
import sys

# Load the module
spec = importlib.util.spec_from_file_location("file_meta_metrics", "file-meta-metrics.py")
file_meta_metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(file_meta_metrics)

# Use the functions
doc_index_csv = 'path/to/doc_index_export.csv'
docket_csv = 'path/to/docket.csv'

file_meta_metrics.get_meta_data(doc_index_csv, docket_csv)
```

### Compound Words Finder

```python
# Find compound words in a word list
from compound_words import temp_func

word_list = ["fish", "cake", "fishcake", "none", "the", "less", "nonetheless"]
compound_words = temp_func(word_list, len(word_list))
print(compound_words)
# Output: ['fishcake', 'nonetheless']
```

## 📝 Configuration

Before using the tools, you may need to update file paths in the source code:

1. **File Size Aggregator**: Update the hardcoded paths in the `main()` function
2. **File Meta Metrics**: Update CSV file paths and output directories
3. **Compound Words**: No configuration needed - works with any word list

## 🔧 Development

Each tool is designed as a standalone utility but can be easily integrated into larger data processing pipelines. The tools were originally developed for TRLA data migration tasks but can be adapted for various file processing needs.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jonathan Jang**

---

*Note: This repository contains utilities originally developed for specific data migration tasks. File paths and configurations may need to be updated for your specific use case.*