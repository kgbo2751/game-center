from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
import random
import sys
from math import sqrt

class LaserAvoidGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()  # 기본 마우스 카메라 조작 비활성화

        # 윈도우 사이즈
        self.win_width = self.win.getProperties().getXSize()
        self.win_height = self.win.getProperties().getYSize()

        # 플레이어 세팅 (작은 노드 + 하얀 원)
        self.player = self.loader.loadModel("models/smiley")
        self.player.setScale(0.05)
        self.player.setColor(0, 1, 0, 1)
        self.player.reparentTo(self.render)
        self.player.setPos(0, 0, 0)

        # 카메라 세팅 - 2D 평면 게임이므로 Z축 고정, orthographic 카메라 사용
        self.cam.setPos(0, -50, 0)
        self.cam.lookAt(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(20, 15)  # 화면 가로 20, 세로 15 유닛
        self.cam.node().setLens(lens)

        # 키 입력 초기화
        self.keyMap = {"w": False, "a": False, "s": False, "d": False}
        for key in self.keyMap.keys():
            self.accept(key, self.updateKeyMap, [key, True])
            self.accept(key + "-up", self.updateKeyMap, [key, False])

        # 레이저 리스트
        self.lasers = []

        # 레이저 생성 주기
        self.laser_spawn_interval = 1.0  # 초
        self.time_since_last_laser = 0

        # 게임 상태
        self.is_game_over = False

        # 경과 시간 표시
        self.elapsed_time = 0.0
        self.time_text = OnscreenText(text="Time: 0.0", pos=(-1.3, 0.9), scale=0.07, fg=(1,1,1,1))

        # 메인 업데이트 태스크 등록
        self.taskMgr.add(self.update, "update")

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def spawn_laser(self):
        # 레이저 길이는 3~7 유닛 랜덤
        length = random.uniform(3, 7)

        # 레이저가 시작할 위치 (화면 경계에서 랜덤)
        # 화면 좌표는 orthographic 렌즈 기준 -10 ~ 10 (가로), -7.5 ~ 7.5 (세로)
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            start_pos = Vec3(random.uniform(-10, 10), 0, 7.5)
        elif side == "bottom":
            start_pos = Vec3(random.uniform(-10, 10), 0, -7.5)
        elif side == "left":
            start_pos = Vec3(-10, 0, random.uniform(-7.5, 7.5))
        else:  # right
            start_pos = Vec3(10, 0, random.uniform(-7.5, 7.5))

        # 목표 위치는 중앙 (0,0,0)
        target_pos = Vec3(0, 0, 0)

        # 방향 벡터 및 정규화
        direction = (target_pos - start_pos).normalized()

        # 레이저 생성: 직선 모델 대신 직사각형 단순 표시
        laser = self.loader.loadModel("models/box")
        laser.setScale(0.1, length, 0.05)  # 두께 0.1, 길이 length, 깊이 0.05
        laser.setColor(1, 0, 0, 1)
        laser.reparentTo(self.render)

        # 레이저는 방향 벡터를 따라 y축 기준으로 길이만큼 놓임
        # box 모델 기본 y축 방향이 앞으로 향함
        laser.setPos(start_pos)
        laser.lookAt(target_pos)

        # 레이저 속도: 7 유닛/초 (중앙으로 빠르게 접근)
        speed = 7

        self.lasers.append({
            "node": laser,
            "direction": direction,
            "speed": speed,
            "length": length,
        })

    def update(self, task):
        dt = globalClock.getDt()

        if self.is_game_over:
            return Task.cont

        # 플레이어 움직임 처리 (WASD)
        speed = 10  # 유닛/초
        pos = self.player.getPos()
        if self.keyMap["w"]:
            pos.z += speed * dt
        if self.keyMap["s"]:
            pos.z -= speed * dt
        if self.keyMap["a"]:
            pos.x -= speed * dt
        if self.keyMap["d"]:
            pos.x += speed * dt

        # 플레이어가 화면 범위 내에 있도록 제한
        pos.x = max(-9, min(9, pos.x))
        pos.z = max(-6.5, min(6.5, pos.z))
        self.player.setPos(pos)

        # 레이저 생성 타이머
        self.time_since_last_laser += dt
        if self.time_since_last_laser > self.laser_spawn_interval:
            self.spawn_laser()
            self.time_since_last_laser = 0

        # 레이저 위치 업데이트
        remove_lasers = []
        for laser in self.lasers:
            node = laser["node"]
            direction = laser["direction"]
            speed = laser["speed"]

            # 이동: direction 방향으로 speed*dt만큼
            new_pos = node.getPos() + direction * speed * dt
            node.setPos(new_pos)

            # 충돌 체크: 플레이어 and 거리 (플레이어 반경 0.05, 레이저 반경 0.05)
            # 레이저는 길이 방향으로 쭉 뻗어있지만 여기서는 중심점으로 간단 체크
            dist = (new_pos - pos).length()
            if dist < 0.5:
                self.game_over()

            # 화면 밖으로 나가면 제거 (중앙 향해 오기 때문에 중심 지나면 제거)
            if new_pos.length() < 0.5:
                node.removeNode()
                remove_lasers.append(laser)

        # 리스트에서 제거
        for laser in remove_lasers:
            self.lasers.remove(laser)

        # 경과 시간 업데이트
        self.elapsed_time += dt
        self.time_text.setText(f"Time: {self.elapsed_time:.2f}")

        return Task.cont

    def game_over(self):
        self.is_game_over = True
        self.time_text.setText(f"Game Over! Time: {self.elapsed_time:.2f}")
        print("Game Over!")

if __name__ == "__main__":
    game = LaserAvoidGame()
    game.run()