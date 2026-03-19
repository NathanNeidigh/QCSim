import cmath
import math
import random
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

    def measure(self, collapse_state: bool =True, *qbits: int) -> int:
        #TODO Partial measurements
        prob = np.abs(self.state) ** 2
        state = random.choices(population=range(2**self.nqbits), weights=list(prob))
        if (collapse_state):
            self.state = np.zeros(2**self.nqbits, dtype=np.complex128)
            self.state[state] = 1
        return int(state[0])


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
        #print(f"Gate:\n{gate}")
        self.state @= gate

    def cgate(self, gate_mat, cqbits, *qbits):
        assert len(qbits) + 1 <= self.nqbits, "Gates cannot function on more qbits than the circuit contains"
        
        cgate_0 = np.identity(2) if 0 not in cqbits else np.array([[0, 0], [0, 1]]) 
        for i in range(1, self.nqbits):
            if i in cqbits:
                cgate_0 = np.kron(np.array([[0, 0], [0, 1]]), cgate_0)
            else:
                cgate_0 = np.kron(np.identity(2), cgate_0)
        cgate_0 = np.identity(2**self.nqbits) - cgate_0

        cgate_1 = np.identity(2) if 0 not in (*qbits, *cqbits) else (gate_mat if 0 in qbits else np.array([[0, 0], [0, 1]]))
        for i in range(1, self.nqbits):
            if i in qbits:
                cgate_1 = np.kron(gate_mat, cgate_1)
            elif i in cqbits:
                cgate_1 = np.kron(np.array([[0, 0], [0, 1]]), cgate_1)
            else:
                cgate_1 = np.kron(np.identity(2), cgate_1)

        cgate = cgate_0 + cgate_1
        #print(f"C-Gate:\n{cgate}")

        c = np.array([2**x for x in cqbits])
        c = np.sum(c)
        P1 = np.zeros(2**self.nqbits)
        P1[c] = 1

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
        gate_mat = np.array([[1, 0], [0, cmath.rect(1, theta)]], dtype=np.complex128)
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
        self.cgate(gate_mat, [cqbit], *qbits)

    def cx(self, cqbit: int, *qbits: int):
        """N-qubit controlled Pauli-X gate"""
        gate_mat = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self.cgate(gate_mat, [cqbit], *qbits)

    def ccx(self, cqbits, *qbits: int):
        """N-qubit Toffoli gate"""
        gate_mat = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self.cgate(gate_mat, cqbits, *qbits)


def deutsch(case: int):
    qc = Qcircuit(2)
    qc.x(1)
    qc.h(0,1)
    
    if case in [2, 3]: # Balanced
        qc.cx(0, 1)
    elif case in [1, 4]: # Contstant
        qc.x(1)
    else:
        raise ValueError("'case' must be 1, 2, 3, or 4")

    qc.h(0)

    N = 100
    x = np.zeros(N)
     
    for i in range(N):
        x[i] = qc.measure(collapse_state=False) % 2
    
    func_type = {"constant": N - np.sum(x), "balanced": np.sum(x)}
    print(f"Constant: {func_type["constant"]} and Balanced: {func_type["balanced"]}")

def grover_sha4(key: int) -> list[int]:
    qc = Qcircuit(5)
    qc.h(*range(4))
    qc.x(4)
    qc.h(4)

    for _ in range(3):
        #Forward Hash Function
        qc.cx(0, 1)
        qc.cx(1, 2)
        qc.cx(2, 3)

        #Search Hash Argument
        for i, bit in enumerate(reversed(format(key, '04b'))):
            if bit == '0':
                print("X: ", bit, ":", i)
                qc.x(i)

        #Phase Kickback
        mcx_gate = np.identity(2**5)
        mcx_gate[31, 31] = 0
        mcx_gate[31, 15] = 1
        mcx_gate[15, 31] = 1
        mcx_gate[15, 15] = 0
        qc.state @= mcx_gate

        #Undo Trap
        for i, bit in enumerate(reversed(format(key, '04b'))):
            if bit == '0':
                qc.x(i)

        #Reverse Hash function
        qc.cx(2, 3)
        qc.cx(1, 2)
        qc.cx(0, 1)

        #Apply diffuser
        qc.h(*range(4))
        qc.x(*range(4))
        qc.h(3)
        mcx_gate = np.identity(2**5)
        mcx_gate[31, 31] = 0
        mcx_gate[23, 23] = 0
        mcx_gate[15, 15] = 0
        mcx_gate[7, 7] = 0

        mcx_gate[31, 23] = 1
        mcx_gate[23, 31] = 1
        mcx_gate[7, 15] = 1
        mcx_gate[15, 7] = 1
        
        #np.set_printoptions(threshold=np.inf, linewidth=1000)
        #print(mcx_gate)

        qc.state @= mcx_gate

        qc.h(3)
        qc.x(*range(4))
        qc.h(*range(4))

    return (np.abs(qc.state)**2).tolist()

def end_convert(index: int, n_bits: int) -> int:
    little_index = 0
    for i in range(n_bits):
        little_index |= ((index >> i) & 1) << (n_bits - 1 - i)
    return little_index

def main():
    #deutsch(1)
    true_key = 0
    print("Key: ", format(true_key, '04b'))
    state = grover_sha4(true_key)

    print("True Key ({}) Prob: {}".format(true_key, state[true_key] + state[true_key + 2**4]))
    print("State Vector:\n{}".format([round(x, 4) for x in state]))

if __name__ == "__main__":
    main()
