import { createAccount, createClient } from "genlayer-js";
import { testnetAsimov } from "genlayer-js/chains";
import { ExecutionResult, TransactionStatus } from "genlayer-js/types";

const account = createAccount();
const client = createClient({
  chain: testnetAsimov,
  account,
});

const gateAddress = "0x...";
const observedAt = BigInt(Math.floor(Date.now() / 1000));
const submittedContent =
  "example.com, example.net, and example.org are reserved for documentation and examples.";
const context = "Verify this claim under the registered authoritative-source policy.";
const primaryUri = "https://www.iana.org/help/example-domains";
const primarySha256 =
  "6fde51fc02d67b032e17adfe1ae5c67daf2c01bed20f533b7754ee32e14c4bc9";
const corroboratingUri = "https://www.rfc-editor.org/rfc/rfc2606.txt";
const corroboratingSha256 =
  "b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0";

const policyTx = await client.writeContract({
  address: gateAddress,
  functionName: "register_policy",
  args: [
    "GenLayer Submission Completeness Policy",
    "Allow only when both registered authoritative sources explicitly support the submitted claim. Deny only when both explicitly contradict it. Otherwise require review.",
  ],
  value: BigInt(0),
});

const policyReceipt = await client.waitForTransactionReceipt({
  hash: policyTx,
  status: TransactionStatus.FINALIZED,
});

if (policyReceipt.txExecutionResultName !== ExecutionResult.FINISHED_WITH_RETURN) {
  throw new Error("register_policy failed");
}

const fingerprint = await client.readContract({
  address: gateAddress,
  functionName: "compute_fingerprint",
  args: [
    1n,
    "Reserved example domains",
    submittedContent,
    context,
    primaryUri,
    primarySha256,
    "IANA",
    corroboratingUri,
    corroboratingSha256,
    "RFC Editor / IETF",
    "IANA help page and RFC 2606 observed 2026-08-25",
    observedAt,
    86400n,
    2,
    604800n,
  ],
  stateStatus: "accepted",
});

const decisionTx = await client.writeContract({
  address: gateAddress,
  functionName: "submit_decision",
  args: [
    1n,
    "Reserved example domains",
    submittedContent,
    context,
    primaryUri,
    primarySha256,
    "IANA",
    corroboratingUri,
    corroboratingSha256,
    "RFC Editor / IETF",
    "IANA help page and RFC 2606 observed 2026-08-25",
    observedAt,
    86400n,
    2,
    604800n,
  ],
  value: BigInt(0),
});

await client.waitForTransactionReceipt({
  hash: decisionTx,
  status: TransactionStatus.FINALIZED,
});

// This triggers strict consensus. Each validator independently fetches the
// registered sources, verifies their complete SHA-256 commitments, and reapplies
// the immutable policy snapshot before a decision is stored.
const resolveTx = await client.writeContract({
  address: gateAddress,
  functionName: "resolve_semantic_decision",
  args: [1n],
  value: BigInt(0),
});

await client.waitForTransactionReceipt({
  hash: resolveTx,
  status: TransactionStatus.FINALIZED,
});

const allowed = await client.readContract({
  address: gateAddress,
  functionName: "is_allowed_for",
  args: [1n, fingerprint, account.address, 3600n],
  stateStatus: "accepted",
});

console.log({ allowed });
