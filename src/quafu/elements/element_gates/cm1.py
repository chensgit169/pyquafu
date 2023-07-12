from .matrices import XMatrix, YMatrix, ZMatrix
from ..quantum_element import ControlledGate


class MCXGate(ControlledGate):
    name = "MCX"

    def __init__(self, ctrls, targ: int):
        super().__init__("X", ctrls, [targ], None, tar_matrix=XMatrix)


class MCYGate(ControlledGate):
    name = "MCY"

    def __init__(self, ctrls, targ: int):
        super().__init__("Y", ctrls, [targ], None, tar_matrix=YMatrix)


class MCZGate(ControlledGate):
    name = "MCZ"

    def __init__(self, ctrls, targ: int):
        super().__init__("Z", ctrls, [targ], None, tar_matrix=ZMatrix)


ControlledGate.register_subclass(MCXGate)
ControlledGate.register_subclass(MCYGate)
ControlledGate.register_subclass(MCZGate)
