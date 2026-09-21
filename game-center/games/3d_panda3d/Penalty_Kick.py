from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, Point3
from direct.task import Task
import random

class PenaltyKickGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.disableMouse()
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(0, 10, 0)
        
        # 게임 변수
        self.score = 0
        self.kick_count = 0
        self.max_kicks = 5
        self.goal_positions = {
            "left": Point3(-2, 10, 0),
            "center": Point3(0, 10, 0),
            "right": Point3(2, 10, 0)
        }
        self.kicker_choice = None
        self.goalkeeper_choice = None
        self.is_game_over = False
        
        # 골대 만들기 (세 기둥)
        self.create_goal()
        
        # 골키퍼 (smiley 모델)
        self.goalkeeper = loader.loadModel("models/smiley")
        self.goalkeeper.setScale(0.5)
        self.goalkeeper.setPos(0, 9.5, 0.5)
        self.goalkeeper.reparentTo(render)
        
        # 공 (smiley 모델 사용)
        self.ball = loader.loadModel("models/smiley")
        self.ball.setScale(0.3)
        self.ball.setPos(0, 0, 0.3)
        self.ball.reparentTo(render)
        
        # 점수 텍스트
        self.score_text = OnscreenText(text="Goal: 0 / 5", pos=(-1.3, 0.9), scale=0.07, fg=(1,1,1,1), align=TextNode.ALeft)
        
        # 상태 텍스트
        self.status_text = OnscreenText(text="Drag Left/Center/Right to Kick", pos=(0, 0.85), scale=0.06)
        
        # 마우스 드래그 시작 위치 저장
        self.drag_start_x = None
        
        # 이벤트 등록
        self.accept("mouse1", self.on_mouse1_down)
        self.accept("mouse1-up", self.on_mouse1_up)
        
        # 애니메이션 상태 변수
        self.ball_moving_forward = False
        self.ball_moving_back = False
        self.ball_move_speed = 10.0
    
    def create_goal(self):
        # 좌측 기둥
        pillar_left = loader.loadModel("models/box")
        pillar_left.setScale(0.2, 0.1, 1)
        pillar_left.setPos(-2.2, 10, 0.5)
        pillar_left.setColor(1, 1, 1, 1)
        pillar_left.reparentTo(render)
        
        # 우측 기둥
        pillar_right = loader.loadModel("models/box")
        pillar_right.setScale(0.2, 0.1, 1)
        pillar_right.setPos(2.2, 10, 0.5)
        pillar_right.setColor(1, 1, 1, 1)
        pillar_right.reparentTo(render)
        
        # 상단 가로대
        crossbar = loader.loadModel("models/box")
        crossbar.setScale(2.5, 0.1, 0.1)
        crossbar.setPos(0, 10, 1)
        crossbar.setColor(1, 1, 1, 1)
        crossbar.reparentTo(render)
    
    def on_mouse1_down(self):
        if self.is_game_over:
            return
        if self.mouseWatcherNode.hasMouse():
            self.drag_start_x = self.mouseWatcherNode.getMouseX()
        
    def on_mouse1_up(self):
        if self.is_game_over:
            return
        if self.drag_start_x is None or not self.mouseWatcherNode.hasMouse():
            return
        drag_end_x = self.mouseWatcherNode.getMouseX()
        diff = drag_end_x - self.drag_start_x
        
        if diff < -0.1:
            self.kicker_choice = "left"
        elif diff > 0.1:
            self.kicker_choice = "right"
        else:
            self.kicker_choice = "center"
        
        self.drag_start_x = None
        
        self.kick()
    
    def kick(self):
        if self.kick_count >= self.max_kicks or self.ball_moving_forward or self.ball_moving_back:
            return
        
        self.goalkeeper_choice = random.choice(["left", "center", "right"])
        
        # 골키퍼 위치 이동
        pos = self.goal_positions[self.goalkeeper_choice]
        self.goalkeeper.setPos(pos.getX(), pos.getY()-0.5, 0.5)
        
        # 공 위치 초기화
        self.ball.setPos(0, 0, 0.3)
        
        # 공 목표 위치 설정
        self.ball_target_pos = self.goal_positions[self.kicker_choice] + Point3(0, 0, 0.3)
        
        # 애니메이션 상태 설정
        self.ball_moving_forward = True
        self.ball_moving_back = False
        
        self.kick_count += 1
        
        # 애니메이션 시작
        taskMgr.add(self.ball_move_task, "ball_move_task")
    
    def ball_move_task(self, task):
        dt = globalClock.getDt()
        current_pos = self.ball.getPos()
        
        if self.ball_moving_forward:
            direction = self.ball_target_pos - current_pos
            distance = direction.length()
            
            if distance < 0.1:
                self.ball.setPos(self.ball_target_pos)
                self.ball_moving_forward = False
                self.ball_moving_back = True
                
                # 결과 판단
                if self.kicker_choice == self.goalkeeper_choice:
                    result = "Miss! Keeper blocked it."
                else:
                    result = "Goal! Success."
                    self.score += 1
                
                self.score_text.setText(f"Goal: {self.score} / {self.kick_count}")
                self.status_text.setText(f"You: {self.kicker_choice} Keeper: {self.goalkeeper_choice} - {result}")
                
                if self.score >= 3:
                    self.status_text.setText(f"Congratulations! Won with 3+ goals on kick {self.kick_count}!")
                    self.is_game_over = True
                elif self.kick_count >= self.max_kicks:
                    self.status_text.setText(f"Game Over! {self.score} goals out of {self.kick_count} kicks.")
                    self.is_game_over = True
                
                return Task.cont
            
            direction.normalize()
            self.ball.setPos(current_pos + direction * self.ball_move_speed * dt)
        
        elif self.ball_moving_back:
            home_pos = Point3(0, 0, 0.3)
            direction = home_pos - current_pos
            distance = direction.length()
            
            if distance < 0.1:
                self.ball.setPos(home_pos)
                self.ball_moving_back = False
                return Task.done
            
            direction.normalize()
            self.ball.setPos(current_pos + direction * self.ball_move_speed * dt)
        
        return Task.cont

game = PenaltyKickGame()
game.run()