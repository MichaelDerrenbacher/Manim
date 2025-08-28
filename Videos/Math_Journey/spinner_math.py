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

class Spinner():
    def __init__(self, type=1, radius=2):
        if type == 1:
            sectors = [Sector(start_angle=TAU/4,
                              angle=TAU/2,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_1),
                       Sector(start_angle=TAU/4,
                              angle=-TAU/2,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_3)
                       ]
        elif type == 2:
            sectors = [Sector(start_angle=TAU/4,
                              angle=TAU/3,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_1),
                       Sector(start_angle=TAU/4,
                              angle=-TAU/3,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_3),
                       Sector(start_angle=TAU / 4 - TAU/3,
                              angle=-TAU / 3,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_5),
                       ]
        elif type == 3:
            sectors = [Sector(start_angle=TAU/4,
                              angle=TAU/4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_1),
                       Sector(start_angle=TAU/4,
                              angle=-TAU/4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_3),
                       Sector(start_angle=3*TAU / 4,
                              angle=TAU / 4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_5),
                       Sector(start_angle=3 * TAU / 4,
                              angle=-TAU / 4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_7),
                       ]
        elif type == 4:
            sectors = [Sector(start_angle=3 * TAU / 4,
                              angle=-TAU/3,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_1),
                       Sector(start_angle=TAU / 4,
                              angle=TAU / 6,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_3),
                       Sector(start_angle=TAU/4,
                              angle=-TAU/4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_5),
                       Sector(start_angle=3 * TAU / 4,
                              angle=TAU / 4,
                              stroke_width=0,
                              outer_radius=radius,
                              fill_color=VIR_7),
                       ]
        else:
            self.field = Dot()
            sectors = [Dot()]

        self.sections = sectors

        self.dot = Dot(color=VIR_16)
        self.arrow = Arrow(start=DOWN*0.25, end=UP*radius, stroke_width=6, color=VIR_16)
        # self.arrow = VGroup(dot, arrow)

        self.field = VGroup(*[s for s in sectors])
        self.text = []
        text_list = ["A", "B", "C", "D"]
        for i, sector in enumerate(sectors):
            self.text.append(Text(f"{text_list[i]}", color=BLACK).move_to(sector))
        self.text_group = VGroup(*[t for t in self.text])

        self.everything = VGroup(self.field, self.text_group, self.dot, self.arrow)

class Barchart():
    def __init__(self, type=1):
        if type == 1:
            chart = BarChart(
                values=[0, 0],
                bar_names=["A", "B"],
                bar_colors=[VIR_1, VIR_3],
                y_range=[0, 100, 20],
                y_length=6,
                x_length=5,
                x_axis_config={"font_size": 36},
                y_axis_config={"decimal_number_config":
                                   {"unit": "\\%",
                                    "num_decimal_places": 0}}
            )
            bar1, bar2 = chart.bars
            dn1 = DecimalNumber(0, num_decimal_places=0)
            dn2 = DecimalNumber(0, num_decimal_places=0)
            dn1.add_updater(lambda mob: mob.next_to(bar1, UP))
            dn2.add_updater(lambda mob: mob.next_to(bar2, UP))
            self.dn = VGroup(dn1, dn2)

        elif type == 2:
            chart = BarChart(
                values=[0, 0, 0],
                bar_names=["A", "B", "C"],
                bar_colors=[VIR_1, VIR_3, VIR_5],
                y_range=[0, 100, 20],
                y_length=6,
                x_length=5,
                x_axis_config={"font_size": 36},
                y_axis_config={"decimal_number_config":
                                   {"unit": "\\%",
                                    "num_decimal_places": 0}}
            )
            bar1, bar2, bar3 = chart.bars
            dn1 = DecimalNumber(0, num_decimal_places=0)
            dn2 = DecimalNumber(0, num_decimal_places=0)
            dn3 = DecimalNumber(0, num_decimal_places=0)

            dn1.add_updater(lambda mob: mob.next_to(bar1, UP))
            dn2.add_updater(lambda mob: mob.next_to(bar2, UP))
            dn3.add_updater(lambda mob: mob.next_to(bar3, UP))
            self.dn = VGroup(dn1, dn2, dn3)
        else:
            chart = BarChart(
                values=[0, 0, 0, 0],
                bar_names=["A", "B", "C", "D"],
                bar_colors=[VIR_1, VIR_3, VIR_5, VIR_7],
                y_range=[0, 100, 20],
                y_length=6,
                x_length=5,
                x_axis_config={"font_size": 36},
                y_axis_config={"decimal_number_config":
                                   {"unit": "\\%",
                                    "num_decimal_places": 0}}
            )
            bar1, bar2, bar3, bar4 = chart.bars
            dn1 = DecimalNumber(0, num_decimal_places=0)
            dn2 = DecimalNumber(0, num_decimal_places=0)
            dn3 = DecimalNumber(0, num_decimal_places=0)
            dn4 = DecimalNumber(0, num_decimal_places=0)

            dn1.add_updater(lambda mob: mob.next_to(bar1, UP))
            dn2.add_updater(lambda mob: mob.next_to(bar2, UP))
            dn3.add_updater(lambda mob: mob.next_to(bar3, UP))
            dn4.add_updater(lambda mob: mob.next_to(bar4, UP))
            self.dn = VGroup(dn1, dn2, dn3, dn4)

        chart.shift(RIGHT*4.5)
        self.chart = chart


class Spinning_1(Scene):
    def construct(self):
        type = 1
        spinner = Spinner(type=type)
        bchart = Barchart(type=type)

        bar1, bar2 = bchart.chart.bars
        # bar1, bar2, bar3, bar4 = bchart.chart.bars
        dn1 = DecimalNumber(0, num_decimal_places=0)
        dn2 = DecimalNumber(0, num_decimal_places=0)
        # dn3 = DecimalNumber(0, num_decimal_places=0)
        # dn4 = DecimalNumber(0, num_decimal_places=0)

        dn1.add_updater(lambda mob: mob.next_to(bar1, UP))
        dn2.add_updater(lambda mob: mob.next_to(bar2, UP))
        # dn3.add_updater(lambda mob: mob.next_to(bar3, UP))
        # dn4.add_updater(lambda mob: mob.next_to(bar4, UP))


        self.play(FadeIn(spinner.field))
        self.wait(1)
        self.play(FadeIn(spinner.text_group))
        self.play(FadeIn(spinner.arrow),
                  FadeIn(spinner.dot))
        # self.play(FadeOut(spinner_1.field))
        # self.play(Indicate(spinner_1.sections[0]))

        self.play(AnimationGroup(*[(element.animate.shift(4*LEFT)) for element in spinner.everything]))
        text = Text("Rule: If spinner lands on B,\ndiscard result and respin", color=WHITE, font_size=32).next_to(spinner.dot, 10*UP).shift(0.2*RIGHT)

        self.play(FadeIn(text))

        self.wait(1)

        self.play(FadeIn(bchart.chart))
        self.wait(2)

        self.play(Rotate(spinner.arrow, angle=-TAU*4.6, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(bchart.chart.animate.change_bar_values([100,0]))
                  # dn1.animate.set_value(100))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*3.8, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*3.5, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.wait(1)

class Spinning_2(Scene):
    def construct(self):
        type = 2
        spinner = Spinner(type=type)
        bchart = Barchart(type=type)

        bar1, bar2, bar3 = bchart.chart.bars
        # bar1, bar2, bar3, bar4 = bchart.chart.bars
        dn1 = DecimalNumber(0, num_decimal_places=0)
        dn2 = DecimalNumber(0, num_decimal_places=0)
        dn3 = DecimalNumber(0, num_decimal_places=0)
        # dn4 = DecimalNumber(0, num_decimal_places=0)

        dn1.add_updater(lambda mob: mob.next_to(bar1, UP))
        dn2.add_updater(lambda mob: mob.next_to(bar2, UP))
        dn3.add_updater(lambda mob: mob.next_to(bar3, UP))
        # dn4.add_updater(lambda mob: mob.next_to(bar4, UP))


        self.play(FadeIn(spinner.field))
        self.wait(1)
        self.play(FadeIn(spinner.text_group))
        self.play(FadeIn(spinner.arrow),
                  FadeIn(spinner.dot))
        # self.play(FadeOut(spinner_1.field))
        # self.play(Indicate(spinner_1.sections[0]))

        self.play(AnimationGroup(*[(element.animate.shift(4*LEFT)) for element in spinner.everything]))
        text = Text("Rule: If spinner lands on C,\ndiscard result and respin", color=WHITE, font_size=32).next_to(spinner.dot, 10*UP).shift(0.2*RIGHT)

        self.play(FadeIn(text))

        self.wait(1)

        self.play(FadeIn(bchart.chart))
        self.wait(2)

        self.play(Rotate(spinner.arrow, angle=-TAU*4.6, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*3.5, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(bchart.chart.animate.change_bar_values([0,100,0]))
                  # dn2.animate.set_value(100))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*3.8, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(bchart.chart.animate.change_bar_values([50,50,0]))
                  # dn1.animate.set_value(50),
                  # dn2.animate.set_value(50))
        self.wait(1)

        self.play(Rotate(spinner.arrow, angle=-TAU*3.5, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*3.8, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(bchart.chart.animate.change_bar_values([33.3,66.7,0]))
                  # dn1.animate.set_value(33.3),
                  # dn2.animate.set_value(66.7))
        self.play(Rotate(spinner.arrow, angle=-TAU*4.3, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.wait(1)
        self.play(Rotate(spinner.arrow, angle=-TAU*4.3, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(bchart.chart.animate.change_bar_values([50,50,0]))
        self.wait(2)

        self.play(FadeOut(bchart.chart))

        image = ImageMobject("spinner_2.png").shift(RIGHT*3.5)
        image.height = 5.5
        self.play(FadeIn(image))
        self.wait(3)


class Spinning_3(Scene):
    def construct(self):
        type = 3
        spinner = Spinner(type=type)
        spinner.everything.shift(4*LEFT)

        text = Text("Rule: If spinner lands on D,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.2*RIGHT)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))

        self.wait(2)

        image = ImageMobject("spinner_3.png").shift(RIGHT*3.5)
        image.height = 5.5
        self.play(FadeIn(image))
        self.wait(3)

class Spinning_4(Scene):
    def construct(self):
        type = 4
        spinner = Spinner(type=type)
        spinner.everything.shift(4*LEFT)

        text = Text("Rule: If spinner lands on D,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.2*RIGHT)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))

        self.wait(2)

        image = ImageMobject("spinner_4.png").shift(RIGHT*3.5)
        image.height = 5.5
        self.play(FadeIn(image))
        self.wait(3)


class Chain_1(Scene):
    def construct(self):
        type = 1
        spinner = Spinner(type=type)
        spinner.everything.shift(4*LEFT)

        d = Dot(color=WHITE).shift(UP*3.5+1*RIGHT)
        cl1 = Circle(radius=0.5, color=VIR_1, fill_opacity=1).shift(UP*2-1*RIGHT)
        cr1 = Circle(radius=0.5, color=VIR_3, fill_opacity=1).shift(UP*2+1*RIGHT)
        al1 = Arrow(start=UP*3.5+1*RIGHT, end=UP*2.25-0.75*RIGHT, color=VIR_1)
        ar1 = Arrow(start=UP*3.5+1*RIGHT, end=UP*2.3+1*RIGHT, color=VIR_3, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=8)

        cl2 = Circle(radius=0.5, color=VIR_1, fill_opacity=1).shift(UP*0-1*RIGHT)
        cr2 = Circle(radius=0.5, color=VIR_3, fill_opacity=1).shift(UP*0+1*RIGHT)
        al2 = Arrow(start=UP*1.5+1*RIGHT, end=UP*0.25-0.75*RIGHT, color=VIR_1)
        ar2 = Arrow(start=UP*1.5+1*RIGHT, end=UP*0.3+1*RIGHT, color=VIR_3, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=8)

        cl3 = Circle(radius=0.5, color=VIR_1, fill_opacity=1).shift(DOWN*2-1*RIGHT)
        cr3 = Circle(radius=0.5, color=VIR_3, fill_opacity=1).shift(DOWN*2+1*RIGHT)
        al3 = Arrow(start=DOWN*0.5+1*RIGHT, end=DOWN*1.75-0.75*RIGHT, color=VIR_1)
        ar3 = Arrow(start=DOWN*0.5+1*RIGHT, end=DOWN*1.7+1*RIGHT, color=VIR_3, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=8)

        al4 = Arrow(start=DOWN*2.5+1*RIGHT, end=DOWN*3.75-0.75*RIGHT, color=VIR_1)
        ar4 = Arrow(start=DOWN*2.5+1*RIGHT, end=DOWN*3.7+1*RIGHT, color=VIR_3, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=8)

        ll1 = Text("A", color=BLACK, font_size=32).move_to(cl1)
        lr1 = Text("B", color=BLACK, font_size=32).move_to(cr1)
        ll2 = Text("A", color=BLACK, font_size=32).move_to(cl2)
        lr2 = Text("B", color=BLACK, font_size=32).move_to(cr2)
        ll3 = Text("A", color=BLACK, font_size=32).move_to(cl3)
        lr3 = Text("B", color=BLACK, font_size=32).move_to(cr3)

        tl1 = Tex(r'$\frac{1}{2}$', color=VIR_1).next_to(al1, UP*0.001).shift(DOWN*0.3)
        tr1 = Tex(r'$\frac{1}{2}$', color=VIR_3).next_to(ar1, RIGHT*0.5)

        tl2 = Tex(r'$\frac{1}{2}$', color=VIR_1).next_to(al2, UP*0.001).shift(DOWN*0.3)
        tr2 = Tex(r'$\frac{1}{2}$', color=VIR_3).next_to(ar2, RIGHT*0.5)

        tl3 = Tex(r'$\frac{1}{2}$', color=VIR_1).next_to(al3, UP*0.001).shift(DOWN*0.3)
        tr3 = Tex(r'$\frac{1}{2}$', color=VIR_3).next_to(ar3, RIGHT*0.5)

        tl4 = Tex(r'$\frac{1}{2}$', color=VIR_1).next_to(al4, UP*0.001).shift(DOWN*0.3)
        tr4 = Tex(r'$\frac{1}{2}$', color=VIR_3).next_to(ar4, RIGHT*0.5)

        e1 = Tex(r'$\frac{1}{2}$', color=VIR_1, font_size=64).shift(RIGHT*2.0)
        p1 = Tex(r'$+$', color=WHITE).next_to(e1, RIGHT*0.3)
        e2_1 = Tex(r'$\frac{1}{2}$', color=VIR_3, font_size=64).next_to(p1, RIGHT*0.3)
        c2 = Tex(r'$\cdot$', color=WHITE, font_size=64).next_to(e2_1, RIGHT*0.3)
        e2_2 = Tex(r'$\frac{1}{2}$', color=VIR_1, font_size=64).next_to(c2, RIGHT*0.3)
        p2 = Tex(r'$+$', color=WHITE).next_to(e2_2, RIGHT*0.3)
        e3_1 = Tex(r'$\frac{1}{2}$', color=VIR_3, font_size=64).next_to(p2, RIGHT * 0.3)
        c3_1 = Tex(r'$\cdot$', color=WHITE, font_size=64).next_to(e3_1, RIGHT*0.3)
        e3_2 = Tex(r'$\frac{1}{2}$', color=VIR_3, font_size=64).next_to(c3_1, RIGHT * 0.3)
        c3_2 = Tex(r'$\cdot$', color=WHITE, font_size=64).next_to(e3_2, RIGHT*0.3)
        e3_3 = Tex(r'$\frac{1}{2}$', color=VIR_1, font_size=64).next_to(c3_2, RIGHT * 0.3)
        d4   = Tex(r'$+\dotsb = 1$', color=WHITE).next_to(e3_3, RIGHT * 0.3)


        text = Text("Rule: If spinner lands on B,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.15*RIGHT)

        te = Text("Chance to get A:", font_size=24).shift(4.25*RIGHT+0.75*UP)

        eqn_big = Tex(r'$\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+...=1$', color=WHITE, font_size=60).shift(RIGHT*4.4)

        eqn = VGroup(e1, p1, e2_1, c2, e2_2, p2, e3_1, c3_1, e3_2, c3_2, e3_3, d4)
        chain1 = VGroup(d, cl1, cr1, al1, ar1, cl2, cr2, al2, ar2, cl3, cr3, al3, ar3, al4, ar4,
                        tl1, tr1, tl2, tr2, tl3, tr3, tl4, tr4,
                        ll1, lr1, ll2, lr2, ll3, lr3)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))

        self.play(FadeIn(te))

        self.play(FadeIn(d))

        self.play(Indicate(d, color=WHITE, scale_factor=1.5))

        self.play(FadeIn(cl1),
                  FadeIn(cr1),
                  FadeIn(al1),
                  FadeIn(ar1),
                  FadeIn(tl1),
                  FadeIn(tr1),
                  FadeIn(ll1),
                  FadeIn(lr1))

        self.play(Rotate(spinner.arrow, angle=-TAU*4.6, about_point=4*LEFT, rate_func=rush_from, run_time=3))

        self.play(Indicate(cl1, color=WHITE, scale_factor=1.1))

        self.play(FadeIn(e1))

        self.wait(2)

        self.play(Rotate(spinner.arrow, angle=-TAU*4.5, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(Indicate(cr1, color=WHITE, scale_factor=1.1))


        self.play(FadeIn(cl2),
                  FadeIn(cr2),
                  FadeIn(al2),
                  FadeIn(ar2),
                  FadeIn(tl2),
                  FadeIn(tr2),
                  FadeIn(ll2),
                  FadeIn(lr2))

        self.play(Rotate(spinner.arrow, angle=-TAU*4.5, about_point=4*LEFT, rate_func=rush_from, run_time=3))
        self.play(Indicate(cl2, color=WHITE, scale_factor=1.1))

        self.play(FadeIn(p1),
                  FadeIn(e2_1),
                  FadeIn(c2),
                  FadeIn(e2_2))

        self.play(FadeIn(cl3),
                  FadeIn(cr3),
                  FadeIn(al3),
                  FadeIn(ar3),
                  FadeIn(tl3),
                  FadeIn(tr3),
                  FadeIn(ll3),
                  FadeIn(lr3))

        self.play(FadeIn(p2),
                  FadeIn(e3_1),
                  FadeIn(c3_1),
                  FadeIn(e3_2),
                  FadeIn(c3_2),
                  FadeIn(e3_3))

        self.play(FadeIn(al4),
                  FadeIn(ar4),
                  FadeIn(tl4),
                  FadeIn(tr4))


        self.play(FadeIn(d4))

        self.play(ReplacementTransform(eqn, eqn_big))

        self.wait(1)

        self.play(AnimationGroup(*[FadeOut(element) for element in spinner.everything]),
                  FadeOut(eqn_big),
                  FadeOut(te),
                  FadeOut(text),
                  AnimationGroup(*[element.animate.shift(LEFT*4) for element in chain1]))

        self.wait(2)

        c1 = Circle(radius=1, color=VIR_3, fill_opacity=1).shift(0.5*RIGHT)
        c2 = Circle(radius=1, color=VIR_1, fill_opacity=1).shift(4.5*RIGHT)
        a1 = ArcBetweenPoints(1.5*RIGHT+1*DOWN, 3.5*RIGHT+1*DOWN, radius=2)
        a2 = ArcBetweenPoints(1.5*RIGHT+1*UP, 0.5*LEFT+1*UP, radius=1)
        a3 = ArcBetweenPoints(5.5*RIGHT+1*UP, 3.5*RIGHT+1*UP, radius=1)

        t1 = Tex(r'$\frac{1}{2}$', color=VIR_1, font_size=64).next_to(a1, UP*0.001).shift(DOWN*0.1)
        t2 = Tex(r'$\frac{1}{2}$', color=VIR_3, font_size=64).next_to(a2, UP*1.25)
        t3 = Tex(r'$\frac{1}{1}$', color=VIR_1, font_size=64).next_to(a3, UP*1.25)

        l1 = Text("B", color=BLACK, font_size=48).move_to(c1)
        r1 = Text("A", color=BLACK, font_size=48).move_to(c2)

        a1.add_tip()
        a2.add_tip()
        a3.add_tip()

        chain2 = VGroup(c1, c2, a1, a2, a3, t1, t2, t3, l1, r1)
        self.play(AnimationGroup(*[FadeIn(element) for element in chain2]))

        # self.play(Indicate(ar1, color=WHITE, scale_factor=1.1),
        #           Indicate(a2, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(ar2, color=WHITE, scale_factor=1.1),
                  Indicate(a2, color=WHITE, scale_factor=1.2))
        self.wait(1)
        self.play(Indicate(al3, color=WHITE, scale_factor=1.1),
                  Indicate(a1, color=WHITE, scale_factor=1.2))

        self.wait(3)
        self.play(AnimationGroup(*[FadeOut(element) for element in chain1]),
                  AnimationGroup(*[element.animate.shift(LEFT * 4) for element in chain2]))

        self.wait(2)

        m = Matrix([[r'1', r'0'], [r'\tfrac{1}{2}', r'\tfrac{1}{2}']]).shift(5*RIGHT)
        an0 = Tex('$A_{n}$', font_size=32).next_to(m, LEFT).shift(UP*0.4)
        bn0 = Tex('$B_{n}$', font_size=32).next_to(m, LEFT).shift(DOWN*0.4)
        an1 = Tex('$A_{n+1}$', font_size=32).next_to(m, UP).shift(LEFT*0.6)
        bn1 = Tex('$B_{n+1}$', font_size=32).next_to(m, UP).shift(RIGHT*0.6)

        abn = VGroup(an0, bn0, an1, bn1)

        self.play(FadeIn(m),
                  AnimationGroup(*[FadeIn(element) for element in abn]))

        self.wait(1)


        self.play(Indicate(c2, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(an0, color=WHITE, scale_factor=1.3))
        self.wait(1)
        self.play(Indicate(a3, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(c2, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(an1, color=WHITE, scale_factor=1.3))
        self.wait(2)

        self.play(Indicate(c1, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(bn0, color=WHITE, scale_factor=1.3))
        self.wait(1)
        self.play(Indicate(a1, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(c2, color=WHITE, scale_factor=1.1))
        self.wait(1)
        self.play(Indicate(an1, color=WHITE, scale_factor=1.3))
        self.wait(1)

        self.play(AnimationGroup(*[FadeOut(element) for element in chain2]),
                  m.animate.shift(9*LEFT+2*UP),
                  AnimationGroup(*[FadeOut(element) for element in abn]))

        P = Tex('$P=$', font_size=48).next_to(m, LEFT*1)

        self.play(FadeIn(P))

        pi = Tex(r'$\boldsymbol{\pi}=$', font_size=48).next_to(P, DOWN*8)


        pim = Matrix([[r'\tfrac{1}{2}'], [r'\tfrac{1}{2}']]).next_to(pi, RIGHT)

        self.play(FadeIn(pim),
                  FadeIn(pi))


        x1 = Tex(r'$X_1 = \boldsymbol{\pi}^TP^1$', font_size=48).next_to(pi, DOWN*6+RIGHT).shift(1.1*LEFT)


        self.play(FadeIn(x1))


        temp_eq1 = Tex(r'$=$').next_to(x1, RIGHT)
        temp_m1 = Matrix([[r'\tfrac{1}{2}', r'\tfrac{1}{2}']]).next_to(temp_eq1, RIGHT)
        temp_m2 = Matrix([[r'1', r'0'], [r'\tfrac{1}{2}', r'\tfrac{1}{2}']]).next_to(temp_m1, RIGHT)
        temp_eq2 = Tex(r'$=$').next_to(temp_m2, RIGHT)
        temp_m3 = Matrix([[r'\tfrac{3}{4}', r'\tfrac{1}{4}']]).next_to(temp_eq2, RIGHT)



        self.play(FadeIn(temp_eq1),
                  FadeIn(temp_m1),
                  FadeIn(temp_m2))
        self.wait(1)
        self.play(FadeIn(temp_eq2),
                  FadeIn(temp_m3))

        self.wait(3)

        self.play(FadeOut(temp_eq1),
                  FadeOut(temp_eq2),
                  FadeOut(temp_m1),
                  FadeOut(temp_m2),
                  FadeOut(temp_m3))

        self.play(x1.animate.shift(UP*3.5+RIGHT*5))
        x0 = Tex(r'$X_0 = \boldsymbol{\pi}^TP^0$', font_size=48).next_to(x1, UP*2.75)

        x2 = Tex(r'$X_2 = \boldsymbol{\pi}^TP^2$', font_size=48).next_to(x1, DOWN*2.75)
        x3 = Tex(r'$X_3 = \boldsymbol{\pi}^TP^3$', font_size=48).next_to(x2, DOWN*2.75)

        self.play(FadeIn(x0),
                  # FadeIn(x1),
                  FadeIn(x2),
                  FadeIn(x3))

        eq0 = Tex(r'$=$').next_to(x0, RIGHT)
        eq1 = Tex(r'$=$').next_to(x1, RIGHT)
        eq2 = Tex(r'$=$').next_to(x2, RIGHT)
        eq3 = Tex(r'$=$').next_to(x3, RIGHT)

        m0 = Matrix([[r'\tfrac{1}{2}', r'\tfrac{1}{2}']]).next_to(eq0, RIGHT)
        m1 = Matrix([[r'\tfrac{3}{4}', r'\tfrac{1}{4}']]).next_to(eq1, RIGHT)
        m2 = Matrix([[r'\tfrac{7}{8}', r'\tfrac{1}{8}']]).next_to(eq2, RIGHT)
        m3 = Matrix([[r'\tfrac{15}{16}', r'\tfrac{1}{16}']]).next_to(eq3, RIGHT)

        self.play(FadeIn(eq0),
                  FadeIn(eq1),
                  FadeIn(eq2),
                  FadeIn(eq3),
                  FadeIn(m0),
                  FadeIn(m1),
                  FadeIn(m2),
                  FadeIn(m3))

        xn = Tex(r'$X_n = \boldsymbol{\pi}^TP^n$', font_size=48).next_to(x3, DOWN*2.75)
        eqn = Tex(r'$=$').next_to(xn, RIGHT*0.8)
        mn = Matrix([[r'\tfrac{2^{n+1}-1}{2^{n+1}}', r'\tfrac{1}{2^{n+1}}']]).next_to(eqn, RIGHT)


        self.play(FadeIn(xn),
                  FadeIn(eqn),
                  FadeIn(mn))

        self.wait(2)

        self.play(FadeOut(x0),
                  FadeOut(x1),
                  FadeOut(x2),
                  FadeOut(x3),
                  FadeOut(eq0),
                  FadeOut(eq1),
                  FadeOut(eq2),
                  FadeOut(eq3),
                  FadeOut(m0),
                  FadeOut(m1),
                  FadeOut(m2),
                  FadeOut(m3),
                  xn.animate.shift(3*UP),
                  eqn.animate.shift(3*UP),
                  mn.animate.shift(3*UP))


        xinf = Tex(r'$\lim\limits_{n\to\infty} X_n = $', font_size=48).next_to(xn, 3*DOWN)
        minf = Matrix([[r'1', r'0']]).next_to(xinf, RIGHT)


        self.play(FadeIn(xinf),
                  FadeIn(minf))

        self.wait(3)


class Chain_2(Scene):
    def construct(self):
        type = 2
        spinner = Spinner(type=type)
        spinner.everything.shift(4*LEFT)
        text = Text("Rule: If spinner lands on C,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.15*RIGHT)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))


        ca = Circle(radius=0.75, color=VIR_1, fill_opacity=1).shift(0.5*RIGHT+1.25*UP)
        cb = Circle(radius=0.75, color=VIR_3, fill_opacity=1).shift(4.5*RIGHT+1.25*UP)
        cc = Circle(radius=0.75, color=VIR_5, fill_opacity=1).shift(2.5*RIGHT+0.75*DOWN)

        aca = ArcBetweenPoints(0.5*RIGHT+0.25*UP, 1.5*RIGHT+0.75*DOWN, radius=1.5)
        acb = ArcBetweenPoints(3.5*RIGHT+0.75*DOWN, 4.5*RIGHT+0.25*UP, radius=1.5)

        aa = ArcBetweenPoints(1.5*RIGHT+2.0*UP, 0.5*LEFT+2.0*UP, radius=1)
        ab = ArcBetweenPoints(5.5*RIGHT+2.0*UP, 3.5*RIGHT+2.0*UP, radius=1)
        ac = ArcBetweenPoints(1.5*RIGHT+1.5*DOWN, 3.5*RIGHT+1.5*DOWN, radius=1)

        tca = Tex(r'$\frac{1}{3}$', color=VIR_1, font_size=64).next_to(aca, UP*0.001).shift(DOWN*0.45+RIGHT*0.2)
        tcb = Tex(r'$\frac{1}{3}$', color=VIR_3, font_size=64).next_to(acb, UP*0.001).shift(DOWN*0.45+LEFT*0.2)
        tcc = Tex(r'$\frac{1}{3}$', color=VIR_5, font_size=64).next_to(ac, DOWN*1.2)

        t2 = Tex(r'$1$', color=VIR_1, font_size=64).next_to(aa, UP*1.25)
        t3 = Tex(r'$1$', color=VIR_3, font_size=64).next_to(ab, UP*1.25)

        ca_text = Text("A", color=BLACK, font_size=48).move_to(ca)
        cb_text = Text("B", color=BLACK, font_size=48).move_to(cb)
        cc_text = Text("C", color=BLACK, font_size=48).move_to(cc)

        aa.add_tip()
        aca.add_tip(at_start=True)
        acb.add_tip()
        ab.add_tip()
        ac.add_tip()

        chain1 = VGroup(ca, cb, cc, aa, aca, acb, ab, ac, tca, tcb, tcc, t2, t3, ca_text, cb_text, cc_text)
        self.play(AnimationGroup(*[FadeIn(element) for element in chain1]))

        self.wait(3)

        P = Tex(r'$P=$').shift(6*LEFT+2*UP)
        Pm = Matrix([[r'1', r'0', r'0'], [r'0', r'1', r'0'], [r'\tfrac{1}{3}', r'\tfrac{1}{3}', r'\tfrac{1}{3}']]).next_to(P, RIGHT)

        self.play(AnimationGroup(*[FadeOut(element) for element in spinner.everything]),
                  FadeOut(text))

        self.play(FadeIn(P),
                  FadeIn(Pm))

        self.wait(1)

        pi = Tex(r'$\boldsymbol{\pi}=$', font_size=48).next_to(P, DOWN*10)
        pim = Matrix([[r'\tfrac{1}{3}'], [r'\tfrac{1}{3}'], [r'\tfrac{1}{3}']]).next_to(pi, RIGHT)

        self.play(FadeIn(pim),
                  FadeIn(pi))

        self.wait(3)

        self.play(AnimationGroup(*[FadeOut(element) for element in chain1]))

        self.wait(3)


        x0 = Tex(r'$X_0 = \boldsymbol{\pi}^TP^0$', font_size=48).shift(UP*3+1*RIGHT)
        x1 = Tex(r'$X_1 = \boldsymbol{\pi}^TP^1$', font_size=48).next_to(x0, DOWN*2.75)
        x2 = Tex(r'$X_2 = \boldsymbol{\pi}^TP^2$', font_size=48).next_to(x1, DOWN*2.75)
        x3 = Tex(r'$X_3 = \boldsymbol{\pi}^TP^3$', font_size=48).next_to(x2, DOWN*2.75)

        self.play(LaggedStart(FadeIn(x0),
                              FadeIn(x1),
                              FadeIn(x2),
                              FadeIn(x3)))

        eq0 = Tex(r'$=$').next_to(x0, RIGHT)
        eq1 = Tex(r'$=$').next_to(x1, RIGHT)
        eq2 = Tex(r'$=$').next_to(x2, RIGHT)
        eq3 = Tex(r'$=$').next_to(x3, RIGHT)

        m0 = Matrix([[r'\tfrac{1}{3}', r'\tfrac{1}{3}', r'\tfrac{1}{3}']]).next_to(eq0, RIGHT)
        m1 = Matrix([[r'\tfrac{4}{9}', r'\tfrac{4}{9}', r'\tfrac{1}{9}']]).next_to(eq1, RIGHT)
        m2 = Matrix([[r'\tfrac{13}{27}', r'\tfrac{13}{27}', r'\tfrac{1}{27}']]).next_to(eq2, RIGHT)
        m3 = Matrix([[r'\tfrac{40}{81}', r'\tfrac{40}{81}', r'\tfrac{1}{81}']]).next_to(eq3, RIGHT)

        self.play(FadeIn(eq0),
                  FadeIn(m0))
        self.play(FadeIn(eq1),
                  FadeIn(m1))
        self.play(FadeIn(eq2),
                  FadeIn(m2))
        self.play(FadeIn(eq3),
                  FadeIn(m3))

        xmat = VGroup(x0, x1, x2, x3, eq0, eq1, eq2, eq3, m0, m1, m2, m3)


        self.wait(3)

        self.play(FadeOut(P),
                  FadeOut(Pm),
                  FadeOut(pim),
                  FadeOut(pi),
                  AnimationGroup(*[element.animate.shift(5 * LEFT) for element in xmat]))

        r = Rectangle(height=5, width=1.1, stroke_color=VIR_1).shift(1.35*LEFT+1.2*UP)
        self.play(FadeIn(r))

        a0 = Tex(r'$f(0) = \tfrac{1}{3}$', font_size=48).next_to(m0, 4.75*RIGHT)
        a1 = Tex(r'$f(1) = \tfrac{4}{9}$', font_size=48).next_to(m1, 4.75*RIGHT)
        a2 = Tex(r'$f(2) = \tfrac{13}{27}$', font_size=48).next_to(m2, 4*RIGHT)
        a3 = Tex(r'$f(3) = \tfrac{40}{81}$', font_size=48).next_to(m3, 4*RIGHT)


        self.play(LaggedStart(FadeIn(a0),
                              FadeIn(a1),
                              FadeIn(a2),
                              FadeIn(a3)))

        self.play(FadeOut(r),
                  AnimationGroup(*[FadeOut(element) for element in xmat]),
                  a0.animate.shift(8*LEFT),
                  a1.animate.shift(8*LEFT),
                  a2.animate.shift(8*LEFT),
                  a3.animate.shift(8*LEFT))


        t = Text("Define f(n) as the chance that the spinner landed on 'A'\nat each spin attempt. f(n) can be described with\na non-homogeneous linear reoccurrence:",
                 font_size=24).shift(UP*2.75+RIGHT*2.25)

        self.play(FadeIn(t))
        an = Tex(r'$f(n) = \tfrac{f(n-1)}{3} + \tfrac{1}{3}$', font_size=48).shift(UP*1.55+RIGHT*1)
        self.play(FadeIn(an))

        t1 = Text("Homogeneous Solution:",
                 font_size=24).shift(UP*0.55+RIGHT*1)
        t2 = Text("Non-Homogeneous Solution:",
                 font_size=24).shift(UP*0.55+RIGHT*1)
        t3 = Text("Combined Solution:",
                 font_size=24).shift(UP*0.55+RIGHT*1)
        self.play(FadeIn(t1))

        homogeneous_1 = Tex(r'$\alpha^n-\tfrac{\alpha^{n-1}}{3}=0$', font_size=48).shift(RIGHT*1+0.35*DOWN)
        homogeneous_2 = Tex(r'$\alpha-\tfrac{1}{3}=0$', font_size=48).next_to(homogeneous_1, DOWN)
        homogeneous_3 = Tex(r'$\alpha=\tfrac{1}{3}$', font_size=48).next_to(homogeneous_2, DOWN)
        self.wait(1)
        self.play(FadeIn(homogeneous_1))
        self.wait(1)
        self.play(FadeIn(homogeneous_2))
        self.wait(1)
        self.play(FadeIn(homogeneous_3))
        self.wait(3)

        homogeneous_f = Tex(r'$f(n)=C_1(\tfrac{1}{3})^n$', font_size=48).shift(RIGHT*1+0.35*DOWN)
        self.play(ReplacementTransform(homogeneous_1, homogeneous_f),
                  ReplacementTransform(homogeneous_2, homogeneous_f),
                  ReplacementTransform(homogeneous_3, homogeneous_f))
        self.wait(2)
        self.play(FadeOut(homogeneous_f),
                  ReplacementTransform(t1, t2))
        self.wait(2)

        nonhomogeneous_0 = Tex(r'$\text{Guess } f(n) = D\tfrac{1}{3}$', font_size=40).next_to(t2, RIGHT)


        nonhomogeneous_1 = Tex(r'$D\tfrac{1}{3}-D\tfrac{1}{9}-\tfrac{1}{3}=0$', font_size=48).shift(RIGHT*1+0.35*DOWN)
        nonhomogeneous_2 = Tex(r'$D-\tfrac{1}{3}-1=0$', font_size=48).next_to(nonhomogeneous_1, DOWN)
        nonhomogeneous_3 = Tex(r'$D\tfrac{2}{3}=1$', font_size=48).next_to(nonhomogeneous_2, DOWN)
        nonhomogeneous_4 = Tex(r'$D=\tfrac{3}{2}$', font_size=48).next_to(nonhomogeneous_3, DOWN)
        nonhomogeneous_f = Tex(r'$f(n) = \tfrac{1}{2}$', font_size=48).shift(RIGHT*1+0.35*DOWN)

        self.wait(1)
        self.play(FadeIn(nonhomogeneous_0))
        self.wait(1)
        self.play(FadeIn(nonhomogeneous_1))
        self.wait(1)
        self.play(FadeIn(nonhomogeneous_2))
        self.wait(1)
        self.play(FadeIn(nonhomogeneous_3))
        self.wait(1)
        self.play(FadeIn(nonhomogeneous_4))
        self.wait(1)

        self.play(ReplacementTransform(nonhomogeneous_0, nonhomogeneous_f),
                  ReplacementTransform(nonhomogeneous_1, nonhomogeneous_f),
                  ReplacementTransform(nonhomogeneous_2, nonhomogeneous_f),
                  ReplacementTransform(nonhomogeneous_3, nonhomogeneous_f),
                  ReplacementTransform(nonhomogeneous_4, nonhomogeneous_f))
        self.wait(3)

        self.play(FadeOut(nonhomogeneous_f),
                  ReplacementTransform(t2, t3))

        combined_1 = Tex(r'$f(n) = C_1(\tfrac{1}{3})^n + \tfrac{1}{2}$', font_size=48).shift(RIGHT*1+0.35*DOWN)
        combined_2 = Tex(r'$f(0) = \tfrac{1}{3} = C_1 + \tfrac{1}{2}$', font_size=48).next_to(combined_1, DOWN)
        combined_3 = Tex(r'$C_1 = -\tfrac{1}{3}$', font_size=48).next_to(combined_2, DOWN)
        combined_f = Tex(r'$f(n) = \tfrac{1}{2}-(\tfrac{1}{3})^{n+1}$', font_size=48).shift(RIGHT*1+0.35*DOWN)
        finf = Tex(r'$\lim\limits_{n\to\infty} f(n) = \tfrac{1}{2}$', font_size=48).next_to(combined_f, DOWN)



        self.wait(1)
        self.play(FadeIn(combined_1))
        self.wait(1)
        self.play(FadeIn(combined_2),
                  Indicate(a0))
        self.wait(1)
        self.play(FadeIn(combined_3))
        self.wait(1)
        self.play(ReplacementTransform(combined_1, combined_f),
                  ReplacementTransform(combined_2, combined_f),
                  ReplacementTransform(combined_3, combined_f))
        self.wait(2)
        self.play(FadeIn(finf))

        self.wait(3)

class Chain_3(Scene):
    def construct(self):
        type = 3
        spinner = Spinner(type=type)
        spinner.everything.shift(4 * LEFT)
        text = Text("Rule: If spinner lands on D,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.15 * RIGHT)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))

        summation = Tex(rf'$\sum\limits_{{n=1}}^{{\infty}} \frac{{1}}{{4^n}} = \frac{1}{3}$', color=WHITE, font_size=64).shift(RIGHT)

        self.play(FadeIn(summation))
        self.wait(1)
        self.play(Indicate(spinner.sections[0], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)
        self.play(Indicate(spinner.sections[0], color=WHITE, scale_factor=1.05, run_time=2),
                  Indicate(spinner.sections[1], color=WHITE, scale_factor=1.05, run_time=2),
                  Indicate(spinner.sections[2], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)
        self.play(Indicate(spinner.sections[3], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)


        self.play(FadeOut(spinner.field),
                  FadeOut(spinner.text_group),
                  FadeOut(spinner.arrow),
                  FadeOut(spinner.dot),
                  FadeOut(text),
                  FadeOut(summation))
        self.wait(1)

        type = 4
        spinner = Spinner(type=type)
        spinner.everything.shift(4 * LEFT)
        text = Text("Rule: If spinner lands on D,\ndiscard result and respin", color=WHITE, font_size=32).next_to(
            spinner.dot, 10 * UP).shift(0.15 * RIGHT)

        self.play(FadeIn(spinner.field),
                  FadeIn(spinner.text_group),
                  FadeIn(spinner.arrow),
                  FadeIn(spinner.dot),
                  FadeIn(text))

        summation = Tex(rf'$\frac{3}{8}\sum\limits_{{n=0}}^{{\infty}} \frac{{1}}{{4^n}} = \frac{1}{2}$', color=WHITE, font_size=64).shift(RIGHT)

        self.play(FadeIn(summation))
        self.wait(1)
        self.play(Indicate(spinner.sections[0], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)
        self.play(Indicate(spinner.sections[0], color=WHITE, scale_factor=1.05, run_time=2),
                  Indicate(spinner.sections[1], color=WHITE, scale_factor=1.05, run_time=2),
                  Indicate(spinner.sections[2], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)
        self.play(Indicate(spinner.sections[3], color=WHITE, scale_factor=1.05, run_time=2))
        self.wait(1)

        self.play(FadeOut(spinner.field),
                  FadeOut(spinner.text_group),
                  FadeOut(spinner.arrow),
                  FadeOut(spinner.dot),
                  FadeOut(text),
                  FadeOut(summation))