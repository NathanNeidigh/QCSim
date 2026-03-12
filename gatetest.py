from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Operator
from qiskit.circuit.library import MCXGate
import numpy as np

mcx = MCXGate(4)
np.set_printoptions(threshold=np.inf, linewidth=1000)
print(Operator(mcx).data.real.astype(np.float16))
print(Operator(mcx).data.shape)