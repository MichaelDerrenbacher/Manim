import math
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



class Setup1(Scene):
    def construct(self):
        div = 2
        screen = Rectangle(width=9/div, height=16/div)

        box_color = WHITE
        arrow_color = LIGHT_GRAY

        g_box = Rectangle(width=1.25, height=0.75, color=box_color).move_to(UP*2.25+RIGHT*0.5)
        h_box = Rectangle(width=1.25, height=0.75, color=box_color).move_to(UP*1+RIGHT*0.5)

        summer = Circle(radius=0.25, color=box_color).move_to(UP*2.25+LEFT*1)

        plus_sum = Text('+', font_size=20, color=box_color).move_to(UP*2.25+LEFT*1)
        plus = Text('+', font_size=16, color=box_color).move_to(UP*2.4+LEFT*1.35)
        minus = Text('-', font_size=24, color=box_color).move_to(UP*1.9+LEFT*1.2)

        a1 = Arrow(start=UP*2.25+LEFT, end=UP*2.25+RIGHT*0.125, stroke_width=2, tip_length=0.15, color=arrow_color)
        a2 = Arrow(start=UP*2.25+LEFT*2.125, end=UP*2.25+LEFT, stroke_width=2, tip_length=0.15, color=arrow_color)
        a3 = Arrow(start=UP*2.25+RIGHT*0.875, end=UP*2.25+RIGHT*2.125, stroke_width=2, tip_length=0.15, color=arrow_color)

        a4_1 = Line(start=UP*1.0+LEFT, end=UP*1.0+LEFT*0.125, stroke_width=2, tip_length=0.15, color=arrow_color)
        a4_2 = Arrow(start=UP*0.74+LEFT, end=UP*1.125*2.0+LEFT, stroke_width=2, tip_length=0.15, color=arrow_color)

        a5_1 = Line(start=UP*2.25+RIGHT*1.5, end=UP*0.99+RIGHT*1.5, stroke_width=2, tip_length=0.15, color=arrow_color)
        a5_2 = Arrow(start=UP*1.0+RIGHT*1.75, end=UP*1.0+RIGHT*.875, stroke_width=2, tip_length=0.15, max_tip_length_to_length_ratio=2, color=arrow_color)

        Vin = Tex('$V_{in}(s)$', font_size=24, color=VIR_1).move_to(UP*2.5+LEFT*1.8)
        Vout = Tex('$V_{out}(s)$', font_size=24, color=VIR_3).move_to(UP*2.5+RIGHT*1.8)

        g_text = Tex('$G(s)$', font_size=24, color=VIR_5).move_to(UP*2.25+RIGHT*0.5)
        h_text = Tex('$H(s)$', font_size=24, color=VIR_7).move_to(UP*1+RIGHT*0.5)
        t_text = Tex('$T(s)$', font_size=24, color=VIR_9).move_to(UP*2.5+LEFT*0.475)

        self.play(
                # FadeIn(screen),
                  FadeIn(summer),
                  FadeIn(a1),
                  FadeIn(a2),
                  FadeIn(a3),
                  FadeIn(a4_1),
                  FadeIn(a4_2),
                  FadeIn(a5_1),
                  FadeIn(a5_2),
                  FadeIn(plus),
                  FadeIn(minus),
                  FadeIn(plus_sum),
                  FadeIn(g_box),
                  FadeIn(h_box),
                  FadeIn(g_text),
                  FadeIn(h_text),
                  FadeIn(Vin),
                  FadeIn(Vout))

        self.wait(2)

        self.play(FadeIn(t_text))

        self.wait(2)

        # ==========================================
        f_1 = Tex('$T(s)$', font_size=32, color=VIR_9).move_to(UP*0+LEFT*1.75)
        f_2 = Tex('=', font_size=32, color=WHITE).next_to(f_1, RIGHT*0.5)
        f_3 = Tex('$V_{in}(s)$', font_size=32, color=VIR_1).next_to(f_2, RIGHT*0.5)
        f_4 = Tex('$-$', font_size=32, color=WHITE).next_to(f_3, RIGHT*0.5)
        f_5 = Tex('$V_{out}(s)$', font_size=32, color=VIR_3).next_to(f_4, RIGHT*0.5)
        f_6 = Tex('$H(s)$', font_size=32, color=VIR_7).next_to(f_5, RIGHT*0.5)


        self.play(Indicate(t_text, color=WHITE))
        self.play(FadeIn(f_1))

        self.play(Indicate(Vin, color=WHITE))
        self.play(FadeIn(f_2),
                  FadeIn(f_3))

        self.play(Indicate(Vout, color=WHITE))
        self.play(FadeIn(f_4),
                  FadeIn(f_5))

        self.play(Indicate(h_text, color=WHITE))
        self.play(FadeIn(f_6))
        # ==========================================

        self.wait(2)

        g_1 = Tex('$V_{out}(s)$', font_size=28, color=VIR_3).move_to(DOWN*0.75+LEFT*1)
        g_2 = Tex('=', font_size=28, color=WHITE).next_to(g_1, RIGHT*0.5)
        g_3 = Tex('$T(s)$', font_size=28, color=VIR_9).next_to(g_2, RIGHT*0.5)
        g_4 = Tex('$G(s)$', font_size=28, color=VIR_5).next_to(g_3, RIGHT*0.5)

        self.play(Indicate(Vout, color=WHITE))
        self.play(FadeIn(g_1))

        self.play(Indicate(t_text, color=WHITE))
        self.play(FadeIn(g_2),
                  FadeIn(g_3))

        self.play(Indicate(g_text, color=WHITE))
        self.play(FadeIn(g_4))
        # ==========================================

        self.wait(2)

        h_1 = Tex(r'$T(s) = \frac{Vout(s)}{G(s)}$', font_size=28, color=WHITE).move_to(DOWN*0.75+LEFT*0)

        h_1[0][0:4].set_fill(color=VIR_9)
        h_1[0][5:5].set_fill(color=WHITE)
        h_1[0][5:12].set_fill(color=VIR_3)
        h_1[0][13:18].set_fill(color=VIR_5)


        self.play(ReplacementTransform(g_1, h_1),
                  FadeOut(g_2),
                  FadeOut(g_3),
                  FadeOut(g_4))

        self.wait(2)


        # ==========================================

        j_1 = Tex(r'$\frac{Vout(s)}{G(s)}$', font_size=28, color=WHITE).move_to(UP*0+LEFT*1.75)
        j_1[0][0:7].set_fill(color=VIR_3)
        j_1[0][8:12].set_fill(color=VIR_5)

        self.play(ReplacementTransform(f_1, j_1),
                  FadeOut(h_1),
                  FadeOut(t_text))
        self.wait(2)

        # ==========================================

        t_1 = Tex(r'$\frac{V_{out}(s)}{G(s)} + V_{out}(s)H(s) = V_{in}(s)$', font_size=28, color=WHITE).move_to(DOWN*0.75+LEFT*0)
        t_1[0][0:7].set_fill(color=VIR_3)
        t_1[0][8:12].set_fill(color=VIR_5)
        t_1[0][13:20].set_fill(color=VIR_3)
        t_1[0][20:24].set_fill(color=VIR_7)
        t_1[0][25:31].set_fill(color=VIR_1)

        self.play(FadeIn(t_1))
        self.wait(2)

        # ==========================================

        k_1 = Tex(r'$V_{out}(s) \left( \frac{1}{G(s)} + H(s) \right) = V_{in}(s)$', font_size=28, color=WHITE).move_to(DOWN*1.5+LEFT*0)
        k_1[0][0:7].set_fill(color=VIR_3)
        k_1[0][10:14].set_fill(color=VIR_5)
        k_1[0][15:19].set_fill(color=VIR_7)
        k_1[0][21:31].set_fill(color=VIR_1)
        self.play(FadeIn(k_1))
        self.wait(2)

        # ==========================================

        l_1 = Tex(r'$V_{out}(s) \left(\frac{1 + G(s)H(s)}{G(s)} \right) = V_{in}(s)$', font_size=28, color=WHITE).move_to(DOWN*2.25+LEFT*0)
        l_1[0][0:7].set_fill(color=VIR_3)
        l_1[0][10:14].set_fill(color=VIR_5)
        l_1[0][14:18].set_fill(color=VIR_7)
        l_1[0][19:23].set_fill(color=VIR_5)
        l_1[0][25:31].set_fill(color=VIR_1)
        self.play(FadeIn(l_1))
        self.wait(2)

        # ==========================================

        p_1 = Tex(r'$ \frac{V_{out}(s)}{V_{in}(s)} = \frac{G(s)}{1 + G(s)H(s)}$', font_size=28, color=WHITE).move_to(DOWN*3.25+LEFT*0)
        p_1[0][0:7].set_fill(color=VIR_3)
        p_1[0][8:14].set_fill(color=VIR_1)
        p_1[0][15:19].set_fill(color=VIR_5)
        p_1[0][22:26].set_fill(color=VIR_5)
        p_1[0][26:31].set_fill(color=VIR_7)
        self.play(FadeIn(p_1))
        self.wait(2)

        self.play(p_1.animate.scale(48/28).shift(UP*3),
                  # FadeOut(g_1),
                  # FadeOut(h_1),
                  FadeOut(k_1),
                  FadeOut(l_1),
                  FadeOut(t_1),
                  FadeOut(j_1),
                  FadeOut(f_2),
                  FadeOut(f_3),
                  FadeOut(f_4),
                  FadeOut(f_5),
                  FadeOut(f_6))


        self.wait(2)

        self.play(
            # FadeIn(screen),
            FadeOut(summer),
            FadeOut(a1),
            FadeOut(a2),
            FadeOut(a3),
            FadeOut(a4_1),
            FadeOut(a4_2),
            FadeOut(a5_1),
            FadeOut(a5_2),
            FadeOut(plus),
            FadeOut(minus),
            FadeOut(plus_sum),
            FadeOut(g_box),
            FadeOut(h_box),
            FadeOut(g_text),
            FadeOut(h_text))
            # FadeOut(Vin),
            # FadeOut(Vout))

        gh_box = Rectangle(width=1.5, height=1, color=box_color).move_to(UP*2.25)
        gh_text = Tex(r'$\frac{G(s)}{1 + G(s)H(s)}$', font_size=28, color=WHITE).move_to(UP*2.25)
        gh_text[0][0:4].set_fill(color=VIR_5)
        gh_text[0][7:11].set_fill(color=VIR_5)
        gh_text[0][11:17].set_fill(color=VIR_7)

        a11 = Arrow(start=UP*2.25+LEFT*2.125, end=UP*2.25+LEFT*0.5, stroke_width=2, tip_length=0.15, color=arrow_color)
        a12 = Arrow(end=UP*2.25+RIGHT*2.125, start=UP*2.25+RIGHT*0.5, stroke_width=2, tip_length=0.15, color=arrow_color)


        self.play(FadeIn(gh_box),
                  FadeIn(gh_text),
                  FadeIn(a11),
                  FadeIn(a12))

        self.wait(2)
