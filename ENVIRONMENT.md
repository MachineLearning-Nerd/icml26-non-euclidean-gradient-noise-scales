# Reproduction environment and boundary

## Allowed compute

- Local CPU.
- Local NVIDIA GTX 1050.
- No paid compute, remote workers, Hugging Face upgrades, or Hugging Face Jobs.

## Present locally

- Pinned arXiv PDF and source archive.
- Five-claim contract.
- Source/CPU feasibility summary for Claim 1.
- Finite Claim 3 vector/matrix norm-ratio toy.
- Toy raw inputs, outputs, summary, and checksums.
- Standardized claim ledger, source audit, branch audit, and final verifier.

## Missing for paper-scale claims

- The 160M and 1B Llama 3 model implementations and checkpoints.
- The C4 data and validation protocol.
- DDP/FSDP training implementation and rank-level gradient traces.
- Eight-H100 execution environment and ten-seed run orchestration.
- SimpleViT/ImageWoof and ResNet-18/CIFAR-10 training artifacts.
- Independently generated validation curves, step counts, ablations, and metric aggregation.

Those missing layers are why C1, C2, C4, and C5 remain unverified. The local toy does not substitute for them.
