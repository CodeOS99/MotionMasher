def load_save_file():
    import playerStats

    try:
        with open('save.motions.masher.topsecret', 'r') as f:
            lines = f.readlines()

        # Skip the first line (the "TOP SECRET" header)
        for line in lines[1:]:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                value, variable_name = parts

                # Convert value to appropriate type
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)

                # Update playerStats attributes
                if hasattr(playerStats, variable_name):
                    setattr(playerStats, variable_name, value)

        print("Game loaded successfully!")
    except Exception as e:
        print(f"Error loading save file: {e}")


def save_game():
    import playerStats

    try:
        with open('save.motions.masher.topsecret', 'w') as f:
            f.write("TOP SECRET! dO NOT EDIT!!1!\n")

            # Save each attribute
            f.write(f"{playerStats.attack_radius} passive_atk_radius\n")
            f.write(f"{playerStats.passive_attack_damage} passive_attack_damage\n")
            f.write(f"{playerStats.passive_attack_cooldown} passive_attack_cooldown\n")
            f.write(f"{playerStats.complete_attack_damage} complete_attack_damage\n")
            f.write(f"{playerStats.money} money\n")
            f.write(f"{playerStats.money_per_hit} money_per_hit\n")
            f.write(f"{playerStats.max_enemy_power} max_enemy_power\n")

        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")