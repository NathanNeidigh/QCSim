from math import sqrt
import numpy as np
import numpy.typing as npt

class Qcircuit:
    MAXQBITS = 16

    def __init__(self, nqbits: int):
        assert nqbits < Qcircuit.MAXQBITS
        self.nqbits = nqbits
        self.qbits = np.vstack((np.ones(nqbits, dtype=np.complex128), np.zeros(nqbits, dtype=np.complex128))) 
    def measure(self) -> npt.NDArray[np.complex128]:
        # TODO: Collapse state vector and return measured states
        return self.qbits

    def h(self, *qbits: int):
        assert len(qbits) <= self.nqbits, "Gates cannot function on more qbits than the circuit contains"
        gate = 1/sqrt(2) * np.array([[1, 1], [1, -1]], dtype=np.float64)
        qbit_mask = np.zeros(self.nqbits, dtype=np.bool)
        for i in qbits: qbit_mask[i] = True

        self.qbits[:, qbit_mask] = gate @ self.qbits[:, qbit_mask]

qc = Qcircuit(2)
print(f"qbits:\n{qc.qbits}")
qc.h(0)
print(qc.measure())
