# This file is placed in the Public Domain.


"repeater"


from .timer  import Timer
from .thread import launch


class Repeater(Timer):

    "Repeater"

    def run(self):
        launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
    )
