from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import random
import math

class TempleRunLikeGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.lanes = [-8, -4, 0, 4, 8]
        self.player_lane = 2
        self.player = self.loader.loadModel("models/smiley")
        self.player.setScale(0.1)
        self.player.setColor(0, 1, 0, 1)
        self.player.reparentTo(self.render)
        self.player.setPos(self.lanes[self.player_lane], 0, -10)

        self.cam.setPos(0, -50, 0)
        self.cam.lookAt(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(20, 30)
        self.cam.node().setLens(lens)

        self.accept("a", self.move_left)
        self.accept("d", self.move_right)
        self.accept("space", self.jump)  # 점프 키 추가

        self.obstacles = []
        self.spawn_interval = 1.0
        self.time_since_last_spawn = 0

        self.is_game_over = False

        self.elapsed_time = 0.0
        self.time_text = OnscreenText(text="Time: 0.0", pos=(-1.3, 0.9), scale=0.1, fg=(1,1,1,1))

        # 점프 관련 변수
        self.is_jumping = False
        self.jump_duration = 0.6  # 점프 지속시간 (초)
        self.jump_elapsed = 0.0
        self.jump_height = 3.0  # 최대 점프 높이

        self.taskMgr.add(self.update, "update")

    def move_left(self):
        if self.is_game_over:
            return
        if self.player_lane > 0:
            self.player_lane -= 1
            self.update_player_pos()

    def move_right(self):
        if self.is_game_over:
            return
        if self.player_lane < len(self.lanes) -1:
            self.player_lane += 1
            self.update_player_pos()

    def update_player_pos(self):
        # 점프 중에도 x 좌표만 바뀌도록 처리
        current_z = self.player.getZ()
        self.player.setPos(self.lanes[self.player_lane], 0, current_z)

    def jump(self):
        if self.is_game_over or self.is_jumping:
            return
        self.is_jumping = True
        self.jump_elapsed = 0.0

    def spawn_obstacle(self):
        lane = random.randint(0, 4)
        obstacle = self.loader.loadModel("models/box")
        obstacle.setScale(1, 0.5, 1)
        obstacle.setColor(1, 0, 0, 1)
        obstacle.reparentTo(self.render)
        obstacle.setPos(self.lanes[lane], 0, 15)
        self.obstacles.append({"node": obstacle, "lane": lane})

    def update(self, task):
        dt = globalClock.getDt()
        if self.is_game_over:
            return Task.cont

        # 점프 처리
        if self.is_jumping:
            self.jump_elapsed += dt
            # 포물선 점프 공식 (y= -4h * (t/T - 0.5)^2 + h)
            t = self.jump_elapsed / self.jump_duration
            if t > 1.0:
                t = 1.0
                self.is_jumping = False
                # 점프 끝나면 플레이어 z좌표는 레인 위치(z=-10)
                self.player.setZ(-10)
            else:
                height = -4 * self.jump_height * (t - 0.5) ** 2 + self.jump_height
                self.player.setZ(-10 + height)

        # 장애물 생성
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn > self.spawn_interval:
            self.spawn_obstacle()
            self.time_since_last_spawn = 0

        # 장애물 이동
        speed = 15
        remove_list = []
        for obs in self.obstacles:
            node = obs["node"]
            pos = node.getPos()
            pos.z -= speed * dt
            node.setPos(pos)

            # 충돌 체크 (장애물과 플레이어가 같은 레인 & z 근접 & 점프 중이 아닐 때만)
            if obs["lane"] == self.player_lane and not self.is_jumping:
                if abs(pos.z - self.player.getZ()) < 1.0:
                    self.game_over()

            # 화면 밖 제거
            if pos.z < -15:
                node.removeNode()
                remove_list.append(obs)

        for obs in remove_list:
            self.obstacles.remove(obs)

        # 경과 시간 업데이트
        self.elapsed_time += dt
        self.time_text.setText(f"Time: {self.elapsed_time:.2f}")

        return Task.cont

    def game_over(self):
        self.is_game_over = True
        self.time_text.setText(f"Game Over! Time: {self.elapsed_time:.2f}")
        print("Game Over!")

if __name__ == "__main__":
    game = TempleRunLikeGame()
    game.run()