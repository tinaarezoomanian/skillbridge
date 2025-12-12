def build_learning_plan(missing, resources):
    plan = []
    for i, s in enumerate(missing):
        plan.append({
            "Week": f"Week {i+1}",
            "Skill": s,
            "Resource": resources[s]
        })
    return plan
