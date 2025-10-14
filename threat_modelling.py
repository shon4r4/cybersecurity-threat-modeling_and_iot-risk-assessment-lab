import yaml
import pandas as pd
import numpy as np

# map likelihood to probability ranges
likelihood_map = {
    "low": (0.01, 0.05),
    "medium": (0.05, 0.1),
    "high": (0.1, 0.2)
}

####################################################
###                 CALCULATE RISK               ###
####################################################

def calculate_risk(threat):
    dread = threat.get("dread", {})

    d = dread.get("damage", {})
    r = dread.get("reproducibility", {})
    e = dread.get("exploitability", {})
    a = dread.get("affected_users", {})
    di = dread.get("discoverability", {})

    total = (d + r + e + a + di) / 5

    return {
        "damage": d,
        "reproducibility": r,
        "exploitability": e,
        "affected_users": a,
        "discoverability": di,
        "dread_score": round(total, 2),
    }

####################################################
###                 WALK THE TREE                ###
####################################################

def walk_tree(node, path=None, results=None):
    if results is None:
        results = []
    if path is None:
        path = []

    for key, value in node.items():
        if isinstance(value, dict) and "impact" in value:
            row = {f"L{i+1}": p for i, p in enumerate(path)} 
            row["threat"] = key
            row["impact"] = value.get("impact")
            row["likelihood"] = value.get("likelihood")
            
            if "dread" in value:
                scores = calculate_risk(value)
                row.update(scores)
            
            results.append(row)

        elif isinstance(value, dict):
            walk_tree(value, path + [key], results)

    return results


####################################################
###            MONTE CARLO SIMULATIONS           ###
####################################################

# Run Monte Carlo simulation for each threat
def simulate_monte_carlo(threat_row, trials):
    likelihood = threat_row["likelihood"]
    low, high = likelihood_map[likelihood]

    outcomes = []
    for _ in range(trials):
        p = np.random.uniform(low, high)
        outcome = np.random.rand() < p
        outcomes.append(outcome)

    incidents = np.sum(outcomes)
    prob = incidents / trials

    return pd.Series({
        "monte_carlo_prob": prob,
        "monte_carlo_incidents": incidents
    })

# Run Monte Carlo for all rows and append result to the df
def run_monte_carlo(df, trials):
    df[["monte_carlo_prob", "monte_carlo_incidents"]] = df.apply(
        lambda row: simulate_monte_carlo(row, trials=trials), axis=1
    )
    return df

if __name__ == "__main__":
    with open("input.yaml", "r") as f:
        data = yaml.safe_load(f)
    
    attack_tree = data.get("attack_tree", {})

    # walk the tree, flatten yaml to df and calculate risk score
    results = walk_tree(attack_tree)
    df = pd.DataFrame(results)
    print(df.sort_values("dread_score", ascending=False))
    df.to_csv("dread_score.csv", index=False)

    # run monte carlo and append to the df
    df = run_monte_carlo(df, trials=50000)
    print(df.sort_values("monte_carlo_prob", ascending=False))
    df.to_csv("monte_carlo_simulation.csv", index=False)
    
    df["priority"] = df["monte_carlo_prob"] * df["dread_score"]
    print(df.sort_values("priority", ascending=False))
    df.to_csv("prioritisation.csv", index=False)