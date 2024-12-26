# tests/__init__.py
import os
import sys

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))