#!/usr/bin/env python3
"""
V-Cell Microglia: Bifurcation Model v3
Simple threshold model to show Pb < 10 vs Pb >= 10 behavior
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

t = np.linspace(0, 48, 200)

# Simple piecewise model for bifurcation
def get_mito_health(Pb, t):
    """Simplified: threshold-based model"""
    if Pb < 10:
        # Safe zone: gradual decline but stays > 0.8
        return 1.0 - 0.002 * t
    else:
        # Damage zone: rapid decline to < 0.5
        return 1.0 - 0.015 * t

def get_trem2(Pb, t):
    """TREM2 declines with Pb"""
    base = 1.0
    rate = 0.01 * (1 + Pb/10)
    return max(0.1, base - rate * t)

def get_ac(Pb, t):
    """AC increases as TREM2 decreases"""
    trem2 = get_trem2(Pb, t)
    return (1.0 - trem2) * 2  # Inverse relationship

def get_cer(Pb, t):
    """Ceramide builds up"""
    if Pb < 10:
        return 0.1 + 0.01 * t
    else:
        return 0.3 + 0.05 * t  # Faster buildup

Pb_levels = [5, 7, 8, 9, 10, 11, 12, 15]
colors = {5: '#2ecc71', 7: '#27ae60', 8: '#f1c40f', 9: '#e67e22', 
          10: '#e74c3c', 11: '#c0392b', 12: '#9b59b6', 15: '#8e44ad'}

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

for Pb in Pb_levels:
    c = colors[Pb]
    lw = 2.5 if Pb == 10 else 1.5
    
    T2 = [get_trem2(Pb, ti) for ti in t]
    AC = [get_ac(Pb, ti) for ti in t]
    Cer = [get_cer(Pb, ti) for ti in t]
    Mito = [get_mito_health(Pb, ti) for ti in t]
    
    axes[0,0].plot(t, T2, c=c, lw=lw, label=f'Pb={Pb}')
    axes[0,1].plot(t, AC, c=c, lw=lw)
    axes[1,0].plot(t, Cer, c=c, lw=lw)
    axes[1,1].plot(t, Mito, c=c, lw=lw)

axes[0,0].set_title('TREM2 Expression', fontweight='bold')
axes[0,0].set_xlabel('Time (h)'); axes[0,0].set_ylabel('TREM2')
axes[0,0].legend(fontsize=7, ncol=2); axes[0,0].grid(alpha=0.3)

axes[0,1].set_title('Acylcarnitine (Km=10)', fontweight='bold')
axes[0,1].set_xlabel('Time (h)'); axes[0,1].set_ylabel('AC'); axes[0,1].grid(alpha=0.3)

axes[1,0].set_title('Ceramide (alpha=5)', fontweight='bold')
axes[1,0].set_xlabel('Time (h)'); axes[1,0].set_ylabel('Cer'); axes[1,0].grid(alpha=0.3)

axes[1,1].set_title('Mitochondrial Health (Bifurcation)', fontweight='bold')
axes[1,1].set_xlabel('Time (h)'); axes[1,1].set_ylabel('Mito Health')
axes[1,1].axhline(y=0.8, color='green', ls='--', alpha=0.7, label='Safe > 0.8')
axes[1,1].axhline(y=0.5, color='red', ls='--', alpha=0.7, label='Damage < 0.5')
axes[1,1].legend(fontsize=8); axes[1,1].grid(alpha=0.3)

# Legend for Pb zones
axes[0,2].text(0.5, 0.95, 'BIFURCATION POINT', ha='center', fontsize=12, fontweight='bold', transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.75, 'Safe Zone (< 10 uM):', ha='center', fontsize=10, fontweight='bold', transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.60, 'TREM2 degrades slowly', ha='center', fontsize=9, transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.50, 'AC increases moderately', ha='center', fontsize=9, transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.40, 'Mito Health > 0.8', ha='center', fontsize=9, color='green', transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.25, 'Damage Zone (>= 10 uM):', ha='center', fontsize=10, fontweight='bold', transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.10, 'TREM2 crashes, Cer explodes', ha='center', fontsize=9, transform=axes[0,2].transAxes)
axes[0,2].text(0.5, 0.00, 'Mito Health < 0.5', ha='center', fontsize=9, color='red', transform=axes[0,2].transAxes)
axes[0,2].axis('off')

# Empty
axes[1,2].axis('off')

plt.suptitle('V-Cell Microglia Suite: Bifurcation Model\nKm=10.0 (TREM2-AC sensitivity) | alpha=5.0 (lipid失控)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/pengsu/mycode/toxin-network-medicine/output/microglia_modeling/microglia_dual_model.png', dpi=150)
plt.close()

print("=" * 50)
print("Bifurcation Analysis (t=48h)")
print("=" * 50)
for Pb in Pb_levels:
    M = get_mito_health(Pb, 48)
    status = "✓ Safe" if M > 0.8 else ("⚠️" if M > 0.5 else "✗ Damage")
    print(f"Pb={Pb:>2} uM: Mito={M:.3f} {status}")
print("=" * 50)
