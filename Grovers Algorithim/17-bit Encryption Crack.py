from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import operator

def binary_17bit_to_hex(binary_string):
    """
    Converts a 17-bit binary string back to +/- sign and 4-digit hex.
    """
    sign_bit = binary_string[0]
    sign = "-" if sign_bit == "1" else "+"
    binary_16 = binary_string[1:]
    int_val = int(binary_16, 2)
    hex_val = format(int_val, '04X')

    return sign, hex_val

# 17 qubits for the key, 1 for the phase target
key = QuantumRegister(17, 'key')
tgt = QuantumRegister(1, 'tgt')
out = ClassicalRegister(17, 'meas')
qc = QuantumCircuit(key, tgt, out)

qc.h(key) # Superposition of all 131,072 keys
qc.x(tgt) # Initialize target to |1>
qc.h(tgt) # Flip target to |-> for phase kickback

targethash = '11010001001100011'

# Oracle Function
def apply_oracle(circuit):
    # Bit 1 is XOR only; Bits 2-16 use Toffoli (CCX) for non-linearity
    circuit.cx(key[0], key[1])
    for i in range(2, 17):
        circuit.ccx(key[i-2], key[i-1], key[i])

    # Trap to target the specific 17-bit Hash)
    # Identify where your target hash string has '0' and update this list with the '0' positions from hash
    # Example Hash: 11010001001100011
    hash_zeros = [2,4,5,6,8,9,12,13,14] 
    
    for bit in hash_zeros:
        circuit.x(key[bit])

    # 17-qubit phase kickback to marks the target state
    circuit.mcx(key[0:17], tgt[0]) 
    
    for bit in hash_zeros:
        circuit.x(key[bit])

    # Mirror of non-linear hash logic
    for i in range(16, 1, -1):
        circuit.ccx(key[i-2], key[i-1], key[i])
    circuit.cx(key[0], key[1])

# Diffuser function
def apply_diffuser(circuit):
    circuit.h(key)
    circuit.x(key)
    # 17-bit Multi-Controlled Z
    circuit.h(key[16])
    circuit.mcx(key[0:16], key[16])
    circuit.h(key[16])
    circuit.x(key)
    circuit.h(key)

# Optimal for 17-bit is 284; 250 is good enough
iterations = 10
for _ in range(iterations):
    apply_oracle(qc)
    apply_diffuser(qc)

qc.measure(key, out)

simulator = AerSimulator(method='matrix_product_state')
compiled_qc = transpile(qc, simulator)

print("Starting 17-bit non-linear simulation...")
result = simulator.run(compiled_qc, shots=1024).result()
counts = result.get_counts()

fixed_counts = {k[::-1]: v for k, v in counts.items()}
sorted_counts = sorted(fixed_counts.items(), key=operator.itemgetter(1), reverse=True)

print(f"\n\n17-Bit Non-Linear Key Crack")
print(f"Target Hash: {targethash}")
top_binary_state = sorted_counts[0][0]
print(f"Cracked Key: {top_binary_state}")
decoded_sign, decoded_hex = binary_17bit_to_hex(top_binary_state)

print(f"Initial Input Password:      {decoded_sign}{decoded_hex}\n")

# 01101101101101100
# 01101101101101100

