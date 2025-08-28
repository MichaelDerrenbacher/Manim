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




class Array():
    def __init__(self, values, is_colorful=False, is_gray=False):

        self.values = []
        self.indices = []
        self.boxes = []
        self.lines = []

        x_global_offset = -1.5
        box_size = 0.5

        if is_colorful:
            colors = virdis_colors
        else:
            colors = [WHITE]*16
        if is_gray:
            colors = [DARK_GRAY] * 16

        for index, value in enumerate(values):
            y_offset = 2
            x_offset = index*box_size+x_global_offset

            self.boxes.append(Rectangle(width=box_size,
                                        height=box_size,
                                        stroke_color=colors[index*2],
                                        fill_opacity=0).move_to(RIGHT*x_offset + UP*y_offset))

            self.indices.append(Tex(rf'${index}$', color=LIGHT_GRAY, font_size=24).move_to(RIGHT*x_offset + UP * (y_offset + box_size - 0.05)))
            self.values.append(Tex(rf'${value}$', color=colors[index*2], font_size=32).move_to(RIGHT*x_offset + UP*y_offset))

        self.everything = VGroup(self.boxes, self.indices, self.values)




class BinaryTree():
    def __init__(self, values, is_colorful=False, is_gray=False):

        self.values = []
        self.indices = []
        self.nodes = []
        self.lines = []

        if is_colorful:
            colors = virdis_colors
        else:
            colors = [WHITE]*16
        if is_gray:
            colors = [DARK_GRAY] * 16

        x_global_offset = 0

        radius = 0.4
        x_offsets = [0, -1, 1, -1.5, -0.5, 0.5, 1.5]
        line_x_offsets = [0, -.707*radius, .707*radius, -.707*radius-1, -.707*radius-0.45, -.707*radius+1, +.707*radius+1]
        line_y_offsets = [0, -.707*radius, -.707*radius, -.707*radius-1.5, -.707*radius-1.5, -.707*radius-1.5, -.707*radius-1.5]


        for index, value in enumerate(values):
            y_offset = -1.5 * (math.log2(index+1) // 1)
            x_offset = x_offsets[index]
            # print(f"{index = }")
            #
            # print(f"{y_offset = }")

            self.nodes.append(Circle(radius=radius,
                                     stroke_color=colors[index*2],
                                     fill_opacity=0).move_to(RIGHT*(x_offset+x_global_offset) + UP*y_offset))
            self.indices.append(Tex(rf'${index}$', color=LIGHT_GRAY, font_size=24).move_to(RIGHT*(x_offset+radius+x_global_offset) + UP*(y_offset+radius)))
            self.values.append(Tex(rf'${value}$', color=colors[index*2], font_size=32).move_to(RIGHT*(x_offset+x_global_offset) + UP*y_offset))

            if index != 0:
                self.lines.append(Line(start=UP*(y_offset+radius)+RIGHT*(x_offset+x_global_offset), end=(line_x_offsets[index]+x_global_offset)*RIGHT + line_y_offsets[index]*UP))

        self.everything = VGroup(self.lines, self.nodes, self.indices, self.values)



        # self.play(AnimationGroup(*[FadeIn(element) for element in a.boxes]),
        #           AnimationGroup(*[FadeIn(element) for element in a.values]),
        #           AnimationGroup(*[FadeIn(element) for element in a.indices]))
        # self.play(AnimationGroup(*[FadeIn(element) for element in b.nodes]),
        #           AnimationGroup(*[FadeIn(element) for element in b.values]),
        #           AnimationGroup(*[FadeIn(element) for element in b.indices]),
        #           AnimationGroup(*[FadeIn(element) for element in b.lines]))


class Setup1(Scene):
    def construct(self):
        nums = [1, 5, 6, 3, 2, 7, 4]

        b1 = BinaryTree(nums, False)
        a1 = Array(nums, False)

        self.play(AnimationGroup(*[FadeIn(element) for element in a1.everything]))
        self.wait(2)
        self.play(AnimationGroup(*[FadeIn(element) for element in b1.everything]))
        self.wait(2)


        b2 = BinaryTree(nums, True)
        a2 = Array(nums, True)

        self.play(AnimationGroup(*[FadeIn(element) for element in a2.everything]))
        self.play(AnimationGroup(*[FadeIn(element) for element in b2.everything]))


        for i in range(7):

            start_values = [1.5*LEFT+1.8*UP]
            end_values = [UP*0.3, DOWN*1.2+LEFT*1, DOWN*1.2+RIGHT*1, DOWN*2.6+LEFT*1.4, DOWN*2.6+LEFT*0.5, DOWN*2.6+RIGHT*0.5, DOWN*2.6+RIGHT*1.4]


            arrow = Arrow(start=start_values[0]+0.5*i*RIGHT, end=end_values[i], color=virdis_colors[i*2])

            self.play(FadeIn(arrow))
            self.wait(0.25)
            self.play(FadeOut(arrow))

        self.wait(2)

        self.play(AnimationGroup(*[FadeOut(element) for element in a2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2.everything]))
        # self.play(AnimationGroup(*[FadeIn(element) for element in a1.everything]),
        #           AnimationGroup(*[FadeIn(element) for element in b1.everything]))

        self.wait(2)

        self.play(Indicate(b1.nodes[1]),
                  Indicate(b1.nodes[3]),
                  Indicate(b1.nodes[4]),
                  FadeIn(b2.nodes[1]),
                  FadeIn(b2.nodes[3]),
                  FadeIn(b2.nodes[4]))

        self.wait(2)

        self.play(Indicate(b1.values[1]))
        self.play(Indicate(b1.values[3]))
        self.play(Indicate(b1.values[4]))

        self.wait(2)

        self.play(FadeOut(b2.nodes[1]),
                  FadeOut(b2.nodes[3]),
                  FadeOut(b2.nodes[4]))

        self.wait(2)

        self.play(Indicate(b1.nodes[2]),
                  Indicate(b1.nodes[5]),
                  Indicate(b1.nodes[6]),
                  FadeIn(b2.nodes[2]),
                  FadeIn(b2.nodes[5]),
                  FadeIn(b2.nodes[6]))

        self.wait(2)

        self.play(Indicate(b1.values[2]))
        self.play(Indicate(b1.values[5]))

        self.wait(2)

        self.play(FadeOut(b2.nodes[2]),
                  FadeOut(b2.nodes[5]),
                  FadeOut(b2.nodes[6]))

        self.play(Indicate(b1.nodes[4]),
                  FadeIn(b2.nodes[4]))

        self.wait(2)

        self.play(Indicate(b1.values[4]))

        self.wait(2)

        self.play(FadeOut(b2.nodes[4]))

        self.wait(2)

        self.remove(*[element for element in a2.everything])
        self.remove(*[element for element in b2.everything])

        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b1.everything]))

        self.wait(2)


class Setup2(Scene):
    def construct(self):
        nums = [1, 5, 6, 3, 2, 7, 4]

        b1 = BinaryTree(nums, False)
        a1 = Array(nums, False)

        b2 = BinaryTree(nums, True)
        a2 = Array(nums, True)

        self.play(AnimationGroup(*[FadeIn(element) for element in a1.everything]))
        self.play(AnimationGroup(*[FadeIn(element) for element in b1.everything]))

        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b2.everything]))

        self.play(AnimationGroup(*[FadeOut(element) for element in a2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2.everything]))

        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b1.everything]))


        self.wait(2)

        code1 = ImageMobject("images/code1.png").move_to(LEFT*2.5+UP)
        code1.scale(0.6)

        self.play(FadeIn(code1))

        self.wait(2)

        self.play(Indicate(b1.nodes[1]),
                  Indicate(b1.nodes[3]),
                  Indicate(b1.nodes[4]),
                  FadeIn(b2.nodes[1]),
                  FadeIn(b2.nodes[3]),
                  FadeIn(b2.nodes[4]))

        self.play(Indicate(a1.boxes[1]),
                  Indicate(a1.boxes[3]),
                  Indicate(a1.boxes[4]),
                  FadeIn(a2.boxes[1]),
                  FadeIn(a2.boxes[3]),
                  FadeIn(a2.boxes[4]))

        self.wait(2)

        root_index = Text(rf'root_index = 1', color=WHITE, font_size=20).move_to(DOWN*2.25).to_edge(LEFT, buff=0.25)
        heap_size = Text(rf'heap_size = 7', color=WHITE, font_size=20).move_to(DOWN*2.75).to_edge(LEFT, buff=0.25)

        code_arrow = Arrow(start=ORIGIN, end=RIGHT*1, stroke_width=10,
                           max_tip_length_to_length_ratio=0.5,
                           max_stroke_width_to_length_ratio=20, color=virdis_colors[0]).move_to(UP*2.17+LEFT*6.5)

        lc = Text(rf'left_child_index = 3', color=WHITE, font_size=20).move_to(DOWN*3.25).to_edge(LEFT, buff=0.25)
        rc = Text(rf'right_child_index = 4', color=WHITE, font_size=20).move_to(DOWN*3.75).to_edge(LEFT, buff=0.25)

        self.play(FadeIn(root_index))
        self.play(FadeIn(heap_size))

        self.wait(1)


        self.play(FadeIn(code_arrow))

        self.wait(1)

        self.play(FadeIn(lc))

        self.wait(1)


        self.play(code_arrow.animate.shift(DOWN*0.2))
        self.wait(1)

        self.play(FadeIn(rc))


        larger = Text(rf'larger_value_index = 1', color=WHITE, font_size=20).move_to(DOWN*2.25).to_edge(LEFT, buff=4)

        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(1)
        self.play(FadeIn(larger))

        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.59))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.78))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.78))
        self.wait(1)


class Setup3(Scene):
    def construct(self):
        nums = [1, 5, 6, 3, 2, 7, 4]

        b1 = BinaryTree(nums, False)
        a1 = Array(nums, False)

        b2 = BinaryTree(nums, True)
        a2 = Array(nums, True)

        nums = [1, 5, 7, 3, 2, 6, 4]

        b3 = BinaryTree(nums, False)
        a3 = Array(nums, False)



        self.play(AnimationGroup(*[FadeIn(element) for element in a1.everything]))
        self.play(AnimationGroup(*[FadeIn(element) for element in b1.everything]))

        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b2.everything]))
        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a3.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b3.everything]))

        self.play(AnimationGroup(*[FadeOut(element) for element in a2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a3.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b3.everything]))

        self.play(AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in a1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5*RIGHT+UP)) for element in b1.everything]))


        self.wait(2)

        code1 = ImageMobject("images/code1.png").move_to(LEFT*2.5+UP)
        code1.scale(0.6)

        self.play(FadeIn(code1))

        self.wait(2)

        self.play(Indicate(b1.nodes[2]),
                  Indicate(b1.nodes[5]),
                  Indicate(b1.nodes[6]),
                  FadeIn(b2.nodes[2]),
                  FadeIn(b2.nodes[5]),
                  FadeIn(b2.nodes[6]))

        self.play(Indicate(a1.boxes[2]),
                  Indicate(a1.boxes[5]),
                  Indicate(a1.boxes[6]),
                  FadeIn(a2.boxes[2]),
                  FadeIn(a2.boxes[5]),
                  FadeIn(a2.boxes[6]))

        self.wait(2)

        root_index = Text(rf'root_index = 2', color=WHITE, font_size=20).move_to(DOWN*2.25).to_edge(LEFT, buff=0.25)
        heap_size = Text(rf'heap_size = 7', color=WHITE, font_size=20).move_to(DOWN*2.75).to_edge(LEFT, buff=0.25)

        code_arrow = Arrow(start=ORIGIN, end=RIGHT*1, stroke_width=10,
                           max_tip_length_to_length_ratio=0.5,
                           max_stroke_width_to_length_ratio=20, color=virdis_colors[0]).move_to(UP*2.17+LEFT*6.5)

        lc = Text(rf'left_child_index = 5', color=WHITE, font_size=20).move_to(DOWN*3.25).to_edge(LEFT, buff=0.25)
        rc = Text(rf'right_child_index = 6', color=WHITE, font_size=20).move_to(DOWN*3.75).to_edge(LEFT, buff=0.25)

        self.play(FadeIn(root_index))
        self.play(FadeIn(heap_size))

        self.wait(1)


        self.play(FadeIn(code_arrow))

        self.wait(1)

        self.play(FadeIn(lc))

        self.wait(1)


        self.play(code_arrow.animate.shift(DOWN*0.2))
        self.wait(1)

        self.play(FadeIn(rc))


        larger1 = Text(rf'larger_value_index = 2', color=WHITE, font_size=20).move_to(DOWN*2.25).to_edge(LEFT, buff=4)
        larger2 = Text(rf'larger_value_index = 5', color=WHITE, font_size=20).move_to(DOWN*2.25).to_edge(LEFT, buff=4)

        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(1)
        self.play(FadeIn(larger1))

        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.59))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.19))
        self.wait(1)

        self.play(ReplacementTransform(larger1, larger2))
        self.wait(1)


        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.59))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.78))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(1)

        # swap
        self.play(Indicate(root_index))
        self.play(Indicate(a1.indices[2]),
                  Indicate(b1.indices[2]))

        self.play(Indicate(larger2))
        self.play(Indicate(a1.indices[5]),
                  Indicate(b1.indices[5]))

        self.play(Indicate(a1.values[2]),
                  Indicate(b1.values[2]))

        self.play(Indicate(a1.values[5]),
                  Indicate(b1.values[5]))

        self.wait(1)

        self.play(Transform(b1.values[2], b3.values[2]),
                  Transform(b1.values[5], b3.values[5]),
                  Transform(a1.values[2], a3.values[2]),
                  Transform(a1.values[5], a3.values[5]))
        self.wait(1)

        self.play(code_arrow.animate.shift(DOWN*0.59))
        self.wait(1)


class Setup4(Scene):
    def construct(self):

        nums1 = [1, 5, 6, 3, 2, 7, 4]
        nums2 = [1, 5, 7, 3, 2, 6, 4]
        nums3 = [7, 5, 1, 3, 2, 6, 4]
        nums4 = [7, 5, 6, 3, 2, 1, 4]

        b1 = BinaryTree(nums1, False)
        a1 = Array(nums1, False)

        b2 = BinaryTree(nums2, False)
        a2 = Array(nums2, False)

        b3 = BinaryTree(nums3, False)
        a3 = Array(nums3, False)

        b4 = BinaryTree(nums4, False)
        a4 = Array(nums4, False)

        b1c = BinaryTree(nums1, True)
        a1c = Array(nums1, True)

        b2c = BinaryTree(nums2, True)
        a2c = Array(nums2, True)

        b3c = BinaryTree(nums3, True)
        a3c = Array(nums3, True)

        b4c = BinaryTree(nums4, True)
        a4c = Array(nums4, True)

        self.play(AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a3.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b3.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a4.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b4.everything]))

        self.play(AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a1c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b1c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a2c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b2c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a3c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b3c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a4c.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b4c.everything]))

        self.play(AnimationGroup(*[FadeOut(element) for element in a2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a3.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b3.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a4.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b4.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a1c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b1c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a2c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a3c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b3c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a4c.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b4c.everything]))


        code2 = ImageMobject("images/code2.png").move_to(LEFT*2.5+UP*2.75)
        code2.scale(0.6)

        self.play(FadeIn(code2))

        self.wait(2)

        code_arrow = Arrow(start=ORIGIN, end=RIGHT*1, stroke_width=10,
                           max_tip_length_to_length_ratio=0.5,
                           max_stroke_width_to_length_ratio=20, color=virdis_colors[0]).move_to(UP*2.17+LEFT*6.5)

        self.play(FadeIn(code_arrow))

        # self.play(code_arrow.animate.shift(DOWN*0.2))

        self.wait(2)


        index1 = Text(rf'index = 2', color=WHITE, font_size=20).move_to(UP*1.4).to_edge(LEFT, buff=0.25)
        self.play(FadeIn(index1))

        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.19))

        self.wait(1)

        self.play(Indicate(b1.nodes[2]),
                  Indicate(b1.nodes[5]),
                  Indicate(b1.nodes[6]),
                  FadeIn(b1c.nodes[2]),
                  FadeIn(b1c.nodes[5]),
                  FadeIn(b1c.nodes[6]),
                  Indicate(a1.boxes[2]),
                  Indicate(a1.boxes[5]),
                  Indicate(a1.boxes[6]),
                  FadeIn(a1c.boxes[2]),
                  FadeIn(a1c.boxes[5]),
                  FadeIn(a1c.boxes[6]))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a1.values, a2.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b1.values, b2.values)]))

        self.wait(2)

        self.play(FadeOut(b1c.nodes[2]),
                  FadeOut(b1c.nodes[5]),
                  FadeOut(b1c.nodes[6]),
                  FadeOut(a1c.boxes[2]),
                  FadeOut(a1c.boxes[5]),
                  FadeOut(a1c.boxes[6]))

        self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.19))
        self.wait(2)

        index2 = Text(rf'index = 1', color=WHITE, font_size=20).move_to(UP*1.4).to_edge(LEFT, buff=0.25)

        self.play(ReplacementTransform(index1, index2))

        self.wait(2)
        self.play(code_arrow.animate.shift(DOWN*0.19))

        self.play(Indicate(b1.nodes[1]),
                  Indicate(b1.nodes[3]),
                  Indicate(b1.nodes[4]),
                  FadeIn(b1c.nodes[1]),
                  FadeIn(b1c.nodes[3]),
                  FadeIn(b1c.nodes[4]),
                  Indicate(a1.boxes[1]),
                  Indicate(a1.boxes[3]),
                  Indicate(a1.boxes[4]),
                  FadeIn(a1c.boxes[1]),
                  FadeIn(a1c.boxes[3]),
                  FadeIn(a1c.boxes[4]))


        self.wait(2)

        self.play(FadeOut(b1c.nodes[1]),
                  FadeOut(b1c.nodes[3]),
                  FadeOut(b1c.nodes[4]),
                  FadeOut(a1c.boxes[1]),
                  FadeOut(a1c.boxes[3]),
                  FadeOut(a1c.boxes[4]))

        self.wait(2)


        self.play(code_arrow.animate.shift(UP * 0.19))

        index3 = Text(rf'index = 0', color=WHITE, font_size=20).move_to(UP * 1.4).to_edge(LEFT, buff=0.25)

        self.play(ReplacementTransform(index2, index3))

        self.wait(2)
        self.play(code_arrow.animate.shift(DOWN * 0.19))

        self.play(Indicate(b1.nodes[0]),
                  Indicate(b1.nodes[1]),
                  Indicate(b1.nodes[2]),
                  FadeIn(b1c.nodes[0]),
                  FadeIn(b1c.nodes[1]),
                  FadeIn(b1c.nodes[2]),
                  Indicate(a1.boxes[0]),
                  Indicate(a1.boxes[1]),
                  Indicate(a1.boxes[2]),
                  FadeIn(a1c.boxes[0]),
                  FadeIn(a1c.boxes[1]),
                  FadeIn(a1c.boxes[2]))

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a2.values, a3.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b2.values, b3.values)]))

        self.wait(2)

        self.play(FadeOut(b1c.nodes[0]),
                  FadeOut(b1c.nodes[1]),
                  FadeOut(b1c.nodes[2]),
                  FadeOut(a1c.boxes[0]),
                  FadeOut(a1c.boxes[1]),
                  FadeOut(a1c.boxes[2]))

        self.play(Indicate(b1.nodes[2]),
                  Indicate(b1.nodes[5]),
                  Indicate(b1.nodes[6]),
                  FadeIn(b1c.nodes[2]),
                  FadeIn(b1c.nodes[5]),
                  FadeIn(b1c.nodes[6]),
                  Indicate(a1.boxes[2]),
                  Indicate(a1.boxes[5]),
                  Indicate(a1.boxes[6]),
                  FadeIn(a1c.boxes[2]),
                  FadeIn(a1c.boxes[5]),
                  FadeIn(a1c.boxes[6]))

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a3.values, a4.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b3.values, b4.values)]))

        self.wait(2)

class Setup5(Scene):
    def construct(self):



        nums0 = [1, 5, 6, 3, 2, 7, 4]
        nums1 = [7, 5, 6, 3, 2, 1, 4]
        nums2  = [4, 5, 6, 3, 2, 1, 7]
        nums3  = [6, 5, 4, 3, 2, 1, 7]
        nums4  = [1, 5, 4, 3, 2, 6, 7]
        nums5  = [5, 1, 4, 3, 2, 6, 7]
        nums6  = [5, 3, 4, 1, 2, 6, 7]
        nums7  = [2, 3, 4, 1, 5, 6, 7]
        nums8  = [4, 3, 2, 1, 5, 6, 7]
        nums9  = [1, 3, 2, 4, 5, 6, 7]
        nums10  = [3, 1, 2, 4, 5, 6, 7]
        nums11  = [2, 1, 3, 4, 5, 6, 7]
        nums12  = [1, 2, 3, 4, 5, 6, 7]

        bgray = BinaryTree(nums12, False, True)
        agray =      Array(nums12, False, True)


        b0 = BinaryTree(nums0, True)
        a0 =      Array(nums0, True)
        b1 = BinaryTree(nums1, True)
        a1 =      Array(nums1, True)
        b2 = BinaryTree(nums2, True)
        a2 =      Array(nums2, True)
        b3 = BinaryTree(nums3, True)
        a3 =      Array(nums3, True)
        b4 = BinaryTree(nums4, True)
        a4 =      Array(nums4, True)
        b5 = BinaryTree(nums5, True)
        a5 =      Array(nums5, True)
        b6 = BinaryTree(nums6, True)
        a6 =      Array(nums6, True)
        b7 = BinaryTree(nums7, True)
        a7 =      Array(nums7, True)
        b8 = BinaryTree(nums8, True)
        a8 =      Array(nums8, True)
        b9 = BinaryTree(nums9, True)
        a9 =      Array(nums9, True)
        b10 = BinaryTree(nums10, True)
        a10 =      Array(nums10, True)
        b11 = BinaryTree(nums11, True)
        a11 =      Array(nums11, True)
        b12 = BinaryTree(nums12, True)
        a12 =      Array(nums12, True)

        a_mobj_list = [a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]
        b_mobj_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12]


        self.play(AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a0.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b0.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b1.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b2.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a3.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b3.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a4.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b4.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a5.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b5.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a6.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b6.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a7.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b7.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a8.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b8.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a9.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b9.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a10.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b10.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a11.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b11.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in a12.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in b12.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in agray.everything]),
                  AnimationGroup(*[(element.animate.shift(4.5 * RIGHT + UP)) for element in bgray.everything]))


        self.play(AnimationGroup(*[FadeOut(element) for element in a1.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b1.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b2.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a3.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b3.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a4.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b4.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a5.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b5.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a6.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b6.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a7.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b7.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a8.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b8.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a9.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b9.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a10.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b10.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a11.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b11.everything]),
                  AnimationGroup(*[FadeOut(element) for element in a12.everything]),
                  AnimationGroup(*[FadeOut(element) for element in b12.everything]),
                  AnimationGroup(*[FadeOut(element) for element in agray.everything]),
                  AnimationGroup(*[FadeOut(element) for element in bgray.everything]))


        code3 = ImageMobject("images/code3_2.png").move_to(LEFT*2.5+UP*1.5)
        code3.scale(0.6)

        self.play(FadeIn(code3))

        self.wait(2)

        code_arrow = Arrow(start=ORIGIN, end=RIGHT*1, stroke_width=10,
                           max_tip_length_to_length_ratio=0.5,
                           max_stroke_width_to_length_ratio=20, color=virdis_colors[0]).move_to(UP*.81+LEFT*6.5)

        self.play(FadeIn(code_arrow))

        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a0.values, a1.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b0.values, b1.values)]))

        self.wait(2)
        self.play(code_arrow.animate.shift(DOWN*0.39))

        self.wait(2)

        # ============= START ============= #
        index1 = Text(rf'heap_end_index = 6 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(FadeIn(index1))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a1.values, a2.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b1.values, b2.values)]))

        self.wait(2)

        self.play(FadeIn(agray.boxes[6]),
                  FadeIn(bgray.nodes[6]))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a2.values, a3.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b2.values, b3.values)]))
        self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        # =============  END  ============= #



        # ============= START ============= #
        index2 = Text(rf'heap_end_index = 5 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(ReplacementTransform(index1, index2))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a3.values, a4.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b3.values, b4.values)]))

        self.wait(2)


        self.play(FadeIn(agray.boxes[5]),
                  FadeIn(bgray.nodes[5]))
        self.wait(2)
        #
        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a4.values, a5.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b4.values, b5.values)]))
        self.wait(2)
        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a5.values, a6.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b5.values, b6.values)]))
        self.wait(2)

        #
        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        # =============  END  ============= #




        # # ============= START ============= #
        index3 = Text(rf'heap_end_index = 4 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(ReplacementTransform(index2, index3))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a6.values, a7.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b6.values, b7.values)]))

        self.wait(2)


        self.play(FadeIn(agray.boxes[4]),
                  FadeIn(bgray.nodes[4]))

        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a7.values, a8.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b7.values, b8.values)]))
        self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        # =============  END  ============= #



        # ============= START ============= #
        index4 = Text(rf'heap_end_index = 3 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(ReplacementTransform(index3, index4))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a8.values, a9.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b8.values, b9.values)]))

        self.wait(2)


        self.play(FadeIn(agray.boxes[3]),
                  FadeIn(bgray.nodes[3]))

        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a9.values, a10.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b9.values, b10.values)]))
        self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        # =============  END  ============= #


        # ============= START ============= #
        index5 = Text(rf'heap_end_index = 2 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(ReplacementTransform(index4, index5))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a10.values, a11.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b10.values, b11.values)]))

        self.wait(2)


        self.play(FadeIn(agray.boxes[2]),
                  FadeIn(bgray.nodes[2]))

        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)
        #
        # self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a9.values, a10.values)]),
        #           AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b9.values, b10.values)]))
        # self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        # =============  END  ============= #


        # ============= START ============= #
        index6 = Text(rf'heap_end_index = 1 (heap_size)', color=WHITE, font_size=20).move_to(DOWN*1.2).to_edge(LEFT, buff=0.25)
        self.play(ReplacementTransform(index5, index6))
        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.39))
        self.wait(2)

        self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a11.values, a12.values)]),
                  AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b11.values, b12.values)]))

        self.wait(2)


        self.play(FadeIn(agray.boxes[1]),
                  FadeIn(bgray.nodes[1]))

        self.wait(2)

        self.play(code_arrow.animate.shift(DOWN*0.60))
        self.wait(2)
        #
        # self.play(AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(a9.values, a10.values)]),
        #           AnimationGroup(*[ReplacementTransform(e1, e2) for e1, e2 in zip(b9.values, b10.values)]))
        # self.wait(2)

        self.play(code_arrow.animate.shift(UP*0.99))
        self.wait(2)
        self.play(FadeOut(code_arrow),
                  FadeOut(index6))
        self.wait(2)

        self.play(FadeIn(agray.boxes[0]),
                  FadeIn(bgray.nodes[0]))

        self.wait(2)

        for i in range(7):
            self.play(FadeOut(agray.boxes[i]),
                      FadeOut(bgray.nodes[i]))
        self.wait(2)

        # =============  END  ============= #
