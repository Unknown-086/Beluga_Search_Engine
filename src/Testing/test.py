import sys
from pathlib import Path
import pandas as pd
import numpy as np
from numba import cuda

def test_imports():
    print("Python path:", sys.path)
    print("NumPy version:", np.__version__)
    print("Pandas version:", pd.__version__)
    print("Current directory:", Path.cwd())
    print("Project root:", Path(__file__).parent.parent.parent)

if __name__ == "__main__":
    test_imports()