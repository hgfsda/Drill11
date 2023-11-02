# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp
import game_framework

# state event check
# ( state event type, event value )


# Boy Run Speed
# fill here
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# Boy Action Speed
# fill here
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Run:

    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600-25)


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Run
        self.transitions = {
            Run: {},
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





class Bird:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
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
