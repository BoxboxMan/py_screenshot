import argparse
import os
import time

import cv2
import yaml
import dxcam
from pynput.keyboard import Listener as KeyboardListener, Key


class Monitor:
    def __init__(self, config_path='./config.yaml'):
        config = yaml.load(open(config_path, 'r', encoding='UTF-8'), Loader=yaml.FullLoader)
        self.args = argparse.Namespace(**config)
        self.monitor = dxcam.create(output_color="BGR")

        KeyboardListener(on_press=self.on_press).start()

    def grab(self):
        return self.monitor.grab()

    def write(self, frame):
        cv2.imwrite(os.path.join(self.args.img_save_path, f'{time.time().__str__()}.img'), frame)
        print("save img success")

    def screenshot(self):
        frame = self.grab()
        self.write(frame)

    def start(self):
        while True:
            if self.args.auoto_screenshot > 0:
                self.lscreen_buttonoop_task()
            time.sleep(self.args.grab_timer)

    def on_press(self, key):
        if key == getattr(Key, self.args.screen_button):
            self.screenshot()


if __name__ == '__main__':
    monitor = Monitor()
    monitor.start()
