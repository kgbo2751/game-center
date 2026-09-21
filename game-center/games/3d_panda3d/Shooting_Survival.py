from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVector3, Point3, CollisionTraverser, CollisionHandlerEvent
from panda3d.core import LineSegs, TextNode, WindowProperties
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import random
import sys

class ZombieGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()
        self.camera.setPos(0, -50, 20)
        self.camera.setP(-20)

        props = WindowProperties()
        props.setCursorHidden(False)
        self.win.requestProperties(props)

        self.player_pos = Point3(0, 0, 0)
        self.health = 100
        self.score = 0
        self.zombies = []
        self.bullets = []

        self.init_player()
        self.init_ui()
        self.accept_inputs()

        self.taskMgr.add(self.update, "updateTask")
        self.spawn_zombie()

    def init_player(self):
        self.player = self.loader.loadModel("models/panda")
        self.player.setScale(0.005)
        self.player.setPos(self.player_pos)
        self.player.reparentTo(self.render)

    def init_ui(self):
        self.health_text = OnscreenText(text="HP: 100", pos=(-1.3, 0.9), scale=0.07, fg=(1,0,0,1), align=TextNode.ALeft)
        self.score_text = OnscreenText(text="Score: 0", pos=(1.1, 0.9), scale=0.07, fg=(1,1,0,1), align=TextNode.ARight)
        self.game_over_text = OnscreenText(text="", pos=(0, 0), scale=0.15, fg=(1, 0, 0, 1), mayChange=True)

    def accept_inputs(self):
        self.keys = {"w": False, "s": False, "a": False, "d": False}
        for key in self.keys:
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])
        self.accept("mouse1", self.fire_bullet)

    def set_key(self, key, value):
        self.keys[key] = value

    def fire_bullet(self):
        if self.health <= 0:
            return

        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            self.camLens.extrude(mpos, pFrom, pTo)
            pFrom = self.render.getRelativePoint(self.camera, pFrom)
            pTo = self.render.getRelativePoint(self.camera, pTo)

            direction = (pTo - pFrom).normalized()
            bullet = LineSegs()
            bullet.setThickness(2.0)
            bullet.setColor(1, 1, 0, 1)
            bullet.moveTo(0, 0, 0.5)
            bullet.drawTo(direction * 2 + Point3(0, 0, 0.5))
            node = bullet.create()
            np = self.render.attachNewNode(node)
            np.setPos(self.player_pos)

            self.bullets.append({
                "node": np,
                "pos": Point3(np.getPos()),
                "dir": direction
            })

    def spawn_zombie(self):
        if self.health <= 0:
            return

        angle = random.uniform(0, 360)
        dist = 30
        x = dist * random.choice([-1, 1]) * random.random()
        y = dist * random.choice([-1, 1]) * random.random()
        z = 0

        zombie = self.loader.loadModel("models/smiley")
        zombie.setScale(0.7)
        zombie.setPos(x, y, z)
        zombie.reparentTo(self.render)
        self.zombies.append(zombie)

        self.doMethodLater(2.0, lambda t: self.spawn_zombie(), "spawnZombie")

    def update(self, task):
        dt = globalClock.getDt()
        speed = 10 * dt

        move = LVector3(0, 0, 0)
        if self.keys["w"]: move.y += 1
        if self.keys["s"]: move.y -= 1
        if self.keys["a"]: move.x -= 1
        if self.keys["d"]: move.x += 1
        move.normalize()
        move *= speed
        self.player_pos += move
        self.player.setPos(self.player_pos)

        # 총알 이동
        for b in self.bullets:
            b["pos"] += b["dir"] * dt * 60
            b["node"].setPos(b["pos"])
        self.bullets = [b for b in self.bullets if b["pos"].length() < 100]

        # 좀비 이동 및 충돌
        for zombie in self.zombies[:]:
            zpos = zombie.getPos()
            direction = self.player_pos - zpos
            direction.setZ(0)
            direction.normalize()
            zombie.setPos(zpos + direction * dt * 3)

            if (zpos - self.player_pos).length() < 1.5:
                self.health -= 10
                zombie.removeNode()
                self.zombies.remove(zombie)
                self.health_text.setText(f"HP: {self.health}")
                if self.health <= 0:
                    self.game_over_text.setText("GAME OVER")
                    return Task.done

        # 총알과 좀비 충돌
        for bullet in self.bullets[:]:
            bpos = bullet["pos"]
            for zombie in self.zombies[:]:
                if (zombie.getPos() - bpos).length() < 1.0:
                    zombie.removeNode()
                    self.zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    bullet["node"].removeNode()
                    self.score += 1
                    self.score_text.setText(f"Score: {self.score}")
                    break

        return Task.cont

app = ZombieGame()
app.run()