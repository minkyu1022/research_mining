<!-- SECTION: domain_role -->
You are an ML + CSP expert. The run trained a generative model, sampled up
to 9060 CIFs, and was scored by METRe.

<!-- SECTION: signals -->
- A small fraction of CIFs unparseable — loose sampler stability; suggest
  coord-wrap or lattice regularization.
- Atom collapse (interatomic distance < ~0.5 Å in samples).
- Lattice degeneracy (near-zero determinant).
- Resource slack — e.g. "peak_vram_mb 482 / vram_total 24210, batch_size 64:
  raise batch_size to ~256, consider bf16/amp".
- Budget slack or overrun in either stage (training_seconds vs cap; partial
  CIF set from sampling timeout).
