class GameCharacter:
    def __init__(self, name, profession, level, health, attack_power):
        self.name = name
        self.profession = profession
        self.level = level
        self.health = health
        self.attack_power = attack_power

    def show_info(self):
        print("charactertest")
        print(f"nametest: {self.name}")
        print(f"professiontest: {self.profession}")
        print(f"leveltest: {self.level}")
        print(f"healthtest: {self.health}")
        print(f"attackpowertest: {self.attack_power}")

    def attack(self, target):
        print(
            f"nametest: {self.name}, targettest: {target}, "
            f"attackpowertest: {self.attack_power}"
        )

    def level_up(self):
        self.level += 1
        self.health += 20
        self.attack_power += 5
        print(f"leveluptest: {self.name}")
        print(
            f"leveltest: {self.level}, healthtest: {self.health}, "
            f"attackpowertest: {self.attack_power}"
        )


if __name__ == "__main__":
    hero = GameCharacter("nametest", "professiontest", 1, 100, 20)
    hero.show_info()
    print()
    hero.attack("targettest")
    print()
    hero.level_up()
