import math
# !! DEBUGGING? DID YOU REMEMBER TO CALL RESET?
class Counter:
    def __init__(self, init_t):
        self.count = 0
        self.prev_t = init_t

    def update(self, curr_t):
        del_t = curr_t - self.prev_t
        self.count += del_t
        self.prev_t = curr_t

    def has_passed(self, n):
        return self.count >= math.ceil(n)

    def reset(self, new_init_t):
        self.count = 0
        self.prev_t = new_init_t
