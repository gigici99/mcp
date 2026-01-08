# src/__init__.py

# Exporting main functions to be accessible via the 'src' package 
from .executor import CommandExecutor
from .java_tools import JavaProjectAnalyzer
from .web_tools import WebProjectAnalyzer

__version__ = "1.0.0"
__author__ = "gigici99"