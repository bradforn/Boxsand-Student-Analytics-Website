#!/usr/bin/env python
import os
import sys
import csv
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import seaborn as sns
from scipy import stats
from sklearn import datasets, linear_model
import re
import time
from datetime import*
from collections import*
from itertools import filterfalse
from plotly.offline import init_notebook_mode, iplot
from IPython.display import display, HTML
import plotly.offline as offline
import plotly.graph_objs as go
import pickle
from polls.main1 import student, course






if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
