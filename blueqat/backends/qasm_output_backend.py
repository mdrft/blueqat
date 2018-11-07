import math
import random
import numpy as np
from ..gate import *
from .backendbase import Backend

class QasmOutputBackend(Backend):
    """Backend for OpenQASM output."""
    def _parse_run_args(self, output_prologue=True, *args, **kwargs):
        return { 'output_prologue': output_prologue }

    def _preprocess_run(self, gates, args, kwargs):
        args = self._parse_run_args(*args, **kwargs)
        n_qubits = find_n_qubits(gates)
        if args['output_prologue']:
            qasmlist = [
                "OPENQASM 2.0;",
                'include "qelib1.inc";',
                f"qreg q[{n_qubits}];",
                f"creg c[{n_qubits}];",
            ]
        else:
            qasmlist = []
        return gates, (qasmlist, n_qubits)

    def _postprocess_run(self, ctx):
        return "\n".join(ctx[0])

    def run(self, gates, args, kwargs):
        return self._run(gates, args, kwargs)

    def _one_qubit_gate_noargs(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername} q[{idx}];")
        return ctx

    gate_x = _one_qubit_gate_noargs
    gate_y = _one_qubit_gate_noargs
    gate_z = _one_qubit_gate_noargs
    gate_h = _one_qubit_gate_noargs
    gate_t = _one_qubit_gate_noargs
    gate_s = _one_qubit_gate_noargs

    def _two_qubit_gate_noargs(self, gate, ctx):
        for control, target in gate.control_target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername} q[{control}],q[{target}];")
        return ctx

    gate_cz = _two_qubit_gate_noargs
    gate_cx = _two_qubit_gate_noargs

    def _one_qubit_gate_args_theta(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"{gate.lowername}({gate.theta}) q[{idx}];")
        return ctx

    gate_rx = _one_qubit_gate_args_theta
    gate_ry = _one_qubit_gate_args_theta
    gate_rz = _one_qubit_gate_args_theta

    def gate_measure(self, gate, ctx):
        for idx in gate.target_iter(ctx[1]):
            ctx[0].append(f"measure q[{idx}] -> c[{idx}];")
        return ctx