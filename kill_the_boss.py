#
# 需求：打boss
#
# 字段说明：
# 1.血量:float类型
# 2.防御力:float类型，定义自身防御力
# 3.攻击力:float类型，定义自身攻击力
# 4.伤害:攻击力-防御力（如果对方防御力>=自身攻击力则为miss，伤害为0）
#
# 需求说明：
# 1.创建一个Boss类，自定义name,血量,防御力,攻击力
# 2.创建一个Hero类，自定义name,血量,防御力,攻击力
# 3.Boss拥有普通攻击（伤害=自身攻击力），群攻大招（伤害=自身攻击力*1.5，对每个Hero造成伤害，每三次普通攻击后，触发一次），以及防御技能（免除所有伤害）
# 4.Hero拥有普通攻击（伤害=自身攻击力），必杀技（伤害=自身攻击力*2，每两次普通攻击后，触发一次），以及防御技能（免除一次伤害）
# 5.Boss和Hero的回合次数保持一致，即每回合放一个技能（攻击还是防御）
# 6.Hero可以组队，有多个Hero同时挑战
# 7.任何一方（Boss或者Hero队伍）生命值耗完即为死亡，程序最后提示 Boss是否挑战成功，结束程序
# 说明：回合制，一秒一次，普通攻击和防御的比例为3:1（随机触发）
#

import random
# import time


class Boss:

    def __init__(self, name, hm, defense, attack):
        self.name = name
        self.hm = hm
        self.defense = defense
        self.attack = attack
        self.action_num = 1
        self.is_defense = False
        self.defense_num = 0

    def common_attack(self):
        return self.attack

    def unique_attack(self):
        return self.attack * 1.5

    def common_defense(self, num):
        self.defense_num = num
        self.is_defense = True

    def defense_attack(self):
        self.defense_num -= 1
        if self.defense_num == 0:
            self.is_defense = False

    def double_harm(self, int_value):
        if random.randint(0, 15) in [0, 1]:
            print(f"{self.name}狂怒了！当次攻击造成两倍伤害！")
            # time.sleep(1.5)
            return int_value*2
        else:
            return int_value

    def use_unique_attack(self, hero_obj_list):
        is_double_harm = self.double_harm(self.unique_attack())
        print(f"{self.name}使用了必杀技！！！！！")
        # time.sleep(1.5)
        for hero_obj in hero_obj_list:
            if not hero_obj.is_defense:
                harm = is_double_harm - hero_obj.defense
                if harm > 0:
                    if hero_obj.hm > 0:
                        hero_obj.hm -= harm
                        if hero_obj.hm <= 0:
                            hero_obj.hm = 0
                        print(f"BOSS必杀技对{hero_obj.name}造成了{harm}点伤害，{hero_obj.name}当前的血量为{hero_obj.hm}")
                        # time.sleep(1.5)
                else:
                    print(f"BOSS必杀技并未对{hero_obj.name}造成伤害，{hero_obj.name}当前的血量为{hero_obj.hm}")
                    # time.sleep(1.5)
            else:
                print(f"{hero_obj.name}使用了防御技能，本次伤害无效，{hero_obj.name}当前的血量为{hero_obj.hm}")
                # time.sleep(1.5)
                hero_obj.is_defense = False
        self.action_num += 1
        return

    def use_attack_or_defense(self, hero_obj_list):
        attack_or_defense = random.randint(0, 4)
        if attack_or_defense == 0 and not self.is_defense:
            self.common_defense(len(hero_obj_list))
            print(f"{self.name}使用了防御技能")
            # time.sleep(1.5)
        else:
            harm_hero = random.choice(hero_obj_list)
            if not harm_hero.is_defense:
                common_harm = self.double_harm(self.common_attack()) - harm_hero.defense
                if common_harm > 0:
                    harm_hero.hm -= common_harm
                    if harm_hero.hm <= 0:
                        harm_hero.hm = 0
                    print(
                        f"{self.name}使用普通攻击攻击了{harm_hero.name},造成了{common_harm}点伤害，"
                        f"{harm_hero.name}当前的血量为{harm_hero.hm}")
                    # time.sleep(1.5)
                else:
                    print(
                        f"{self.name}使用普通攻击攻击了{harm_hero.name},但并未对{harm_hero.name}造成伤害，"
                        f"{harm_hero.name}当前的血量为{harm_hero.hm}")
                    # time.sleep(1.5)
            else:
                print(
                    f"{self.name}使用普通攻击攻击了{harm_hero.name},但由于{harm_hero.name}使用了防御技能，"
                    f"本次BOSS攻击不生效,{harm_hero.name}当前的血量为{harm_hero.hm}")
                # time.sleep(1.5)
                harm_hero.is_defense = False
        self.action_num += 1
        return

    def boss_action(self, hero_obj_list):
        print(f"第{self.action_num}回合")
        # time.sleep(1.5)
        if self.action_num % 3 == 0:
            self.use_unique_attack(hero_obj_list)
        else:
            self.use_attack_or_defense(hero_obj_list)


class Hero:

    def __init__(self, name, hm, defense, attack):
        self.name = name
        self.hm = hm
        self.defense = defense
        self.attack = attack
        self.action_num = 1
        self.is_defense = False
        self.all_harm = 0

    def common_attack(self):
        return self.attack

    def unique_attack(self):
        return self.attack * 1.6

    def common_defense(self):
        self.is_defense = True

    def double_harm(self, int_value):
        if random.randint(0, 15) == 0:
            print(f"{self.name}狂怒了！当次攻击造成两倍伤害！")
            # time.sleep(1.5)
            return int_value*2
        else:
            return int_value

    def add_up_harm(self, value):
        self.all_harm += value

    def use_unique_attack(self, boss_obj):
        if not boss_obj.is_defense:
            harm = self.double_harm(self.unique_attack()) - boss_obj.defense
            if harm > 0:
                boss_obj.hm -= harm
                self.add_up_harm(harm)
                if boss_obj.hm < 0:
                    boss_obj.hm = 0
                print(f"{self.name}使用必杀技！对boss造成了{harm}点伤害，当前boss血量为{boss_obj.hm}")
                # time.sleep(1.5)
            else:
                print(f"{self.name}使用了必杀技！但并未对{harm}造成伤害，当前boss血量为{boss_obj.hm}")
                # time.sleep(1.5)
        else:
            boss_obj.defense_attack()
            print(f"{self.name}使用了必杀技！但由于boss使用了防御技能，本次攻击无效，当前boss血量为{boss_obj.hm}")
            # time.sleep(1.5)
        self.action_num += 1
        return

    def user_attack_or_defense(self, boss_obj):
        attack_or_defense = random.randint(0, 4)
        if attack_or_defense == 0 and not self.is_defense:
            self.common_defense()
            print(f"{self.name}使用了防御技能")
            # time.sleep(1.5)
        else:
            common_harm = self.double_harm(self.common_attack()) - boss_obj.defense
            if not boss_obj.is_defense:
                if common_harm > 0:
                    boss_obj.hm -= common_harm
                    self.add_up_harm(common_harm)
                    if boss_obj.hm < 0:
                        boss_obj.hm = 0
                    print(f"{self.name}使用普通攻击造成了{common_harm}点伤害，当前boss血量为{boss_obj.hm}")
                    # time.sleep(1.5)
                else:
                    print(f"{self.name}使用了普通攻击，但并未对boss造成伤害，当前boss血量为{boss_obj.hm}")
                    # time.sleep(1.5)
            else:
                print(f"{self.name}使用了普通攻击，但由于boss使用了防御技能，本次攻击无效，当前boss血量为{boss_obj.hm}")
                # time.sleep(1.5)
                boss_obj.defense_attack()
        self.action_num += 1
        return

    def hero_action(self, boss_obj):
        if self.action_num % 2 == 0:
            self.use_unique_attack(boss_obj)
        else:
            self.user_attack_or_defense(boss_obj)


if __name__ == '__main__':
    boss_list = [Boss("哥斯拉", 450, 45, 60), Boss("特美拉", 500, 30, 70), Boss("江凯", 500, 40, 60),
                 Boss("菜鸡", 500, 50, 55), Boss("巨猪", 400, 30, 80)]
    boss = random.choice(boss_list)
    all_hero_list = [Hero("奥特曼", 160, 30, 70), Hero("假面超人", 200, 40, 60),
                     Hero("绿巨人", 60, 80, 55), Hero("力王", 50, 30, 150)]
    hero_tuple = random.sample(all_hero_list, 2)
    hero_alive_list = list(hero_tuple)
    boss_is_alive = True
    print(f"本次遇到的boss为{boss.name}")
    # time.sleep(1.5)
    print(f"本方出战英雄为{hero_tuple[0].name}和{hero_tuple[1].name}，战斗开始")
    # time.sleep(1.5)
    while hero_alive_list and boss_is_alive:
        boss.boss_action(hero_alive_list)
        for hero in hero_tuple:
            if hero.hm <= 0:
                print(f"{hero.name}已死，无法行动")
                # time.sleep(1.5)
                if hero in hero_alive_list:
                    hero_alive_list.remove(hero)
            else:
                hero.hero_action(boss)
                if boss.hm <= 0:
                    print(f"{hero.name}成功击倒了boss！")
                    # time.sleep(1.5)
                    boss_is_alive = False
                    break
    print("")
    if boss.hm <= 0:
        print(f'BOSS{boss.name}被歼灭，游戏结束，游戏获胜！')
        # time.sleep(1.5)
    else:
        print('英雄全军覆没，游戏结束，游戏失败。')
        # time.sleep(1.5)
    print(f'BOSS{boss.name}剩余血量:{boss.hm}\n')
    for hero_hm in hero_tuple:
        print(f'英雄{hero_hm.name}剩余血量:{hero_hm.hm}')
        print(f'英雄{hero_hm.name}累计造成伤害:{hero_hm.all_harm}')
