from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectWaitBar, OnscreenText
from panda3d.core import Point3, Vec3, TransparencyAttrib, LPoint3f
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Func, Wait, LerpColorScaleInterval
import random

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.player_x = 0

        # Paper스 체력 30으로 변경
        self.boss_hp = 30

        # 플레이어 체력 3으로 설정
        self.player_hp = 3

        # UI - Paper스 HP바
        self.hp_bar = DirectWaitBar(text="", value=100, pos=(0, 0, 0.8), scale=0.6)
        self.hp_text = OnscreenText(text="Boss HP", pos=(0, 0.9), scale=0.07)

        # 플레이어 체력 표시 (좌측 상단)
        self.player_hp_text = OnscreenText(text=f"Player HP: {self.player_hp}", pos=(-1.2, 0.9), scale=0.07)

        self.load_models()

        self.accept("a", self.move_player, [-1])
        self.accept("d", self.move_player, [1])
        self.accept("mouse1", self.swing_sword)

        self.taskMgr.doMethodLater(3, self.boss_attack, 'bossAttack')

        self.warning_effect = None
        self.game_over = False

    def load_models(self):
        self.player = Actor("models/panda-model",
                            {"walk": "models/panda-walk4"})
        self.player.reparentTo(self.render)
        self.player.setScale(0.0025)
        self.player.setPos(self.player_x, 10, 0)

        self.boss = loader.loadModel("models/box")
        self.boss.reparentTo(self.render)
        self.boss.setScale(1.5, 1.5, 3)
        self.boss.setPos(0, 20, 0)

    def move_player(self, direction):
        if self.game_over:
            return
        self.player_x = max(-5, min(5, self.player_x + direction))
        self.player.setX(self.player_x)
        self.player.play("walk")
        self.doMethodLater(0.5, self.stop_walk, 'stopWalk')

    def stop_walk(self, task):
        self.player.stop()
        return task.done

    def swing_sword(self):
        if self.game_over:
            return
        print("Sword swung!")
        seq = Sequence(
            Func(self.player.setColorScale, (1, 0.5, 0.5, 1)),
            Wait(0.2),
            Func(self.player.clearColorScale)
        )
        seq.start()

        if abs(self.player_x - self.boss.getX()) < 1.5:
            self.boss_hp -= 1
            print(f"Boss hit! HP left: {self.boss_hp}")
            self.update_hp_bar()
            if self.boss_hp <= 0:
                print("Boss defeated!")
                self.boss.hide()
                self.show_message("Boss Defeated!")
                self.game_over = True

    def update_hp_bar(self):
        self.hp_bar['value'] = (self.boss_hp / 30) * 100

    def boss_attack(self, task):
        if self.game_over:
            return task.done

        attack_pos = random.choice([-3, 0, 3])
        print(f"Boss will attack at {attack_pos}")

        if self.warning_effect:
            self.warning_effect.removeNode()
        self.warning_effect = loader.loadModel("models/smiley")
        self.warning_effect.reparentTo(self.render)
        self.warning_effect.setScale(0.7)
        self.warning_effect.setPos(attack_pos, 19, 0.5)
        self.warning_effect.setColor(1, 0, 0, 1)
        self.warning_effect.setTransparency(TransparencyAttrib.MAlpha)

        blink = Sequence(
            LerpColorScaleInterval(self.warning_effect, 0.5, (1, 0, 0, 0.2)),
            LerpColorScaleInterval(self.warning_effect, 0.5, (1, 0, 0, 1)),
        )
        blink.loop()

        self.taskMgr.doMethodLater(1, self.execute_attack, 'executeAttack', extraArgs=[attack_pos], appendTask=True)
        return task.again

    def execute_attack(self, attack_pos, task):
        if self.warning_effect:
            self.warning_effect.removeNode()
            self.warning_effect = None

        flash = loader.loadModel("models/smiley")
        flash.reparentTo(self.boss)
        flash.setScale(2)
        flash.setColor(1, 0, 0, 1)
        flash.setTransparency(TransparencyAttrib.MAlpha)
        flash.setPos(0, 0, 2)

        flash_seq = Sequence(
            LerpColorScaleInterval(flash, 0.3, (1, 0, 0, 0)),
            Func(flash.removeNode)
        )
        flash_seq.start()

        if abs(self.player_x - attack_pos) < 1.5:
            print("Player hit by boss attack!")
            self.player_hp -= 1
            self.player_hp_text.setText(f"Player HP: {self.player_hp}")
            hurt_seq = Sequence(
                Func(self.player.setColorScale, (1, 0, 0, 1)),
                Wait(0.3),
                Func(self.player.clearColorScale)
            )
            hurt_seq.start()

            if self.player_hp <= 0:
                print("Game Over")
                self.show_message("Game Over")
                self.game_over = True
                return task.done
        else:
            print("Player dodged the attack!")

        return task.done

    def show_message(self, text):
        self.msg = OnscreenText(text=text, pos=(0, 0), scale=0.15, fg=(1,1,1,1), mayChange=False, align=0)

game = Game()
game.run()