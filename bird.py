# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image
import game_framework
import random

# state event check
# ( state event type, event value )


# bird Run Speed
# fill here
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# bird Action Speed
# fill here
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Run:

    @staticmethod
    def enter(bird, e):
        bird.dir = -1 if bird.face_dir == 1 else 1
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x <= 25:
            bird.face_dir = 0
            bird.dir = 1
        elif bird.x >= 1600 - 25:
            bird.face_dir = 1
            bird.dir = -1


    @staticmethod
    def draw(bird):
        if bird.face_dir == 0:
            bird.image.clip_draw(int(bird.frame) * 183, 336, 180, 168, bird.x, bird.y, 100, 100)
        elif bird.face_dir == 1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, 336, 180, 168, 0, 'h', bird.x, bird.y, 100, 100)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {
            Run: {},
        }

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.bird, e)
                self.cur_state = next_state
                self.cur_state.enter(self.bird, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.bird)





class Bird:
    def __init__(self):
        self.x, self.y = random.randint(100, 1600), random.randint(300, 500)
        self.frame = 0
        self.face_dir = random.randint(0, 1)   # 0 오른쪽 , 1 왼쪽
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
