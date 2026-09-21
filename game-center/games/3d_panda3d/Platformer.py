from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import random

BLOCK_SPACING = 4
BLOCK_WIDTH = 2
PLAYER_JUMP_VEL = 18
GRAVITY = -30
AUTO_MOVE_SPEED = 7
MOVE_SPEED = 10  # WASD 좌우 이동 속도

class PlatformerGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(0, -20, 8)
        self.camera.lookAt(0, 0, 0)
        
        self.platforms = []
        self.last_block_x = 0
        self.elapsed_time = 0.0
        
        self.init_blocks()
        self.init_player()
        self.init_ui()
        
        # 키 상태 저장용 변수
        self.key_map = {"left": False, "right": False, "jump": False}
        
        # 키 이벤트 등록
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("space", self.set_key, ["jump", True])
        self.accept("space-up", self.set_key, ["jump", False])

        taskMgr.add(self.update, "update")

    def set_key(self, key, value):
        self.key_map[key] = value

    def init_player(self):
        self.player = loader.loadModel("models/box")
        self.player.setScale(1, 1, 1)
        if self.platforms:
            start_block = self.platforms[0]
            self.player.setPos(start_block.getX(), 0, start_block.getZ() + 1)
        else:
            self.player.setPos(0, 0, 5)
        self.player.reparentTo(render)

        self.player_vel = Vec3(0, 0, 0)
        self.on_ground = False

    def init_blocks(self):
        for i in range(10):
            self.create_block(i * BLOCK_SPACING)

    def create_block(self, x):
        if random.random() < 0.3:
            return
        block = loader.loadModel("models/box")
        block.setScale(BLOCK_WIDTH, 1, 1)
        block.setPos(x, 0, 0)
        block.setColor(random.random(), random.random(), random.random(), 1)
        block.reparentTo(render)
        self.platforms.append(block)
        self.last_block_x = x

    def init_ui(self):
        self.time_text = OnscreenText(text="Time: 0.0", pos=(-1.3, 0.9), scale=0.07, fg=(1,1,1,1), align=TextNode.ALeft)

    def update(self, task):
        dt = globalClock.getDt()
        self.elapsed_time += dt
        self.time_text.setText(f"Time: {self.elapsed_time:.1f}")

        # 자동 오른쪽 이동
        self.player.setX(self.player.getX() + AUTO_MOVE_SPEED * dt)

        # WASD 좌우 이동 (공중에서도 가능)
        move_x = 0
        if self.key_map["left"]:
            move_x -= MOVE_SPEED * dt
        if self.key_map["right"]:
            move_x += MOVE_SPEED * dt
        self.player.setX(self.player.getX() + move_x)

        # 점프 처리 (땅에 있을 때만 가능)
        if self.key_map["jump"] and self.on_ground:
            self.player_vel.z = PLAYER_JUMP_VEL
            self.on_ground = False

        # 중력 적용
        self.player_vel.z += GRAVITY * dt
        self.player.setZ(self.player.getZ() + self.player_vel.z * dt)

        # 바닥 충돌 체크
        self.on_ground = False
        player_x = self.player.getX()
        player_z = self.player.getZ()
        for block in self.platforms:
            block_x = block.getX()
            block_z = block.getZ()
            if (player_x + 0.5 > block_x - BLOCK_WIDTH/2 and player_x - 0.5 < block_x + BLOCK_WIDTH/2):
                if (player_z <= block_z + 1) and (player_z >= block_z):
                    if self.player_vel.z <= 0:
                        self.player.setZ(block_z + 1)
                        self.player_vel.z = 0
                        self.on_ground = True
                        break

        # 카메라를 플레이어 위치에 맞게 좌우 이동 (Y축, Z축 고정)
        self.camera.setX(self.player.getX())
        self.camera.setZ(8)

        # 새로운 블록 생성
        if self.last_block_x < self.player.getX() + 40:
            self.create_block(self.last_block_x + BLOCK_SPACING)

        # 지나간 플랫폼 제거
        for block in self.platforms:
            if block.getX() < self.player.getX() - 20:
                block.removeNode()
        self.platforms = [b for b in self.platforms if b.getX() >= self.player.getX() - 20]

        # 낙사 체크 - 화면 아래(-10)로 떨어지면 게임오버 처리
        if self.player.getZ() < -10:
            print("Game Over!")
            if self.platforms:
                self.player.setPos(self.platforms[0].getX(), 0, self.platforms[0].getZ() + 1)
            else:
                self.player.setPos(0, 0, 5)
            self.player_vel = Vec3(0, 0, 0)
            self.elapsed_time = 0.0

        return Task.cont

game = PlatformerGame()
game.run()