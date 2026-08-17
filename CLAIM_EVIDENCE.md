# Non-Euclidean GNS claim-to-evidence ledger

This dossier separates paper-reported claims, source-audited statements, and evidence independently produced in this repository. The overall verdict is `INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY`; `publication_allowed` is false.

## C1 — 160M Llama step reductions for Signum and Muon

Paper claim: non-Euclidean GNS adaptive batching reports 66.61% and 66.77% reductions in optimizer steps for Signum and Muon while matching the constant-batch validation-loss baseline.

Paper production path: train the 160M Llama 3 model on 3.2B C4 tokens with ten seeds, compare B=64, B=256, Euclidean GNS, and non-Euclidean GNS schedules, then calculate the median reduction in steps needed to reach the baseline’s minimum validation loss. The source anchors are sections/experiments.tex:1-36 and 124-129, especially the Table 2 rows at lines 17-25.

Local evidence: the source PDF/archive and outputs/claim1_source_audit/summary.json establish only the source and local feasibility boundary. No Llama model, C4 data, training script, checkpoint, validation trace, or step-count calculation is present.

Status: UNVERIFIED LOCALLY.

## C2 — 160M results for signSGD, AdamW, and spectral descent

Paper claim: the same setup reports 22.58% for signSGD, 67.13% for AdamW, and 16.49% for stochastic spectral descent.

Paper production path: repeat the controlled ten-seed 160M protocol for each optimizer, using the optimizer-matched GNS schedule, then aggregate validation-loss and step-to-baseline metrics. The source anchors are sections/experiments.tex:1-25 and 124-129; the exact table values are at lines 17-23.

Local evidence: these numbers are preserved as paper-reported source facts. There is no local training run or independent metric output.

Status: UNVERIFIED.

## C3 — dual-norm GNS formulas

Paper claim: sign-based updates use the Manhattan GNS ||sigma_k||_1^2 / ||grad L(x_k)||_1^2, while spectral updates use the Nuclear GNS ||C_row,k^(1/2)||_S1^2 / ||grad L(X_k)||_S1^2.

Paper production path: derive the dual-norm error bound for sign descent, define coordinate-wise standard deviations, derive the row-wise covariance bound for spectral descent, and place the squared ratios in the summary table. The source anchors are sections/methods_new.tex:42-113 for sign descent, 118-205 for spectral descent, and 270-317 for the norm-geometry table.

Local evidence: src/claim3_norm_ratio_toy.py computes a finite four-sample vector case and four-sample 2x2 matrix case. The recorded outputs are l1_gns=0.48195497964664763 and s1_gns=0.23082879701965114. The spectral calculation uses the toy’s explicit diagonal covariance-square-root proxy. This checks bounded arithmetic only.

Status: TOY_SOURCE_NORM_RATIO.

## C4 — 1B Llama results

Paper claim: for the 1B Llama 3 setup, adaptive batching reports 31.84% and 12.11% reductions for signSGD and Signum, while AdamW does not reach the constant-batch baseline validation loss.

Paper production path: train the 1B model on 22B C4 tokens with sequence length 2048, compare the B=256 baseline with non-Euclidean GNS starting at B=64, and calculate steps to the baseline loss. The source anchors are sections/experiments.tex:124-159, especially the Table 3 rows at lines 149-153.

Local evidence: the source table is pinned in the archive, but no 1B model, 22B-token dataset, checkpoint, validation trace, or step-count calculation is present.

Status: UNVERIFIED.

## C5 — distributed variance estimator and adaptive algorithm

Paper claim: Algorithm 1 estimates the needed variance statistics from per-rank local gradients using DDP AllReduce and FSDP ReduceScatter/AllGather-compatible operations, then drives adaptive batch-size updates.

Paper production path: compute local gradients on each rank, aggregate the coordinate-wise squared gradients or row-wise Gram matrices, apply the B/(R-1) correction, form the GNS, smooth noise and signal with EMA, update after warm-up and every F iterations, enforce monotonic batch growth, and scale the learning rate by sqrt(B). The source anchors are sections/implementation.tex:3-49 for distributed estimation, 97-112 for heuristics, and 155-175 for Algorithm 1. Experimental settings are further specified in sections/appendix_exps.tex:40-63.

Local evidence: the pinned source contains the equations and algorithm. This repository has no DDP/FSDP implementation, rank-level gradient traces, collective-operation log, or distributed execution.

Status: UNVERIFIED.

## Boundary

The finite toy is evidence for selected norm-ratio arithmetic, not evidence for optimizer convergence, distributed variance estimation, adaptive scheduling, model quality, or the paper’s reported benchmark numbers. No claim is promoted to full reproduction.
