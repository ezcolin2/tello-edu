class PIDParams():

    def __init__(self, pid_value_lr, pid_value_ud, pid_value_fb):
        self.pid_value_lr = pid_value_lr # P, I, D 값
        self.pid_value_ud = pid_value_ud # P, I, D 값
        self.pid_value_fb = pid_value_fb # P, I, D 값
