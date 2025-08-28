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
        cir = ImageMobject("images/oscope_1.png").move_to(2 * UP + 3.5 * LEFT).scale(1).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in = Tex('$V_{in}$', font_size=30, color=VIR_1).move_to(UP * 2.35 + LEFT * 6.1)
        v_out = Tex('$V_{out}$', font_size=30, color=VIR_3).move_to(UP * 2.35 + LEFT * 0.85)

        # c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP*3.6+LEFT*4.2)
        r1 = Tex('$R_1$', font_size=30, color=VIR_7).move_to(UP * 2.7 + LEFT * 4.2)

        # c2 = Tex('$C_1$', font_size=30, color=VIR_9).move_to(UP*1.55+LEFT*2.4)
        r2 = Tex('$R_2$', font_size=30, color=VIR_11).move_to(UP * 1.55 + LEFT * 3.3)

        elements = VGroup(v_in, v_out, r1, r2)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        it_arrow = Arc(radius=0.33, arc_center=[ORIGIN], start_angle=0, angle=3 * PI / 2, stroke_width=3,
                       color=VIR_13).move_to(4 * LEFT + 1.4 * UP)
        it_arrow.add_tip(tip_width=0.2)
        it_arrow.flip(UP)

        it = Tex('$i_t$', font_size=30, color=VIR_13).move_to(4.175 * LEFT + 1.6 * UP)
        self.play(FadeIn(it_arrow),
                  FadeIn(it))

        eqn_1 = Tex(r'$i_t = \frac{V_{in}}{R_1+R_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        eqn_1[0][0:2].set_fill(color=VIR_13)
        eqn_1[0][3:6].set_fill(color=VIR_1)
        eqn_1[0][7:9].set_fill(color=VIR_7)
        eqn_1[0][10:12].set_fill(color=VIR_11)

        self.play(FadeIn(eqn_1))

        eqn_2 = Tex(r'$V_{out} = i_t R_2$', font_size=42).move_to(1.5 * UP + 3 * RIGHT)
        eqn_2[0][0:4].set_fill(color=VIR_3)
        eqn_2[0][5:7].set_fill(color=VIR_13)
        eqn_2[0][7:9].set_fill(color=VIR_11)

        self.play(FadeIn(eqn_2))

        tf_z = Tex(r'$V_{out} = V_{in} \frac{R_2}{R_1+R_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        tf_z[0][0:4].set_fill(color=VIR_3)
        tf_z[0][5:8].set_fill(color=VIR_1)
        tf_z[0][8:10].set_fill(color=VIR_11)
        tf_z[0][11:13].set_fill(color=VIR_7)
        tf_z[0][14:16].set_fill(color=VIR_11)

        self.play(ReplacementTransform(eqn_1, tf_z),
                  FadeOut(eqn_2),
                  FadeOut(it_arrow),
                  FadeOut(it))

        self.wait(2)

        ax = semilogx(
            x_range=[1e3, 1e9],  # powers of ten!
            x_length=12,
            y_range=[-80, 20, 20],
            y_length=3,
            background_line_style={'stroke_color': WHITE, 'stroke_width': 1}
        ).shift(2 * DOWN)

        R2_value = ValueTracker(1)

        def voltage_divider(R1, R2):
            return R2 / (R1 + R2)
            # return 1.0/(1.0 + 1j*2*PI*f*1600*100e-9)

        ampliplot = ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(9, R2_value.get_value())))).set_color(
            VIR_3).shift(2 * DOWN)

        tf_label = Tex(r'$\left|\frac{V_{out}}{V_{in}}\right|$', font_size=42).move_to(0.1 * UP + 6.4 * LEFT)
        tf_label[0][3:7].set_fill(color=VIR_3)
        tf_label[0][8:11].set_fill(color=VIR_1)

        self.play(FadeIn(ax),
                  FadeIn(tf_label))

        R1_label = Tex(r'$R_1=$', font_size=32).move_to(2.5 * RIGHT + 1.5 * UP)
        R2_label = Tex(r'$R_2=$', font_size=32).move_to(2.5 * RIGHT + 1 * UP)

        R1_label[0][0:2].set_fill(color=VIR_7)
        R2_label[0][0:2].set_fill(color=VIR_11)

        R1_number = Tex(r'$9.00\text{ M}\Omega$', font_size=32).next_to(R1_label, RIGHT)

        R2_number = DecimalNumber(
            R2_value.get_value(),
            num_decimal_places=2,
            font_size=32
        ).next_to(R2_label, RIGHT)
        R2_unit = Tex(r'$\text{M}\Omega$', font_size=32).next_to(R2_number, RIGHT * 0.7)

        R2_number.add_updater(
            lambda mob: mob.set_value(R2_value.get_value())
        )

        ampliplot.add_updater(
            lambda mob: mob.become(
                ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(9, R2_value.get_value()))), color=VIR_3)).shift(
                2 * DOWN)
        )

        self.play(FadeIn(R1_label),
                  FadeIn(R1_number),
                  FadeIn(R2_number),
                  FadeIn(R2_label),
                  FadeIn(R2_unit))

        self.play(FadeIn(ampliplot))

        self.play(R2_value.animate.set_value(9))
        self.wait(2)
        self.play(R2_value.animate.set_value(0.1), rate_func=smooth)
        self.wait(2)
        self.play(R2_value.animate.set_value(1), rate_func=smooth)
        self.wait(2)


class Setup2(Scene):
    def construct(self):
        cir = ImageMobject("images/oscope_2.png").move_to(2 * UP + 3.5 * LEFT).scale(1).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in = Tex('$V_{in}$', font_size=30, color=VIR_1).move_to(UP * 2.35 + LEFT * 6.1)
        v_out = Tex('$V_{out}$', font_size=30, color=VIR_3).move_to(UP * 2.35 + LEFT * 0.85)

        c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP * 2.7 + LEFT * 4.2)
        # r1 = Tex('$R_1$', font_size=30, color=VIR_7).move_to(UP*2.7+LEFT*4.2)

        c2 = Tex('$C_2$', font_size=30, color=VIR_9).move_to(UP * 1.55 + LEFT * 3.3)
        # r2 = Tex('$R_2$', font_size=30, color=VIR_11).move_to(UP*1.55+LEFT*3.3)

        elements = VGroup(v_in, v_out, c1, c2)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        tf_z_0 = Tex(r'$V_{out} = V_{in} \frac{Z_2}{Z_1+Z_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        tf_z_0[0][0:4].set_fill(color=VIR_3)
        tf_z_0[0][5:8].set_fill(color=VIR_1)

        self.play(FadeIn(tf_z_0))
        self.wait(2)

        z1 = Tex(r'$Z_1 = \frac{1}{sC_1}\text{,}$', font_size=42).move_to(1.7 * UP + 2 * RIGHT)
        z1[0][6:8].set_fill(color=VIR_5)
        z2 = Tex(r'$Z_2 = \frac{1}{sC_2}$', font_size=42).move_to(1.7 * UP + 4 * RIGHT)
        z2[0][6:8].set_fill(color=VIR_9)

        self.play(FadeIn(z1),
                  FadeIn(z2))
        self.wait(2)

        tf_z_1 = Tex(r'$V_{out} = V_{in} \frac{\frac{1}{sC_2}}{\frac{1}{sC_1}+\frac{1}{sC_2}}$', font_size=42).move_to(
            0.8 * UP + 3 * RIGHT)
        tf_z_1[0][0:4].set_fill(color=VIR_3)
        tf_z_1[0][5:8].set_fill(color=VIR_1)
        tf_z_1[0][11:13].set_fill(color=VIR_9)
        tf_z_1[0][17:19].set_fill(color=VIR_5)
        tf_z_1[0][23:25].set_fill(color=VIR_9)

        self.play(FadeIn(tf_z_1))
        self.wait(2)

        tf_z = Tex(r'$V_{out} = V_{in} \frac{C_1}{C_1+C_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        tf_z[0][0:4].set_fill(color=VIR_3)
        tf_z[0][5:8].set_fill(color=VIR_1)
        tf_z[0][8:10].set_fill(color=VIR_5)
        tf_z[0][11:13].set_fill(color=VIR_5)
        tf_z[0][14:16].set_fill(color=VIR_9)

        self.play(ReplacementTransform(tf_z_0, tf_z),
                  FadeOut(z1),
                  FadeOut(z2),
                  FadeOut(tf_z_1))

        self.wait(2)

        ax = semilogx(
            x_range=[1e3, 1e9],  # powers of ten!
            x_length=12,
            y_range=[-80, 20, 20],
            y_length=3,
            background_line_style={'stroke_color': WHITE, 'stroke_width': 1}
        ).shift(2 * DOWN)

        R2_value = ValueTracker(12)

        def voltage_divider(R1, R2):
            return R1 / (R1 + R2)
            # return 1.0/(1.0 + 1j*2*PI*f*1600*100e-9)

        ampliplot = ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(1.33, R2_value.get_value())))).set_color(
            VIR_3).shift(2 * DOWN)

        tf_label = Tex(r'$\left|\frac{V_{out}}{V_{in}}\right|$', font_size=42).move_to(0.1 * UP + 6.4 * LEFT)
        tf_label[0][3:7].set_fill(color=VIR_3)
        tf_label[0][8:11].set_fill(color=VIR_1)

        self.play(FadeIn(ax),
                  FadeIn(tf_label))

        R1_label = Tex(r'$C_1=$', font_size=32).move_to(2.5 * RIGHT + 1.5 * UP)
        R2_label = Tex(r'$C_2=$', font_size=32).move_to(2.5 * RIGHT + 1 * UP)

        R1_label[0][0:2].set_fill(color=VIR_7)
        R2_label[0][0:2].set_fill(color=VIR_11)

        R1_number = Tex(r'$1.33\text{ pF}$', font_size=32).next_to(R1_label, RIGHT)

        R2_number = DecimalNumber(
            R2_value.get_value(),
            num_decimal_places=2,
            font_size=32
        ).next_to(R2_label, RIGHT)
        R2_unit = Tex(r'$\text{pF}$', font_size=32).next_to(R2_number, RIGHT * 1.2)

        R2_number.add_updater(
            lambda mob: mob.set_value(R2_value.get_value())
        )

        ampliplot.add_updater(
            lambda mob: mob.become(
                ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(1.33, R2_value.get_value()))), color=VIR_3)).shift(
                2 * DOWN)
        )

        self.play(FadeIn(R1_label),
                  FadeIn(R1_number),
                  FadeIn(R2_number),
                  FadeIn(R2_label),
                  FadeIn(R2_unit))

        self.play(FadeIn(ampliplot))

        self.play(R2_value.animate.set_value(99))
        self.wait(2)
        self.play(R2_value.animate.set_value(0.12), rate_func=smooth)
        self.wait(2)
        self.play(R2_value.animate.set_value(12), rate_func=smooth)
        self.wait(2)


class Setup3(Scene):
    def construct(self):
        cir = ImageMobject("images/oscope_3.png").move_to(2 * UP + 3.5 * LEFT).scale(1).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in = Tex('$V_{in}$', font_size=30, color=VIR_1).move_to(UP * 2.35 + LEFT * 6.1)
        v_out = Tex('$V_{out}$', font_size=30, color=VIR_3).move_to(UP * 2.35 + LEFT * 0.85)

        # c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP*3.6+LEFT*4.2)
        r1 = Tex('$R_1$', font_size=30, color=VIR_7).move_to(UP * 2.7 + LEFT * 4.2)

        c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP * 1.55 + LEFT * 2.4)
        r2 = Tex('$R_2$', font_size=30, color=VIR_11).move_to(UP * 1.55 + LEFT * 3.3)

        elements = VGroup(v_in, v_out, r1, r2, c1)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        tf_z_0 = Tex(r'$V_{out} = V_{in} \frac{Z_2}{Z_1+Z_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        tf_z_0[0][0:4].set_fill(color=VIR_3)
        tf_z_0[0][5:8].set_fill(color=VIR_1)

        self.play(FadeIn(tf_z_0))
        self.wait(2)

        z1 = Tex(r'$Z_1 = R_1\text{,}$', font_size=42).move_to(1.5 * UP + 1.75 * RIGHT)
        z1[0][3:5].set_fill(color=VIR_7)
        z2 = Tex(r'$Z_2 = R_2 || \frac{1}{sC_1}$', font_size=42).move_to(1.5 * UP + 4.25 * RIGHT)
        z2[0][3:5].set_fill(color=VIR_11)
        z2[0][10:12].set_fill(color=VIR_5)

        self.play(FadeIn(z1),
                  FadeIn(z2))
        self.wait(2)

        z2_1 = Tex(r'$Z_2 = \frac{\frac{R_2}{sC_1}}{R_2+\frac{1}{sC_1}}$', font_size=42).move_to(
            1.5 * UP + 4.25 * RIGHT)
        z2_1[0][3:5].set_fill(color=VIR_11)
        z2_1[0][7:9].set_fill(color=VIR_5)
        z2_1[0][10:12].set_fill(color=VIR_11)
        z2_1[0][16:18].set_fill(color=VIR_5)

        self.play(ReplacementTransform(z2, z2_1))
        self.wait(2)

        z2_2 = Tex(r'$Z_2 = \frac{R_2}{sC_1R_2+1}$', font_size=42).move_to(1.5 * UP + 4.25 * RIGHT)
        z2_2[0][3:5].set_fill(color=VIR_11)
        z2_2[0][7:9].set_fill(color=VIR_5)
        z2_2[0][9:11].set_fill(color=VIR_11)

        self.play(ReplacementTransform(z2_1, z2_2))

        tf_z_1 = Tex(r'$V_{out} = V_{in} \frac{\frac{R_2}{sC_1R_2+1}}{R_1 + \frac{R_2}{sC_1R_2+1}}$',
                     font_size=42).move_to(0.5 * UP + 3 * RIGHT)
        tf_z_1[0][0:4].set_fill(color=VIR_3)
        tf_z_1[0][5:8].set_fill(color=VIR_1)
        tf_z_1[0][8:10].set_fill(color=VIR_11)
        tf_z_1[0][12:14].set_fill(color=VIR_5)
        tf_z_1[0][14:16].set_fill(color=VIR_11)
        tf_z_1[0][19:21].set_fill(color=VIR_7)
        tf_z_1[0][22:24].set_fill(color=VIR_11)
        tf_z_1[0][26:28].set_fill(color=VIR_5)
        tf_z_1[0][28:30].set_fill(color=VIR_11)

        self.play(FadeIn(tf_z_1))
        self.wait(2)

        tf_z_2 = Tex(r'$V_{out} = V_{in} \frac{R_2}{sC_1R_1R_2 + R_1 + R_2}$', font_size=42).move_to(
            2.5 * UP + 3 * RIGHT)
        tf_z_2[0][0:4].set_fill(color=VIR_3)
        tf_z_2[0][5:8].set_fill(color=VIR_1)
        tf_z_2[0][8:10].set_fill(color=VIR_11)
        tf_z_2[0][12:14].set_fill(color=VIR_5)
        tf_z_2[0][14:16].set_fill(color=VIR_7)
        tf_z_2[0][16:18].set_fill(color=VIR_11)
        tf_z_2[0][19:21].set_fill(color=VIR_7)
        tf_z_2[0][22:24].set_fill(color=VIR_11)

        self.play(ReplacementTransform(tf_z_0, tf_z_2),
                  FadeOut(z1),
                  FadeOut(z2_2),
                  FadeOut(tf_z_1))
        self.wait(2)

        ax = semilogx(
            x_range=[1e3, 1e9],  # powers of ten!
            x_length=12,
            y_range=[-80, 20, 20],
            y_length=3,
            background_line_style={'stroke_color': WHITE, 'stroke_width': 1}
        ).shift(2 * DOWN)

        R2_value = ValueTracker(1)

        def voltage_divider(w, R1, R2, C1):
            R1 = R1 * 1E6
            R2 = R2 * 1E6
            C1 = C1 * 1E-12
            w = 2*math.pi * w
            return R2 / (R1 + R2 + w * C1 * R1 * R2)


            # return 1.0/(1.0 + 1j*2*PI*f*1600*100e-9)

        ampliplot = ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(x, 9, 1, R2_value.get_value())))).set_color(
            VIR_3).shift(2 * DOWN)

        tf_label = Tex(r'$\left|\frac{V_{out}}{V_{in}}\right|$', font_size=42).move_to(0.1 * UP + 6.4 * LEFT)
        tf_label[0][3:7].set_fill(color=VIR_3)
        tf_label[0][8:11].set_fill(color=VIR_1)

        self.play(FadeIn(ax),
                  FadeIn(tf_label))

        R1_label = Tex(r'$R_1=$', font_size=32).move_to(2.5 * RIGHT + 1.5 * UP)
        R2_label = Tex(r'$R_2=$', font_size=32).move_to(2.5 * RIGHT + 1 * UP)
        C1_label = Tex(r'$C_1=$', font_size=32).move_to(2.5 * RIGHT + 0.5 * UP)

        R1_label[0][0:2].set_fill(color=VIR_7)
        R2_label[0][0:2].set_fill(color=VIR_11)
        C1_label[0][0:2].set_fill(color=VIR_5)

        R1_number = Tex(r'$9.00\text{ M}\Omega$', font_size=32).next_to(R1_label, RIGHT)
        R2_real_number = Tex(r'$1.00\text{ M}\Omega$', font_size=32).next_to(R2_label, RIGHT)

        R2_number = DecimalNumber(
            R2_value.get_value(),
            num_decimal_places=2,
            font_size=32
        ).next_to(C1_label, RIGHT)
        R2_unit = Tex(r'$\text{pF}$', font_size=32).next_to(R2_number, RIGHT * 1.2)

        R2_number.add_updater(
            lambda mob: mob.set_value(R2_value.get_value())
        )

        ampliplot.add_updater(
            lambda mob: mob.become(
                ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(x, 9, 1, R2_value.get_value()))),
                        color=VIR_3)).shift(2 * DOWN)
        )

        self.play(FadeIn(R1_label),
                  FadeIn(R1_number),
                  FadeIn(R2_number),
                  FadeIn(R2_label),
                  FadeIn(R2_unit),
                  FadeIn(R2_real_number),
                  FadeIn(C1_label))

        self.play(FadeIn(ampliplot))
        self.wait(2)
        self.play(R2_value.animate.set_value(50))
        self.wait(2)
        self.play(R2_value.animate.set_value(0.1), rate_func=smooth)
        self.wait(2)
        self.play(R2_value.animate.set_value(12), rate_func=smooth)
        self.wait(2)
        # self.play(R2_value.animate.set_value(17.7), rate_func=smooth)
        # self.wait(2)

class Setup4(Scene):
    def construct(self):
        cir = ImageMobject("images/oscope_4.png").move_to(2 * UP + 3.5 * LEFT).scale(1).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in = Tex('$V_{in}$', font_size=30, color=VIR_1).move_to(UP * 2.35 + LEFT * 6.1)
        v_out = Tex('$V_{out}$', font_size=30, color=VIR_3).move_to(UP * 2.35 + LEFT * 0.85)

        c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP * 3.6 + LEFT * 4.2)
        r1 = Tex('$R_1$', font_size=30, color=VIR_7).move_to(UP * 2.7 + LEFT * 4.2)

        c2 = Tex('$C_2$', font_size=30, color=VIR_9).move_to(UP * 1.55 + LEFT * 2.4)
        r2 = Tex('$R_2$', font_size=30, color=VIR_11).move_to(UP * 1.55 + LEFT * 3.3)

        elements = VGroup(v_in, v_out, c1, r1, c2, r2)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        tf_z = Tex(r'$V_{out} = V_{in} \frac{Z_2}{Z_1+Z_2}$', font_size=42).move_to(2.5 * UP + 3 * RIGHT)
        tf_z[0][0:4].set_fill(color=VIR_3)
        tf_z[0][5:8].set_fill(color=VIR_1)

        self.play(FadeIn(tf_z))
        self.wait(2)

        z1 = Tex(r'$Z_1 = R_1 || \frac{1}{sC_1}\text{,}$', font_size=42).move_to(1.5 * UP + 1.6 * RIGHT)
        z1[0][3:5].set_fill(color=VIR_7)
        z1[0][10:12].set_fill(color=VIR_5)

        z2 = Tex(r'$Z_2 = R_2 || \frac{1}{sC_2}$', font_size=42).move_to(1.5 * UP + 4.4 * RIGHT)
        z2[0][3:5].set_fill(color=VIR_11)
        z2[0][10:12].set_fill(color=VIR_9)

        self.play(FadeIn(z1),
                  FadeIn(z2))
        self.wait(2)

        z1_1 = Tex(r'$Z_1 = \frac{R_1}{sC_1R_1+1}\text{,}$', font_size=42).move_to(1.5 * UP + 1.6 * RIGHT)
        z1_1[0][3:5].set_fill(color=VIR_7)
        z1_1[0][7:9].set_fill(color=VIR_5)
        z1_1[0][9:11].set_fill(color=VIR_7)

        z2_1 = Tex(r'$Z_2 = \frac{R_2}{sC_2R_2+1}$', font_size=42).move_to(1.5 * UP + 4.4 * RIGHT)
        z2_1[0][3:5].set_fill(color=VIR_11)
        z2_1[0][7:9].set_fill(color=VIR_9)
        z2_1[0][9:11].set_fill(color=VIR_11)

        self.play(ReplacementTransform(z1, z1_1),
                  ReplacementTransform(z2, z2_1))
        self.wait(2)

        tf_z_1 = Tex(r'$V_{out} = V_{in} \frac{\frac{R_2}{sC_2R_2+1}}{\frac{R_1}{sC_1R_1+1} + \frac{R_2}{sC_2R_2+1}}$',
                     font_size=42).move_to(0.5 * UP + 3 * RIGHT)
        tf_z_1[0][0:4].set_fill(color=VIR_3)
        tf_z_1[0][5:8].set_fill(color=VIR_1)
        tf_z_1[0][8:10].set_fill(color=VIR_11)
        tf_z_1[0][12:14].set_fill(color=VIR_9)
        tf_z_1[0][14:16].set_fill(color=VIR_11)
        tf_z_1[0][19:21].set_fill(color=VIR_7)
        tf_z_1[0][23:25].set_fill(color=VIR_5)
        tf_z_1[0][25:27].set_fill(color=VIR_7)
        tf_z_1[0][8 + 22:10 + 22].set_fill(color=VIR_11)
        tf_z_1[0][12 + 22:14 + 22].set_fill(color=VIR_9)
        tf_z_1[0][14 + 22:16 + 22].set_fill(color=VIR_11)
        # tf_z_1[0][19:21].set_fill(color=VIR_9)
        # tf_z_1[0][22:24].set_fill(color=VIR_11)
        # tf_z_1[0][26:28].set_fill(color=VIR_5)
        # tf_z_1[0][28:30].set_fill(color=VIR_11)

        self.play(FadeIn(tf_z_1))
        self.wait(2)

        tf_z_2 = Tex(r'$V_{out} = V_{in} \frac{\frac{R_2}{sC_2R_2+1}}{\frac{sC_2R_1R_2+R1+sC_1R_1R_2+R_2}{(sC_1R_1+1)(sC_2R_2+1)}}$',
                     font_size=42).move_to(0.5 * DOWN + 3 * RIGHT)

        VOUT = VIR_3
        VIN = VIR_1
        R2 = VIR_11
        C2 = VIR_9
        R1 = VIR_7
        C1 = VIR_5


        tf_z_2[0][0:4].set_fill(color=VOUT)
        tf_z_2[0][5:8].set_fill(color=VIN)
        tf_z_2[0][8:10].set_fill(color=R2)
        tf_z_2[0][12:14].set_fill(color=C2)
        tf_z_2[0][14:16].set_fill(color=R2)
        tf_z_2[0][20:22].set_fill(color=C2)
        tf_z_2[0][22:24].set_fill(color=R1)
        tf_z_2[0][24:26].set_fill(color=R2)

        tf_z_2[0][27:29].set_fill(color=R1)
        tf_z_2[0][31:33].set_fill(color=C1)
        tf_z_2[0][33:35].set_fill(color=R1)
        tf_z_2[0][35:37].set_fill(color=R2)
        tf_z_2[0][38:40].set_fill(color=R2)
        tf_z_2[0][43:45].set_fill(color=C1)
        tf_z_2[0][45:47].set_fill(color=R1)
        tf_z_2[0][52:54].set_fill(color=C2)
        tf_z_2[0][54:56].set_fill(color=R2)

        self.play(FadeIn(tf_z_2))
        self.wait(2)

        tf_z_3 = Tex(r'$V_{out} = V_{in} \frac{R_2}{sC_2R_2+1}\frac{(sC_1R_1+1)(sC_2R_2+1)}{sR_1R_2(C_1+C_2)+R_1+R_2}$',
                     font_size=42).move_to(1.5 * DOWN + 3 * RIGHT)


        tf_z_3[0][0:4].set_fill(color=VOUT)
        tf_z_3[0][5:8].set_fill(color=VIN)
        tf_z_3[0][8:10].set_fill(color=R2)
        tf_z_3[0][12:14].set_fill(color=C2)
        tf_z_3[0][14:16].set_fill(color=R2)
        tf_z_3[0][20:22].set_fill(color=C1)
        tf_z_3[0][22:24].set_fill(color=R1)
        tf_z_3[0][29:31].set_fill(color=C2)
        tf_z_3[0][31:33].set_fill(color=R2)
        tf_z_3[0][38:40].set_fill(color=R1)
        tf_z_3[0][40:42].set_fill(color=R2)
        tf_z_3[0][43:45].set_fill(color=C1)
        tf_z_3[0][46:48].set_fill(color=C2)
        tf_z_3[0][50:52].set_fill(color=R1)
        tf_z_3[0][53:55].set_fill(color=R2)

        self.play(FadeIn(tf_z_3))
        self.wait(2)

        self.play(Indicate(tf_z_3[0][27:36]))
        self.play(Indicate(tf_z_3[0][11:18]))
        self.wait(2)


        tf_z_4 = Tex(r'$V_{out} = V_{in} \frac{R_2}{1}\frac{sC_1R_1+1}{sR_1R_2(C_1+C_2)+R_1+R_2}$',
                     font_size=42).move_to(1.5 * DOWN + 3 * RIGHT)

        tf_z_4[0][0:4].set_fill(color=VOUT)
        tf_z_4[0][5:8].set_fill(color=VIN)
        tf_z_4[0][8:10].set_fill(color=R2)
        tf_z_4[0][13:15].set_fill(color=C1)
        tf_z_4[0][15:17].set_fill(color=R1)
        tf_z_4[0][21:23].set_fill(color=R1)
        tf_z_4[0][23:25].set_fill(color=R2)
        tf_z_4[0][26:28].set_fill(color=C1)
        tf_z_4[0][29:31].set_fill(color=C2)
        tf_z_4[0][33:35].set_fill(color=R1)
        tf_z_4[0][36:38].set_fill(color=R2)

        self.play(ReplacementTransform(tf_z_3, tf_z_4))
        self.wait(2)

        tf_z_5 = Tex(r'$V_{out} = V_{in} \frac{sC_1R_1R_2+R_2}{sR_1R_2(C_1+C_2)+R_1+R_2}$',
                     font_size=42).move_to(1.5 * DOWN + 3 * RIGHT)

        tf_z_5[0][0:4].set_fill(color=VOUT)
        tf_z_5[0][5:8].set_fill(color=VIN)
        tf_z_5[0][9:11].set_fill(color=C1)
        tf_z_5[0][11:13].set_fill(color=R1)
        tf_z_5[0][13:15].set_fill(color=R2)
        tf_z_5[0][16:18].set_fill(color=R2)
        tf_z_5[0][20:22].set_fill(color=R1)
        tf_z_5[0][22:24].set_fill(color=R2)
        tf_z_5[0][25:27].set_fill(color=C1)
        tf_z_5[0][28:30].set_fill(color=C2)
        tf_z_5[0][32:34].set_fill(color=R1)
        tf_z_5[0][35:37].set_fill(color=R2)

        self.play(ReplacementTransform(tf_z_4, tf_z_5))

        self.wait(2)
        self.play(tf_z_5.animate.shift(4*UP),
                  FadeOut(tf_z),
                  FadeOut(z1_1),
                  FadeOut(z2_1),
                  FadeOut(tf_z_1),
                  FadeOut(tf_z_2))
        self.wait(2)


        s0 = Tex(r"$s = 0$").move_to(1.5 * UP + 3 * RIGHT)

        s0_eqn = Tex(r"$ \frac{V_{out}}{V_{in}} = \frac{R_2}{R_1+R_2} $").move_to(0.5 * UP + 3 * RIGHT)

        s0_eqn[0][0:4].set_fill(color=VOUT)
        s0_eqn[0][5:8].set_fill(color=VIN)
        s0_eqn[0][9:11].set_fill(color=R2)
        s0_eqn[0][12:14].set_fill(color=R1)
        s0_eqn[0][15:17].set_fill(color=R2)

        self.play(FadeIn(s0))
        self.wait(2)
        self.play(FadeIn(s0_eqn))
        self.wait(2)

        self.play(FadeOut(s0),
                  FadeOut(s0_eqn))

        sinf = Tex(r"$\lim\limits_{s\to\infty}$").move_to(1.5 * UP + 3 * RIGHT)
        sinf_eqn = Tex(r"$\frac{V_{out}}{V_{in}} = \frac{C_1}{C_1+C_2}$").move_to(0.5 * UP + 3 * RIGHT)

        sinf_eqn[0][0:4].set_fill(color=VOUT)
        sinf_eqn[0][5:8].set_fill(color=VIN)
        sinf_eqn[0][9:11].set_fill(color=C1)
        sinf_eqn[0][12:14].set_fill(color=C1)
        sinf_eqn[0][15:17].set_fill(color=C2)

        self.play(FadeIn(sinf))
        self.wait(2)
        self.play(FadeIn(sinf_eqn))
        self.wait(2)
        self.play(FadeOut(sinf),
                  FadeOut(sinf_eqn))
        self.wait(2)

        ####################




        #
        # # Observe second level labels
        # tex__ = tf_z_5.copy().next_to(tf_z_5, DOWN)
        # for part in tex__:
        #     self.add(index_labels(part, color=YELLOW))
        #
        # self.add(tf_z_5, tex__)

        ax = semilogx(
            x_range=[1e3, 1e9],  # powers of ten!
            x_length=12,
            y_range=[-80, 20, 20],
            y_length=3,
            background_line_style={'stroke_color': WHITE, 'stroke_width': 1}
        ).shift(2 * DOWN)

        R2_value = ValueTracker(1.33)

        def voltage_divider(w, R1, R2, C1, C2):
            R1 = R1 * 1E6
            R2 = R2 * 1E6
            C1 = C1 * 1E-12
            C2 = C2 * 1E-12
            w = 2*math.pi * w

            return (w*C1*R1*R2 + R2) / (w*R1*R2*(C1+C2) + R1 + R2)

            # return 1.0/(1.0 + 1j*2*PI*f*1600*100e-9)

        ampliplot = ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(x, 9, 1, R2_value.get_value(), 12)))).set_color(
            VIR_3).shift(2 * DOWN)

        tf_label = Tex(r'$\left|\frac{V_{out}}{V_{in}}\right|$', font_size=42).move_to(0.1 * UP + 6.4 * LEFT)
        tf_label[0][3:7].set_fill(color=VIR_3)
        tf_label[0][8:11].set_fill(color=VIR_1)

        self.play(FadeIn(ax),
                  FadeIn(tf_label))

        R1_label = Tex(r'$R_1=$', font_size=32).move_to(2.5 * RIGHT + 1.5 * UP)
        R2_label = Tex(r'$R_2=$', font_size=32).move_to(2.5 * RIGHT + 1 * UP)
        C1_label = Tex(r'$C_1=$', font_size=32).move_to(2.5 * RIGHT + 0.5 * UP)
        C2_label = Tex(r'$C_2=$', font_size=32).move_to(2.5 * RIGHT + 0.0 * UP)


        R1_label[0][0:2].set_fill(color=VIR_7)
        R2_label[0][0:2].set_fill(color=VIR_11)
        C1_label[0][0:2].set_fill(color=VIR_5)
        C2_label[0][0:2].set_fill(color=C2)

        R1_number = Tex(r'$9.00\text{ M}\Omega$', font_size=32).next_to(R1_label, RIGHT)
        R2_real_number = Tex(r'$1.00\text{ M}\Omega$', font_size=32).next_to(R2_label, RIGHT)
        C2_number = Tex(r'12.00$\text{pF}$', font_size=32).next_to(C2_label, RIGHT * 1.2)

        R2_number = DecimalNumber(
            R2_value.get_value(),
            num_decimal_places=2,
            font_size=32
        ).next_to(C1_label, RIGHT)
        R2_unit = Tex(r'$\text{pF}$', font_size=32).next_to(R2_number, RIGHT * 1.2)

        R2_number.add_updater(
            lambda mob: mob.set_value(R2_value.get_value())
        )

        ampliplot.add_updater(
            lambda mob: mob.become(
                ax.plot(lambda x: 20 * np.log10(np.abs(voltage_divider(x, 9, 1, R2_value.get_value(), 12))),
                        color=VIR_3)).shift(2 * DOWN)
        )

        self.play(FadeIn(R1_label),
                  FadeIn(R1_number),
                  FadeIn(R2_number),
                  FadeIn(R2_label),
                  FadeIn(R2_unit),
                  FadeIn(R2_real_number),
                  FadeIn(C1_label),
                  FadeIn(C2_label),
                  FadeIn(C2_number))

        self.play(FadeIn(ampliplot))

        self.wait(2)
        self.play(R2_value.animate.set_value(99))
        self.wait(2)
        self.play(R2_value.animate.set_value(0.12), rate_func=smooth)
        self.wait(2)
        self.play(R2_value.animate.set_value(1.33), rate_func=smooth)
        self.wait(2)



class Setup5(Scene):
    def construct(self):
        cir = ImageMobject("images/oscope_4.png").move_to(2 * UP + 3.5 * LEFT).scale(1).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in = Tex('$V_{in}$', font_size=30, color=VIR_1).move_to(UP * 2.35 + LEFT * 6.1)
        v_out = Tex('$V_{out}$', font_size=30, color=VIR_3).move_to(UP * 2.35 + LEFT * 0.85)

        c1 = Tex('$C_1$', font_size=30, color=VIR_5).move_to(UP * 3.6 + LEFT * 4.2)
        r1 = Tex('$R_1$', font_size=30, color=VIR_7).move_to(UP * 2.7 + LEFT * 4.2)

        c2 = Tex('$C_2$', font_size=30, color=VIR_9).move_to(UP * 1.55 + LEFT * 2.4)
        r2 = Tex('$R_2$', font_size=30, color=VIR_11).move_to(UP * 1.55 + LEFT * 3.3)

        elements = VGroup(v_in, v_out, c1, r1, c2, r2)

        self.play(AnimationGroup(*[FadeIn(element) for element in elements], lag_ratio=0.2))
        self.wait(2)

        R1 = Tex(r'$R_1 = 9.00\text{ M}\Omega$', font_size=24).move_to(5*LEFT+1.5*UP)
        R2 = Tex(r'$R_2 = 1.00\text{ M}\Omega$', font_size=24).next_to(R1, DOWN)
        C1 = Tex(r'$C_1 = 1-4\text{pF}$', font_size=24).next_to(R2, DOWN)
        C2 = Tex(r'$C_2 = 12.00\text{pF}$', font_size=24).next_to(C1, DOWN)

        # R2 = VIR_11
        # C2 = VIR_9
        # R1 = VIR_7
        # C1 = VIR_5

        R1[0][0:2].set_fill(VIR_7)
        R2[0][0:2].set_fill(VIR_11)
        C1[0][0:2].set_fill(VIR_5)
        C2[0][0:2].set_fill(VIR_9)

        self.play(FadeIn(R1),
                  FadeIn(R2),
                  FadeIn(C1),
                  FadeIn(C2))
        self.wait(2)
