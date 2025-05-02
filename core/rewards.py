# core/rewards.py

import json

def load_rewards(path="data/rewards.json"):
    with open(path) as f:
        return json.load(f)

def apply_reward(player, reward):
    effect = reward["effect"]
    value = reward["value"]

    if effect == "max_health":
        player.max_health += value
        player.health += value
    elif effect == "regen":
        player.regen = value  # Assume you add regen to Player later
    elif effect == "bullet_speed":
        player.bullet_speed += value
    elif effect == "shoot_cooldown":
        player.shoot_cooldown = max(0.05, player.shoot_cooldown + value)  # negative = faster
    elif effect == "move_speed":
        player.move_speed += value
