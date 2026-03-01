import numpy as np

# 1. Setup
n = 4
secret_s = "1011"  # The hidden string we want to find
s_int = int(secret_s, 2)
dim = 2**n

# Helper: One-qubit Hadamard matrix
H1 = np.array([[1, 1], [1, -1]]) #* 1/np.sqrt(2)

# Create n-qubit Hadamard H_n = H \otimes H \otimes ...
Hn = H1
for _ in range(n - 1):
    Hn = np.kron(Hn, H1)

# 2. STEP 1: Start with |0000> and apply H^n
# Initial state: [1, 0, 0, ..., 0]
psi = np.zeros(dim)
psi[0] = 1.0
psi = Hn @ psi
# Now psi is a uniform superposition: 1/sqrt(16) for all states

# 3. STEP 2: The Oracle (Phase Kickback)
# This mimics U_f |x>|-> = (-1)^{s.x} |x>|->
# We apply a phase (-1) to state |x> if (s AND x) has odd number of bits
oracle_matrix = np.eye(dim)
for x in range(dim):
    # Calculate dot product s \cdot x (bitwise AND followed by parity)
    dot_product = bin(s_int & x).count('1')
    if dot_product % 2 == 1:
        oracle_matrix[x, x] = -1

psi = oracle_matrix @ psi

# 4. STEP 3: Final Hadamard (Inversion)
psi = Hn @ psi

# 5. Result
# Probabilities are amplitudes squared
probabilities = np.abs(psi)**2
measured_int = np.argmax(probabilities)
measured_s = format(measured_int, f'0{n}b')

print(f"Secret string s: {secret_s}")
print(f"Measured string: {measured_s}")
print(f"Confidence: {probabilities[measured_int]*100:.1f}%")