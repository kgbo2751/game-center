from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, CardMaker, LineSegs
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

class RacingGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.create_track()

        # 플레이어 차량
        self.player = self.create_car(color=(0, 0, 1, 1))
        self.player.setPos(-8, -9, 0.5)
        self.player_speed = 0
        self.player_direction = 0  # 0: 오른쪽, 1: 위, 2: 왼쪽, 3: 아래
        self.player_laps = 0
        self.player_last_on_line = False

        # AI 차량들
        self.ais = []
        ai_start_positions = [(-8, -8.5), (-9, -8), (-7, -8.5)]
        for pos in ai_start_positions:
            ai_car = self.create_car(color=(1, 0, 0, 1))
            ai_car.setPos(pos[0], pos[1], 0.5)
            self.ais.append({
                "node": ai_car,
                "direction": 0,
                "laps": 0,
                "speed": 10,
                "last_on_line": False,
            })

        self.laps_to_finish = 2
        self.finished = False

        # 키 입력 맵
        self.key_map = {"w": False, "a": False, "s": False, "d": False}
        for key in self.key_map.keys():
            self.accept(key, self.set_key, [key, True])
            self.accept(f"{key}-up", self.set_key, [key, False])

        # 카메라: 위에서 아래로 내려다Paper는 탑뷰
        self.camera.setPos(0, 0, 40)
        self.camera.setHpr(0, -90, 0)

        self.winner_text = OnscreenText(text="", pos=(0, 0.8), scale=0.07, fg=(1,1,0,1))

        self.taskMgr.add(self.update, "update")

    def create_track(self):
        # 바닥 생성 (20x20 크기)
        cm = CardMaker('floor')
        cm.setFrame(-10, 10, -10, 10)
        floor = render.attachNewNode(cm.generate())
        floor.setPos(0, 0, 0)
        floor.setColor(0.4, 0.4, 0.4, 1)

        # 벽 생성 (box 모델 필요, 없으면 cube.egg 등 대체 필요)
        wall_thickness = 0.5
        wall_height = 2
        wall_color = (1, 1, 1, 0.7)

        wall_left = loader.loadModel("models/box")
        wall_left.setScale(wall_thickness, 20, wall_height)
        wall_left.setPos(-10, 0, wall_height / 2)
        wall_left.setColor(*wall_color)
        wall_left.reparentTo(render)

        wall_right = loader.loadModel("models/box")
        wall_right.setScale(wall_thickness, 20, wall_height)
        wall_right.setPos(10, 0, wall_height / 2)
        wall_right.setColor(*wall_color)
        wall_right.reparentTo(render)

        wall_front = loader.loadModel("models/box")
        wall_front.setScale(20, wall_thickness, wall_height)
        wall_front.setPos(0, 10, wall_height / 2)
        wall_front.setColor(*wall_color)
        wall_front.reparentTo(render)

        wall_back = loader.loadModel("models/box")
        wall_back.setScale(20, wall_thickness, wall_height)
        wall_back.setPos(0, -10, wall_height / 2)
        wall_back.setColor(*wall_color)
        wall_back.reparentTo(render)

        # 스타팅/피니시 라인 (랩 완료 지점) - y=-9에 세로선 (x = -1 ~ 1)
        ls = LineSegs()
        ls.setColor(1, 1, 1, 1)  # 흰색
        ls.setThickness(4.0)
        ls.moveTo(-1, -9, 0.51)
        ls.drawTo(1, -9, 0.51)
        start_line = render.attachNewNode(ls.create())

    def create_car(self, color=(1,0,0,1)):
        car = loader.loadModel("models/box")
        car.setScale(1, 2, 0.5)
        car.setColor(*color)
        car.reparentTo(render)
        car.setZ(0.5)
        return car

    def set_key(self, key, value):
        self.key_map[key] = value

    def update_car_pos(self, car_data, dt):
        speed = car_data["speed"]
        pos = car_data["node"].getPos()
        direction = car_data["direction"]

        dist = speed * dt
        x, y = pos.getX(), pos.getY()

        if direction == 0:  # 오른쪽
            x += dist
            if x >= 9:
                x = 9
                direction = 1
        elif direction == 1:  # 위
            y += dist
            if y >= 9:
                y = 9
                direction = 2
        elif direction == 2:  # 왼쪽
            x -= dist
            if x <= -9:
                x = -9
                direction = 3
        elif direction == 3:  # 아래
            y -= dist
            if y <= -9:
                y = -9
                direction = 0
                # 랩 완료는 여기서 처리하지 않고 별도로 update에서 처리

        car_data["node"].setPos(x, y, 0.5)
        car_data["direction"] = direction

        heading = {0: 90, 1: 0, 2: 270, 3: 180}[direction]
        car_data["node"].setH(heading)

    def update(self, task):
        dt = globalClock.getDt()
        if self.finished:
            return Task.cont

        # 플레이어 속도 조절
        if self.key_map["w"]:
            self.player_speed += 20 * dt
        elif self.key_map["s"]:
            self.player_speed -= 20 * dt
        else:
            self.player_speed *= 0.9
        self.player_speed = max(0, min(self.player_speed, 30))

        player_data = {
            "node": self.player,
            "direction": self.player_direction,
            "laps": self.player_laps,
            "speed": self.player_speed,
            "last_on_line": self.player_last_on_line,
        }
        self.update_car_pos(player_data, dt)

        # 스타팅 라인 통과 체크 (y <= -9 근처, x가 -1~1 안에 있으면 통과로 간주)
        on_line = (-9.2 <= player_data["node"].getY() <= -8.8) and (-1 <= player_data["node"].getX() <= 1)
        if on_line and not player_data["last_on_line"]:
            player_data["laps"] += 1
        player_data["last_on_line"] = on_line

        self.player_direction = player_data["direction"]
        self.player_laps = player_data["laps"]
        self.player_last_on_line = player_data["last_on_line"]

        # AI 업데이트
        for ai in self.ais:
            self.update_car_pos(ai, dt)
            on_line_ai = (-9.2 <= ai["node"].getY() <= -8.8) and (-1 <= ai["node"].getX() <= 1)
            if on_line_ai and not ai["last_on_line"]:
                ai["laps"] += 1
            ai["last_on_line"] = on_line_ai

        # 우승자 체크
        if self.player_laps >= self.laps_to_finish:
            self.finish("Player")
        else:
            for i, ai in enumerate(self.ais):
                if ai["laps"] >= self.laps_to_finish:
                    self.finish(f"AI Player {i+1}")
                    break

        return Task.cont

    def finish(self, winner):
        self.finished = True
        self.winner_text.setText(f"🏆 Winner: {winner} 🏆")
        print(f"Game Over! Winner: {winner}")

app = RacingGame()
app.run()