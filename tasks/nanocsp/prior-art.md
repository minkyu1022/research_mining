# Published generative models for inorganic crystal structure generation

Last updated: 2026-05-26. Scope: inorganic crystals only (MOFs, molecular
crystals, and organic-inorganic hybrids excluded).

Used by `idea` subagent as the novelty boundary — no emitted cell may
share BOTH (paradigm, architecture) axes with any entry below. Single-axis
overlap is allowed.

## Diffusion (continuous / score-based denoising)

- **CDVAE** (2022): `vae`+`score-matching` + `equivariant-GNN`. VAE encoder + score-based Langevin decoder for periodic materials; foundational MP-20 baseline. ICLR 2022 / arXiv:2110.06197.
- **DiffCSP** (2023): `diffusion` + `equivariant-GNN`. Joint equivariant diffusion over lattice (Cartesian) and fractional coords. NeurIPS 2023 / arXiv:2309.04475.
- **DiffCSP++** (2024): `diffusion` + `equivariant-GNN`. Space-group / Wyckoff-conditioned extension of DiffCSP. ICLR 2024.
- **MatterGen** (2025): `diffusion` + `equivariant-GNN`. Joint diffusion over atom types, coords, lattice; property-conditional fine-tuning. Nature 2025.
- **UniMat** (2024): `diffusion` + `CNN` (3D U-Net). Unified 4D periodic-table tensor representation. arXiv:2311.09235.
- **SyMat** (2023): `diffusion` + `equivariant-GNN`. Symmetry-enhanced CDVAE variant. NeurIPS 2023.
- **GemsDiff** (2023): `diffusion` + `equivariant-GNN`. Equivariant GNN-based diffusion. AI4Mat 2023.
- **DP-CDVAE** (2024): `diffusion` + `equivariant-GNN`. DDPM-based CDVAE variant. Sci. Reports 2024.
- **Cond-CDVAE / Con-CDVAE** (2024): `diffusion`+`vae` + `equivariant-GNN`. Composition / pressure-conditioned CDVAE. npj Comp. Mat. 2024 (arXiv:2403.10846).
- **CrysTens** (2024): `diffusion` (also GAN variant) + `CNN`. Image-like pairwise distance representation.
- **StructRepDiff** (2024): `diffusion` + `MLP`. Diffusion in EAM descriptor space.
- **EH-Diff** (2025): `diffusion` + `hypergraph-NN` (equivariant). Equivariant hypergraph diffusion for periodic crystals. arXiv:2501.18850.
- **TransVAE-CSP** (2025): `vae`+`diffusion` + `equivariant-transformer`. Transformer-enhanced equivariant encoder.
- **TGDMat** (2025): `diffusion` + `GNN`. Text-guided contextual diffusion.
- **DAO-G** (2025): `diffusion`+`ebm` + `GNN`. Energy-based diffusion.
- **Chemeleon** (2025): `diffusion` + `equivariant-GNN`+`transformer`. Multi-modal text-guided diffusion via cross-modal contrastive alignment. Digital Discovery / PMC 2025.
- **SymmCD** (2025): `diffusion` + `GNN`. Symmetry-preserving diffusion over Wyckoff binary matrix + coords. ICLR 2025 / arXiv:2502.03638.
- **DiffCrysGen** (2025): `score-matching` + `CNN`. SDE-based score net over 2D point-cloud / matrix representation. arXiv:2505.07442.
- **CrystalDiT** (2025): `diffusion` + `transformer`. Diffusion Transformer (DiT) for crystals. arXiv:2508.16614.
- **Space-Group Equivariant Crystal Diffusion** (2025): `diffusion` + `equivariant-GNN`. Space-group equivariant denoiser. arXiv:2505.10994.
- **Symmetry-aware Conditional Diffusion** (2026 preprint): `diffusion` + `equivariant-GNN`. Symmetry-conditional crystal diffusion. arXiv:2601.08115.
- **Equivariant Diffusion for CSP** (2025): `diffusion` + `equivariant-GNN`. arXiv:2512.07289.
- **PXRDGen** (2025): `diffusion` (or flow) + `GNN`+`transformer`. PXRD-conditional generator + Rietveld refinement. Nat. Commun. 2025 / arXiv:2409.04727.

## Flow matching / continuous normalizing flows

- **FlowMM** (2024): `flow-matching` + `equivariant-GNN`. Riemannian flow matching adapted to crystal symmetries. ICML 2024 / arXiv:2406.04713.
- **FlowLLM** (2024): `flow-matching`+`autoregressive` + `LLM`+`equivariant-GNN`. LLM as base distribution, RFM refines coords/lattice. NeurIPS 2024 / arXiv:2410.23405.
- **CrystalFlow** (2024-25): `flow-matching` + `equivariant-GNN`. Pressure-conditioned continuous normalizing flows. PMC 2025 / arXiv:2412.11693.
- **OMatG** (2025): `stochastic interpolants` + `equivariant-GNN`. Unified stochastic-interpolant framework covering diffusion and flow as special cases. ICML 2025 / arXiv:2502.02582.
- **Multimodal Crystal Flow** (2026 preprint): `flow-matching` + `transformer`. Any-to-any modality flow for unified crystal modeling. arXiv:2602.20210.

## VAE (variational autoencoder)

- **iMatGen** (2019): `vae` + `CNN` (voxel). Hierarchical voxel VAE for vanadium oxides. Matter 2019.
- **FTCP** (2022): `vae` + `MLP`. Fourier-transformed (reciprocal+real space) VAE. Matter 2022.
- **PCVAE** (2023): `vae` + `MLP`. Physics-informed descriptors (Bravais lattice, space group, lattice constants) via fully-connected encoder/decoder.
- **WyCryst** (2024): `vae` + `MLP`+`GNN`. Wyckoff-positions property-guided VAE. arXiv:2311.17916.
- **LCOM** (2023): `vae`+`diffusion` + `equivariant-GNN`. Conservative-model CDVAE extension.

## GAN (generative adversarial)

- **CrystalGAN** (2019): `gan` + `MLP` (point cloud). Hydride generation.
- **DD3DCS** (2019): `gan` + `CNN` (voxel). Voxel-grid GAN for general structures.
- **CondGAN** (2019): `gan` + `MLP` (bag-of-atoms). Composition-conditioned GAN.
- **MatGAN** (2020): `gan` + `MLP`. Element-conditioned composition+structure GAN. npj Comp. Mat. 2020.
- **GANCSP / CrystalGAN-CSP** (2020): `gan` + `MLP` (point cloud). Composition-aware GAN for CSP. ACS Cent. Sci. 2020 / arXiv:2004.01396.
- **ICSG3D** (2020): `vae`+`gan` + `CNN` (voxel). Energy-conditioned cubic structures.
- **CubicGAN** (2021): `gan` + `MLP`. Cubic-system generator.
- **CCDCGAN** (2021, ext. 2022): `vae`+`gan` + `CNN` (voxel). Two-stage VAE-GAN.
- **PGCGM** (2023): `gan` + `MLP` (Wyckoff). Physics-informed Wyckoff GAN for ternaries.
- **CGWGAN** (2024): `gan` + `MLP` (Wyckoff). Two-step template-based Wyckoff GAN.
- **LCMGM** (2024): `vae`+`gan` + `CNN`. Mesh-grid (reciprocal+real-space, FTCP-style) tensor decoded by convolutional encoder/decoder with adversarial latent sampling. npj Comp. Mat. 2024.
- **NSGAN** (2024): `gan`+`rl-generative` (GA hybrid) + `MLP`. Hybrid GAN-genetic-algorithm for alloys.
- **VGD-CG** (2024): `gan`+`vae`+`diffusion` + `MLP`. Property-targeted composition generator.

## Autoregressive / language-model-based

- **XYZTransformer** (2023): `autoregressive` + `transformer`. Fine-tuned LLM on XYZ-format structures.
- **CrystaLLM** (2024): `autoregressive` + `LLM` (GPT-2). CIF-format LLM. Nat. Commun. 2024 / arXiv:2307.04340.
- **CrystalTextLLM** (2024): `autoregressive` + `LLM` (Llama-2). Fine-tuned Llama on text point-cloud crystals.
- **CrysText** (2024): `autoregressive` + `LLM` (Llama-3.1). CIF generation, RL variant with GRPO. ChemRxiv 2024.
- **CrystalFormer** (2024): `autoregressive` + `transformer`. Space-group-conditioned decoder-only transformer over Wyckoff tokens.
- **WyFormer / Wyckoff Transformer** (2025): `autoregressive` + `transformer`. Permutation-invariant Wyckoff token autoregressor. ICML 2025 / arXiv:2503.02407.
- **Matra-Genoa** (2025): `autoregressive` + `transformer`. Wyckoff autoregressive transformer on 2M structures.
- **MatExpert** (2024): `autoregressive` + `LLM`. Multi-step conversational agent.
- **GenMS** (2024): `autoregressive`+`diffusion` + `LLM`+`GNN`. Two-stage LLM formula → diffusion structure.
- **Mat2Seq** (2025): `autoregressive` + `LLM`. Domain-agnostic invariant sequence encoding.
- **NatureLM-Mat3D** (2025): `autoregressive` + `LLM` (Llama-3). Fine-tuned multi-domain sequence LM.
- **MatLLMSearch** (2025): `autoregressive`+`rl-generative` + `LLM`. LLM with evolutionary search.
- **Uni-3DAR** (2025): `autoregressive` + `transformer`. Octree-compressed voxel autoregression.
- **UniGenX** (2025): `autoregressive`+`diffusion` + `transformer`. Hybrid autoregressive composition + coordinate diffusion.
- **deCIFer** (2025): `autoregressive` + `LLM`. CIF autoregression conditioned on PXRD. arXiv:2502.02189.
- **CrysReas / CrystalReasoner** (2026 preprint): `autoregressive`+`rl-generative` + `LLM`. RL-aligned property-conditioned LLM. arXiv:2605.14344.
- **MatterGPT** (2024): `autoregressive` + `transformer`. Decoder-only transformer trained from scratch on SLICES tokens (not fine-tuned from a pretrained LM). arXiv:2408.07608.
- **SLI2Cry** (2023): `autoregressive` + `RNN`. Invertible SLICES representation with RNN.

## Energy-based / EBM

- **ContinuouSP** (2025): `ebm` + `GNN` (CGCNN energy). Energy-based CSP enforcing invariance + continuity. arXiv:2502.02026.

## RL / active-learning generative

- **Crystal-GFN** (2023): `rl-generative` (GFlowNet) + `MLP`. Space-group / prototype GFlowNet. NeurIPS 2023 workshop.
- **CHGlownet** (2023): `rl-generative` (GFlowNet) + `GNN`. Graph-based generative flow network.
- **CrystalFormer-RL** (2025): `rl-generative` + `transformer`. RL fine-tuning of CrystalFormer. arXiv:2504.02367.
- **OMatG-IRL** (2026 preprint): `rl-generative` + `equivariant-GNN`. Inference-time RL on velocity fields for CSP. arXiv:2602.00424.
- **RL-guided latent crystal diffusion** (Park & Walsh 2025): `rl-generative`+`latent-diffusion` + `equivariant-GNN`. GRPO policy gradient on CDVAE/DiffCSP-style latent diffusion backbone. arXiv:2511.07158.

## Hybrid / other

- **CrysBFN** (2025): `bfn` + `equivariant-GNN`. Periodic E(3)-equivariant Bayesian flow network. ICLR 2025 / arXiv:2502.02016.
- **CrystalGRW** (2025): `geodesic-walk` + `equivariant-GNN`. Torus-manifold diffusion via geodesic walks. arXiv:2501.08998.
- **KLDM** (2025): `diffusion` (manifold/velocity) + `GNN`. Manifold diffusion via velocity space.
- **WyckoffDiff** (2025): `masked-discrete-diffusion` + `GNN`+`transformer`. Discrete diffusion over Wyckoff/space-group tokens. arXiv:2502.06485.
- **ADiT** (All-atom Diffusion Transformer) (2025): `latent-diffusion` + `transformer` (DiT + VAE). Unified latent diffusion over molecules + materials (materials portion = inorganic crystals). ICML 2025 / arXiv:2503.03965.
- **CGMD** (2024): `diffusion`+`vae`+`flow-matching` + `MLP`. Combined diffusion/VAE/flow point-cloud model.
- **CrysLLMGen / LLM-meets-Diffusion** (2025): `autoregressive`+`diffusion` + `LLM`+`GNN`. Hybrid LLM-diffusion crystal generator. NeurIPS 2025 / arXiv:2510.23040.
- **Fourier Latent Crystallographic Diffusion** (2026 preprint): `latent-diffusion` + `transformer`. arXiv:2602.12045.
- **DeepCSP** (2024): `diffusion`+`vae` + `equivariant-GNN`. Conditional CDVAE (Cond-CDVAE) variant with GemNet/DimeNet++ backbone. npj Comp. Mat. 2024 / arXiv:2403.10846.

## Excluded (not a learned generative model)

- **GNoME** (2023) — symmetry-aware elemental substitution + random structure search as the candidate generator, followed by a GNN energy-screening model. No learned structure generation in the diffusion/VAE/GAN/AR sense.

## Total: 72 entries (all uncertain labels resolved). MOFFlow / MOFDiff / MOF-BFN excluded as MOF-specific; GNoME excluded as non-generative-ML.
