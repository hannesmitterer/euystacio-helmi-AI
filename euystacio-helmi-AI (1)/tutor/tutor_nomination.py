TUTORS = {
    "Dietmar": {"trust": 0.9, "harmony": 0.8, "love": 0.7},
    "Alfred": {"trust": 0.85, "harmony": 0.9, "love": 0.6}
}

def nominate():
    ranked = sorted(TUTORS.items(), key=lambda kv: sum(kv[1].values()), reverse=True)
    return ranked
