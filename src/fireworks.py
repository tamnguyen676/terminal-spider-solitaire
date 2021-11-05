from asciimatics.effects import Stars, Print
from asciimatics.particles import RingFirework, SerpentFirework, StarFirework, \
    PalmFirework
from asciimatics.renderers import SpeechBubble, FigletText, Rainbow, Box
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from random import randint, choice


def demo(screen, score):
    scenes = []
    effects = [
        Stars(screen, screen.width),
        Print(screen,
              SpeechBubble("Press Q to Return"),
              y=screen.height - 3,
              start_frame=100),
        Print(screen,
              SpeechBubble(f"Score: {score}"),
              y=screen.height // 2,
              start_frame=50)
    ]
    for _ in range(50):
        fireworks = [
            (PalmFirework, 25, 30),
            (PalmFirework, 25, 30),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (RingFirework, 20, 30),
            (SerpentFirework, 30, 35),
        ]
        firework, start, stop = choice(fireworks)
        effects.insert(
            1,
            firework(screen,
                     randint(0, screen.width),
                     randint(screen.height // 8, screen.height * 3 // 4),
                     randint(start, stop),
                     start_frame=randint(0, 250)))

    effects.append(Print(screen,
                         Rainbow(screen, FigletText("YOU WIN!")),
                         screen.height // 2 - 6,
                         speed=1,
                         start_frame=50))

    scenes.append(Scene(effects, -1))

    screen.play(scenes, stop_on_resize=True)


def start_fireworks(score):
    try:
        Screen.wrapper(demo, arguments=(score,))
        return
    except ResizeScreenError:
        pass
