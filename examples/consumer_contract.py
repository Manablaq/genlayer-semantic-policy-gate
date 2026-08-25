# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *


@gl.contract_interface
class SemanticPolicyGate:
    class View:
        def is_allowed_for(
            self,
            decision_id: u256,
            expected_fingerprint: str,
            expected_policy_owner: Address,
            consumer_max_age_seconds: u256,
        ) -> bool: ...

    class Write:
        pass


class PolicyGatedAction(gl.Contract):
    owner: Address
    gate: Address
    expected_policy_owner: Address
    consumer_max_age_seconds: u256
    expected_fingerprints: TreeMap[u256, str]
    executed: TreeMap[u256, bool]

    def __init__(
        self,
        gate: Address,
        expected_policy_owner: Address,
        consumer_max_age_seconds: u256,
    ):
        if consumer_max_age_seconds == u256(0):
            raise gl.vm.UserError("consumer max age is required")
        self.owner = gl.message.sender_address
        self.gate = gate
        self.expected_policy_owner = expected_policy_owner
        self.consumer_max_age_seconds = consumer_max_age_seconds

    @gl.public.write
    def configure_action(self, action_id: u256, expected_fingerprint: str) -> None:
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("only consumer owner")
        if self.executed.get(action_id, False):
            raise gl.vm.UserError("action already executed")
        if len(expected_fingerprint.strip()) != 64:
            raise gl.vm.UserError("expected fingerprint must be SHA-256")
        self.expected_fingerprints[action_id] = expected_fingerprint.strip().lower()

    @gl.public.write
    def execute_if_allowed(self, action_id: u256, decision_id: u256) -> None:
        if self.executed.get(action_id, False):
            raise gl.vm.UserError("already executed")

        expected_fingerprint = self.expected_fingerprints.get(action_id, "")
        if expected_fingerprint == "":
            raise gl.vm.UserError("action fingerprint not configured")

        gate = SemanticPolicyGate(self.gate)
        if not gate.view().is_allowed_for(
            decision_id,
            expected_fingerprint,
            self.expected_policy_owner,
            self.consumer_max_age_seconds,
        ):
            raise gl.vm.UserError("policy decision not allowed")

        self.executed[action_id] = True
        # Put application-specific action here: accept submission, release
        # escrow, publish listing, mint credential, or unlock workflow.
