import { createAccount, createClient } from "genlayer-js";
import { testnetAsimov } from "genlayer-js/chains";
import { ExecutionResult, TransactionStatus } from "genlayer-js/types";

const account = createAccount();
const client = createClient({
  chain: testnetAsimov,
  account,
});

const gateAddress = "0x...";

const policyTx = await client.writeContract({
  address: gateAddress,
  functionName: "register_policy",
  args: [
    "GenLayer Submission Completeness Policy",
    "A valid GenLayer contract submission must include a repository URL, documentation URL, Bradbury contract address, and test evidence.",
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

const decisionTx = await client.writeContract({
  address: gateAddress,
  functionName: "submit_decision",
  args: [
    1n,
    "OutcomeAttestationRegistry submission",
    "https://github.com/Manablaq/genlayer-outcome-attestation-registry",
    [
      "Repository: https://github.com/Manablaq/genlayer-outcome-attestation-registry",
      "Documentation: https://manablaq.github.io/genlayer-outcome-attestation-registry/",
      "Contract: 0xd660ef089b4798e9c47B94CDDDE0EcEe5Fd29F63",
      "Test Evidence: https://github.com/Manablaq/genlayer-outcome-attestation-registry/blob/main/TEST_LOG_BRADBURY.md",
    ].join("\n"),
    "Submission package for a reusable GenLayer Intelligent Contract primitive.",
    604800n,
  ],
  value: BigInt(0),
});

await client.waitForTransactionReceipt({
  hash: decisionTx,
  status: TransactionStatus.FINALIZED,
});

const resolveTx = await client.writeContract({
  address: gateAddress,
  functionName: "resolve_required_fields_decision",
  args: [1n],
  value: BigInt(0),
});

await client.waitForTransactionReceipt({
  hash: resolveTx,
  status: TransactionStatus.FINALIZED,
});

const allowed = await client.readContract({
  address: gateAddress,
  functionName: "is_allowed",
  args: [1n, 7000],
  stateStatus: "accepted",
});

console.log({ allowed });
