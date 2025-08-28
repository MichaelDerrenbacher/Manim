import math
from typing import Callable

from manim import *
from colour import Color
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.scene.scene import Scene
from manim.utils.rate_functions import smooth
from pyglet.resource import animation
from typing import TYPE_CHECKING, Any, Callable, Iterable, Sequence

"""
16 VIRIDIS
"""
VIR_1: str = "#fde725"
VIR_2: str = "#d2e21b"
VIR_3: str = "#a5db36"
VIR_4: str = "#7ad151"
VIR_5: str = "#54c568"
VIR_6: str = "#35b779"
VIR_7: str = "#22a884"
VIR_8: str = "#1f988b"
VIR_9: str = "#23888e"
VIR_10: str = "#2a788e"
VIR_11: str = "#31688e"
VIR_12: str = "#39568c"
VIR_13: str = "#414487"
VIR_14: str = "#472f7d"
VIR_15: str = "#481a6c"
VIR_16: str = "#440154"

viridis_colors = [VIR_1,
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


class semilogx(NumberPlane):
    def SIformat(self, value, decimals=0, digits=None, unit=""):
        sign = +1
        if value < 0:
            sign = -1
            value = -value
        if value >= 1e-24 and value <= 1e24:
            prefixes = ['y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
            pten24 = int((np.log10(value) + 24) / 3) * 3
            prefix = prefixes[pten24 // 3]
            mantissa = value / (10 ** (pten24 - 24))
            if digits != None:
                mantLen = int(np.log10(mantissa)) + 1
                if digits > mantLen:
                    decimals = digits - mantLen
                else:
                    decimals = 0
                    mantissa = (mantissa // 10 ** (mantLen - digits)) * 10 ** (mantLen - digits)
            return f"{{:.{decimals}f}}\,{{:s}}".format(sign * mantissa, prefix + unit)
        elif value == 0:
            return f"{{:.{decimals}f}}\,{{:s}}".format(0, unit)
        else:
            return "{:.2g}".format(value)

    def __init__(
            self,
            x_range=(
                    -config["frame_x_radius"],
                    config["frame_x_radius"],
                    1,
            ),
            y_range=(
                    -config["frame_y_radius"],
                    config["frame_y_radius"],
                    1,
            ),
            x_length=None,
            y_length=None,
            x_unit="Hz",
            y_unit="dB",
            foreground_line_style=None,
            background_line_style=None,
            faded_line_style=None,
            faded_line_ratio: int = 1,
            make_smooth_after_applying_functions: bool = True,
            **kwargs,
    ):
        # init
        if x_range[0] <= 0:
            raise Exception("wrong lower limit on x_range")

        self.x_unit = x_unit
        self.y_unit = y_unit

        self.foreground_line_style = foreground_line_style
        self.background_line_style = background_line_style

        super().__init__(
            x_range=[int(np.log10(x_range[0])), int(np.log10(x_range[1]) + 0.99), 1],
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={"stroke_width": 3},
            x_axis_config={"scaling": LogBase()},
            y_axis_config={"scaling": LinearBase()},
            background_line_style=self.background_line_style,
            tips=False,
            **kwargs,
        )

        # remove all lines created automatically
        self.remove(self.background_lines)
        self.remove(self.x_axis[0])
        self.remove(self.y_axis[0])

        self.x_labels = VGroup(
            *[Tex(self.SIformat(10 ** x, digits=1, unit=x_unit)).scale(0.6)
              .next_to(self.c2p(10 ** x, self.y_range[0]), DOWN, buff=0.15)
              for x in np.arange(self.x_range[0], self.x_range[1] + 1, self.x_range[2])]
        )
        self.add(self.x_labels)

        self.y_labels = VGroup(
            *[Tex(self.SIformat(y, digits=1, unit=y_unit)).scale(0.6)
              .next_to(self.c2p(10 ** self.x_range[0], y), LEFT, buff=0.15)
              for y in np.arange(self.y_range[0], self.y_range[1] + 1, self.y_range[2])]
        )
        self.add(self.y_labels)

        background_line_stroke_color = self.background_line_style['stroke_color']
        background_line_stroke_width = self.background_line_style['stroke_width']
        background_line_stroke_opacity = self.background_line_style['stroke_opacity']
        self.x_major_grid = VGroup(
            *[
                Line(self.c2p(n * 10 ** x, self.y_range[0]), self.c2p(n * 10 ** x, self.y_range[1]),
                     stroke_color=background_line_stroke_color,
                     stroke_width=background_line_stroke_width,
                     stroke_opacity=background_line_stroke_opacity,
                     )
                for n in [1] for x in np.arange(self.x_range[0], self.x_range[1] + 1, self.x_range[2])
            ]
        )
        self.add(self.x_major_grid)

        self.y_major_grid = VGroup(
            *[
                Line(self.c2p(10 ** self.x_range[0], y), self.c2p(10 ** self.x_range[1], y),
                     stroke_color=LIGHT_GRAY,  # = background_line_stroke_color,
                     stroke_width=background_line_stroke_width,
                     stroke_opacity=background_line_stroke_opacity,
                     )
                for n in [1] for y in np.arange(self.y_range[0], self.y_range[1] + 1, self.y_range[2])
            ]
        )
        self.add(self.y_major_grid)

        background_line_stroke_width = self.background_line_style['stroke_width'] / 3
        self.x_minor_grid = VGroup(
            *[
                Line(self.c2p(n * 10 ** x, self.y_range[0]), self.c2p(n * 10 ** x, self.y_range[1]),
                     stroke_color=LIGHT_GRAY,  # = background_line_stroke_color,
                     stroke_width=background_line_stroke_width,
                     stroke_opacity=background_line_stroke_opacity,
                     )
                for n in [2, 3, 4, 5, 6, 7, 8, 9] for x in np.arange(self.x_range[0], self.x_range[1], self.x_range[2])
            ]
        )
        self.add(self.x_minor_grid)

        self.y_minor_grid = VGroup(
            *[
                Line(self.c2p(10 ** self.x_range[0], n * self.y_range[2] + y),
                     self.c2p(10 ** self.x_range[1], n * self.y_range[2] + y),
                     stroke_color=LIGHT_GRAY,  # background_line_stroke_color,
                     stroke_width=background_line_stroke_width,
                     stroke_opacity=background_line_stroke_opacity,
                     )
                for n in [.5] for y in np.arange(self.y_range[0], self.y_range[1], self.y_range[2])
            ]
        )
        self.add(self.y_minor_grid)


class Setup1(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        cir = ImageMobject("max_power_cir.png").move_to(2 * UP + 3.5 * LEFT).scale(1.2).set_z_index(-1)
        self.play(FadeIn(cir))
        self.wait(2)


        v_th = Tex(r'$V_{th}$', font_size=36, color=VTH).move_to(UP * 1.95 + LEFT * 4.9)

        rth = Tex(r'$R_{th}$', font_size=36, color=RTH).move_to(UP * 2.50 + LEFT * 4.4)
        rl = Tex(r'$R_{L}$', font_size=36, color=RL).move_to(UP * 1.95 + LEFT * 0.6)

        elements = VGroup(v_th, rth, rl)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        p1 = Tex(r'$V = I R $', font_size=36).move_to(UP * 3 + RIGHT * 2.5)
        p2 = Tex(r'$P = I V$', font_size=36).move_to(UP * 2.5 + RIGHT * 2.5)
        p3 = Tex(r'$P = I^2 R$', font_size=36).move_to(UP * 2.75 + RIGHT * 2.5)
        p4 = Tex(r'$P_{L} = I_{L}\text{}^2 R_{L}$', font_size=36).move_to(UP * 2.75 + RIGHT * 2.5)
        p4[0][0:2].set_fill(color=PL)
        p4[0][6:8].set_fill(color=RL)
        p4[0][3:5].set_fill(color=IL)

        self.play(FadeIn(p1))
        self.wait(2)
        self.play(FadeIn(p2))
        self.wait(2)
        self.play(ReplacementTransform(p1, p3),
                  FadeOut(p2))
        self.wait(2)
        self.play(ReplacementTransform(p3, p4))
        self.wait(2)


        i1 = Tex(r'$I_{L} = \frac{V_{Th}}{R_{Th}+R_{L}}$', font_size=36).move_to(UP * 2.75 + RIGHT * 5)
        i1[0][0:2].set_fill(color=IL)
        i1[0][3:6].set_fill(color=VTH)
        i1[0][7:10].set_fill(color=RTH)
        i1[0][11:13].set_fill(color=RL)

        self.play(FadeIn(i1))
        self.wait(2)

        p5 = Tex(r'$P_{L} = V_{Th}\text{}^2 \frac{R_L}{(R_{Th}+R_{L})^2}$', font_size=36).move_to(UP * 2.0 + RIGHT * 3.8)
        p5[0][0:2].set_fill(color=PL)
        p5[0][3:6].set_fill(color=VTH)
        p5[0][7:9].set_fill(color=RL)
        p5[0][11:14].set_fill(color=RTH)
        p5[0][15:17].set_fill(color=RL)
        self.play(FadeIn(p5))
        self.wait(2)

        axes = NumberPlane(
            x_range=[-0.001, 20.001, 1],  # x_min, x_max, x_step
            y_range=[-0.001, 0.25001, 0.125],  # y_min, y_max, y_step
            x_length=12,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20],
                           "label_direction": LEFT * 0.0 + DOWN*0.4,
                           "numbers_to_exclude": []},
            y_axis_config={"numbers_to_include": [0, 0.125, 0.250],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(1.5*DOWN)


        def func(x):
            return 1 * x / (x+1)**2

        graph = axes.plot(func, color=PL)

        eqn1 = Tex(r'$P_{L} \text{ vs } \frac{R_L}{R_{TH}} \text{ with } V_{Th} = 1 \text{V}$', font_size=36).move_to(UP * 0.4 + RIGHT * 0.0)
        eqn1[0][0:2].set_fill(color=PL)
        eqn1[0][4:6].set_fill(color=RL)
        eqn1[0][7:10].set_fill(color=RTH)
        eqn1[0][14:17].set_fill(color=VTH)

        ylabel = Tex(r"$P_{L}$", font_size=36).move_to(LEFT*6.7+DOWN*1.45)
        ylabel[0][0:2].set_fill(color=PL)

        xlabel = Tex(r"$\frac{R_L}{R_{TH}}$", font_size=36).move_to(DOWN*3.5)
        xlabel[0][0:2].set_fill(color=RL)
        xlabel[0][3:6].set_fill(color=RTH)

        self.play(FadeIn(axes),
                  FadeIn(graph),
                  FadeIn(eqn1),
                  FadeIn(xlabel),
                  FadeIn(ylabel))
        self.wait(2)


        circle = Circle(radius=0.25, color=VIR_1).move_to(LEFT*5.15+UP*.05)

        self.play(FadeIn(circle))
        self.wait(2)
        self.play(FadeOut(circle))
        self.wait(2)

        self.play(FadeOut(axes),
                  FadeOut(graph),
                  FadeOut(eqn1),
                  FadeOut(xlabel),
                  FadeOut(ylabel))
        self.wait(2)


        self.play(Indicate(p5, color=WHITE))

        self.wait(2)

        short = Tex(r'$R_L = 0\Omega:$', font_size=36).move_to(UP * 1 + RIGHT * 3.8)
        short[0][0:2].set_fill(color=RL)
        self.play(FadeIn(short))
        self.wait(2)

        p6 = Tex(r'$P_{L} = V_{Th}\text{}^2 \frac{0}{(R_{Th}+0)^2} = 0\text{W}$', font_size=36).move_to(UP * 0.0 + RIGHT * 3.8)
        p6[0][0:2].set_fill(color=PL)
        p6[0][3:6].set_fill(color=VTH)
        p6[0][10:13].set_fill(color=RTH)


        self.play(FadeIn(p6))
        self.wait(2)

        openc = Tex(r'$\lim\limits_{R_L\to\infty\Omega}:$', font_size=36).move_to(UP * 1 + RIGHT * 3.8)
        openc[0][3:5].set_fill(color=RL)
        self.play(FadeOut(p6),
                  ReplacementTransform(short, openc))
        self.wait(2)

        p6 = Tex(r'$P_{L} = V_{Th}\text{}^2 \frac{\infty}{(R_{Th}+\infty)^2} = 0\text{W}$', font_size=36).move_to(UP * 0.0 + RIGHT * 3.8)
        p6[0][0:2].set_fill(color=PL)
        p6[0][3:6].set_fill(color=VTH)
        p6[0][10:13].set_fill(color=RTH)

        self.play(FadeIn(p6))
        self.wait(2)
        self.play(FadeOut(p6),
                  FadeOut(openc))
        self.wait(2)

        p7 = Tex(r'$ max(P_{L}) = \text{?}$', font_size=36).move_to(UP * 1.0 + RIGHT * 3.8)
        p7[0][4:6].set_fill(color=PL)

        self.play(FadeIn(p7))
        self.wait(2)

class Setup2(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        p1 = Tex(r'$P_{L} = V_{Th}\text{}^2 \frac{R_L}{(R_{Th}+R_{L})^2}$', font_size=48).move_to(UP * 3.0 + LEFT * 3)
        p1[0][0:2].set_fill(color=PL)
        p1[0][3:6].set_fill(color=VTH)
        p1[0][7:9].set_fill(color=RL)
        p1[0][11:14].set_fill(color=RTH)
        p1[0][15:17].set_fill(color=RL)
        self.play(FadeIn(p1))
        self.wait(2)

        p2 = Tex(r'$\frac{d P_L}{d R_L} = 0$', font_size=48).move_to(UP * 2.0 + LEFT * 3)
        p2[0][1:3].set_fill(color=PL)
        p2[0][5:7].set_fill(color=RL)
        self.play(FadeIn(p2))
        self.wait(2)

        quo_1 = Tex(r'$h(x) = \frac{f(x)}{g(x)}$', font_size=48).move_to(UP * 3.0 + RIGHT * 3)
        quo_2 = Tex(r"$h'(x) = \frac{f'(x)g(x)-f(x)g'(x)}{(g(x))^2}$", font_size=48).move_to(UP * 2.0 + RIGHT * 3)

        self.play(FadeIn(quo_1))
        self.wait(2)
        self.play(FadeIn(quo_2))
        self.wait(2)


        fx = Tex(r'$f(x) = R_L$', font_size=36).move_to(UP * 1.0 + RIGHT * 2.2)
        fxp = Tex(r"$f'(x) = 1$", font_size=36).move_to(UP * 0.5 + RIGHT * 2.07)
        gx = Tex(r'$g(x) = (R_{th} + R_L)^2$', font_size=36).move_to(UP * 0.0 + RIGHT * 2.925)
        gxp = Tex(r"$g'(x) = 2(R_{th} + R_L)$", font_size=36).move_to(UP * -0.5 + RIGHT * 3)
        fx[0][5:7].set_fill(color=RL)
        gx[0][6:9].set_fill(color=RTH)
        gx[0][10:12].set_fill(color=RL)
        gxp[0][8:11].set_fill(color=RTH)
        gxp[0][12:14].set_fill(color=RL)

        elements = VGroup(fx, fxp, gx, gxp)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        elements2 = VGroup(elements, quo_1, quo_2)

        p3 = Tex(r'$\frac{d P_L}{d R_L} = V_{th}\text{}^2\left(\frac{1 (R_{th}+R_L)^2 - 2R_L(R_{th}+R_L)}{(R_{th} + R_L)^4}\right) = 0$', font_size=48).move_to(UP * 0.5 + LEFT * 0)
        p3[0][1:3].set_fill(color=PL)
        p3[0][5:7].set_fill(color=RL)
        p3[0][8:11].set_fill(color=VTH)
        p3[0][15:18].set_fill(color=RTH)
        p3[0][19:21].set_fill(color=RL)
        p3[0][25:27].set_fill(color=RL)
        p3[0][28:31].set_fill(color=RTH)
        p3[0][32:34].set_fill(color=RL)
        p3[0][37:40].set_fill(color=RTH)
        p3[0][41:43].set_fill(color=RL)

        self.play(ReplacementTransform(elements2, p3),
                  p1.animate.shift(3*RIGHT),
                  p2.animate.shift(3*RIGHT))
        self.wait(2)

        self.play(Indicate(p3[0][13:35], color=WHITE, scale_factor=1.1))
        self.wait(2)


        p4 = Tex(r'$1 (R_{th}+R_L)^2 - 2R_L(R_{th}+R_L) = 0$', font_size=48).move_to(DOWN * 1 + LEFT * 0)
        off = 13
        p4[0][15-off:18-off].set_fill(color=RTH)
        p4[0][19-off:21-off].set_fill(color=RL)
        p4[0][25-off:27-off].set_fill(color=RL)
        p4[0][28-off:31-off].set_fill(color=RTH)
        p4[0][32-off:34-off].set_fill(color=RL)
        p4[0][37-off:40-off].set_fill(color=RTH)
        p4[0][41-off:43-off].set_fill(color=RL)

        self.play(FadeIn(p4))
        self.wait(2)


        p5 = Tex(r'$R_{th}\text{}^2 + 2R_{th}R_L + R_L\text{}^2 - 2R_L\text{}^2-2R_{th}R_L = 0$', font_size=48).move_to(DOWN * 1 + LEFT * 0)
        p5[0][0:3].set_fill(color=RTH)
        p5[0][6:9].set_fill(color=RTH)
        p5[0][9:11].set_fill(color=RL)
        p5[0][12:14].set_fill(color=RL)
        p5[0][17:19].set_fill(color=RL)
        p5[0][22:25].set_fill(color=RTH)
        p5[0][25:27].set_fill(color=RL)

        self.play(ReplacementTransform(p4, p5))
        self.wait(2)


        p6 = Tex(r'$R_{th}\text{}^2 - R_L\text{}^2 = 0$', font_size=48).move_to(DOWN * 1 + LEFT * 0)
        p6[0][0:3].set_fill(color=RTH)
        p6[0][5:7].set_fill(color=RL)

        self.play(ReplacementTransform(p5, p6))
        self.wait(2)

        p7 = Tex(r'$R_{th} = R_L$', font_size=48).move_to(DOWN * 1 + LEFT * 0)
        p7[0][0:3].set_fill(color=RTH)
        p7[0][4:6].set_fill(color=RL)

        self.play(ReplacementTransform(p6, p7))
        self.wait(2)

        self.play(FadeOut(p1),
                  FadeOut(p2),
                  FadeOut(p3),
                  p7.animate.shift(UP*4))
        self.wait(2)


        axes = NumberPlane(
            x_range=[-0.001, 20.001, 1],  # x_min, x_max, x_step
            y_range=[-0.001, 0.25001, 0.125],  # y_min, y_max, y_step
            x_length=12,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20],
                           "label_direction": LEFT * 0.0 + DOWN*0.4,
                           "numbers_to_exclude": []},
            y_axis_config={"numbers_to_include": [0, 0.125, 0.250],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(1.5*DOWN)


        def func(x):
            return 1 * x / (x+1)**2

        graph = axes.plot(func, color=PL)

        eqn1 = Tex(r'$P_{L} \text{ vs } \frac{R_L}{R_{TH}} \text{ with } V_{Th} = 1 \text{V}$', font_size=36).move_to(UP * 0.4 + RIGHT * 0.0)
        eqn1[0][0:2].set_fill(color=PL)
        eqn1[0][4:6].set_fill(color=RL)
        eqn1[0][7:10].set_fill(color=RTH)
        eqn1[0][14:17].set_fill(color=VTH)

        ylabel = Tex(r"$P_{L}$", font_size=36).move_to(LEFT*6.7+DOWN*1.45)
        ylabel[0][0:2].set_fill(color=PL)

        xlabel = Tex(r"$\frac{R_L}{R_{TH}}$", font_size=36).move_to(DOWN*3.5)
        xlabel[0][0:2].set_fill(color=RL)
        xlabel[0][3:6].set_fill(color=RTH)

        self.play(FadeIn(axes),
                  FadeIn(graph),
                  FadeIn(eqn1),
                  FadeIn(xlabel),
                  FadeIn(ylabel))
        self.wait(2)


        axes2 = NumberPlane(
            # x_range=[-0.001, 20.001, 1],  # x_min, x_max, x_step
            y_range=[-0.001, 0.25001, 0.125],  # y_min, y_max, y_step
            x_length=12,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20],
                           "label_direction": LEFT * 0.0 + DOWN*0.4,
                           "numbers_to_exclude": [],
                           "scaling": LogBase(custom_labels=True)},
            y_axis_config={"numbers_to_include": [0, 0.125, 0.250],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(1.5*DOWN)


        def func(x):
            return 1 * x / (x+1)**2

        graph2 = axes2.plot(func, color=PL).shift(0.08*LEFT)

        self.play(ReplacementTransform(axes, axes2),
                  ReplacementTransform(graph, graph2))
        self.wait(2)


class Setup3(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        cir = ImageMobject("max_power_cir.png").move_to(1.5 * UP + 0 * LEFT).scale(2).set_z_index(-1)
        self.play(FadeIn(cir))
        self.wait(2)


        v_th = Tex(r'$V_{th}$', font_size=48, color=VTH).move_to(UP * 1.4 + LEFT * 2.4)

        rth = Tex(r'$R_{th}$', font_size=48, color=RTH).move_to(UP * 2.45 + LEFT * 1.5)
        rl = Tex(r'$R_{L}$', font_size=48, color=RL).move_to(UP * 1.4 + RIGHT * 4.75)

        elements = VGroup(v_th, rth, rl)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)


        p1 = Tex(r'$R_{th} = R_L$', font_size=48).move_to(DOWN * 1 + LEFT * 0)
        p1[0][0:3].set_fill(color=RTH)
        p1[0][4:6].set_fill(color=RL)

        p2 = Tex(r'$max(P_{L}) = \frac{V_{th}\text{}^2}{4R_{th}}$', font_size=48).move_to(DOWN * 2)
        p2[0][4:6].set_fill(color=PL)
        p2[0][8:11].set_fill(color=VTH)
        p2[0][14:17].set_fill(color=RTH)


        self.play(FadeIn(p1))
        self.wait(2)

        self.play(FadeIn(p2))
        self.wait(2)



class Setup4(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        l1 = Line(start=LEFT*2+UP*2.1, end=RIGHT*2+UP*2.1, stroke_width=2, stroke_color=RED)
        l2 = Line(start=LEFT*2+UP*1.9, end=RIGHT*2+UP*1.9, stroke_width=2, stroke_color=GRAY)

        r1 = Rectangle(width=4, height=3, stroke_width=2, stroke_color=VIR_1).move_to(LEFT*4+UP*2)
        t1 = Text(r"Power Supply", font_size=36).move_to(LEFT*4+UP*3)

        r2 = Rectangle(width=4, height=3, stroke_width=2, stroke_color=VIR_3).move_to(RIGHT*4+UP*2)
        t2 = Text(r"Circuit Board", font_size=36).move_to(RIGHT*4+UP*3)

        elements = VGroup(r1, r2, l1, l2, t1, t2)

        self.play(AnimationGroup(*[DrawBorderThenFill(element) for element in elements], lag_ratio=0.2))

        self.wait(2)

        t3 = Text(r"Soft Short", font_size=24).move_to(RIGHT*4+UP*2)

        self.play(DrawBorderThenFill(t3))
        self.wait(2)


        p1 = Tex(r'$R_{th} = R_L$', font_size=48).move_to(DOWN * 0 + LEFT * 0)
        p1[0][0:3].set_fill(color=RTH)
        p1[0][4:6].set_fill(color=RL)

        p2 = Tex(r'$max(P_{L}) = \frac{V_{th}\text{}^2}{4R_{th}}$', font_size=48).move_to(DOWN * 1)
        p2[0][4:6].set_fill(color=PL)
        p2[0][8:11].set_fill(color=VTH)
        p2[0][14:17].set_fill(color=RTH)


        self.play(FadeIn(p1))
        self.wait(2)

        self.play(FadeIn(p2))
        self.wait(2)



        f1 = Tex(r"$V_{th} = 5\text{V}$", font_size=36).move_to(LEFT*4+UP*1.5)
        f2 = Tex(r"$R_{th} = 5\Omega$", font_size=36).move_to(LEFT*4+UP*1)
        f1[0][0:3].set_fill(color=VTH)
        f2[0][0:3].set_fill(color=RTH)


        elements1 = VGroup(f1, f2)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements1], lag_ratio=0.2))


        p3 = Tex(r'$max(P_{L}) = \frac{5^2}{4\cdot 5} = 1.25 \text{W}$', font_size=48).move_to(DOWN * 2)
        p3[0][4:6].set_fill(color=PL)

        self.play(FadeIn(p3))
        self.wait(2)



        f3 = Tex(r"$R_{L} = 5\Omega$", font_size=36).move_to(RIGHT*4+UP*1.5)
        f4 = Tex(r"$P_{L} = 1.25\text{W}$", font_size=36).move_to(RIGHT*4+UP*1)

        f3[0][0:2].set_fill(color=RL)
        f4[0][0:2].set_fill(color=PL)

        elements2 = VGroup(f3, f4)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements2], lag_ratio=0.2))

        self.wait(2)


class Setup5(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        t1 = Text(r"?", font_size=128).move_to(UP*1.5)



        t2 = Text(r"Use a known affected board?", font_size=32).move_to(UP*0)



        t3 = Text(r"Replace the soft short with a low resistance connection?", font_size=32).move_to(UP*0)






        self.play(FadeIn(t1))
        self.wait(2)
        self.play(FadeIn(t2))
        self.wait(2)
        self.play(ReplacementTransform(t2, t3))
        self.wait(2)
        self.play(FadeOut(t1),
                  FadeOut(t3))


class Setup6(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9


        t1 = Text(r"Failure Analysis", gradient=(VIR_1, VIR_3)).scale(1.5).move_to(UP*1.5)
        t2 = Text(r"done using the basics", gradient=(VIR_5, VIR_7)).scale(1.5).move_to(UP*0.5)


        self.play(Write(t1),
                  Write(t2))
        self.wait(2)
        self.play(FadeOut(t1),
                  FadeOut(t2))

class Setup7(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9


        t1 = Text(r"Failure Analysis",).scale(1.5).move_to(UP*1.5)
        t2 = Text(r"done using the basics", gradient=(VIR_5, VIR_7)).scale(1.5).move_to(UP*0.5)


        self.play(Write(t1),
                  Write(t2))
        self.wait(2)
        self.play(FadeOut(t1),
                  FadeOut(t2))

class Setup8(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        axes = NumberPlane(
            x_range=[-0.001, 20.001, 1],  # x_min, x_max, x_step
            y_range=[-0.001, 0.25001, 0.125],  # y_min, y_max, y_step
            x_length=12,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [],
                           "label_direction": LEFT * 0.0 + DOWN*0.4,
                           "numbers_to_exclude": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20]},
            y_axis_config={"numbers_to_include": [],
                           "numbers_to_exclude": [0, 0.125, 0.250],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(1.5*DOWN)


        def func(x):
            return 1 * x / (x+1)**2

        graph = axes.plot(func, color=PL)

        self.add(axes, graph)

        self.wait(2)


class Setup9(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9

        l1 = Line(start=LEFT * 2 + UP * 2.1, end=RIGHT * 2 + UP * 2.1, stroke_width=2, stroke_color=RED)
        l2 = Line(start=LEFT * 2 + UP * 1.9, end=RIGHT * 2 + UP * 1.9, stroke_width=2, stroke_color=GRAY)

        r1 = Rectangle(width=4, height=3, stroke_width=2, stroke_color=VIR_1).move_to(LEFT * 4 + UP * 2)
        t1 = Text(r"Power Supply", font_size=36).move_to(LEFT * 4 + UP * 3)

        r2 = Rectangle(width=4, height=3, stroke_width=2, stroke_color=VIR_3).move_to(RIGHT * 4 + UP * 2)
        t2 = Text(r"Circuit Board", font_size=36).move_to(RIGHT * 4 + UP * 3)

        elements = VGroup(r1, r2, l1, l2, t1, t2)

        self.play(AnimationGroup(*[DrawBorderThenFill(element) for element in elements], lag_ratio=0.2))

        t3 = Text(r"Soft Short", font_size=24).move_to(RIGHT * 4 + UP * 2)

        self.play(DrawBorderThenFill(t3))
        self.wait(2)

        t4 = Text(r"Definitions:", font_size=24).move_to(LEFT * 6 + DOWN * 0.5)
        t5 = Text(r"Soft Short: an unintentional low impedance connection; not necessarily 0Ω", font_size=18).move_to(LEFT * 1.5 + DOWN * 1.0)
        t6 = Text(r"Ambient Temperature: The temperature of the environment surrounding a circuit, typically 25°C", font_size=18).move_to(LEFT * 0.125 + DOWN * 1.5)
        t7 = Text(r"Temperature Rise: The increase from ambient temperature due to heating", font_size=18).move_to(LEFT * 1.575 + DOWN * 2.0)


        elements2 = VGroup(t4,t5,t6,t7)

        self.play(AnimationGroup(*[Write(element) for element in elements2], lag_ratio=0.2))
        self.wait(2)


class Setup10(Scene):
    def construct(self):
        VTH = VIR_1
        RTH = VIR_3
        RL = VIR_5
        IL = VIR_7
        PL = VIR_9
        p7 = Tex(r'$R_{th} = R_L$', font_size=48).move_to(UP * 3 + LEFT * 0)
        p7[0][0:3].set_fill(color=RTH)
        p7[0][4:6].set_fill(color=RL)


        self.add(p7)

        eqn1 = Tex(r'$P_{L} \text{ vs } \frac{R_L}{R_{TH}} \text{ with } V_{Th} = 1 \text{V}$', font_size=36).move_to(UP * 0.4 + RIGHT * 0.0)
        eqn1[0][0:2].set_fill(color=PL)
        eqn1[0][4:6].set_fill(color=RL)
        eqn1[0][7:10].set_fill(color=RTH)
        eqn1[0][14:17].set_fill(color=VTH)

        ylabel = Tex(r"$P_{L}$", font_size=36).move_to(LEFT*6.7+DOWN*1.45)
        ylabel[0][0:2].set_fill(color=PL)

        xlabel = Tex(r"$\frac{R_L}{R_{TH}}$", font_size=36).move_to(DOWN*3.5)
        xlabel[0][0:2].set_fill(color=RL)
        xlabel[0][3:6].set_fill(color=RTH)

        self.play(FadeIn(eqn1),
                  FadeIn(xlabel),
                  FadeIn(ylabel))

        axes2 = NumberPlane(
            # x_range=[-0.001, 20.001, 1],  # x_min, x_max, x_step
            y_range=[-0.001, 0.25001, 0.125],  # y_min, y_max, y_step
            x_length=12,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20],
                           "label_direction": LEFT * 0.0 + DOWN*0.4,
                           "numbers_to_exclude": [],
                           "scaling": LogBase(custom_labels=True)},
            y_axis_config={"numbers_to_include": [0, 0.125, 0.250],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(1.5*DOWN)


        def func(x):
            return 1 * x / (x+1)**2

        graph2 = axes2.plot(func, color=PL).shift(0.08*LEFT)

        self.add(axes2, graph2)
        self.wait(2)

        circle1 = Circle(radius=0.25, color=VIR_1).move_to(LEFT*0.675+DOWN*1.95)
        circle2 = Circle(radius=0.25, color=VIR_1).move_to(RIGHT*1.025+DOWN*1.95)

        self.play(FadeIn(circle1),
                  FadeIn(circle2))
        self.wait(2)
        self.play(FadeOut(circle1),
                  FadeOut(circle2))
        self.wait(2)
        #