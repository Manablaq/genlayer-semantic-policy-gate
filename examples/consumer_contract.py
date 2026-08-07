# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


@gl.contract_interface
class SemanticPolicyGate:
    class View:
        def is_allowed(self, decision_id: u256, min_confidence: u32) -> bool: ...
        def is_fresh(self, decision_id: u256) -> bool: ...

    class Write:
        pass


class PolicyGatedAction(gl.Contract):
    gate: Address
    executed: TreeMap[u256, bool]

    def __init__(self, gate: Address):
        self.gate = gate

    @gl.public.write
    def execute_if_allowed(self, decision_id: u256) -> None:
        if self.executed.get(decision_id, False):
            raise gl.vm.UserError("already executed")

        gate = SemanticPolicyGate(self.gate)
        if not gate.view().is_fresh(decision_id):
            raise gl.vm.UserError("decision expired")
        if not gate.view().is_allowed(decision_id, u32(8000)):
            raise gl.vm.UserError("policy decision not allowed")

        self.executed[decision_id] = True
        # Put application-specific action here: accept submission, release
        # escrow, publish listing, mint credential, or unlock workflow.
