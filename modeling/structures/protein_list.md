# Pb/As-Sensitive Bridging Proteins

## Seed Proteins (from user_style_guide)

| Protein | Gene | Function | Pb/As Sensitivity |
|---------|------|----------|------------------|
| NLRP3 | NLRP3 | Inflammasome | HIGH |
| MFN2 | MFN2 | Mitochondrial fusion | HIGH |
| PINK1 | PINK1 | Mitophagy | HIGH |
| LRRK2 | LRRK2 | Neuroinflammation | MODERATE |
| NOTCH1 | NOTCH1 | Neurodevelopment | MODERATE |

## 10 Bridging Proteins (Predicted)

| Protein | UniProt | Interaction | Relevance |
|---------|----------|-------------|------------|
| CASP1 | P29474 | Interacts with NLRP3 | Apoptosis |
| IL1B | P01584 | NLRP3 downstream | Inflammation |
| TXN | P10599 | ROS regulation | Antioxidant |
| SQSTM1 | Q13501 | p62 - autophagy | Ubiquitin |
| MAP1LC3A | Q8WXR9 | LC3 - autophagy | Autophagy |
| BDNF | P23560 | Neuroprotection | Neuro |
| GSR | P16455 | Glutathione reductase | Oxidative stress |
| HMOX1 | P09601 | Heme oxygenase-1 | Antioxidant |
| NFE2L2 | Q14145 | Nrf2 - antioxidant | Oxidative stress |
| APP | P05067 | Amyloid precursor | Neurodegeneration |

## PDB/AlphaFold Structures

| Protein | Source | PDB ID | Status |
|---------|--------|--------|--------|
| NLRP3 | AlphaFold | AF-Q9N2R1 | Available |
| MFN2 | AlphaFold | AF-Q8IWA4 | Available |
| PINK1 | PDB | 6ELS | Crystallized |
| CASP1 | PDB | 1SC4 | Crystallized |
| IL1B | PDB | 1ITB | Crystallized |

---

## V-Cell Mechanistic Chain

Pb → Mitochondrial morphology (MFN2/PINK1) → ROS release → NLRP3 activation → Endothelial damage → SBP elevation

**Key Equations:**
- d[ROS]/dt = α₁×[Pb] - β₁×[Antioxidants]
- d[NLRP3]/dt = α₂×[ROS] - β₂×[Anti-inflammatory]
- d[SBP]/dt = α₃×[NLRP3] - β₃×[BP_medication]
