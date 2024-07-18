# This file is placed in the Public Domain.


"at repeating intervals"


from .launch import launch
from .timer  import Timer


class Repeater(Timer):

    "Repeater"

    def run(self):
        launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
    )
