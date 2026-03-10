from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import operator

# Setup the 4-bit Key Space
key = QuantumRegister(4, 'q')
tgt = QuantumRegister(1, 't')
out = ClassicalRegister(4, 'c')
qc = QuantumCircuit(key, tgt, out)

# Qubit initilization
qc.h(key)
qc.x(tgt)
qc.h(tgt)

# Oracle loop
def apply_oracle(circuit):
    # Shift-XOR Hash
    circuit.cx(key[0], key[1])
    circuit.cx(key[1], key[2])
    circuit.cx(key[2], key[3])

    # Hash ordering for bit numbers 0 1 2 3
    # To target '0011' (Left-to-Right), we flip the 0 and 1 qubits
    circuit.x(key[0])
    circuit.x(key[1])
    #circuit.x(key[2])
    #circuit.x(key[3])

    # The Tripwire: 4-controlled NOT
    circuit.mcx(key[0:4], tgt[0])
    
    # Undo Trap
    circuit.x(key[0])
    circuit.x(key[1])
    #circuit.x(key[2])
    #circuit.x(key[3])

    # The Mirror
    circuit.cx(key[2], key[3])
    circuit.cx(key[1], key[2])
    circuit.cx(key[0], key[1])

def apply_diffuser(circuit):
    circuit.h(key)
    circuit.x(key)
    # MCZ for 4 bits (H-MCX-H)
    circuit.h(key[3])
    circuit.mcx(key[0:3], key[3])
    circuit.h(key[3])
    circuit.x(key)
    circuit.h(key)

# Optimal iterations for 1 target in a 16-state space is 3
iterations = 3
target_hash = "0011" # if you change this, you need to update 0's index in lines 25-28 & 34-37

for _ in range(iterations):
    apply_oracle(qc)
    apply_diffuser(qc)

qc.measure(key, out)

simulator = AerSimulator()
compiled_qc = transpile(qc, simulator)
result = simulator.run(compiled_qc, shots=1024).result()
counts = result.get_counts()

fixed_counts = {k[::-1]: v for k, v in counts.items()}
sorted_counts = sorted(fixed_counts.items(), key=operator.itemgetter(1), reverse=True)

print(f"\n4-BIT Key Crack")
print(f"Target hash: {target_hash}")
print("-" * 37)

for i in range(3):
    state, count = sorted_counts[i]
    print(f"Rank {i+1}: Key {state} | Probability: {(count/1024)*100:.1f}%")

print('\n')


"""
Verification Table from "SHA-4_test.py"
Key  | Hash
-----------
0000 | 0000        
0001 | 0001        
0010 | 0011        
0011 | 0010        
0100 | 0111        
0101 | 0110        
0110 | 0100         
0111 | 0101        
1000 | 1111        
1001 | 1110        
1010 | 1100        
1011 | 1101        
1100 | 1000        
1101 | 1001        
1110 | 1011        
1111 | 1010  

"""