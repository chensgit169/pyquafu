# (C) Copyright 2023 Beijing Academy of Quantum Information Sciences
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""quafu PyTorch quantum layer"""

import torch
import numpy as np
from quafu import QuantumCircuit
from quafu.algorithms.layers.qnode import compute_vjp, jacobian, run_circ


class ExecuteCircuits(torch.autograd.Function):
    """TODO(zhaoyilun): document"""

    @staticmethod
    def forward(ctx, parameters, kwargs):
        ctx.run_fn = kwargs["run_fn"]
        ctx.circ = kwargs["circ"]
        ctx.save_for_backward(parameters)
        parameters = parameters.numpy().tolist()
        outputs = []
        for para in parameters:
            out = ctx.run_fn(ctx.circ, para)
            outputs.append(out)
        outputs = np.stack(outputs)
        outputs = torch.from_numpy(outputs)
        return outputs

    @staticmethod
    def backward(ctx, grad_out):
        (parameters,) = ctx.saved_tensors
        jac = jacobian(ctx.circ, parameters.numpy())
        vjp = compute_vjp(jac, grad_out.numpy())
        vjp = torch.from_numpy(vjp)
        return vjp, None


# TODO(zhaoyilun): doc
def exec(
    circ: QuantumCircuit, parameters: torch.Tensor, run_fn=run_circ, grad_fn=None
):
    """execute.

    Args:
        circ:
        run_fn:
        grad_fn:
    """

    kwargs = {"circ": circ, "run_fn": run_fn, "grad_fn": grad_fn}

    return ExecuteCircuits.apply(parameters, kwargs)
