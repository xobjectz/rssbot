# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"repeater"


from .thread import launch
from .timer  import Timer


class Repeater(Timer):

    "Repeat a timer every x seconds."

    def run(self):
        launch(self.start)
        super().run()
