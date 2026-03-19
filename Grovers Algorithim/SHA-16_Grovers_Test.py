from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import operator

# --- 1. SETUP (16-bit Key Space) ---
key = QuantumRegister(16, 'key')
tgt = QuantumRegister(1, 'tgt')
out = ClassicalRegister(16, 'meas')
qc = QuantumCircuit(key, tgt, out)

# Initialization
qc.h(key)
qc.x(tgt)
qc.h(tgt)

# --- 2. THE ORACLE ---
def apply_oracle(circuit):
    # FORWARD HASH (Ripple XOR for 16 bits)
    for i in range(15):
        circuit.cx(key[i], key[i+1])

    # THE TRAP (Example Target Hash: 0100011010101100)
    # Define which bits are '0' in your target 16-bit hash
    # Note: These indices refer to the string position (0 to 15)
    hash_zeros = [0, 2, 3, 4, 7, 9, 11, 14, 15]

    for bit in hash_zeros:
        circuit.x(key[bit])

    # Phase Kickback (16-controlled NOT)
    circuit.mcx(key[0:16], tgt[0])
    
    # Undo Trap Wrapping
    for bit in hash_zeros:
        circuit.x(key[bit])

    # REVERSE HASH (Uncomputation)
    for i in range(14, -1, -1):
        circuit.cx(key[i], key[i+1])

# --- 3. THE DIFFUSER ---
def apply_diffuser(circuit):
    circuit.h(key)
    circuit.x(key)
    # 16-bit MCZ (H on last bit, MCX on the rest, H on last bit)
    circuit.h(key[15])
    circuit.mcx(key[0:15], key[15])
    circuit.h(key[15])
    circuit.x(key)
    circuit.h(key)

# --- 4. EXECUTION ---
# For 16 bits, we need significantly more iterations
# Warning: High iterations in a simulator can be slow! 
# We'll use 201 for theoretical perfection.
iterations = 201
target_hash_str = "0100011010101100" 

for _ in range(iterations):
    apply_oracle(qc)
    apply_diffuser(qc)

qc.measure(key, out)

# --- 5. RESULTS ---
simulator = AerSimulator()
# 16-bit simulation is memory intensive; we'll transpile for speed
compiled_qc = transpile(qc, simulator)
result = simulator.run(compiled_qc, shots=1024).result()
counts = result.get_counts()

# Reversing keys to match human "Left-to-Right" reading
fixed_counts = {k[::-1]: v for k, v in counts.items()}
sorted_counts = sorted(fixed_counts.items(), key=operator.itemgetter(1), reverse=True)

print(f"\nSHA-16-BIT Key Crack")
print(f"Targeting Hash: {target_hash_str}")
print("-" * 41)

for i in range(min(5, len(sorted_counts))):
    state, count = sorted_counts[i]
    print(f"Rank {i+1}: Key {state} | Probability: {(count/1024)*100:.1f}%")

# key: 0110010111111010