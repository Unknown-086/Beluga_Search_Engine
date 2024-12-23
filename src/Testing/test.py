import numpy as np
import pandas as pd
from numba import jit
import fastapi
import uvicorn
import httpx


def test_setup():
    # Test numpy
    arr = np.array([1, 2, 3])
    print(f"NumPy: {arr.mean()}")

    # Test pandas
    df = pd.DataFrame({'test': [1, 2, 3]})
    print(f"Pandas: {df.head()}")

    # Test numba
    @jit(nopython=True)
    def add(a, b):
        return a + b

    print(f"Numba: {add(1, 2)}")

    print("All imports successful!")


if __name__ == "__main__":
    test_setup()