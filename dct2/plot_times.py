import numpy as np
import matplotlib.pyplot as plt

# Carica i dati
times_custom = np.loadtxt("times_custom.txt")
times_scipy = np.loadtxt("times_scipy.txt")
N_values = np.loadtxt("N_values.txt")

# Plot
plt.figure(figsize=(8,6))
plt.semilogy(N_values, times_custom, 'o-', label='DCT2 Custom (O(N^3))')
plt.semilogy(N_values, times_scipy, 's-', label='DCT2 Scipy (O(N^2 logN))')

plt.xlabel('Dimensione matrice N')
plt.ylabel('Tempo di esecuzione (s)')
plt.title('Confronto tempi DCT2 custom vs scipy')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()
plt.savefig("confronto_tempi.png")
plt.show()
