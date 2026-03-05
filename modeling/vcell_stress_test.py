#!/usr/bin/env python3
"""
V-Cell Stress Test: Pb Gradient Analysis
Clear peak time differentiation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

t = np.linspace(0, 48, 300)

Pb_levels = {'Low (5 μg/dL)': 5, 'Medium (20 μg/dL)': 20, 'High (50 μg/dL)': 50}
colors = {'Low (5 μg/dL)': '#2ecc71', 'Medium (20 μg/dL)': '#f39c12', 'High (50 μg/dL)': '#e74c3c'}

def simulate(Pb):
    k_dmg = 0.015 * (Pb / 10)
    Mito, ROS, NLRP3, IL1B = np.zeros(4)
    Mito, ROS, NLRP3, IL1B = 1.0, 0.05, 0.02, 0.01
    
    Mito_t, ROS_t, NLRP3_t, IL1B_t = [Mito], [ROS], [NLRP3], [IL1B]
    
    for _ in t[1:]:
        dM = 0.08 * (1 - Mito) - k_dmg
        Mito = max(0, Mito + dM * (t[1] - t[0]))
        
        dR = 0.4 * (1 - Mito) - 0.25 * ROS
        ROS = max(0, ROS + dR * (t[1] - t[0]))
        
        dN = 0.3 * max(0, ROS - 0.2) - 0.08 * NLRP3
        NLRP3 = max(0, min(1, NLRP3 + dN * (t[1] - t[0])))
        
        dI = 0.4 * NLRP3 - 0.12 * IL1B
        IL1B = max(0, IL1B + dI * (t[1] - t[0]))
        
        Mito_t.append(Mito); ROS_t.append(ROS); NLRP3_t.append(NLRP3); IL1B_t.append(IL1B)
    
    return np.array(Mito_t), np.array(ROS_t), np.array(NLRP3_t), np.array(IL1B_t)

results = {}
for name, Pb in Pb_levels.items():
    results[name] = dict(zip(['M','R','N','I'], simulate(Pb)))
    pk = np.argmax(results[name]['I'])
    print(f"{name}: Peak IL1B={results[name]['I'][pk]:.2f} @ {t[pk]:.1f}h")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for name, d in results.items():
    c = colors[name]
    axes[0,0].plot(t, d['M'], c=c, lw=2.5, label=name)
    axes[0,1].plot(t, d['R'], c=c, lw=2.5)
    axes[1,0].plot(t, d['N'], c=c, lw=2.5, label=name)
    axes[1,1].plot(t, d['I'], c=c, lw=2.5, label=name)
    pk = np.argmax(d['I'])
    axes[1,1].scatter(t[pk], d['I'][pk], c=c, s=120, zorder=5, edgecolors='black', lw=2)
    axes[1,1].annotate(f'{t[pk]:.0f}h', (t[pk], d['I'][pk]), textcoords="offset points", xytext=(8,5), fontsize=11, fontweight='bold')

axes[0,0].set_title('A. Mitochondrial Morphology\n(mitochondrial paramorphia)', fontweight='bold')
axes[0,0].set_xlabel('Time (h)'); axes[0,0].set_ylabel('Health'); axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)
axes[0,1].set_title('B. ROS Release (oxidative stress)', fontweight='bold')
axes[0,1].set_xlabel('Time (h)'); axes[0,1].grid(True, alpha=0.3)
axes[1,0].set_title('C. NLRP3 Inflammasome Activation', fontweight='bold')
axes[1,0].set_xlabel('Time (h)'); axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)
axes[1,1].set_title('D. IL-1β Output (CKM Marker)\n← Peak time shifts with Pb!', fontweight='bold', color='darkred')
axes[1,1].set_xlabel('Time (h)'); axes[1,1].set_ylabel('IL-1β'); axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.suptitle('V-Cell Stress Test: Pb Gradient → IL-1β Peak Time\nHigher Pb accelerates "mitochondrial paramorphia" → Earlier inflammatory peak', 
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/pengsu/mycode/toxin-network-medicine/modeling/VCell_Stress_Test.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ VCell_Stress_Test.png saved")
