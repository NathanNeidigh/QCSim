import cmath
import math
import numpy as np
import numpy.typing as npt

class Qcircuit:
    MAXQBITS = 16

    def __init__(self, nqbits: int, initial_state: npt.NDArray[np.complex128] | None = None):
        assert nqbits < Qcircuit.MAXQBITS
        self.nqbits = nqbits
        if initial_state == None:
            self.state = np.zeros(2**nqbits, dtype=np.complex128)
            self.state[0] = 1
        else:
            self.state = initial_state

    def measure(self, *qbits: int) -> npt.NDArray[np.complex128]:
        # TODO: Collapse state vector and return measured 
        return self.state

    def gate(self, gate_mat, *qbits):
        assert len(qbits) <= self.nqbits, "Gates cannot function on more qbits than the circuit contains"
        # Reorder qbit indexes to follow msb. Bit 0 should be the least significant
        qbits = np.array(sorted(list(qbits)))
        qbits = (-1 * (qbits + 1)) % self.nqbits

        gate = np.identity(2) if 0 not in qbits else gate_mat
        for i in range(1, self.nqbits):
            if i in qbits:
                gate = np.kron(gate, gate_mat)
            else:
                gate = np.kron(gate, np.identity(2))
        print(f"Gate:\n{gate}")
        self.state @= gate

    def cgate(self, gate_mat, cqbit: int, *qbits):
        #TODO
        assert len(qbits) + 1 <= self.nqbits, "Gates cannot function on more qbits than the circuit contains"
        # Reorder qbit indexes to follow msb. Bit 0 should be the least significant
        qbits = np.array(sorted(list(qbits)))
        qbits = (-1 * (qbits + 1)) % self.nqbits
        cqbit = (-1 * (cqbit + 1)) % self.nqbits

        cgate_0 = np.identity(2) if 0 != cqbit else np.array([[1, 0], [0, 0]]) 
        for i in range(1, self.nqbits):
            if i == cqbit:
                cgate_0 = np.kron(cgate_0, np.array([[1, 0], [0, 0]]))
            else:
                cgate_0 = np.kron(cgate_0, np.identity(2))

        cgate_1 = np.identity(2) if 0 not in (*qbits, cqbit) else (gate_mat if 0 in qbits else np.array([[0, 0], [0, 1]]))
        for i in range(1, self.nqbits):
            if i in qbits:
                cgate_1 = np.kron(cgate_1, gate_mat)
            elif i == cqbit:
                cgate_1 = np.kron(cgate_1, np.array([[0, 0], [0, 1]]))
            else:
                cgate_1 = np.kron(cgate_1, np.identity(2))

        cgate = cgate_0 + cgate_1
        print(f"C-Gate:\n{cgate}")
        self.state @= cgate

    def h(self, *qbits: int):
        """N-qubit Hadamard Gate"""
        gate_mat = 1/math.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=np.float64)
        self.gate(gate_mat, *qbits)

    def id(self, *qbits: int):
        """N-qubit Identity Gate"""
        gate_mat = np.identity(2)
        self.gate(gate_mat, *qbits)

    def p(self, theta: float, *qbits: int):
        """N-qubit Phase Gate"""
        gate_mat = np.array([[1, 0], [0, theta * 1j]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def r(self, theta: float, phi: float, *qbits: int):
        """N-qubit Rotation theta (radians) about the cos(phi)x + sin(phi)y axis"""
        gate_mat = np.array([[math.cos(theta/2), cmath.rect(-math.sin(theta/2), math.pi - phi)], [cmath.rect(-math.sin(theta/2), math.pi + phi), math.cos(theta/2)]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def rx(self, theta: float, *qbits: int):
        """N-qubit Rotation theta (radians) about the X-axis"""
        gate_mat = np.array([[math.cos(theta/2), -1j*math.sin(theta/2)], [-1j*math.sin(theta/2), math.cos(theta/2)]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def ry(self, theta: float, *qbits: int):
        """N-qubit Rotation theta (radians) about the Y-axis"""
        gate_mat = np.array([[math.cos(theta/2), -math.sin(theta/2)], [-math.sin(theta/2), math.cos(theta/2)]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def rz(self, phi: float, *qbits: int):
        """N-qubit Rotation phi (radians) about the Z-axis"""
        gate_mat = np.array([[cmath.rect(1, -phi/2), 0], [0, cmath.rect(1, phi/2)]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def u(self, theta: float, phi: float, lam: float, *qbits: int):
        """N-qubit Rotation in terms of ZYZ Euler angles"""
        gate_mat = np.array([[math.cos(theta/2), cmath.rect(-math.sin(theta/2), lam)], [cmath.rect(math.sin(theta/2), phi), cmath.rect(math.cos(theta/2), phi + lam)]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def x(self, *qbits: int):
        """N-qubit Pauli-X gate"""
        gate_mat = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)
    
    def y(self, *qbits: int):
        """N-qubit Pauli-Y gate"""
        gate_mat = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def z(self, *qbits: int):
        """N-qubit Pauli-Z gate"""
        gate_mat = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        self.gate(gate_mat, *qbits)

    def ch(self, cqbit: int, *qbits: int):
        """N-qbit controlled Hadamard Gate"""
        gate_mat = 1/math.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=np.float64)
        self.cgate(gate_mat, cqbit, *qbits)

    def cx(self, cqbit: int, *qbits: int):
        """N-qubit controlled Pauli-X gate"""
        gate_mat = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self.cgate(gate_mat, cqbit, *qbits)


qc = Qcircuit(2)
qc.state = np.array([0, 1, 0, 0], dtype=np.complex128)
print(f"state:\n{qc.state}")
qc.ch(0, 1)
print(f"state:\n{qc.state}")
