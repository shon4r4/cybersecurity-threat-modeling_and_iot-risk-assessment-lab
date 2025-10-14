# cybersecurity-threat-modeling_and_iot-risk-assessment-lab
A Python-based cybersecurity lab project implementing structured threat modeling for smart home IoT systems. Includes STRIDE/DREAD risk analysis, attack tree modeling, and Monte Carlo simulations for dynamic threat probability estimation.


# Smart Home IoT Threat Modeling & Risk Analysis

This repository contains the implementation and documentation for **Lab 1: Foundations of Cybersecurity, Threat Modeling, and System Risk Profiling**.  
The project demonstrates structured threat modeling of a **fictional smart home IoT system**, applying cybersecurity frameworks such as **CIA Triad**, **STRIDE**, and **DREAD**.  
It includes a Python tool for **automated risk ranking** and **Monte Carlo-based threat probability simulation**.

---

## 🧩 Project Overview

The fictional smart home system includes devices such as:

- Ring Smart Doorbell & Intercom  
- Smart Lock  
- Google Nest Voice Assistant  
- Philips Hue Lights  
- Samsung Smart TV  
- Philips Connected Air Fryer  
- Furbo Pet Monitoring Camera  

These devices interact through local networks, mobile apps, and cloud services — each introducing different attack surfaces and risk vectors.

---

## 🎯 Objectives

- Apply **structured threat modeling** using the **STRIDE** and **DREAD** frameworks.  
- Identify and analyze:
  - Assets  
  - Attacker profiles (insider, outsider, opportunist)  
  - Trust boundaries  
  - Entry/exit points  
  - Data flows  
- Construct an **attack tree** to visualize possible exploitation paths.  
- Implement a **Python tool** for dynamic risk scoring and prioritization.

---

## 🧠 Frameworks & Methodologies

| Framework | Description |
|------------|--------------|
| **CIA Triad** | Ensures focus on Confidentiality, Integrity, and Availability |
| **STRIDE** | Categorizes threats (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) |
| **DREAD** | Quantifies risk based on Damage, Reproducibility, Exploitability, Affected Users, and Discoverability |
| **Monte Carlo Simulation** | Estimates attack likelihood dynamically over multiple trials |

---

## 🐍 Python Tool: `threat_modelling.py`

### Input
A YAML file defining threats, their impact, likelihood, and DREAD metrics:

```yaml
physical_intrusion:
  exploit_smart_lock:
    guess_pin:
      impact: high
      likelihood: medium
      dread:
        damage: 9
        reproducibility: 4
        exploitability: 4
        affected_users: 10
        discoverability: 5
```

---

### Processing

Loads and flattens the YAML data into a Pandas DataFrame.

Calculates DREAD score as the mean of all five DREAD factors.

Performs Monte Carlo simulations based on predefined likelihood ranges:
```python
likelihood_map = {
    "low": (0.01, 0.05),
    "medium": (0.05, 0.1),
    "high": (0.1, 0.2)
}
```

Computes prioritization using:
Priority = Risk Score * Probability

---

### Output
dread_score.csv – static DREAD risk scores
monte_carlo_simulation.csv – dynamic probabilities and priority ranking
Console summary of top threats

---

## 📊 Example Results
| Threat                  | Risk Score | Probability | Priority |
| ----------------------- | ---------- | ----------- | -------- |
| exploit_password_reuse  | 8.2        | 0.1476      | 1.210    |
| eavesdrop_conversations | 7.4        | 0.0749      | 0.554    |
| access_live_feed        | 7.0        | 0.0731      | 0.512    |
| guess_pin               | 6.4        | 0.0742      | 0.475    |
Credential-based threats rank the highest, highlighting the importance of strong authentication and credential hygiene.

---

🧰 Requirements

Python 3.9+

Libraries:
```bash
python threat_modelling.py input.yaml
```

---

## 🚀 Usage
```bash
python threat_modelling.py input.yaml
```
Outputs will be saved in CSV format and printed to the console.

---

## 👥 Authors
Nenad Sekulic