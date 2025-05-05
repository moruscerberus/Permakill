# core/rewards.py
from core.assets import Assets

def load_rewards():
    return Assets.jsons["rewards"]

def apply_reward(player, reward):
    effect = reward["effect"]
    value = reward["value"]

    if effect == "max_health":
        player.max_health += value
        player.health += value
    elif effect == "regen":
        player.regen = value
    elif effect == "bullet_speed":
        player.bullet_speed += value
    elif effect == "shoot_cooldown":
        player.shoot_cooldown = max(0.05, player.shoot_cooldown + value)
    elif effect == "move_speed":
        player.move_speed += value
