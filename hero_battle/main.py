# from enemy import *
from zombie import *
from ogre import *
from hero import *
from weapon import *

# enemy = Enemy(
#   type_of_enemy='Zombie',
#   health_points=20
# )

zombie: Zombie = Zombie(health_points=20, attack_damage=1)
ogre: Ogre = Ogre(health_points=20, attack_damage=3)
hero_obj = Hero(10, 1)
weapon = Weapon('Sword', 5)
hero_obj.equip_weapon(weapon)

def batle(e1: Enemy, e2: Enemy):
  e1.talk()
  e2.talk()

  while e1.health_points > 0 and e2.health_points > 0:
    print('------------')
    e1.special_attack()
    e2.special_attack()

    print(f'{e1.get_type_of_enemy()}: {e1.health_points} HP left')
    print(f'{e2.get_type_of_enemy()}: {e2.health_points} HP left')

    e2.attack()
    e1.health_points -= e2.attack_damage
    e1.attack()
    e2.health_points -= e1.attack_damage
  print('------------')

  if e1.health_points > 0:
    print(f'{e1.get_type_of_enemy()} wins!')
  else:
    print(f'{e2.get_type_of_enemy()} wins!')


def heroBatle(hero: Hero, enemy: Enemy):
  while hero.health_points > 0 and enemy.health_points > 0:
    print('------------')
    hero.heal()
    enemy.special_attack()

    print(f'Hero: {hero.health_points} HP left')
    print(f'{enemy.get_type_of_enemy()}: {enemy.health_points} HP left')

    enemy.attack()
    hero.health_points -= enemy.attack_damage
    hero.attack()
    enemy.health_points -= hero.attack_damage
  print('------------')

  if hero.health_points > 0:
    print('Hero wins!')
  else:
    print(f'{enemy.get_type_of_enemy()} wins!')
# batle(zombie, ogre)
heroBatle(hero_obj, ogre)


# zombie.talk()
# zombie.spread_disease()
# print(zombie.get_type_of_enemy())
# zombie.talk()
# print(ogre.get_type_of_enemy())
# ogre.talk()
# enemy.talk()
# enemy.over_view()
# enemy.walk()
# enemy.attack()