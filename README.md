Bank Asset Size Matching & Formatting

This repository contains a Python-based solution for cleaning, matching, and formatting bank data. The primary goal is to match banks from two datasets based on their names and associate each bank with its respective asset size. The final output is a cleaned dataset with asset sizes in Indian-style currency format.

Key Features:

Data Preprocessing: Standardizes bank names and removes unnecessary suffixes for accurate matching.

Fuzzy Matching: Utilizes thefuzz library for approximate string matching between bank names in two datasets.

Data Transformation: Formats asset sizes into the Indian currency style for better presentation.

Output: Exports the final matched and formatted dataset to an Excel file.

Technologies:

Python

pandas

thefuzz (for fuzzy matching)

Excel for output
