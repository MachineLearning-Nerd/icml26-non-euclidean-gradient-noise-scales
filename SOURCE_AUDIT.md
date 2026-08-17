# Non-Euclidean GNS source audit

## Pinned artifacts

The local source artifacts are the arXiv 2602.03001 PDF and source archive:

| Artifact | SHA-256 |
| --- | --- |
| evidence/source/arxiv.pdf | 2894a33a0229e0193aec2f2c71e41f518251390f7de92a04e30c62cfd82506d2 |
| evidence/source/arxiv_source.tar.gz | 5375db1a154fbebff89303c15957bdef4592eb0556c02cb8f625285e563ca5de |

The archive has 46 members: 41 regular files and 5 directory entries. No regular member has an executable mode. The archive metadata file 00README.json reports TeX Live 2025 and pdflatex.

## Source member pins

Selected source members used for the claim audit are pinned below:

| Member | SHA-256 |
| --- | --- |
| 00README.json | 567bffe7ca323817f2d4d89689bc3503ea28c9920162939f2384203f7c2ead04 |
| example_paper.tex | 1a0a50e14348d263730ecef1b6a7c761e620289fedad40da60d24b0ea951c393 |
| sections/abstract.tex | 1d2d8499a139418e2fc981c5b508f3bee7e985d1f6bfb4287106e2e7de9a1bd3 |
| sections/introduction_new.tex | 34a7a59fe057012b2163fa7c02b0a62dcebd7988a55070f98d95456d232e95e4 |
| sections/methods_new.tex | 555a5aef7a2ddffc5f7b16e3e904ec4c303f5dfc96c7a135c016d2152f6615dc |
| sections/implementation.tex | 178ce7fcba63d6cb28350ea49d8b14ab16bb46d254f286413b45e7ab8ced0fdf |
| sections/experiments.tex | 975d2dcb4fb54179fb3f9a7566c3053affea1bef2ee9e2c13ab1372093187f33 |
| sections/appendix_exps.tex | ff66820b0e429588fa3de04f8b3be79bb80f969e7d3cbb8983f2932a823e0230 |
| Llama_results/introduction/gns_l1.csv | f3f7360372c80ca0d02d72c96c927726bbc9d96ecda175db977c7b704f660975 |
| Llama_results/introduction/gns_l2.csv | 62a52a363eda8b3f1b3d406ea417f356fe5b21f1e84329c0dec9ee7c5b3ec679 |
| Llama_results/llama_160M_main_csv/MUON_gns.csv | 02383ff6fb3c12f3eff1bc1496f5564290eced7888234d2b3f1d8041296b673c |
| Llama_results/llama_160M_main_csv/signum_gns.csv | ab5ef987494260ba1acbd880bb54c4123ea6d38efd32bb09e697d47d79b1bcb8 |

The complete archive remains available locally; the archive hash and member-count checks are enforced by verify_final.py. The CSV files are source-linked paper traces and are not presented as locally generated results.

## Paper production path

The source contains the theoretical derivation, the distributed estimation equations, Algorithm 1, language-model tables and traces, vision tables, and appendix hyperparameter settings. The central paper-reported language setup is 160M and 1B Llama 3 on C4 with 3.2B and 22B tokens, sequence length 2048, ten seeds, DDP, and eight H100 GPUs on one node. The vision section reports SimpleViT/ImageWoof and the appendix also describes ResNet-18/CIFAR-10.

The local repository does not contain the paper’s training implementation, model checkpoints, C4/ImageWoof/CIFAR-10 data, distributed logs, or independently generated metric files. The source archive is therefore evidence of what the paper says, not proof that this repository reproduced it.
