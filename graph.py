from matplotlib import pyplot as plt
from IPython.display import clear_output

import numpy as np
for i in range(50):
    clear_output(wait=True)
    y = np.random.random([10,1])
    plt.plot(y)
    plt.savefig("test.png")