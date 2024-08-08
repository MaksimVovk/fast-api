from enemy import *
import random

class Zombie(Enemy):
    def __init__(self, type_of_enemy: str = 'Zombie', health_points: int = 10, attack_damage: int = 1):
      super().__init__(
        type_of_enemy = type_of_enemy,
        health_points = health_points,
        attack_damage = attack_damage
      )

    def talk(self):
      print('*Grumbling...*')

    def spread_disease(self):
       print('The zombie is trying to spread infection!')

    def special_attack(self):
       did_special_attack = random.random() < .5

       if did_special_attack:
          self.health_points = self.health_points + 2
          print('Zombie regenerate 2 hp!')