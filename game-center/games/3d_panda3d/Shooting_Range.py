from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Func
import random

class ShootingRangeGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # 마우스 커서(십자선) 생성
        self.crosshair = self.create_crosshair()
        self.crosshair.reparentTo(self.aspect2d)
        self.crosshair.setScale(0.03)
        self.crosshair.setPos(0, 0, 0)
        # 마우스 위치 따라 십자선 이동 태스크 등록
        self.taskMgr.add(self.update_crosshair_pos, "update_crosshair_pos")

        # 표적 위치: 좌중, 우중 (aspect2d x 기준 -0.7, 0.7)
        self.targets_pos = [(-0.7, 0, 0), (0.7, 0, 0)]

        self.target = self.loader.loadModel("models/box")
        self.target.setScale(0.1)
        self.target.setColor(1, 0, 0, 1)
        self.target.setTransparency(True)  # 투명도 조절 가능하게
        self.target.reparentTo(self.aspect2d)
        self.target.hide()

        self.target_visible = False

        # 점수
        self.score = 0
        self.score_text = OnscreenText(text="Score: 0", pos=(-1.3, 0.9), scale=0.07, fg=(1,1,1,1))

        # 총알 궤적 리스트
        self.bullet_traces = []

        # 마우스 클릭 이벤트
        self.accept("mouse1", self.shoot)

        # 표적 깜빡임 애니메이션으로 등장 시작
        self.show_target_animation()

        # 총알 궤적 업데이트 태스크
        self.taskMgr.add(self.update_bullets, "update_bullets")

    def create_crosshair(self):
        cm = CardMaker('cross')
        cm.setFrame(-0.02, 0.02, -0.002, 0.002)
        cross_x = self.aspect2d.attachNewNode(cm.generate())
        cross_x.setColor(1,1,1,1)

        cm2 = CardMaker('cross2')
        cm2.setFrame(-0.002, 0.002, -0.02, 0.02)
        cross_y = self.aspect2d.attachNewNode(cm2.generate())
        cross_y.setColor(1,1,1,1)

        cross = self.aspect2d.attachNewNode("crosshair")
        cross_x.reparentTo(cross)
        cross_y.reparentTo(cross)

        return cross

    def update_crosshair_pos(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()  # -1~1 범위
            self.crosshair.setPos(mpos.getX(), 0, mpos.getY())
        return Task.cont

    def show_target_animation(self):
        pos = random.choice(self.targets_pos)
        self.target.setPos(pos)
        self.target.show()
        self.target_visible = True

        fade_in = LerpColorScaleInterval(self.target, 0.5, (1,1,1,1), startColorScale=(1,1,1,0))
        blink1 = LerpColorScaleInterval(self.target, 0.25, (1,1,1,0.3), startColorScale=(1,1,1,1))
        blink2 = LerpColorScaleInterval(self.target, 0.25, (1,1,1,1), startColorScale=(1,1,1,0.3))
        blink = Sequence(blink1, blink2)
        blink_loop = Sequence(blink, blink, blink)
        fade_out = LerpColorScaleInterval(self.target, 0.5, (1,1,1,0), startColorScale=(1,1,1,1))
        hide = Func(self.target.hide)
        set_invisible = Func(self.set_target_invisible)

        seq = Sequence(fade_in, blink_loop, fade_out, hide, set_invisible, Func(self.schedule_next_target))
        seq.start()

    def set_target_invisible(self):
        self.target_visible = False

    def schedule_next_target(self):
        delay = random.uniform(1.0, 3.0)
        self.taskMgr.doMethodLater(delay, self.task_show_target, "show_target_task")

    def task_show_target(self, task):
        self.show_target_animation()
        return Task.done

    def shoot(self):
        if not self.mouseWatcherNode.hasMouse():
            return

        mpos = self.mouseWatcherNode.getMouse()  # 마우스 좌표 (-1~1 범위)

        # 십자선 위치 기준으로 총알 궤적 생성
        start_pos = (0, 0, 0)  # 화면 중앙 (aspect2d 기준)
        end_pos = (mpos.getX(), 0, mpos.getY())  # 마우스 위치

        # 표적 맞추면 점수 증가 및 표적 숨김 (기존 로직 유지)
        if self.target_visible:
            # 표적 위치 근처에 마우스가 있으면 맞춘 것으로 처리
            # 화면 좌표가 aspect2d 좌표라 근접 거리 체크 가능
            target_pos = self.target.getPos()
            dist = ((target_pos.getX() - end_pos[0])**2 + (target_pos.getZ() - end_pos[2])**2)**0.5
            if dist < 0.15:  # 적당한 반경 내에서 맞은 걸로 인정
                self.score += 1
                self.score_text.setText(f"Score: {self.score}")
                self.target.hide()
                self.target_visible = False

        # 궤적 생성
        line_segs = LineSegs()
        line_segs.setThickness(2.0)
        line_segs.setColor(1, 1, 0, 1)
        line_segs.moveTo(*start_pos)
        line_segs.drawTo(*end_pos)

        node = line_segs.create()
        np = self.aspect2d.attachNewNode(node)
        self.bullet_traces.append({"node": np, "timer": 0.2})

    def create_bullet_trace(self):
        if self.target_visible:
            target_pos = self.target.getPos()
        else:
            target_pos = (0, 0, 0.2)

        line_segs = LineSegs()
        line_segs.setThickness(2.0)
        line_segs.setColor(1, 1, 0, 1)
        line_segs.moveTo(0, 0, 0)
        line_segs.drawTo(target_pos)

        node = line_segs.create()
        np = self.aspect2d.attachNewNode(node)
        return np

    def update_bullets(self, task):
        dt = globalClock.getDt()
        remove_list = []
        for bt in self.bullet_traces:
            bt["timer"] -= dt
            if bt["timer"] <= 0:
                bt["node"].removeNode()
                remove_list.append(bt)
        for bt in remove_list:
            self.bullet_traces.remove(bt)
        return Task.cont

if __name__ == "__main__":
    game = ShootingRangeGame()
    game.run()