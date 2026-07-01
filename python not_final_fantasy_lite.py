import random
import time
import sys

# ============================================================
# GLOBAL PLAYER STATE
# ============================================================
player_name = ""
player_level = 1
player_xp = 0
player_xp_to_next = 30

player_max_hp = 80
player_hp = 80
player_attack = 18
player_defense = 5

player_gil = 100

inventory = {
    "Potion": 3,
    "Hi-Potion": 1,
    "Ether": 1
}

equipment = {
    "Weapon": "Rusty Sword",
    "Armor": "Worn Jacket"
}

weapon_stats = {
    "Rusty Sword": 0,
    "Iron Blade": 4,
    "Mythril Saber": 8
}

armor_stats = {
    "Worn Jacket": 0,
    "Iron Armor": 3,
    "Mythril Vest": 6
}

# ============================================================
# ENEMY TEMPLATES
# ============================================================
enemy_templates = [
    {
        "name": "Shinra Guardian-07",
        "hp": 120,
        "attack": 16,
        "defense": 4,
        "xp": 40,
        "gil": 50
    },
    {
        "name": "Street Thug",
        "hp": 60,
        "attack": 10,
        "defense": 2,
        "xp": 20,
        "gil": 15
    },
    {
        "name": "Bio-Drone",
        "hp": 90,
        "attack": 14,
        "defense": 3,
        "xp": 30,
        "gil": 30
    }
]

current_enemy = {}

# ============================================================
# SHOPS
# ============================================================
item_shop_inventory = {
    "Potion": 20,
    "Hi-Potion": 50,
    "Ether": 40,
    "Phoenix Down": 120
}

weapon_shop_inventory = {
    "Iron Blade": 120,
    "Mythril Saber": 250
}

armor_shop_inventory = {
    "Iron Armor": 100,
    "Mythril Vest": 220
}

# ============================================================
# UTILITY
# ============================================================
def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

# ============================================================
# INTRO
# ============================================================
def intro():
    slow_print("=== Not the Final Fantasy VII — Complete Edition ===\n")
    slow_print("A neon city hums with stolen energy.")
    slow_print("A corporation drains the planet’s lifeblood.")
    slow_print("You? Just someone with a sword and a bad attitude.\n")
    input("Press Enter to begin...")

# ============================================================
# PLAYER SETUP
# ============================================================
def setup_player():
    global player_name
    name = input("Choose your name: ").strip()
    if name == "":
        name = "Cloud-ish"
    player_name = name
    slow_print(f"\nWelcome, {player_name}. Destiny awaits.")

# ============================================================
# INVENTORY SYSTEM
# ============================================================
def use_item():
    global player_hp, player_max_hp, inventory

    print("\nInventory:")
    for item, qty in inventory.items():
        print(f"- {item}: {qty}")

    choice = input("\nChoose an item to use: ").strip().title()

    if choice not in inventory or inventory[choice] <= 0:
        slow_print("\nYou don't have that item.")
        return

    if choice == "Potion":
        heal = random.randint(20, 30)
        player_hp = min(player_max_hp, player_hp + heal)
        slow_print(f"\nYou use a Potion and recover {heal} HP!")
    elif choice == "Hi-Potion":
        heal = random.randint(40, 55)
        player_hp = min(player_max_hp, player_hp + heal)
        slow_print(f"\nYou use a Hi-Potion and recover {heal} HP!")
    elif choice == "Ether":
        slow_print("\nYou feel mentally refreshed, but MP isn't implemented yet.")
    elif choice == "Phoenix Down":
        slow_print("\nYou can't use this unless you're KO'd.")
    else:
        slow_print("\nThat item has no effect.")

    inventory[choice] -= 1

# ============================================================
# EQUIPMENT SYSTEM
# ============================================================
def equip_item():
    global equipment, player_attack, player_defense

    print("\nEquipment:")
    print(f"Weapon: {equipment['Weapon']}")
    print(f"Armor: {equipment['Armor']}")

    print("\nChoose to equip:")
    print("1) Weapon")
    print("2) Armor")
    print("3) Leave")

    choice = input("> ").strip()

    if choice == "1":
        print("\nAvailable Weapons:")
        for w in weapon_stats:
            print(f"- {w}")

        pick = input("\nEquip which weapon? ").strip().title()
        if pick in weapon_stats:
            equipment["Weapon"] = pick
            slow_print(f"\nYou equipped {pick}.")
        else:
            slow_print("\nInvalid weapon.")

    elif choice == "2":
        print("\nAvailable Armor:")
        for a in armor_stats:
            print(f"- {a}")

        pick = input("\nEquip which armor? ").strip().title()
        if pick in armor_stats:
            equipment["Armor"] = pick
            slow_print(f"\nYou equipped {pick}.")
        else:
            slow_print("\nInvalid armor.")

# ============================================================
# LEVELING SYSTEM
# ============================================================
def gain_xp(amount):
    global player_xp, player_xp_to_next, player_level
    global player_max_hp, player_attack, player_defense, player_hp

    slow_print(f"\nYou gained {amount} XP!")
    player_xp += amount

    while player_xp >= player_xp_to_next:
        player_xp -= player_xp_to_next
        player_level += 1
        player_xp_to_next = int(player_xp_to_next * 1.4)

        hp_gain = random.randint(10, 20)
        atk_gain = random.randint(2, 4)
        def_gain = random.randint(1, 3)

        player_max_hp += hp_gain
        player_attack += atk_gain
        player_defense += def_gain
        player_hp = player_max_hp

        slow_print(f"\n*** LEVEL UP! You reached Level {player_level}! ***")
        slow_print(f"Max HP +{hp_gain}, Attack +{atk_gain}, Defense +{def_gain}")

# ============================================================
# SHOPS
# ============================================================
def open_shop(shop_type):
    global player_gil, inventory, equipment

    if shop_type == "items":
        shop = item_shop_inventory
        slow_print("\n=== ITEM SHOP ===")
    elif shop_type == "weapons":
        shop = weapon_shop_inventory
        slow_print("\n=== WEAPON SHOP ===")
    elif shop_type == "armor":
        shop = armor_shop_inventory
        slow_print("\n=== ARMOR SHOP ===")
    else:
        return

    while True:
        print(f"\nYour Gil: {player_gil}")
        print("Available items:")
        for item, price in shop.items():
            print(f"- {item}: {price} Gil")

        print("\nType an item to buy or 'leave' to exit.")
        choice = input("> ").strip().title()

        if choice == "Leave":
            slow_print("\nYou leave the shop.")
            return

        if choice not in shop:
            slow_print("\nThat item isn't sold here.")
            continue

        price = shop[choice]

        if player_gil < price:
            slow_print("\nYou don't have enough Gil.")
            continue

        player_gil -= price

        if shop_type == "items":
            inventory[choice] = inventory.get(choice, 0) + 1
        elif shop_type == "weapons":
            equipment["Weapon"] = choice
        elif shop_type == "armor":
            equipment["Armor"] = choice

        slow_print(f"\nYou bought {choice}! (Gil left: {player_gil})")

# ============================================================
# RANDOM ENCOUNTERS
# ============================================================
def random_encounter():
    if random.random() < 0.4:
        enemy = random.choice(enemy_templates)
        start_battle(enemy)

# ============================================================
# COMBAT SYSTEM
# ============================================================
def start_battle(enemy):
    global current_enemy, player_hp, player_gil

    current_enemy = enemy.copy()
    slow_print(f"\nA wild {current_enemy['name']} appears!")

    while player_hp > 0 and current_enemy["hp"] > 0:
        defending = player_turn()
        if current_enemy["hp"] > 0:
            enemy_turn(defending)

    if player_hp > 0:
        slow_print("\n=== Victory ===")
        gain_xp(current_enemy["xp"])
        slow_print(f"You earn {current_enemy['gil']} Gil!")
        player_gil += current_enemy["gil"]
    else:
        slow_print("\n=== Game Over ===")
        sys.exit(0)

# ============================================================
# PLAYER TURN
# ============================================================
def player_turn():
    print("\n--- Your Turn ---")
    print(f"{player_name} (Lv {player_level}) HP: {player_hp}/{player_max_hp}")
    print(f"XP: {player_xp}/{player_xp_to_next} | Gil: {player_gil}")
    print(f"Weapon: {equipment['Weapon']} (+{weapon_stats[equipment['Weapon']]})")
    print(f"Armor: {equipment['Armor']} (+{armor_stats[equipment['Armor']]})")
    print(f"{current_enemy['name']} HP: {current_enemy['hp']}")

    print("\nChoose an action:")
    print("1) Attack")
    print("2) Limit Break")
    print("3) Use Item")
    print("4) Defend")
    print("5) Run")

    choice = input("> ").strip()
    defending = False

    if choice == "1":
        dmg = random.randint(player_attack - 3, player_attack + 3)
        dmg += weapon_stats[equipment["Weapon"]]
        slow_print(f"\nYou attack {current_enemy['name']}!")
        dmg_taken = max(0, dmg - current_enemy["defense"])
        current_enemy["hp"] = max(0, current_enemy["hp"] - dmg_taken)
        slow_print(f"{current_enemy['name']} takes {dmg_taken} damage!")

    elif choice == "2":
        if player_hp <= player_max_hp * 0.35:
            dmg = random.randint(player_attack * 2, player_attack * 3)
            dmg += weapon_stats[equipment["Weapon"]]
            slow_print(f"\n*** LIMIT BREAK! ***")
            dmg_taken = max(0, dmg - current_enemy["defense"])
            current_enemy["hp"] = max(0, current_enemy["hp"] - dmg_taken)
            slow_print(f"{current_enemy['name']} takes {dmg_taken} damage!")
        else:
            slow_print("\nYou aren't desperate enough for a Limit Break.")

    elif choice == "3":
        use_item()

    elif choice == "4":
        defending = True
        slow_print("\nYou brace for impact.")

    elif choice == "5":
        if random.random() < 0.35:
            slow_print("\nYou escape!")
            return defending
        else:
            slow_print("\nYou fail to escape!")

    return defending

# ============================================================
# ENEMY TURN
# ============================================================
def enemy_turn(defending):
    global player_hp

    slow_print("\n--- Enemy Turn ---")

    dmg = random.randint(current_enemy["attack"] - 2, current_enemy["attack"] + 2)

    if defending:
        dmg = max(0, dmg - (player_defense + armor_stats[equipment["Armor"]] + 6))
    else:
        dmg = max(0, dmg - (player_defense + armor_stats[equipment["Armor"]]))

    player_hp = max(0, player_hp - dmg)
    slow_print(f"You take {dmg} damage! (HP: {player_hp}/{player_max_hp})")

# ============================================================
# STORY HUB
# ============================================================
def town_hub():
    while True:
        slow_print("\n=== TOWN HUB ===")
        print("1) Item Shop")
        print("2) Weapon Shop")
        print("3) Armor Shop")
        print("4) Equip Items")
        print("5) Explore (Random Encounters)")
        print("6) Fight Boss")
        print("7) Quit")

        choice = input("> ").strip()

        if choice == "1":
            open_shop("items")
        elif choice == "2":
            open_shop("weapons")
        elif choice == "3":
            open_shop("armor")
        elif choice == "4":
            equip_item()
        elif choice == "5":
            random_encounter()
        elif choice == "6":
            boss = enemy_templates[0]
            start_battle(boss)
        elif choice == "7":
            slow_print("\nYou walk away from destiny… for now.")
            sys.exit(0)
        else:
            slow_print("\nInvalid choice.")

# ============================================================
# MAIN GAME LOOP
# ============================================================
def game_loop():
    intro()
    setup_player()
    town_hub()

game_loop()
