#!/usr/bin/env python3
"""
V-Cell Molecular Dynamics Model V1.0
Pb-SBP-CKM Mediation Cascade Simulation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib
matplotlib.use('Agg')

# Parameters
t = np.linspace(0, 72, 100)

k_synth = 1.0
k_deg_pb = 0.15
k_leak = 0.8
k_scav = 0.5
k_nlrp3 = 0.3
k_casp1 = 0.4
k_il1b = 0.6

def model(y, t):
    Mito, ROS, NLRP3, CASP1, IL1B = y
    Pb = 35 * np.exp(-0.01 * t)
    
    dMito = k_synth - k_deg_pb * Pb * Mito
    Nrf2 = max(0, 1 - ROS)
    dROS = k_leak * (1 - Mito) - k_scav * Nrf2 * ROS
    Hill = (ROS**2) / (0.3**2 + ROS**2)
    dNLRP3 = k_nlrp3 * Hill * (1 - NLRP3)
    dCASP1 = k_casp1 * NLRP3 * (1 - CASP1)
    dIL1B = k_il1b * CASP1 - 0.1 * IL1B
    return [dMito, dROS, dNLRP3, dCASP1, dIL1B]

y0 = [1.0, 0.1, 0.05, 0.1, 0.05]
sol = odeint(model, y0, t)
Mito, ROS, NLRP3, CASP1, IL1B = sol[:,0], sol[:,1], sol[:,2], sol[:,3], sol[:,4]

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0,0].plot(t, Mito, 'b-', lw=2)
axes[0,0].set_title('A. Mitochondrial Morphology\n(mitochondrial paramorphia)')
axes[0,0].set_xlabel('Time (h)'); axes[0,0].set_ylabel('Health')

axes[0,1].plot(t, ROS, 'r-', lw=2)
axes[0,1].set_title('B. ROS Release\n(oxidative stress)')

axes[1,0].plot(t, NLRP3, 'purple', lw=2, label='NLRP3')
axes[1,0].plot(t, CASP1, 'orange', lw=2, label='CASP1')
axes[1,0].set_title('C. Inflammasome Cascade')
axes[1,0].legend()

axes[1,1].plot(t, IL1B, 'darkred', lw=2)
axes[1,1].set_title('D. IL-1β Output\n(CKM marker)')

plt.suptitle('V-Cell Dynamics: Pb → Mitochondrial → NLRP3 → CKM\n(mitochondrial paramorphia & enhanced MFN2 ubiquitination)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/pengsu/mycode/toxin-network-medicine/modeling/VCell_Dynamics_Pb_CKM.png', dpi=150)
plt.close()

print("✅ VCell_Dynamics_Pb_CKM.png saved")
print(f"IL-1β final: {IL1B[-1]:.3f}")
