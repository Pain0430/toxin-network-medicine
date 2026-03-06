#!/usr/bin/env python3
"""
V-Cell Microglia Suite: Dual Dynamics Model
TREM2-Acylcarnitine (2023) vs TREM2-Ceramide (2024)
Pb threshold: 10 µM
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib
matplotlib.use('Agg')

t = np.linspace(0, 48, 100)

# Parameters
Pb_threshold = 10.0
k_syn_T = 0.5
k_deg_T_base = 0.02

# Model A
k_prod_AC = 0.3
k_clear_AC = 0.15
Km = 0.3

# Model B
k_syn_Cer = 0.2
k_deg_Cer = 0.1
alpha = 1.5
k_m_rep = 0.08
k_m_dam = 0.05
TREM2_base = 1.0

def model_A(y, t, Pb):
    TREM2, AC = y
    k_deg_T = k_deg_T_base * (1 + Pb / Pb_threshold)
    dTREM2 = k_syn_T - k_deg_T * TREM2
    dAC = k_prod_AC * (Km / (Km + TREM2)) - k_clear_AC * AC
    return [dTREM2, dAC]

def model_B(y, t, Pb):
    TREM2, Cer, Mito = y
    k_deg_T = k_deg_T_base * (1 + Pb / Pb_threshold)
    dTREM2 = k_syn_T - k_deg_T * TREM2
    fb = alpha * max(0, TREM2_base - TREM2) / TREM2_base
    dCer = k_syn_Cer * (1 + fb) - k_deg_Cer * Cer
    dMito = k_m_rep * (1 - Mito) - k_m_dam * Cer * Mito
    return [dTREM2, dCer, dMito]

Pb_levels = [5, 10, 15]
colors = {5: 'green', 10: 'orange', 15: 'red'}

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

results_A, results_B = {}, {}

for Pb in Pb_levels:
    y0_A = [1.0, 0.05]
    sol_A = odeint(model_A, y0_A, t, args=(Pb,))
    results_A[Pb] = {'TREM2': sol_A[:,0], 'AC': sol_A[:,1]}
    
    y0_B = [1.0, 0.05, 1.0]
    sol_B = odeint(model_B, y0_B, t, args=(Pb,))
    results_B[Pb] = {'TREM2': sol_B[:,0], 'Cer': sol_B[:,1], 'Mito': sol_B[:,2]}

for Pb in Pb_levels:
    c = colors[Pb]
    axes[0,0].plot(t, results_A[Pb]['TREM2'], c=c, lw=2, label=f'Pb={Pb}µM')
    axes[0,1].plot(t, results_A[Pb]['AC'], c=c, lw=2)
    axes[1,0].plot(t, results_B[Pb]['TREM2'], c=c, lw=2, label=f'Pb={Pb}µM')
    axes[1,1].plot(t, results_B[Pb]['Cer'], c=c, lw=2)
    axes[1,2].plot(t, results_B[Pb]['Mito'], c=c, lw=2)

axes[0,0].set_title('Model A (2023): TREM2 Expression\n(TREM2-Acylcarnitine axis)', fontweight='bold')
axes[0,0].set_xlabel('Time (h)'); axes[0,0].set_ylabel('TREM2'); axes[0,0].legend(); axes[0,0].grid(alpha=0.3)

axes[0,1].set_title('Model A: Acylcarnitine Accumulation', fontweight='bold')
axes[0,1].set_xlabel('Time (h)'); axes[0,1].set_ylabel('Acylcarnitine'); axes[0,1].grid(alpha=0.3)

axes[0,2].text(0.5, 0.5, 'Key Parameters:\n• Pb threshold: 10 µM\n• Km = 0.3\n• Phase lag: 4-8h', 
               ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               transform=axes[0,2].transAxes)
axes[0,2].axis('off')

axes[1,0].set_title('Model B (2024): TREM2 Expression\n(TREM2-Ceramide-Mito axis)', fontweight='bold')
axes[1,0].set_xlabel('Time (h)'); axes[1,0].set_ylabel('TREM2'); axes[1,0].legend(); axes[1,0].grid(alpha=0.3)

axes[1,1].set_title('Model B: Ceramide Accumulation\n(→ Mitochondrial Paramorphia)', fontweight='bold')
axes[1,1].set_xlabel('Time (h)'); axes[1,1].set_ylabel('Ceramide'); axes[1,1].grid(alpha=0.3)

axes[1,2].set_title('Model B: Mitochondrial Health\n(mitochondrial paramorphia)', fontweight='bold')
axes[1,2].set_xlabel('Time (h)'); axes[1,2].set_ylabel('Mito Health'); axes[1,2].grid(alpha=0.3)

plt.suptitle('V-Cell Microglia Suite: Dual Dynamics\nTREM2-Acylcarnitine (2023) vs TREM2-Ceramide (2024)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/pengsu/mycode/toxin-network-medicine/output/microglia_modeling/microglia_dual_model.png', 
            dpi=150, bbox_inches='tight')
plt.close()

print("=" * 50)
print("V-Cell Microglia Suite Results")
print("=" * 50)
for Pb in [5, 10, 15]:
    print(f"\nPb = {Pb} µM:")
    print(f"  Model A: TREM2 = {results_A[Pb]['TREM2'][-1]:.3f}, AC = {results_A[Pb]['AC'][-1]:.3f}")
    print(f"  Model B: TREM2 = {results_B[Pb]['TREM2'][-1]:.3f}, Cer = {results_B[Pb]['Cer'][-1]:.3f}, Mito = {results_B[Pb]['Mito'][-1]:.3f}")

print("\n✅ microglia_dual_model.png saved")
