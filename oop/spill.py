from __future__ import annotations
import random
from typing import List, Optional
from enum import Enum


class ItemType(Enum):
    HEALTH_POTION = "Health Potion"
    STRENGTH_POTION = "Strength Potion"
    SHIELD = "Shield"


class Character:
    def __init__(self, health: int, strength: int, name: str) -> None:
        self.health = health
        self.strength = strength
        self.name = name
        self.shield = 0

    def attack(self, target: Character, weapon: Weapon) -> None:
        attack_damage = self.calculate_damage(weapon)
        actual_damage = target.take_damage(attack_damage)
        print(
            f"{target.get_name()} has {target.get_health()} health left after {self.get_name()} did {actual_damage} damage"
        )

    def take_damage(self, damage: int) -> int:
        actual_damage = max(1, damage - self.shield)
        self.health -= actual_damage
        return actual_damage

    def calculate_damage(self, weapon: Weapon) -> int:
        return int(random.randint(1, 4)) * (weapon.damage + self.strength)

    def get_health(self) -> int:
        return self.health

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def get_name(self) -> str:
        return self.name


class Hero(Character):
    def __init__(
        self,
        health: int,
        strength: int,
        max_health: int,
        name: str,
        weapons: List[Weapon] = None,
    ) -> None:
        super().__init__(health, strength, name)
        self.weapons = weapons or []
        self.items: List[Item] = []
        self.experience = 0
        self.level = 1
        self.max_health = max_health
        self.skill_points = 0

    def heal(self, amount=1):
        if self.health + amount <= self.max_health:
            self.health += amount
        else:
            self.health = self.max_health

    def gain_experience(self, amount: int):
        self.experience += amount
        while self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.skill_points += 2
        self.max_health += 20
        self.health = self.max_health
        print(f"\n🎉 Level Up! You are now level {self.level}")
        print(f"You have {self.skill_points} skill points available")

    def use_item(self, item: Item) -> bool:
        if item in self.items:
            item.apply_effect(self)
            self.items.remove(item)
            return True
        return False

    def add_item(self, item: Item):
        self.items.append(item)
        print(f"Gained {item.name}!")

    def spend_skill_points(self, choice: str):
        if self.skill_points <= 0:
            print("No skill points available!")
            return

        match choice.upper():
            case "S":
                self.strength += 2
                print(f"Strength increased to {self.strength}")
            case "H":
                self.max_health += 30
                self.health += 30
                print(f"Max health increased to {self.max_health}")
            case _:
                print("Invalid choice")
                return

        self.skill_points -= 1


class Item:
    def __init__(self, name: str, effect_value: int):
        self.name = name
        self.effect_value = effect_value
        self.type = ItemType.HEALTH_POTION

    def apply_effect(self, character: Hero):
        match self.type:
            case ItemType.HEALTH_POTION:
                character.heal(self.effect_value)
                print(f"Healed for {self.effect_value} health!")
            case ItemType.STRENGTH_POTION:
                character.strength += self.effect_value
                print(f"Strength increased by {self.effect_value}!")
            case ItemType.SHIELD:
                character.shield += self.effect_value
                print(f"Shield increased by {self.effect_value}!")


class Enemy(Character):
    def __init__(
        self, health: int, strength: int, name: str, experience_value: int
    ) -> None:
        super().__init__(health, strength, name)
        self.experience_value = experience_value


class Weapon:
    def __init__(self, name: str, damage: int, level_requirement: int = 1) -> None:
        self.name = name
        self.damage = damage
        self.level_requirement = level_requirement


class Game:
    def __init__(self) -> None:
        self.enemies = self.create_enemies()
        self.available_weapons = self.create_weapons()
        self.hero = self.create_hero()
        self.run()

    def create_enemies(self) -> list[Enemy]:
        return [
            Enemy(200, 10, "Wolf", 50),
            Enemy(30, 7, "Snake", 30),
            Enemy(540, 3, "Bear", 100),
            Enemy(150, 15, "Bandit", 80),
            Enemy(400, 8, "Troll", 120),
        ]

    def create_weapons(self) -> list[Weapon]:
        return [
            Weapon("Rusty Sword", 3, 1),
            Weapon("Steel Sword", 5, 2),
            Weapon("Battle Axe", 8, 3),
            Weapon("Legendary Blade", 12, 5),
        ]

    def create_hero(self) -> Hero:
        starter_weapon = self.available_weapons[0]
        return Hero(300, 5, 300, "Hero", [starter_weapon])

    def drop_item(self) -> Optional[Item]:
        if random.random() < 0.3:  # 30% chance to drop an item
            item_type = ItemType.HEALTH_POTION.value
            effect_value = random.randint(10, 30)
            return Item(item_type.value, effect_value)
        return None

    def check_weapon_upgrades(self):
        for weapon in self.available_weapons:
            if (
                weapon not in self.hero.weapons
                and self.hero.level >= weapon.level_requirement
            ):
                self.hero.weapons.append(weapon)
                print(f"\nNew weapon unlocked: {weapon.name} (Damage: {weapon.damage})")

    def run(self) -> None:
        while any(enemy.is_alive for enemy in self.enemies) and self.hero.is_alive:
            current_enemy = random.choice([e for e in self.enemies if e.is_alive])
            print(f"\nEncountered {current_enemy.get_name()}!")
            print(f"Your health: {self.hero.health}/{self.hero.max_health}")

            while current_enemy.is_alive and self.hero.is_alive:
                available_weapons = [
                    f"{i+1}: {w.name}" for i, w in enumerate(self.hero.weapons)
                ]
                print("\nWeapons:", ", ".join(available_weapons))
                print(f"Items: {[item.name for item in self.hero.items]}")

                choice = input(
                    "Select action: H (heal), A (attack), I (use item), S (spend skill point): "
                )

                match choice.upper():
                    case "H":
                        self.hero.heal(10)
                        print(f"Healed up to {self.hero.health}")
                    case "A":
                        if len(self.hero.weapons) > 1:
                            weapon_choice = int(input("Select weapon (number): ")) - 1
                            if 0 <= weapon_choice < len(self.hero.weapons):
                                weapon = self.hero.weapons[weapon_choice]
                            else:
                                print("Invalid weapon choice")
                                continue
                        else:
                            weapon = self.hero.weapons[0]
                        self.hero.attack(current_enemy, weapon)
                    case "I":
                        if self.hero.items:
                            item = self.hero.items[0]  # Use first item for simplicity
                            self.hero.use_item(item)
                        else:
                            print("No items available!")
                            continue
                    case "S":
                        if self.hero.skill_points > 0:
                            choice = input("Spend point on: (S)trength or (H)ealth? ")
                            self.hero.spend_skill_points(choice)
                        else:
                            print("No skill points available!")
                            continue
                    case _:
                        print("Invalid choice!")
                        continue

                if current_enemy.is_alive:
                    current_enemy.attack(self.hero, Weapon("Claws", 1))

                if not current_enemy.is_alive:
                    print(f"\nDefeated {current_enemy.get_name()}!")
                    self.hero.gain_experience(current_enemy.experience_value)
                    dropped_item = self.drop_item()
                    if dropped_item:
                        self.hero.add_item(dropped_item)
                    self.check_weapon_upgrades()

        if self.hero.is_alive:
            print("\nCongratulations! You've defeated all enemies!")
        else:
            print("\nYou have died!")


class GameDisplay:
    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    game = Game()
