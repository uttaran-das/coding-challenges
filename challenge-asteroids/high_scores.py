import os

def load_high_scores():
    if os.path.exists("high_scores.txt"):
        with open("high_scores.txt", "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    return []

def save_high_scores(high_scores):
    with open("high_scores.txt", "w") as file:
        for score in high_scores:
            file.write(f"{score}\n")

def update_high_scores(new_score, high_scores):
    high_scores.append(new_score)
    high_scores.sort(reverse=True)
    if len(high_scores) > 10:
        high_scores.pop()
    save_high_scores(high_scores)
    return high_scores