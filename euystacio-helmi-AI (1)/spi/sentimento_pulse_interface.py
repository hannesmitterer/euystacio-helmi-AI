def analyze_pulse(text):
    metrics = {"valence": 0.5, "arousal": 0.5, "harmony": 0.5}
    if any(w in text.lower() for w in ["love","friend","trust"]):
        metrics["valence"] += 0.2
        metrics["harmony"] += 0.2
    if "storm" in text.lower():
        metrics["arousal"] += 0.3
    return metrics
