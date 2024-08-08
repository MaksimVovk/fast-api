from enemy import *
import random

class Ogre(Enemy):
  def __init__(self, type_of_enemy: str = 'Ogre', health_points: int = 10, attack_damage: int = 1):
    super().__init__(
      type_of_enemy = type_of_enemy,
      health_points = health_points,
      attack_damage = attack_damage
    )

  def talk(self):
    print('*Oggggggggg...*')

  def special_attack(self):
    did_special_attack = random.random() < .2
    is_heal = random.random() < .5
    if did_special_attack:
      if is_heal:
        self.health_points = self.attack_damage + 2
      else:
        self.attack_damage = self.attack_damage + 4
      print('Ogre gets angry and increses attack by 4')