from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

qc = QuantumCircuit(9)
qc.mcx(list(range(8)), 8)
U = Operator(qc).data.real.astype(np.float16)
np.set_printoptions(threshold=np.inf, linewidth=1000)
print(np.eye(2**9) - U)
