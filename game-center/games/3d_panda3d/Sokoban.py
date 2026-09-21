from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, NodePath, Vec3

class Sokoban3D(ShowBase):
    def __init__(self):
        super().__init__()

        # 카메라 탑다운 세팅
        self.disableMouse()
        self.camera.setPos(3, -10, 10)
        self.camera.lookAt(3, 3, 0)

        self.level = [
            "WWWWWW",
            "W....W",
            "W.BGPW",
            "W....W",
            "WWWWWW",
        ]
        self.rows = len(self.level)
        self.cols = len(self.level[0])

        self.boxes = {}
        self.goals = []
        self.player = None

        self.load_map()

        self.accept("arrow_up", self.try_move, [0, 1])
        self.accept("arrow_down", self.try_move, [0, -1])
        self.accept("arrow_left", self.try_move, [-1, 0])
        self.accept("arrow_right", self.try_move, [1, 0])

    def make_tile(self, color=(1,1,1,1), scale=(1,1,1)):
        cm = CardMaker('card')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        tile = NodePath(cm.generate())
        tile.setColor(color)
        tile.setScale(*scale)
        tile.setTwoSided(True)
        tile.reparentTo(render)
        return tile

    def load_map(self):
        for r in range(self.rows):
            for c in range(self.cols):
                ch = self.level[r][c]
                x, y = c, self.rows - 1 - r

                # 바닥 타일 (회색 평면)
                floor = self.make_tile(color=(0.8, 0.8, 0.8, 1), scale=(0.9, 0.9, 1))
                floor.setPos(x, y, 0)

                if ch == 'W':
                    # 벽 타일 (진한 회색 큐브처럼 Paper이게 높이 줌)
                    wall = self.make_tile(color=(0.3, 0.3, 0.3, 1), scale=(0.9, 0.9, 0.9))
                    wall.setPos(x, y, 0.45)
                elif ch == 'B':
                    # 박스 타일 (주황색)
                    box = self.make_tile(color=(1, 0.5, 0, 1), scale=(0.8, 0.8, 0.8))
                    box.setPos(x, y, 0.4)
                    self.boxes[(x, y)] = box
                elif ch == 'G':
                    # 목표 타일 (초록색 평면, 낮게)
                    goal = self.make_tile(color=(0, 1, 0, 0.5), scale=(0.8, 0.8, 0.1))
                    goal.setPos(x, y, 0.05)
                    self.goals.append((x, y))
                elif ch == 'P':
                    # 플레이어 타일 (파란색)
                    player = self.make_tile(color=(0, 0, 1, 1), scale=(0.8, 0.8, 0.8))
                    player.setPos(x, y, 0.4)
                    self.player = player
                    self.player_pos = (x, y)

    def try_move(self, dx, dy):
        px, py = self.player_pos
        nx, ny = px + dx, py + dy

        # 경계 체크
        if nx < 0 or nx >= self.cols or ny < 0 or ny >= self.rows:
            return

        # 벽인지 검사
        map_r = self.rows - 1 - ny
        map_c = nx
        if self.level[map_r][map_c] == 'W':
            return

        # 박스 있는지 검사
        if (nx, ny) in self.boxes:
            bx, by = nx + dx, ny + dy
            # 박스 밀 위치 검사
            if bx < 0 or bx >= self.cols or by < 0 or by >= self.rows:
                return
            map_r2 = self.rows - 1 - by
            map_c2 = bx
            if self.level[map_r2][map_c2] == 'W' or (bx, by) in self.boxes:
                return
            # 박스 이동
            box = self.boxes.pop((nx, ny))
            box.setPos(bx, by, 0.4)
            self.boxes[(bx, by)] = box
            # 플레이어 이동
            self.player.setPos(nx, ny, 0.4)
            self.player_pos = (nx, ny)
        else:
            # 플레이어 그냥 이동
            self.player.setPos(nx, ny, 0.4)
            self.player_pos = (nx, ny)

        self.check_win()

    def check_win(self):
        for pos in self.boxes.keys():
            if pos not in self.goals:
                return
        print("Game Cleared! 🎉")

app = Sokoban3D()
app.run()