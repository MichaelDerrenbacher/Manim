import math
from typing import Callable

from manim import *
from colour import Color
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.scene.scene import Scene
from manim.utils.rate_functions import smooth
from pyglet.libs.x11.xinput import LedFeedbackClass
from pyglet.resource import animation
from typing import TYPE_CHECKING, Any, Callable, Iterable, Sequence
from manim_code_blocks import *

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
        l1 = Line(start=LEFT*2.5+UP*2.0, end=LEFT*0.5+UP*2.0, stroke_width=6, stroke_color=WHITE)
        l2 = Line(start=RIGHT*3.0+UP*2, end=RIGHT*5.25+UP*2, stroke_width=6, stroke_color=WHITE)

        r1 = Rectangle(width=3.5, height=3.5, stroke_width=4, stroke_color=VIR_4).move_to(LEFT*4.25+UP*2)
        t1 = Text(r"DAC", font_size=36).move_to(LEFT*4.25+UP*2.25)
        t2 = Text(r"Digital to Analog", font_size=24).move_to(LEFT*4.25+UP*1.75)
        t3 = Text(r"Converter", font_size=24).move_to(LEFT*4.25+UP*1.5)


        r2 = Rectangle(width=3.5, height=3.5, stroke_width=4, stroke_color=VIR_8).move_to(RIGHT*1.25+UP*2)
        t4 = Text(r"Signal", font_size=36).move_to(RIGHT*1.25+UP*2.25)
        t5 = Text(r"Conditioning", font_size=36).move_to(RIGHT*1.25+UP*1.75)


        elements = VGroup(r1, l1, t1, t2, t3)

        self.play(AnimationGroup(*[DrawBorderThenFill(element) for element in elements], lag_ratio=0.3))

        self.wait(2)

        v1 = Tex(r"$V_{dac}$", font_size=36, color=VIR_1).move_to(LEFT*1.5+UP*2.65)
        v2 = Tex(r"$V_{out}$", font_size=36, color=VIR_3).move_to(RIGHT*(3.875+0.25)+UP*2.65)
        tv1 = Text(r"0V — 5V", font_size=24).move_to(LEFT*1.5+UP*2.25)
        tv2 = Text(r"-10V — 10V", font_size=24).move_to(RIGHT*(3.875+0.25)+UP*2.25)

        self.play(DrawBorderThenFill(tv1),
                  DrawBorderThenFill(v1))
        self.wait(2)

        self.play(DrawBorderThenFill(l2),
                  DrawBorderThenFill(tv2),
                  DrawBorderThenFill(v2))
        self.wait(2)

        elements2 = VGroup(r2, t4, t5)

        self.play(AnimationGroup(*[DrawBorderThenFill(element) for element in elements2], lag_ratio=0.3))

        self.wait(2)

        ta1 = Text(r"0V — 5V", font_size=24).move_to(LEFT*2+DOWN*1)
        ta2 = Text(r"-10V — 10V", font_size=24).move_to(RIGHT*2+DOWN*1)
        to1 = Text(r"offset = 2.5V", font_size=24).move_to(LEFT*2+DOWN*1.5)
        to2 = Text(r"offset = 0.0V", font_size=24).move_to(RIGHT*2+DOWN*1.5)
        tr1 = Text(r"range = 5.0V", font_size=24).move_to(LEFT*2+DOWN*2)
        tr2 = Text(r"range = 20.0V", font_size=24).move_to(RIGHT*2+DOWN*2)

        v11 = Tex(r"$V_{dac}$", font_size=36, color=VIR_1).move_to(LEFT*2+DOWN * 0.5)
        v22 = Tex(r"$V_{out}$", font_size=36, color=VIR_3).move_to(RIGHT*2+DOWN * 0.5)

        self.play(FadeIn(v11),
                  FadeIn(v22),
                  FadeIn(ta1),
                  FadeIn(ta2))

        f1 = Tex(r"$f(V_{dac}) = V_{out}$", font_size=48, color=WHITE).move_to(DOWN*2)
        f1[0][2:6].set_fill(color=VIR_1)
        f1[0][8:13].set_fill(color=VIR_3)

        f2 = Tex(r"$f(0V) = -10V$", font_size=48, color=WHITE).move_to(DOWN*2)
        f2[0][2:4].set_fill(color=VIR_1)
        f2[0][6:10].set_fill(color=VIR_3)

        f3 = Tex(r"$f(5V) = +10V$", font_size=48, color=WHITE).move_to(DOWN*2)
        f3[0][2:4].set_fill(color=VIR_1)
        f3[0][6:10].set_fill(color=VIR_3)

        f4 = Tex(r"$f(V_{dac}) =\text{ }?$", font_size=48, color=WHITE).move_to(DOWN*2)
        f4[0][2:6].set_fill(color=VIR_1)

        self.play(FadeIn(f1))
        self.wait(2)
        self.play(ReplacementTransform(f1, f2))
        self.wait(2)
        self.play(ReplacementTransform(f2, f3))
        self.wait(2)
        self.play(ReplacementTransform(f3, f4))
        self.wait(2)
        self.play(f4.animate.move_to(DOWN*3.125))


        self.play(FadeIn(to1),
                  FadeIn(to2))
        self.wait(2)
        self.play(FadeIn(tr1),
                  FadeIn(tr2))
        self.wait(2)


        f5 = Tex(r"$V_{dac} = 0V \text{ — } 5V$", font_size=48, color=WHITE).move_to(DOWN*3.125)
        f5[0][0:4].set_fill(color=VIR_1)

        f6 = Tex(r"$V_{dac} - 2.5V = -2.5V \text{ — } 2.5V$", font_size=48, color=WHITE).move_to(DOWN*3.125)
        f6[0][0:4].set_fill(color=VIR_1)

        f7 = Tex(r"$4 \cdot (V_{dac} - 2.5V) = -10.0V \text{ — } 10.0V$", font_size=48, color=WHITE).move_to(DOWN*3.125)
        # f7 = Tex(r"$4 \cdot (V_{out1} - 2.5V) = -10.0V \text{ — } 10.0V = V_{out2}$", font_size=48, color=WHITE).move_to(DOWN*3.25)
        f7[0][3:7].set_fill(color=VIR_1)
        # f7[0][28:33].set_fill(color=VIR_3)

        f8 = Tex(r"$V_{out} = 4 \cdot (V_{dac} - 2.5V) $", font_size=28, color=WHITE).move_to(RIGHT*1.25+UP*1)
        f8[0][0:4].set_fill(color=VIR_3)
        f8[0][8:12].set_fill(color=VIR_1)

        self.play(ReplacementTransform(f4, f5))
        self.wait(2)
        self.play(ReplacementTransform(f5, f6))
        self.wait(2)
        self.play(ReplacementTransform(f6, f7))
        self.wait(2)

        self.play(Indicate(f7[0][8:12], scale_factor=1.1, color=VIR_6))
        self.wait(1)
        self.play(Indicate(f7[0][0:1], scale_factor=1.1, color=VIR_6))

        self.wait(2)

        # offset = Text(r"-2.5V", font_size=24).move_to(LEFT*2+DOWN*1.5)

        self.play(FadeOut(v11),
                  FadeOut(v22),
                  FadeOut(ta1),
                  FadeOut(ta2),
                  FadeOut(to1),
                  FadeOut(to2),
                  FadeOut(tr1),
                  FadeOut(tr2),
                  ReplacementTransform(f7, f8))
        self.wait(2)



class Setup2(Scene):
    def construct(self):
        VDAC = VIR_1
        VOUT1 = VIR_3
        VREF = VIR_5
        V1 = VIR_7

        R1 = VIR_9
        R2 = VIR_10
        R3 = VIR_11
        R4 = VIR_12

        R5 = VIR_14
        R6 = VIR_15

        VP = VIR_14
        VM = VIR_15

        cir_half = ImageMobject("afe_half.png").move_to(1 * UP + 3.0 * LEFT).scale(1.05).set_z_index(-2)
        cir_full = ImageMobject("afe_full.png").move_to(1 * UP + 3.0 * LEFT).scale(1.05).set_z_index(-1)

        self.add(cir_half, cir_full)
        self.wait(2)

        vdac = Tex(r"$V_{dac}$", font_size=36, color=VDAC).move_to(LEFT * 6.05 + UP * 1.8)
        vref = Tex(r"$V_{ref}$", font_size=36, color=VREF).move_to(LEFT*5.35+UP*0.15)
        vout1 = Tex(r"$V_{out}$", font_size=36, color=VOUT1).move_to(RIGHT*1.4+UP*1.5)
        v1 = Tex(r"$V_{1}$", font_size=36, color=V1).move_to(LEFT*2.25+UP*1.6)

        r1 = Tex(r"$R_1$", font_size=36, color=R1).move_to(LEFT*5+UP*2.75)
        r2 = Tex(r"$R_2$", font_size=36, color=R2).move_to(LEFT*5+UP*0.4)
        r3 = Tex(r"$R_3$", font_size=36, color=R3).move_to(LEFT*3.5+UP*2.75)
        r4 = Tex(r"$R_4$", font_size=36, color=R4).move_to(LEFT*3.5+UP*0.4)
        r5 = Tex(r"$R_5$", font_size=36, color=R5).move_to(RIGHT*0.75+UP*1)
        r6 = Tex(r"$R_6$", font_size=36, color=R6).move_to(RIGHT*0.75+UP*0)

        elements = VGroup(vdac, vref, vout1, r1, r2, r3, r4, r5, r6)

        self.play(AnimationGroup(*[Write(element) for element in elements], lag_ratio=0.15))
        self.wait(2)


        self.play(FadeOut(cir_full),
                  FadeOut(r5),
                  FadeOut(r6),
                  FadeOut(vout1),
                  FadeIn(v1))
        self.wait(2)

        vp = Tex(r"$V_p$", font_size=36, color=VP).move_to(LEFT*4.25+UP*2.75)
        vm = Tex(r"$V_m$", font_size=36, color=VM).move_to(LEFT*4.25+UP*0.4)

        self.play(FadeIn(vp),
                  FadeIn(vm))


        e1 = Tex(r"$V_p = V_m$", font_size=40, color=WHITE).move_to(RIGHT*0+UP*2.75)
        e1[0][0:2].set_fill(color=VP)
        e1[0][3:5].set_fill(color=VM)

        e2 = Tex(r"$i_{R_1} = i_{R_3}$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*2.75)
        e2[0][1:3].set_fill(color=R1)
        e2[0][5:7].set_fill(color=R3)

        e3 = Tex(r"$i_{R_2} = i_{R_4}$", font_size=40, color=WHITE).move_to(RIGHT*5+UP*2.75)
        e3[0][1:3].set_fill(color=R2)
        e3[0][5:7].set_fill(color=R4)

        elements1 = VGroup(e1, e2, e3)

        self.play(AnimationGroup(*[Write(element) for element in elements1], lag_ratio=0.2))
        self.wait(2)


        e4 = Tex(r"$V_p = V_{dac} \frac{R_3}{R_1 + R_3}$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*1.5)
        e4[0][0:2].set_fill(color=VP)
        e4[0][3:7].set_fill(color=VDAC)
        e4[0][7:9].set_fill(color=R3)
        e4[0][10:12].set_fill(color=R1)
        e4[0][13:15].set_fill(color=R3)
        self.play(FadeIn(e4))
        self.wait(2)

        e5 = Tex(r"$i_{R_2} = \frac{V_{ref} - V_m}{R_2}$", font_size=40, color=WHITE).move_to(RIGHT*0.5+UP*0.5)
        e5[0][1:3].set_fill(color=R2)
        e5[0][4:8].set_fill(color=VREF)
        e5[0][9:11].set_fill(color=VM)
        e5[0][12:14].set_fill(color=R2)

        e6 = Tex(r"$i_{R_4} = \frac{V_m - V_1}{R_4}$", font_size=40, color=WHITE).move_to(RIGHT*4.5+UP*0.5)
        e6[0][1:3].set_fill(color=R4)
        e6[0][4:6].set_fill(color=VM)
        e6[0][7:9].set_fill(color=V1)
        e6[0][10:12].set_fill(color=R4)

        e7 = Tex(r"$=$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*0.5)

        self.play(FadeIn(e5))
        self.wait(2)
        self.play(FadeIn(e6))
        self.wait(2)
        self.play(FadeIn(e7))
        self.wait(2)

        elements2 = VGroup(e5, e6, e7)

        # e8 = Tex(r"$R_4(V_{ref} - V_m) = R_2(V_m - V_1)$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*0.5)
        # e8[0][0:2].set_fill(color=R4)
        # e8[0][3:7].set_fill(color=VREF)
        # e8[0][8:10].set_fill(color=VM)
        # e8[0][12:14].set_fill(color=R2)
        # e8[0][15:17].set_fill(color=VM)
        # e8[0][18:20].set_fill(color=V1)
        #
        # self.play(ReplacementTransform(elements2, e8))
        # self.wait(2)

        e9 = Tex(r"$\frac{R_4}{R_2}(V_{ref} - V_m) = V_m - V_1$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*0.5)
        e9[0][0:2].set_fill(color=R4)
        e9[0][3:5].set_fill(color=R2)
        e9[0][6:10].set_fill(color=VREF)
        e9[0][11:13].set_fill(color=VM)
        e9[0][15:17].set_fill(color=VM)
        e9[0][18:20].set_fill(color=V1)

        self.play(ReplacementTransform(elements2, e9))
        self.wait(2)

        ea = Tex(r"$\frac{R_4}{R_2}V_{ref} - \left(1 + \frac{R_4}{R_2}\right)V_m = - V_1$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*0.5)
        ea[0][0:2].set_fill(color=R4)
        ea[0][3:5].set_fill(color=R2)
        ea[0][5:9].set_fill(color=VREF)
        ea[0][13:15].set_fill(color=R4)
        ea[0][16:18].set_fill(color=R2)
        ea[0][19:21].set_fill(color=VM)
        ea[0][23:25].set_fill(color=V1)

        self.play(ReplacementTransform(e9, ea))
        self.wait(2)

        eb = Tex(r"$V_1 = V_{dac}\left( \frac{R_2+R_4}{R_2} \frac{R_3}{R_1+R_3} \right) - V_{ref} \left( \frac{R_4}{R_2} \right)$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*0.5)
        eb[0][0:2].set_fill(color=V1)
        eb[0][3:7].set_fill(color=VDAC)
        eb[0][8:10].set_fill(color=R2)
        eb[0][11:13].set_fill(color=R4)
        eb[0][14:16].set_fill(color=R2)
        eb[0][16:18].set_fill(color=R3)
        eb[0][19:21].set_fill(color=R1)
        eb[0][22:24].set_fill(color=R3)
        eb[0][26:30].set_fill(color=VREF)
        eb[0][31:33].set_fill(color=R4)
        eb[0][34:36].set_fill(color=R2)

        self.play(ReplacementTransform(ea, eb))
        self.wait(2)

        ec = Tex(r"$\text{if }R_1=R_2=R_3=R_4$", font_size=40, color=WHITE).move_to(RIGHT*2.5+DOWN*.75)
        ec[0][2:4].set_fill(color=R1)
        ec[0][5:7].set_fill(color=R2)
        ec[0][8:10].set_fill(color=R3)
        ec[0][11:13].set_fill(color=R4)
        self.play(FadeIn(ec))
        self.wait(2)

        ed = Tex(r"$V_1 = V_{dac} - V_{ref}$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*-1.75)
        ed[0][0:2].set_fill(color=V1)
        ed[0][3:7].set_fill(color=VDAC)
        ed[0][8:12].set_fill(color=VREF)

        self.play(FadeIn(ed))
        self.wait(2)

        ee = Tex(r"$V_{out} = 4 \cdot (V_{dac} - 2.5V) $", font_size=40, color=WHITE).move_to(LEFT*3.25+UP*-1.75)
        ee[0][0:4].set_fill(color=VOUT1)
        ee[0][8:12].set_fill(color=VDAC)
        ee[0][13:17].set_fill(color=VREF)

        self.play(FadeIn(ee))
        self.wait(2)

        self.play(Indicate(ed[0][8:12], scale_factor=1.1, color=WHITE),
                  Indicate(ee[0][13:17], scale_factor=1.1, color=WHITE))
        self.wait(2)
        vref2 = Tex(r"$2.5V$", font_size=36, color=VREF).move_to(LEFT*5.35+UP*0.15)

        ef = Tex(r"$V_1 = V_{dac} - 2.5V$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*-1.75)
        ef[0][0:2].set_fill(color=V1)
        ef[0][3:7].set_fill(color=VDAC)
        ef[0][8:12].set_fill(color=VREF)
        self.play(ReplacementTransform(ed, ef),
                  ReplacementTransform(vref, vref2))
        self.wait(2)

        self.play(Indicate(ee[0][5:6], scale_factor=1.25, color=WHITE))
        self.wait(2)



class Setup3(Scene):
    def construct(self):
        VDAC = VIR_1
        VOUT1 = VIR_3
        VREF = VIR_5
        V1 = VIR_7

        R = VIR_10

        R5 = VIR_14
        R6 = VIR_15

        VP = VIR_14
        VM = VIR_15

        cir_half = ImageMobject("afe_half.png").move_to(1 * UP + 3.0 * LEFT).scale(1.05).set_z_index(-2)
        cir_full = ImageMobject("afe_full.png").move_to(1 * UP + 3.0 * LEFT).scale(1.05).set_z_index(-1)

        self.add(cir_full)
        self.wait(2)


        vdac = Tex(r"$V_{dac}$", font_size=36, color=VDAC).move_to(LEFT * 6.05 + UP * 1.8)
        vref = Tex(r"$2.5V$", font_size=36, color=VREF).move_to(LEFT*5.35+UP*0.15)
        vout1 = Tex(r"$V_{out}$", font_size=36, color=VOUT1).move_to(RIGHT*1.4+UP*1.5)
        v1 = Tex(r"$V_{1}$", font_size=36, color=V1).move_to(LEFT*1.75+UP*1.8)

        r1 = Tex(r"$R$", font_size=36, color=R).move_to(LEFT*5+UP*2.75)
        r2 = Tex(r"$R$", font_size=36, color=R).move_to(LEFT*5+UP*0.4)
        r3 = Tex(r"$R$", font_size=36, color=R).move_to(LEFT*3.5+UP*2.75)
        r4 = Tex(r"$R$", font_size=36, color=R).move_to(LEFT*3.5+UP*0.4)
        r5 = Tex(r"$R_5$", font_size=36, color=R5).move_to(RIGHT*0.75+UP*1)
        r6 = Tex(r"$R_6$", font_size=36, color=R6).move_to(RIGHT*0.75+UP*0)

        elements = VGroup(vdac, vref, vout1, r1, r2, r3, r4, r5, r6, v1)

        self.play(AnimationGroup(*[Write(element) for element in elements], lag_ratio=0.0))




        ee = Tex(r"$V_{out} = 4 \cdot (V_{dac} - 2.5V) $", font_size=40, color=WHITE).move_to(LEFT*3.25+UP*-1.75)
        ee[0][0:4].set_fill(color=VOUT1)
        ee[0][8:12].set_fill(color=VDAC)
        ee[0][13:17].set_fill(color=VREF)
        self.play(FadeIn(ee))
        self.wait(2)

        ef = Tex(r"$V_1 = V_{dac} - 2.5V$", font_size=40, color=WHITE).move_to(RIGHT*2.5+UP*-1.75)
        ef[0][0:2].set_fill(color=V1)
        ef[0][3:7].set_fill(color=VDAC)
        ef[0][8:12].set_fill(color=VREF)
        self.play(FadeIn(ef))
        self.wait(2)

        rect = Rectangle(height=3.5, width=4, color=VIR_1).move_to(0.75*UP)
        self.play(FadeIn(rect))
        self.wait(2)
        self.play(FadeOut(rect))
        self.wait(2)


        e1 = Tex(r"$V_{out} = V_1 \left(1 + \frac{R_5}{R_6} \right)$", font_size=40, color=WHITE).move_to(RIGHT*4.5+UP*1.5)
        e1[0][0:4].set_fill(color=VOUT1)
        e1[0][5:7].set_fill(color=V1)
        e1[0][10:12].set_fill(color=R5)
        e1[0][13:15].set_fill(color=R6)
        self.play(FadeIn(e1))
        self.wait(2)

        e2 = Tex(r"$\text{if }R_5 = 3R_6$", font_size=40, color=WHITE).move_to(RIGHT*4.5+UP*0.75)
        e2[0][2:4].set_fill(color=R5)
        e2[0][6:8].set_fill(color=R6)
        self.play(FadeIn(e2))
        self.wait(2)

        r5_2 = Tex(r"$3R_6$", font_size=36, color=R6).move_to(RIGHT*0.75+UP*1)
        r5_2[0][0:1].set_fill(color=WHITE)

        e3 = Tex(r"$V_{out} = 4 V_1$", font_size=40, color=WHITE).move_to(RIGHT*4.5+UP*0)
        e3[0][0:4].set_fill(color=VOUT1)
        e3[0][6:8].set_fill(color=V1)
        self.play(FadeIn(e3),
                  ReplacementTransform(r5, r5_2))
        self.wait(2)

        e4 = Tex(r"$V_{out} = 4 \cdot (V_{dac} - 2.5V)$", font_size=40, color=WHITE).move_to(RIGHT * 2.5 + UP * -1.75)
        e4[0][0:4].set_fill(color=VOUT1)
        e4[0][8:12].set_fill(color=VDAC)
        e4[0][13:17].set_fill(color=VREF)
        self.play(ReplacementTransform(ef, e4),
                  FadeOut(v1))
        self.wait(2)

        self.play(FadeOut(ee),
                  FadeOut(e1),
                  FadeOut(e2),
                  FadeOut(e3),
                  e4.animate.move_to(RIGHT*4.5+UP*1.5))
        self.wait(2)


        axes = NumberPlane(
            x_range=[-0.001, 5.001, 1],  # x_min, x_max, x_step
            y_range=[-10.01, 10.01, 5],  # y_min, y_max, y_step
            x_length=12,
            y_length=2.5,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0,1,2,3,4,5],
                           "label_direction": LEFT * 0.0 + DOWN*0.4},
            y_axis_config={"numbers_to_include": [-10, 0, 10],
                           "label_direction": LEFT * 0.6 + DOWN*0.0},
            background_line_style={"stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3},  # Adjust grid line opacity
        ).scale(1).move_to(2*DOWN)


        def func(x):
            return 4*(x - 2.5)

        graph = axes.plot(func, color=VOUT1)

        elements2 = VGroup(vdac, vref, vout1, r1, r2, r3, r4, r5_2, r6, e4)


        l1 = Tex(r"$V_{out} \text{ vs } V_{dac}$", font_size=40, color=WHITE).move_to(RIGHT * 0 + DOWN * 0.4)
        l1[0][0:4].set_fill(color=VOUT1)
        l1[0][6:10].set_fill(color=VDAC)

        l2 = Tex(r"$V_{out}$", font_size=40, color=VOUT1).move_to(LEFT * 5.9 + DOWN * 0.4)
        l3 = Tex(r"$V_{dac}$", font_size=40, color=VDAC).move_to(RIGHT * 6.75 + DOWN * 2)


        self.play(FadeIn(axes),
                  FadeIn(graph),
                  FadeIn(l1),
                  FadeIn(l2),
                  FadeIn(l3),
                  cir_full.animate.shift(1*UP),
                  AnimationGroup(*[(element.animate.shift(1*UP)) for element in elements2], lag_ratio=0.0))

        self.wait(2)

class Setup4_2(Scene):
    def construct(self):
        VDAC = VIR_1
        VOUT1 = VIR_3
        VREF = VIR_5
        V1 = VIR_7

        R = VIR_10

        R5 = VIR_14
        R6 = VIR_15

        VP = VIR_14
        VM = VIR_15

        cir = ImageMobject("ina_2.png").move_to(1 * DOWN + 2 * LEFT).scale(1.0).set_z_index(-2)
        t1 = Text("Source: INA145 Datasheet", font_size=24).move_to(3.5 * DOWN + 4.5 * LEFT)

        rg1 = Tex(r"$R_{G1} = 13.3k\Omega$", font_size=36, color=WHITE).move_to(RIGHT * 0.20 + UP * 1)
        rg2 = Tex(r"$R_{G2} = 40.2k\Omega$", font_size=36, color=WHITE).move_to(RIGHT * 0.20 + UP * 0.5)
        gain = Tex(r"$\text{Gain } = \left(1+\frac{40.2k}{13.3k}\right) = 4.023$", font_size=36, color=WHITE).move_to(RIGHT * 4.25 + UP * 0.75)

        self.play(FadeIn(cir),
                  FadeIn(t1))

        self.wait(2)

        self.play(FadeIn(rg1),
                  FadeIn(rg2))
        self.wait(2)

        self.play(FadeIn(gain))
        self.wait(2)

        e1 = Tex(r"$V_{out} = 4 \cdot (V_{dac} - 2.5V)$", font_size=40, color=WHITE).move_to(UP * 3.75)
        e1[0][0:4].set_fill(color=VOUT1)
        e1[0][8:12].set_fill(color=VDAC)
        e1[0][13:17].set_fill(color=VREF)

        self.play(FadeIn(e1))
        self.wait(2)


        e2 = Tex(r"$V_{out} = 4.023 \cdot (V_{dac} - 2.5V)$", font_size=40, color=WHITE).move_to(UP * 3.75)
        e2[0][0:4].set_fill(color=VOUT1)
        e2[0][12:16].set_fill(color=VDAC)
        e2[0][17:21].set_fill(color=VREF)

        self.play(ReplacementTransform(e1, e2))

        code_str = """
void output_dac(float output_value)
{
    float calibrated_value = output_value / 4.023 + 2.5;
    calibrated_value = clamp(calibrated_value, 0.0, 5.0);
    write_dac(calibrated_value);
}
        """

        # Create a Code object
        code = Code(
            code_string=code_str,
            tab_width=4,
            background="rectangle",  # Can be "rectangle" or "window"
            language="c",    # Specify the language for syntax highlighting
        ).scale(0.5).move_to(UP*2.5)

        # Display the code block
        self.play(Create(code, run_time=3))
        self.wait(2)
        self.play(FadeOut(code),
                  FadeOut(cir),
                  FadeOut(t1),
                  e2.animate.shift(DOWN),
                  rg1.animate.shift(LEFT*3.2),
                  rg2.animate.shift(LEFT*3.2),
                  gain.animate.shift(LEFT*2)
        )
        self.wait(2)

        rg1_tol = Tex(r"$R_{G1} = 13.3k\Omega \pm 1\% $", font_size=36, color=WHITE).move_to(LEFT * 3 + UP * 1)
        rg2_tol = Tex(r"$R_{G2} = 40.2k\Omega \pm 1\% $", font_size=36, color=WHITE).move_to(LEFT * 3 + UP * 0.5)

        self.play(ReplacementTransform(rg1, rg1_tol),
                  ReplacementTransform(rg2, rg2_tol))

        rg1_tol2 = Tex(r"$R_{G1} = 13.3k\Omega + 1\% $", font_size=36, color=WHITE).move_to(LEFT * 3 + UP * 1)
        rg2_tol2 = Tex(r"$R_{G2} = 40.2k\Omega - 1\% $", font_size=36, color=WHITE).move_to(LEFT * 3 + UP * 0.5)




        self.wait(2)

        gain2 = Tex(r"$\text{Gain } = \left(1+\frac{39.8k}{13.4k}\right) = 3.963$", font_size=36, color=WHITE).move_to(RIGHT * 2.25 + UP * 0.75)

        e3 = Tex(r"$V_{out} = 3.963 \cdot (V_{dac} - 2.5V)$", font_size=40, color=WHITE).move_to(UP * 2.75)
        e3[0][0:4].set_fill(color=VOUT1)
        e3[0][12:16].set_fill(color=VDAC)
        e3[0][17:21].set_fill(color=VREF)
        self.play(ReplacementTransform(rg1_tol, rg1_tol2),
                  ReplacementTransform(rg2_tol, rg2_tol2),
                  ReplacementTransform(e2, e3),
                  ReplacementTransform(gain, gain2))
        self.wait(2)


        e4 = Tex(r"$V_{out} = 3.963 \cdot (0.0V - 2.5V) = -9.9V$", font_size=40, color=WHITE).move_to(UP * 2.75)
        e5 = Tex(r"$V_{out} = 3.963 \cdot (5.0V - 2.5V) = \text{ }9.9V$", font_size=40, color=WHITE).move_to(UP * 2.75)
        e4[0][0:4].set_fill(color=VOUT1)
        e4[0][12:16].set_fill(color=VDAC)
        e4[0][17:21].set_fill(color=VREF)
        e5[0][0:4].set_fill(color=VOUT1)
        e5[0][12:16].set_fill(color=VDAC)
        e5[0][17:21].set_fill(color=VREF)
        self.play(ReplacementTransform(e3, e4))
        self.wait(2)
        self.play(ReplacementTransform(e4, e5))
        self.wait(2)

class Setup5(Scene):
    def construct(self):
        VDAC = VIR_1
        VOUT1 = VIR_3
        VREF = VIR_5
        V1 = VIR_7

        R = VIR_10

        R5 = VIR_14
        R6 = VIR_15

        VP = VIR_14
        VM = VIR_15

        cir = ImageMobject("gain_hq.png").scale(0.6).set_z_index(-2)
        self.play(FadeIn(cir))
        self.wait(2)

class Setup6(Scene):
    def construct(self):
        VDAC = VIR_1
        VOUT1 = VIR_3
        VREF = VIR_5
        V1 = VIR_7

        R = VIR_10

        R5 = VIR_14
        R6 = VIR_15

        VP = VIR_14
        VM = VIR_15

        cir1 = ImageMobject("proj_1_inverted.png").scale(0.5).set_z_index(-2).move_to(LEFT*3.6+0.5*UP)
        cir2 = ImageMobject("proj_2_inverted.png").scale(0.5).set_z_index(-1).move_to(RIGHT*3.6+0.5*UP)

        self.play(FadeIn(cir1),
                  FadeIn(cir2))


        self.wait(2)

