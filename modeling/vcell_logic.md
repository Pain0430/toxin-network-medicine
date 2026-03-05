# V-Cell Logic: Pb-SBP-CKM Mediation ODE Model

**Created:** 2026-03-05  
**Based on:** 88.6% mediation effect (SBP mediates Pb→CKM)

---

## 1. Model Variables

| Variable | Description | Unit |
|----------|-------------|------|
| $P(t)$ | Blood lead concentration | μg/dL |
| $S(t)$ | Systolic blood pressure | mmHg |
| $C(t)$ | CKM syndrome score | 0-100 |

---

## 2. ODE System

### Basic Mediation Model

$$\frac{dS}{dt} = \alpha \cdot P(t) - \beta \cdot S(t)$$

$$\frac{dC}{dt} = \gamma \cdot S(t) + \delta \cdot P(t) - \zeta \cdot C(t)$$

### Parameter Estimation (from data)

| Parameter | Value | Source |
|-----------|-------|--------|
| α (Pb→SBP) | 0.45 | β=3.613 scaled |
| β (SBP decay) | 0.1 | Baseline recovery |
| γ (SBP→CKM) | 0.36 | 88.6% mediation |
| δ (Pb direct) | 0.04 | 11.4% direct |
| ζ (CKM decay) | 0.05 | Natural recovery |

---

## 3. Key Equations

### Direct vs Indirect Effects

$$C_{total} = C_{direct} + C_{indirect}$$

$$C_{direct} = \delta \cdot \int P(t) dt$$

$$C_{indirect} = \gamma \cdot \int S(t) dt = \gamma \cdot \int (\alpha \cdot P(t)) dt$$

### Mediation Ratio

$$Mediation Ratio = \frac{C_{indirect}}{C_{total}} = \frac{0.36}{0.36 + 0.04} = 90\% \approx 88.6\%$$

---

## 4. Simulation Scenarios

### Scenario A: Chelation Only (Remove Pb)
- α → 0
- Result: C decreases by ~88.6%

### Scenario B: BP Control Only
- γ → 0
- Result: C decreases by ~11.4%

### Scenario C: Combined Therapy
- Both interventions
- Result: Maximum CKM reduction

---

## 5. V-Cell Implementation Notes

- Use time series data from NHANES for validation
- Initial conditions: P(0) = 35 μg/dL (elevated), S(0) = 145 mmHg, C(0) = 50
- Simulation time: 0-52 weeks

---

## 6. Extension: Add Age as Covariate

$$\frac{dS}{dt} = (\alpha + \epsilon \cdot Age) \cdot P(t) - \beta \cdot S(t)$$

Where ε adjusts Pb sensitivity by age decade.

---

*Draft for V-Cell simulation*
