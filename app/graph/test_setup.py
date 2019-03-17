""" add to let pytest deal with absolute imports
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
