from typing import Callable

from manim import *
from colour import Color
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.scene.scene import Scene
from manim.utils.rate_functions import smooth
from pyglet.resource import animation

"""
16 VIRDIS
"""
VIR_1:       str = "#fde725"
VIR_2:       str = "#d2e21b"
VIR_3:       str = "#a5db36"
VIR_4:       str = "#7ad151"
VIR_5:       str = "#54c568"
VIR_6:       str = "#35b779"
VIR_7:       str = "#22a884"
VIR_8:       str = "#1f988b"
VIR_9:       str = "#23888e"
VIR_10:      str = "#2a788e"
VIR_11:      str = "#31688e"
VIR_12:      str = "#39568c"
VIR_13:      str = "#414487"
VIR_14:      str = "#472f7d"
VIR_15:      str = "#481a6c"
VIR_16:      str = "#440154"

virdis_colors = [VIR_1,
                 VIR_2,
                 VIR_3,
                 VIR_4,
                 VIR_5,
                 VIR_6,
                 VIR_7,
                 VIR_8,
                 VIR_9,
                 VIR_10,
                 VIR_11,
                 VIR_12,
                 VIR_13,
                 VIR_14,
                 VIR_15,
                 VIR_16]

class InfiniteSquares():
    def __init__(self, level):
        h = 4
        w = 2

        x_offset = -w/2
        x_mult = 1
        y_offset = h/4
        y_mult = 1

        self.text = []
        self.rectangles = []
        for i in range(level):
            if i == 0:
                pass
            elif i % 2 == 1:
                h = h / 2
                y_offset = y_offset - 1 * y_mult
                x_offset = x_offset + 2 * x_mult
            else:
                w = w / 2
                y_offset = y_offset + 2 * y_mult
                x_offset = x_offset - 1 / 2 * x_mult
                x_mult = x_mult / 2
                y_mult = y_mult / 2

            self.rectangles.append(Rectangle(height=h, width=w,
                                             fill_opacity=1,
                                             fill_color=virdis_colors[i])
                                   .move_to(RIGHT*x_offset + UP*y_offset))
            self.text.append(Tex(rf'$\frac{{{1}}}{{{2**(i+1)}}}$', color=BLACK, font_size=128/1.5**i)
                             .move_to(RIGHT*x_offset + UP*y_offset))


class InfiniteSummation():
    def __init__(self, level):
        self.text = []
        for i in range(level):
            if i == 0:
                self.text.append(Tex(rf'$\frac{{{1}}}{{{2 ** (i + 1)}}}$', color=virdis_colors[i], font_size=64))
            elif i > 0:
                self.text.append(Tex(rf'+$\frac{{{1}}}{{{2 ** (i + 1)}}}$', color=virdis_colors[i], font_size=64))
                self.text[i].next_to(self.text[i-1], RIGHT/2)

        self.text.append(Tex(rf'+...', color=WHITE, font_size=64))
        self.text[level].next_to(self.text[level-1], RIGHT/2)


class Squares(Scene):
    def construct(self):
        r = InfiniteSquares(16)
        e = InfiniteSummation(8)

        self.wait(1)
        i = 0
        for square, text in zip(r.rectangles, r.text):
            rtime = 1/(i/4+1)
            if i > len(e.text)-1:
                self.play(FadeIn(square.shift(0*LEFT+0.5*UP), run_time=rtime),
                          FadeIn(text.shift(0*LEFT+0.5*UP), run_time=rtime))
            else:
                self.play(FadeIn(square.shift(0*LEFT+0.5*UP), run_time=rtime),
                          FadeIn(text.shift(0*LEFT+0.5*UP), run_time=rtime),
                          FadeIn(e.text[i].shift(4.5*LEFT+2*DOWN), run_time=rtime))
            self.wait(rtime)
            i = i + 1
        self.wait(2)
        s = Tex(rf'=1', color=WHITE, font_size=64).next_to(e.text[-1], RIGHT/2)

        self.play(FadeIn(s))
        self.wait(2)


        self.play(AnimationGroup(*[FadeOut(element) for element in r.rectangles]),
                  AnimationGroup(*[FadeOut(element) for element in r.text]))

        # self.play(e.text[0]..shift(2*UP+5*LEFT))
        self.play(AnimationGroup(*[element.animate.shift(3*UP+2*LEFT) for element in e.text]),
                  s.animate.shift(3*UP+2*LEFT))

        summation = Tex(rf'$=\sum\limits_{{n=1}}^{{\infty}} \frac{{1}}{{2^n}}$', color=WHITE, font_size=64).next_to(s, RIGHT/2).shift(DOWN*0.075)
        self.wait(1)

        self.play(FadeIn(summation))

        self.wait(2)

        # self.play(AnimationGroup(*[FadeIn(element) for element in r.rectangles]))
        # self.play(AnimationGroup(*[FadeIn(element) for element in r.text]))
        # self.wait(2)
        # self.play(AnimationGroup(*[FadeOut(element) for element in r.rectangles]),
        #           AnimationGroup(*[FadeOut(element) for element in r.text]))

#
# h = 4
# w = 2
#
# x_offset = -1
# x_mult = 1
# y_offset = 1
# y_mult = 1
#
# rectangles = []
# for i in range(5):
#     if i == 0:
#         pass
#     elif i % 2 == 1:
#         h = h / 2
#         y_offset = y_offset - 1 * y_mult
#         x_offset = x_offset + 2 * x_mult
#     else:
#         w = w / 2
#         y_offset = y_offset + 2 * y_mult
#         x_offset = x_offset - 1/2 * x_mult
#         x_mult = x_mult/2
#         y_mult = y_mult/2
#
#
#     print(x_offset)