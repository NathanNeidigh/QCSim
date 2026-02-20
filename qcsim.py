import numpy as np

class Qcircuit:
    MAXQBITS = 16

    def __init__(self, nqbits: int):
        assert nqbits < Qcircuit.MAXQBITS
        self.nqbits = nqbits
        self.state = np.zeros(nqbits, dtype=np.complex128)

    def measure(self) -> np.typing.NDarray:
        # TODO: Collapse state vector and return measured states


