import keyboard as keyb
import threading
import os

data_file_path = "./clicker_data.txt"
start_data = '''0\n1\n1\n0\n'''


class Clicker:

    def my_multiplier_cost(self):
        return (self.my_click_multiplier + 1) ** 2

    def auto_multiplier_cost(self):
        return (self.auto_click_multiplier + 1) ** 3

    def auto_cnt_cost(self):
        return (self.auto_click_cnt + 2) ** 3

    def increment_my_multiplier(self):
        cost = self.my_multiplier_cost()
        if cost <= self.counter:
            self.counter -= cost
            self.my_click_multiplier += 1
            self.draw(-cost)

    def increment_auto_multiplier(self):
        cost = self.auto_multiplier_cost()
        if cost <= self.counter:
            self.counter -= cost
            self.auto_click_multiplier += 1
            self.draw(-cost)

    def increment_auto_cnt(self):
        cost = self.auto_cnt_cost()
        if cost <= self.counter:
            self.counter -= cost
            self.auto_click_cnt += 1
            self.draw(-cost)

    def draw(self, cnt):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" if cnt >= 0 else "-", abs(cnt))
        print("total clicks: ", self.counter)
        print("current clicks per second: ", self.auto_click_multiplier * self.auto_click_cnt)
        print("my_click_multiplier: ", self.my_click_multiplier)
        print("auto_click_multiplier: ", self.auto_click_multiplier)
        print("auto_click_cnt: ", self.auto_click_cnt)
        print("increase my_click_multiplier by 1 pressing \"shift + m\" for ", self.my_multiplier_cost(), " clicks")
        print("increase auto_click_multiplier by 1 pressing \"shift + a\" for ", self.auto_multiplier_cost(), " clicks")
        print("increase auto_click_cnt by 1 pressing \"shift + c\" for ", self.auto_cnt_cost(), " clicks")

    def click(self, is_my_click):
        cnt = self.my_click_multiplier if is_my_click else self.auto_click_multiplier * self.auto_click_cnt
        self.counter += cnt
        self.draw(cnt)

    def finish(self):
        self.finished = 1

    def __init__(self):
        print("init\n")
        if not os.path.exists(data_file_path):
            with open(data_file_path, 'w') as f:
                f.write(start_data)
        with open(data_file_path, 'r') as f:
            lines = f.readlines()
            self.counter = int(lines[0])
            self.my_click_multiplier = int(lines[1])
            self.auto_click_multiplier = int(lines[2])
            self.auto_click_cnt = int(lines[3])
            self.finished = 0

        keyb.add_hotkey("space", Clicker.click, [self, True], True, 1, True)
        keyb.add_hotkey("esc", Clicker.finish, [self], True, 1, True)
        keyb.add_hotkey("shift + m", Clicker.increment_my_multiplier, [self], True, 1, True)
        keyb.add_hotkey("shift + a", Clicker.increment_auto_multiplier, [self], True, 1, True)
        keyb.add_hotkey("shift + c", Clicker.increment_auto_cnt, [self], True, 1, True)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.draw(0)
        print("finished")
        with open(data_file_path, 'w') as f:
            f.write(str(self.counter) + '\n')
            f.write(str(self.my_click_multiplier) + '\n')
            f.write(str(self.auto_click_multiplier) + '\n')
            f.write(str(self.auto_click_cnt) + '\n')


with Clicker() as clicker:
    while not clicker.finished:
        threading.Event().wait(1)
        clicker.click(False)
