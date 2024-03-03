from typing import Dict

from pynput import mouse

from service.click_tracker import ClickTracker
from service.move_tracker import MoveTracker


class Trackers(mouse.Listener):
    def __init__(
            self,
            click_trackers: Dict[mouse.Button, ClickTracker],
            move_tracker: MoveTracker,
    ):
        """
        Implemented by pynput.mouse
        The `mouse.Listener` will create a thread.
        """
        self.click_trackers = click_trackers
        self.move_tracker = move_tracker

    def reset(self):
        """Reset the mouse listener"""
        super(Trackers, self).__init__(
            on_move=self.move_tracker.track, on_click=self.on_click
        )

    def on_click(self, x, y, button, pressed):
        """Pick the right tracker and track"""
        if pressed:
            self.click_trackers[button].track(x, y)
