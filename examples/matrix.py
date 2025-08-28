from typing import Callable

from manim import *
from colour import Color
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.scene.scene import Scene
from manim.utils.rate_functions import smooth

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


# manim -pqh --disable_caching matrix.py circuit
class matrix(Scene):
    def construct(self):

        m0 = Matrix([[1, 1, 0], [2, 2, 1], [0, 1, -2]]).move_to([-1.5, 2, 0])
        m1 = Matrix([['x'], ['y'], ['z']]).next_to(m0, RIGHT)
        sign = Text('=', font_size=32).next_to(m1, RIGHT)
        m2 = Matrix([[1], [5], [0]]).next_to(sign, RIGHT)

        rect_1 = Rectangle(color=VIR_1, height=1.5, width=8).move_to([0, 2.4, 0])
        rect_2 = Rectangle(color=VIR_1, height=1.5, width=6).move_to([0, -1, 0])

        rect_3 = Rectangle(color=VIR_1, height=1, width=6).move_to([0, -2.5, 0])
        rect_4 = Rectangle(color=VIR_1, height=0.8, width=8).move_to([0, 2.0, 0])

        eqn = VGroup(m0, m1, sign, m2)

        trans_1 = Matrix([[2, 2, 1, 5], [1, 1, 0, 1]]).move_to([0, -1, 0])        
        trans_2 = Matrix([[2, 2, 1, 5], [-2, -2, 0, -2]]).move_to([0, -1, 0])        

        line = Line([-3, 0, 0], [3, 0, 0]).move_to([0, -1.9, 0])   
        res_1 = Matrix([[0, 0, 1, 3]]).move_to([0, -2.5, 0])   

        trans_eqn_1_0 = Tex("-2").move_to([-3, -1.4, 0])
        trans_eqn_1_1 = Tex("-2").move_to([-3, -1.4, 0])
        trans_eqn_1_2 = Tex("-2").move_to([-3, -1.4, 0])
        trans_eqn_1_3 = Tex("-2").move_to([-3, -1.4, 0])


        m0_1 = Matrix([[1, 1, 0], [0, 0, 1], [0, 1, -2]]).move_to([-1.5, 2, 0])
        m2_1 = Matrix([[1], [3], [0]]).next_to(sign, RIGHT)

        m0_2 = Matrix([[1, 1, 0], [0, 0, 1], [0, 1, 0]]).move_to([-1.5, 2, 0])
        m2_2 = Matrix([[1], [3], [6]]).next_to(sign, RIGHT)


        m0_3 = Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]]).move_to([-1.5, 2, 0])
        m2_3 = Matrix([[-5], [3], [6]]).next_to(sign, RIGHT)

        m0_4 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).move_to([-1.5, 2, 0])
        m2_4 = Matrix([[-5], [6], [3]]).next_to(sign, RIGHT)

        m0_5 = Matrix([[-5, 6, 0], [-10, 12, 3], [0, 6, -6]]).move_to([-1.5, 2, 0])

        m0_6 = Matrix([["-5 + 6 + 0"], ["-10 + 12 + 3"], ["0 + 6 + -6"]]).move_to([-1.5, 2, 0])


        final_res_1 = Tex("x = -5").move_to([0, 0, 0])
        final_res_2 = Tex("y = 6").next_to(final_res_1, DOWN)
        final_res_3 = Tex("z = 3").next_to(final_res_2, DOWN)
        final_res = VGroup(final_res_1, final_res_2, final_res_3)

        m0.save_state()
        m2.save_state()

        self.play(DrawBorderThenFill(eqn, run_time=1))
        self.wait(2)
        self.play(FadeIn(rect_1, run_time=1))
        self.wait(2)
        self.play(DrawBorderThenFill(trans_1, run_time=1),
                  Transform(rect_1, rect_2, run_time=1))
        self.play(FadeOut(rect_1, run_time=1))
        self.wait(1)
        self.play(DrawBorderThenFill(trans_eqn_1_0, run_time=1))
        self.wait(1)
        self.play(trans_eqn_1_0.animate.move_to([-2.1, -1.4, 0]),
                  trans_eqn_1_1.animate.move_to([-.75, -1.4, 0]),
                  trans_eqn_1_2.animate.move_to([0.5, -1.4, 0]),
                  trans_eqn_1_3.animate.move_to([1.9, -1.4, 0]))
        self.play(FadeOut(trans_eqn_1_0, run_time=0.2),
                  FadeOut(trans_eqn_1_1, run_time=0.2),
                  FadeOut(trans_eqn_1_2, run_time=0.2),
                  FadeOut(trans_eqn_1_3, run_time=0.2),
                  Transform(trans_1, trans_2, run_time=0.6))
        
        self.wait(1)
        self.play(DrawBorderThenFill(line, run_time=0.5))
        self.wait(1)
        self.play(DrawBorderThenFill(res_1, run_time=1))
        self.wait(1)
        self.play(FadeIn(rect_3, run_time=1))
        self.play(Transform(rect_3, rect_4, run_time=1),
                  Transform(m0, m0_1, run_time=2),
                  Transform(m2, m2_1, run_time=2))
        self.play(FadeOut(rect_3, run_time=1),
                  FadeOut(trans_1, run_time=1),
                  FadeOut(res_1, run_time=1),
                  FadeOut(line, run_time=1))
        self.play(Transform(m0, m0_2, run_time=1),
                  Transform(m2, m2_2, run_time=1))
        self.play(Transform(m0, m0_3, run_time=1),
                  Transform(m2, m2_3, run_time=1))
        self.play(Transform(m0, m0_4, run_time=1),
                  Transform(m2, m2_4, run_time=1))
        self.wait(1)
        self.play(DrawBorderThenFill(final_res, run_time=1))
        self.wait(1)
        self.play(Restore(m0, run_time=1),
                  Restore(m2, run_time=1))

        mf = Matrix([[-5], [6], [3]]).next_to(m0, RIGHT)


        self.wait(1)
        # self.play(Transform(m0, m0_5, run_time=1),
        #           FadeOut(m1, run_time=1))

        self.play(sign.animate.next_to(mf, RIGHT),
                  m2.animate.move_to([3.25, 2, 0.0]),
                  Transform(m1, mf, run_time=1))

        # self.play(m2.animate.next_to(sign, RIGHT))
        self.wait(1)

        self.play(Transform(m0, m0_5, run_time=1),
                  FadeOut(m1, run_time=1))

        
        self.wait(1)
        self.play(Transform(m0, m0_6, run_time=1),
                  sign.animate.next_to(m0_6, RIGHT),
                  m2.animate.move_to([1.5, 2, 0.0]))

        self.wait(1)




class circuit(Scene):
    def construct(self):

        #------------------------------------------
        # Setup
        #------------------------------------------

        image = ImageMobject("images/simple_circuit.png")
        image.height = 3
        self.add(image)

        R1 = Tex(r'$\text{R}_{1}$', font_size=48).move_to([-1.9, 0.7, 0])
        R2 = Tex(r'$\text{R}_{2}$', font_size=48).move_to([0.4, 0, 0])
        R3 = Tex(r'$\text{R}_{3}$', font_size=48).move_to([1.6, 0.7, 0])
        Vin = Tex(r'$\text{V}_{\text{in}}$', font_size=48).move_to([-3, 0, 0])
        Vdep = Tex(r'$\text{2V}_{1}$', font_size=48).move_to([4.6, 0, 0])
        Vdep_0 = Tex(r'$\text{2V}_{1}$', font_size=48).move_to([4.6, 0, 0])
        V1_0 = Tex(r'$\text{+  V}_{1}\text{  -}$', font_size=48, color=VIR_1).move_to([-2.1, 1.8, 0])
        V1 = Tex(r'$\text{+  V}_{1}\text{  -}$', font_size=48, color=WHITE).move_to([-2.1, 1.8, 0])
        V3 = Tex(r'$\text{+  V}_{3}\text{  -}$', font_size=48, color=VIR_5).move_to([1.5, 1.8, 0])
        V2_V = Tex(r'$\text{V}_{2}$', font_size=48, color=VIR_3).move_to([-0.8, 0, 0])
        V2_P = Tex(r'$\text{+}$', font_size=48, color=VIR_3).next_to(V2_V, UP)
        V2_N = Tex(r'$\text{-}$', font_size=48, color=VIR_3).next_to(V2_V, DOWN)
        V2 = VGroup(V2_V, V2_P, V2_N)

        Vdep_0[0][1:3].set_color(VIR_1)

        circuit = VGroup(R1, R2, R3, Vin, Vdep, V1, V2, V3)

        self.add(R1, R2, R3, Vin, Vdep, V1)

        self.play(Transform(V1, V1_0),
                  DrawBorderThenFill(V2),
                  DrawBorderThenFill(V3),
                  Transform(Vdep, Vdep_0))
        self.wait(1)


        a1 = Arc(radius=0.4, arc_center=[0,0,0], start_angle=-PI/4, angle=3*PI/2, stroke_width=3, color=VIR_7).move_to([-2, -0.5+1, 0])
        a2 = Arc(radius=0.4, arc_center=[0,0,0], start_angle=-PI/4, angle=3*PI/2, stroke_width=3, color=VIR_9).move_to([1.6, -0.5+1, 0])
        a3 = Arc(radius=0.8, arc_center=[0,0,0], start_angle=-PI/4, angle=3*PI/2, stroke_width=3, color=VIR_11).move_to([0, -0.25+1, 0]).stretch_to_fit_width(4.5)


        a1.flip(UP)
        # a = ArcBetweenPoints(1*LEFT, 1*RIGHT, radius=1.1, angle=PI)
        a1.add_tip(tip_width=0.3)
        a2.add_tip(tip_width=0.3)
        a3.add_tip(tip_width=0.3)

        # self.play(circuit.move_to([-1, -1, 0]))
        self.play(AnimationGroup(*[(element.animate.shift(1*UP)) for element in circuit]),
                  image.animate.shift(1*UP))
        self.wait(1)
        # self.play(AnimationGroup(*[FadeIn(square) for square in squares], lag_ratio=0.15))
        self.play(DrawBorderThenFill(a1),
                  DrawBorderThenFill(a2))
        
        self.wait(1)


        #------------------------------------------
        # Equation 1
        #------------------------------------------
        
        # eqn_1_1 = Tex(r'$V_{1} = V_{in} + V_1$', font_size=48).move_to([-2, -1, 0])
        # eqn_1_2 = Tex(r'$\text{V}_{\text{in}} = \text{V}_{1} + \text{V}_{2}$', font_size=48).move_to([-2, -1, 0])
        # eqn_1_2 = Tex(r'$\text{V}_{\text{in}} = \text{V}_{1} + \text{V}_{2}$', font_size=48).move_to([-2, -1, 0])

        # 

        # eqn_1_1[0][1:2].set_color(YELLOW)
        # eqn_1_2[0][2].set_color(RED)

        eqn_1_1 = Tex(r'$\text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        eqn_1_2 = Tex(r'$\text{V}_{\text{in}} = \text{V}_{1}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        eqn_1_3 = Tex(r'$\text{V}_{\text{in}} = \text{V}_{1} + \text{V}_{2}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        # self.add(index_labels(eqn_1_1[0]))

        eqn_1_2[0][4:6].set_color(VIR_1)
        eqn_1_3[0][4:6].set_color(VIR_1)
        eqn_1_3[0][7:].set_color(VIR_3)



        self.play(Indicate(a1, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(Indicate(Vin, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(FadeIn(eqn_1_1, run_time=1))
        self.play(Indicate(V1, scale_factor=1.1, color=VIR_1, run_time=1))
        self.play(FadeIn(eqn_1_2, run_time=1))
        self.play(Indicate(V2, scale_factor=1.1, color=VIR_3, run_time=1))
        self.play(FadeIn(eqn_1_3, run_time=1))


#         tex = MathTex(r'f(x) &= 3 + 2 + 1\\ &= 5 + 1 \\ &= 6', font_size=96)
#         self.add(tex)

        self.wait(1)

        #------------------------------------------
        # Equation 2
        #------------------------------------------

        eqn_2_1 = Tex(r'$2\text{V}_{\text{1}}$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])
        eqn_2_2 = Tex(r'$2\text{V}_{\text{1}} + \text{V}_{3}$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])
        eqn_2_3 = Tex(r'$2\text{V}_{\text{1}} + \text{V}_{3} = \text{V}_{2}$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])
        # self.add(index_labels(eqn_2_3[0]))

        eqn_2_1[0][1:3].set_color(VIR_1)

        eqn_2_2[0][1:3].set_color(VIR_1)
        eqn_2_2[0][4:6].set_color(VIR_5)

        eqn_2_3[0][1:3].set_color(VIR_1)
        eqn_2_3[0][4:6].set_color(VIR_5)
        eqn_2_3[0][7:].set_color(VIR_3)

        self.play(Indicate(a2, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(Indicate(Vdep, scale_factor=1.1, color=VIR_1, run_time=1))
        self.play(FadeIn(eqn_2_1, run_time=1))
        self.play(Indicate(V3, scale_factor=1.1, color=VIR_5, run_time=1))
        self.play(FadeIn(eqn_2_2, run_time=1))
        self.play(Indicate(V2, scale_factor=1.1, color=VIR_3, run_time=1))
        self.play(FadeIn(eqn_2_3, run_time=1))


        #------------------------------------------
        # Equation 3
        #------------------------------------------


        eqn_3_1 = Tex(r'$2\text{V}_{\text{1}}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        eqn_3_2 = Tex(r'$2\text{V}_{\text{1}} + \text{V}_{\text{3}}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        eqn_3_3 = Tex(r'$2\text{V}_{\text{1}} + \text{V}_{\text{3}} + \text{V}_{\text{1}}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        eqn_3_4 = Tex(r'$2\text{V}_{\text{1}} + \text{V}_{\text{3}} + \text{V}_{\text{1}} = \text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        # self.add(index_labels(eqn_3_4[0]))

        eqn_3_1[0][1:3].set_color(VIR_1)

        eqn_3_2[0][1:3].set_color(VIR_1)
        eqn_3_2[0][4:6].set_color(VIR_5)

        eqn_3_3[0][1:3].set_color(VIR_1)
        eqn_3_3[0][4:6].set_color(VIR_5)
        eqn_3_3[0][7:9].set_color(VIR_1)

        eqn_3_4[0][1:3].set_color(VIR_1)
        eqn_3_4[0][4:6].set_color(VIR_5)
        eqn_3_4[0][7:9].set_color(VIR_1)
        # eqn_3_4[0][10:].set_color(VIR_1)

        self.play(FadeOut(a1),
                  FadeOut(a2))
        
        self.play(DrawBorderThenFill(a3))
        self.wait(1)


        # self.play(FadeIn(eqn_3_4, run_time=1))

        self.play(Indicate(a3, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(Indicate(Vdep, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(FadeIn(eqn_3_1, run_time=1))
        self.play(Indicate(V3, scale_factor=1.1, color=VIR_5, run_time=1))
        self.play(FadeIn(eqn_3_2, run_time=1))
        self.play(Indicate(V1, scale_factor=1.1, color=VIR_1, run_time=1))
        self.play(FadeIn(eqn_3_3, run_time=1))
        self.play(Indicate(Vin, scale_factor=1.1, color=WHITE, run_time=1))
        self.play(FadeIn(eqn_3_4, run_time=1))


        self.play(FadeOut(eqn_1_1, run_time=1),
                  FadeOut(eqn_1_2, run_time=1),
                  FadeOut(eqn_2_1, run_time=1),
                  FadeOut(eqn_2_2, run_time=1),
                  FadeOut(eqn_3_1, run_time=1),
                  FadeOut(eqn_3_2, run_time=1),
                  FadeOut(eqn_3_3, run_time=1))


        self.play(FadeOut(a3))

        eqn_1_4 = Tex(r'$1\text{V}_{1} + 1\text{V}_{2} + 0\text{V}_{3}  = \text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        eqn_2_4 = Tex(r'$2\text{V}_{1} - 1\text{V}_{2} + 1\text{V}_{3} = 0$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])
        eqn_3_5 = Tex(r'$3\text{V}_{1} + 0\text{V}_{2} + 1\text{V}_{3} = \text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])

        eqn_1_4[0][1:3].set_color(VIR_1)
        eqn_1_4[0][5:7].set_color(VIR_3)
        eqn_1_4[0][9:11].set_color(VIR_5)
        eqn_2_4[0][1:3].set_color(VIR_1)
        eqn_2_4[0][5:7].set_color(VIR_3)
        eqn_2_4[0][9:11].set_color(VIR_5)
        eqn_3_5[0][1:3].set_color(VIR_1)
        eqn_3_5[0][5:7].set_color(VIR_3)
        eqn_3_5[0][9:11].set_color(VIR_5)

        eqn_1 = eqn_1_3.copy()
        eqn_2 = eqn_2_3.copy()
        eqn_3 = eqn_3_4.copy()
        


        self.play(Transform(eqn_1_3, eqn_1_4, run_time=1),
                  Transform(eqn_2_3, eqn_2_4, run_time=1),
                  Transform(eqn_3_4, eqn_3_5, run_time=1))
        

        m0 = Matrix([[1, 1, 0], [2, -1, 1], [3, 0, 1]]).to_edge(LEFT).shift([3, -2, 0])
        m1 = Matrix([[r'\text{V}_{1}'], [r'\text{V}_{2}'], [r'\text{V}_{3}']]).next_to(m0, RIGHT)
        sign = Text('=', font_size=32).next_to(m1, RIGHT)
        m2 = Matrix([[r'\text{V}_{\text{in}}'], [0], [r'\text{V}_{\text{in}}']]).next_to(sign, RIGHT)
        
        # self.add(index_labels(m1[0]))
        m1[0][0:1].set_color(VIR_1)
        m1[0][1:2].set_color(VIR_3)
        m1[0][2:3].set_color(VIR_5)
        self.wait(1)

        self.play(Transform(eqn_1_3, m0),
                  Transform(eqn_2_3, m1),
                  Transform(eqn_3_4, m2),
                  FadeIn(sign))
        self.wait(1)


        #------------------------------------------
        # First Pass
        #------------------------------------------
        labels = VGroup(R1, R2, R3, Vin, Vdep, V1)
        matrixes = VGroup(eqn_1_3, eqn_2_3, eqn_3_4, sign)
        self.play(AnimationGroup(*[(FadeOut(element)) for element in circuit]),
                  AnimationGroup(*[(FadeOut(element)) for element in labels]),
                  FadeOut(image),
                  AnimationGroup(*[element.animate.shift(4*UP) for element in matrixes]))
        
        self.wait(1)

        l1 = Tex("1)", font_size=36).to_edge(LEFT).shift([2.2, 2.8, 0])
        l2 = Tex("2)", font_size=36).next_to(l1, 1.75*DOWN)
        l3 = Tex("3)", font_size=36).next_to(l2, 1.75*DOWN)

        minus = Tex("-", font_size=64).shift([-3, -1.95, 0])

        self.play(FadeIn(l1),
                  FadeIn(l2),
                  FadeIn(l3))

        self.wait(1)

        op1 = Matrix([[3, 0, 1, r'\text{V}_{\text{in}}'], [2, -1, 1, 0]]).shift([0, -1.5, 0])
        res1 = Matrix([[1, 1, 0, r'\text{V}_{\text{in}}']]).shift([0, -3.1, 0])
        l4 = Tex(r'\text{Row 3 - Row 2}', font_size=36).next_to(op1, 1*UP)
        line = Line([-3, 0, 0], [3, 0, 0]).move_to([0, -2.5, 0])

        self.play(FadeIn(l4))
        self.play(FadeIn(op1))
        self.play(FadeIn(line),
                  FadeIn(minus))
        self.play(FadeIn(res1))

        rect_1 = Rectangle(color=VIR_1, height=1.1, width=5.5).move_to([0, -3.1, 0])
        rect_2 = Rectangle(color=VIR_1, height=1.1, width=8).move_to([0.15, 1.1, 0])


        self.play(FadeIn(rect_1))

        m0_1 = Matrix([[1, 1, 0], [2, -1, 1], [1, 1, 0]]).to_edge(LEFT).shift([3, 2, 0])

        self.play(Transform(rect_1, rect_2))
        eqn_1_3.save_state()
        self.play(Transform(eqn_1_3, m0_1))

        self.play(FadeOut(line),
                  FadeOut(l4),
                  FadeOut(op1),
                  FadeOut(minus),
                  FadeOut(res1))

        self.play(FadeOut(rect_1))
        self.play(Indicate(l1))
        self.play(Indicate(l3))


        self.wait(1)
        self.play(Restore(eqn_1_3, run_time=1))
        self.wait(1)
        A = Matrix([[1, 1, 0], [2, -1, 1], [3, 0, 1]]).shift([0.5, -1, 0])
        A_label = Tex(r'\text{A = }').next_to(A, LEFT)
        self.play(DrawBorderThenFill(A),
                  DrawBorderThenFill(A_label))
        A_rank = Tex(r'\text{Rank(A) = 2}').next_to(A, DOWN)
        A_text = Tex(r'\text{The Matrix A only has 2 linearly independent rows}').next_to(A_rank, DOWN)
        self.play(DrawBorderThenFill(A_rank),
                  DrawBorderThenFill(A_text))
        
        self.wait(5)

        self.play(FadeOut(A),
                  FadeOut(A_label),
                  FadeOut(A_rank),
                  FadeOut(A_text),
                  FadeOut(eqn_1_3),
                  FadeOut(eqn_2_3),
                  FadeOut(eqn_3_4),
                  FadeOut(sign),
                  FadeOut(l1),
                  FadeOut(l2),
                  FadeOut(l3))
        
        self.play(FadeIn(image),
                  AnimationGroup(*[(FadeIn(element)) for element in circuit]),
                  FadeIn(eqn_1),
                  FadeIn(eqn_2),
                  FadeIn(eqn_3))
        
        self.wait(1)

        self.play(FadeIn(a3))
        self.play(Indicate(a3))
        self.play(FadeOut(a3))

        self.play(FadeOut(eqn_3))


        #------------------------------------------
        # Current Sum
        #------------------------------------------


        a_i1 = Arrow(start=LEFT, end=RIGHT, stroke_width=3, color=VIR_7).move_to([2, 0, 0]).next_to(V1, 0.25*UP)
        a_i2 = Arrow(start=UP, end=DOWN, stroke_width=3, color=VIR_9).move_to([2, -1, 0]).next_to(V2, 0.25*LEFT)
        a_i3 = Arrow(start=LEFT, end=RIGHT, stroke_width=3, color=VIR_11).move_to([2, -2, 0]).next_to(V3, 0.25*UP)

        i1 = Tex(r'$\text{i}_1$', font_size=48, color=VIR_7).next_to(a_i1, 0.1*UP)
        i2 = Tex(r'$\text{i}_2$', font_size=48, color=VIR_9).next_to(a_i2, 0.2*LEFT)
        i3 = Tex(r'$\text{i}_3$', font_size=48, color=VIR_11).next_to(a_i3, 0.1*UP)

        self.play(DrawBorderThenFill(i1),
                  DrawBorderThenFill(i2),
                  DrawBorderThenFill(i3),
                  DrawBorderThenFill(a_i1),
                  DrawBorderThenFill(a_i2),
                  DrawBorderThenFill(a_i3))
        

        eqn_4_1 = Tex(r'$\text{i}_1$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        eqn_4_2 = Tex(r'$\text{i}_1 = \text{i}_2$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
        eqn_4_3 = Tex(r'$\text{i}_1 = \text{i}_2 + \text{i}_3$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])

        eqn_4_4 = Tex(r'$\frac{\text{V}_1}{\text{R}_1} = \frac{\text{V}_2}{\text{R}_2} + \frac{\text{V}_3}{\text{R}_3}$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])
    
        eqn_4_1[0][0:2].set_color(VIR_7)

        eqn_4_2[0][0:2].set_color(VIR_7)
        eqn_4_2[0][3:5].set_color(VIR_9)

        eqn_4_3[0][0:2].set_color(VIR_7)
        eqn_4_3[0][3:5].set_color(VIR_9)
        eqn_4_3[0][6:8].set_color(VIR_11)

        eqn_4_4[0][0:2].set_color(VIR_1)
        eqn_4_4[0][6:8].set_color(VIR_3)
        eqn_4_4[0][12:14].set_color(VIR_5)


        self.play(Indicate(i1, color=WHITE),
                  Indicate(a_i1, color=WHITE))
        self.play(FadeIn(eqn_4_1, run_time=1))
        self.play(Indicate(i2, color=WHITE),
                  Indicate(a_i2, color=WHITE))
        self.play(FadeIn(eqn_4_2, run_time=1))
        self.play(Indicate(i3, color=WHITE),
                  Indicate(a_i3, color=WHITE))
        self.play(FadeIn(eqn_4_3, run_time=1))
        self.play(FadeOut(eqn_4_1, run_time=1),
                  FadeOut(eqn_4_2, run_time=1))
                  
        # self.add(index_labels(eqn_4_4[0]))
        self.play(Transform(eqn_4_3, eqn_4_4, run_time=1))

        self.wait(1)

        # self.play(Transform(eqn_4_3, eqn_4_4, run_time=1))

        # eqn_1_4 = Tex(r'$1\text{V}_{1} + 1\text{V}_{2} + 0\text{V}_{2}  = \text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        # eqn_2_4 = Tex(r'$2\text{V}_{1} - 1\text{V}_{2} + 1\text{V}_{3} = 0$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])

        # eqn_1_4 = Tex(r'$1\text{V}_{1} + 1\text{V}_{2} + 0\text{V}_{2}  = \text{V}_{\text{in}}$', font_size=48).to_edge(LEFT).shift([4, -1, 0])
        # eqn_2_4 = Tex(r'$2\text{V}_{1} - 1\text{V}_{2} + 1\text{V}_{3} = 0$', font_size=48).to_edge(LEFT).shift([4, -1.75, 0])
        eqn_4_5 = Tex(r'$\frac{\text{V}_1}{\text{R}_1} - \frac{\text{V}_2}{\text{R}_2} - \frac{\text{V}_3}{\text{R}_3} = 0$', font_size=48).to_edge(LEFT).shift([4, -2.5, 0])

        eqn_4_5[0][0:2].set_color(VIR_1)
        eqn_4_5[0][6:8].set_color(VIR_3)
        eqn_4_5[0][12:14].set_color(VIR_5)


        self.play(Transform(eqn_1, eqn_1_4, run_time=1),
                  Transform(eqn_2, eqn_2_4, run_time=1),
                  Transform(eqn_4_3, eqn_4_5, run_time=1))
        

        m0_new = Matrix([[1, 1, 0], [2, -1, 1], [r'\tfrac{1}{\text{R}_1}', r'\tfrac{-1}{\text{R}_2}', r'\tfrac{-1}{\text{R}_3}']]).to_edge(LEFT).shift([3, -2, 0])
        m1_new = Matrix([[r'\text{V}_{1}'], [r'\text{V}_{2}'], [r'\text{V}_{3}']]).next_to(m0_new, RIGHT)
        sign_new = Text('=', font_size=32).next_to(m1_new, RIGHT)
        m2_new = Matrix([[r'\text{V}_{\text{in}}'], [0], [0]]).next_to(sign_new, RIGHT)
        
        m1_new[0][0:1].set_color(VIR_1)
        m1_new[0][1:2].set_color(VIR_3)
        m1_new[0][2:3].set_color(VIR_5)

        self.wait(1)

        self.play(Transform(eqn_1, m0_new, run_time=1),
                  Transform(eqn_2, m1_new, run_time=1),
                  Transform(eqn_4_3, m2_new, run_time=1),
                  FadeIn(sign_new))
        
        currents = VGroup(i1, a_i1, i2, a_i2, i3, a_i3)

        self.wait(1)

        l1 = Tex("1)", font_size=36).to_edge(LEFT).shift([2.2, 1.8, 0])
        l2 = Tex("2)", font_size=36).next_to(l1, 1.75*DOWN)
        l3 = Tex("3)", font_size=36).next_to(l2, 1.75*DOWN)

        matrixes_new = VGroup(eqn_1, eqn_2, eqn_4_3, sign_new)

        self.play(FadeOut(image),
                  AnimationGroup(*[(FadeOut(element)) for element in currents]),
                  AnimationGroup(*[(FadeOut(element)) for element in circuit]),
                  AnimationGroup(*[element.animate.shift(3*UP) for element in matrixes_new]))

        self.play(FadeIn(l1),
                  FadeIn(l2),
                  FadeIn(l3))
        

        m0_new_1 = Matrix([[1, 1, 0], [3, 0, 1], [r'\tfrac{1}{\text{R}_1}', r'\tfrac{-1}{\text{R}_2}', r'\tfrac{-1}{\text{R}_3}']]).to_edge(LEFT).shift([3, 1, 0])
        m2_new_1 = Matrix([[r'\text{V}_{\text{in}}'], [r'\text{V}_{\text{in}}'], [0]]).next_to(sign_new, RIGHT)
        op_new_1 = Tex(r'\text{Row 2 = Row 1 + Row 2}', font_size=36).shift(1*DOWN)

        self.play(FadeIn(op_new_1))
        self.play(Transform(eqn_1, m0_new_1, run_time=1),
                  Transform(eqn_4_3, m2_new_1, run_time=1))
        
        m0_new_2 = Matrix([[1, 1, 0], 
                           [r'3+\tfrac{\text{R}_3}{\text{R}_1}', r'\tfrac{\text{-R}_3}{\text{R}_2}', 0], 
                           [r'\tfrac{1}{\text{R}_1}', r'\tfrac{-1}{\text{R}_2}', r'\tfrac{-1}{\text{R}_3}']]
                           ).to_edge(LEFT).shift([2, 1, 0])
        m2_new_2 = Matrix([[r'\text{V}_{\text{in}}'], [r'\text{V}_{\text{in}}'], [0]]).next_to(sign_new, RIGHT)
        op_new_2 = Tex(r'$\text{Row 2 = Row 2 + R}_3\text{(Row 3)}$', font_size=36).shift(1*DOWN)

        self.play(Transform(op_new_1, op_new_2, run_time=1))
        self.play(Transform(eqn_1, m0_new_2, run_time=1),
                  Transform(eqn_4_3, m2_new_2, run_time=1),
                #   sign_new.animate.shift(RIGHT),
                #   eqn_2.animate.shift(RIGHT),
                #   eqn_4_3.animate.shift(RIGHT),
                  l1.animate.shift(1*LEFT),
                  l2.animate.shift(1*LEFT),
                  l3.animate.shift(1*LEFT))


    # m0_new_2  m1_new  sign_new  m2_new_2
    # eqn_1     eqn_2             eqn_4_3



        op_new_2 = Tex(r'\text{Row 2 = Row 1 + Row 2}', font_size=36).shift(1*DOWN)
        
        m0_new_3 = Matrix([[1, 1, 0], 
                           [r'3+\tfrac{\text{R}_3}{\text{R}_1}+\tfrac{\text{R}_3}{\text{R}_2}', 0, 0], 
                           [r'\tfrac{1}{\text{R}_1}', r'\tfrac{-1}{\text{R}_2}', r'\tfrac{-1}{\text{R}_3}']]
                           ).to_edge(LEFT).shift([1, 1, 0])
        m2_new_3 = Matrix([[r'\text{V}_{\text{in}}'], [r'\text{V}_{\text{in}} (1 + \tfrac{\text{R}_3}{\text{R}_2})'], [0]]).next_to(sign_new, RIGHT)
        op_new_3 = Tex(r'$\text{Row 2 = Row 2 + } \tfrac{\text{R}_3}{\text{R}_2} \text{(Row 1)}$', font_size=36).shift(1*DOWN)

        self.play(Transform(op_new_1, op_new_3, run_time=1))
        self.play(Transform(eqn_1, m0_new_3, run_time=1),
                  Transform(eqn_4_3, m2_new_3, run_time=1),
                  l1.animate.shift(1*LEFT),
                  l2.animate.shift(1*LEFT),
                  l3.animate.shift(1*LEFT))
                #   sign_new.animate.shift(RIGHT),
                #   eqn_2.animate.shift(LEFT))
                #   eqn_4_3.animate.shift(RIGHT))
        
        # self.add(m2_new_3)
        res_left = Tex(r'$\text{V}_1 = $', font_size=64).to_edge(LEFT).shift([1.5, -2.5, 0])
        res_right = Tex(r'$\text{V}_{\text{in}}$', font_size=64).next_to(res_left, 0.5*RIGHT)
        res_v1 = Tex(r'$\frac{(1 + \tfrac{\text{R}_3}{\text{R}_2})}{3 + \tfrac{\text{R}_3}{\text{R}_1} + \tfrac{\text{R}_3}{\text{R}_2}}$', font_size=64).to_edge(LEFT).shift([4.25, -2, 0])
        res_v2 = Tex(r'$\frac{(1 + \tfrac{2000\Omega}{1000\Omega})}{3 + \tfrac{2000\Omega}{500\Omega} + \tfrac{2000\Omega}{1000\Omega}}$', font_size=64).to_edge(LEFT).shift([4.25, -2, 0])
        res_v3 = Tex(r'$\frac{(1 + 2)}{3 + 4 + 2}$', font_size=64).to_edge(LEFT).shift([4.25, -2.5, 0])
        res_v4 = Tex(r'$\frac{1}{3}$', font_size=64).to_edge(LEFT).shift([3.25, -2.5, 0])

        res_left[0][0:2].set_color(VIR_1)


        self.play(FadeOut(op_new_1))
        self.play(DrawBorderThenFill(res_left),
                  DrawBorderThenFill(res_right),
                  DrawBorderThenFill(res_v1))

        
        R1_val = Tex(r'$\text{R}_1 = 500\Omega $', font_size=48).to_edge(LEFT).shift([9, -1.5, 0])
        R2_val = Tex(r'$\text{R}_2 = 1000\Omega $', font_size=48).to_edge(LEFT).shift([9, -2, 0])
        R3_val = Tex(r'$\text{R}_3 = 2000\Omega $', font_size=48).to_edge(LEFT).shift([9, -2.5, 0])

        # self.play(res_v1.animate.shift(2.5*LEFT))

        self.play(DrawBorderThenFill(R1_val),
                  DrawBorderThenFill(R2_val),
                  DrawBorderThenFill(R3_val))
        


        self.wait(1)
        self.play(Transform(res_v1, res_v2))
        self.wait(1)
        self.play(Transform(res_v1, res_v3))
        self.wait(1)
        self.play(Transform(res_v1, res_v4),
                  res_right.animate.shift(.5*RIGHT))
        self.wait(1)
        self.play(res_left.animate.shift(3*RIGHT+1*UP),
                  res_v1.animate.shift(3*RIGHT+1*UP),
                  res_right.animate.shift(3*RIGHT+1*UP))
        
        res_2 = Tex(r'$\text{V}_2 = \frac{2}{3} \text{V}_{\text{in}}$', font_size=64).to_edge(LEFT).shift([4.5, -2.5, 0])
        res_3 = Tex(r'$\text{V}_3 = 0 \text{V}_{\text{in}}$', font_size=64).to_edge(LEFT).shift([4.5, -3.5, 0])
        res_2[0][0:2].set_color(VIR_3)
        res_3[0][0:2].set_color(VIR_5)

        self.play(DrawBorderThenFill(res_2),
                  DrawBorderThenFill(res_3))

        self.wait(2)

        final_1 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).to_edge(LEFT).shift([0.0, 1, 0])
        final_2 = Matrix([[r'\text{V}_{1}'], [r'\text{V}_{2}'], [r'\text{V}_{3}']]).next_to(final_1, RIGHT)
        final_3 = Text('=', font_size=32).next_to(final_2, RIGHT)
        final_4 = Matrix([[r'\text{V}_{\text{in}} \frac{\text{R}_1(\text{R}_2+\text{R}_3)}{3 \text{R}_1 \text{R}_2 + \text{R}_1 \text{R}_3 + \text{R}_2 \text{R}_3}'], [r'\text{V}_{\text{in}} \frac{\text{R}_2(2\text{R}_1+\text{R}_3)}{3 \text{R}_1 \text{R}_2 + \text{R}_1 \text{R}_3 + \text{R}_2 \text{R}_3}'], [r'-\text{V}_{\text{in}} \frac{\text{R}_3(2\text{R}_1-\text{R}_2)}{3 \text{R}_1 \text{R}_2 + \text{R}_1 \text{R}_3 + \text{R}_2 \text{R}_3}']], v_buff=1.6).next_to(final_3, RIGHT)

        final_2[0][0:1].set_color(VIR_1)
        final_2[0][1:2].set_color(VIR_3)
        final_2[0][2:3].set_color(VIR_5)

        self.play(FadeOut(eqn_1),
                  FadeOut(eqn_2),
                  FadeOut(eqn_4_3),
                  FadeOut(sign_new),
                  FadeOut(l1),
                  FadeOut(l2),
                  FadeOut(l3),
                  FadeOut(R1_val),
                  FadeOut(R2_val),
                  FadeOut(R3_val),
                  FadeOut(res_2),
                  FadeOut(res_3),
                  FadeOut(res_left),
                  FadeOut(res_right),
                  FadeOut(res_v1))

        self.play(DrawBorderThenFill(final_1),
                  DrawBorderThenFill(final_2),
                  DrawBorderThenFill(final_3),
                  DrawBorderThenFill(final_4))


        self.wait(1)

class intro_text_1(Scene):
    def construct(self):
        t1 = Text(r'Algebra', font_size=48, color=VIR_1).shift(0*LEFT + 3.5*UP)
        t2 = Text(r'Trigonometry', font_size=48, color=VIR_2).shift(0*LEFT + 2.5*UP)
        t3 = Text(r'Calculus', font_size=48, color=VIR_3).shift(0*LEFT + 1.5*UP)
        t4 = Text(r'Linear Algebra', font_size=48, color=VIR_4).shift(0*LEFT + 0.5*UP)
        t5 = Text(r'Infinite Series', font_size=48, color=VIR_5).shift(0*LEFT + -0.5*UP)
        t6 = Text(r'Probability', font_size=48, color=VIR_6).shift(0*LEFT + -1.5*UP)
        t7 = Text(r'Differential Equations', font_size=48, color=VIR_7).shift(0*LEFT + -2.5*UP)
        t8 = Text(r'...', font_size=48, color=VIR_8).shift(0*LEFT + -3.5*UP)

        fade_time = 0.5
        self.play(FadeIn(t1, run_time=fade_time))
        self.play(FadeIn(t2, run_time=fade_time))
        self.play(FadeIn(t3, run_time=fade_time))
        self.play(FadeIn(t4, run_time=fade_time))
        self.play(FadeIn(t5, run_time=fade_time))
        self.play(FadeIn(t6, run_time=fade_time))
        self.play(FadeIn(t7, run_time=fade_time))
        self.play(FadeIn(t8, run_time=fade_time))



        self.wait(3)

        self.play(FadeIn(t1, run_time=1),
                  FadeIn(t2, run_time=1),
                  FadeIn(t3, run_time=1),
                  FadeIn(t4, run_time=1),
                  FadeIn(t5, run_time=1),
                  FadeIn(t6, run_time=1),
                  FadeIn(t7, run_time=1),
                  FadeIn(t8, run_time=1))

        self.play(Indicate(t4, color=WHITE))
        self.wait(2)


class intro_text_2(Scene):
    def construct(self):
        math_text = Text(r'Math Problem', font_size=36).shift(3*LEFT + 2*UP)
        engineering_text = Text(r'Engineering Problem', font_size=36).shift(3*RIGHT + 2*UP)

        arrow_math = Arrow(start=UP, end=DOWN, stroke_width=5, color=VIR_1).next_to(math_text, DOWN)
        solved_text_1 = Text(r'Solved Problem', font_size=36).next_to(arrow_math, DOWN)

        solution_text = Text("Solution", font_size=32, color=VIR_1).next_to(arrow_math, 2*RIGHT)


        self.play(FadeIn(math_text, run_time=1))
        self.wait(1)
        self.play(FadeIn(arrow_math, run_time=1),
                  FadeIn(solution_text, run_time=1))
        self.wait(1)
        self.play(FadeIn(solved_text_1, run_time=1))
        self.wait(1)
        self.play(FadeIn(engineering_text, run_time=1))
        self.wait(1)
        self.play(arrow_math.animate.shift(6*RIGHT),
                  solution_text.animate.shift(6*RIGHT))
        self.wait(1)
        solved_text_2 = Text(r'Solved Problem', font_size=36).next_to(arrow_math, DOWN)
        self.play(FadeIn(solved_text_2, run_time=1))
        self.wait(2)


class circuit_test(Scene):
    def construct(self):
        res_v1 = Tex(r'$\text{V}_1 = \frac{\text{V}_{\text{in}} (1 + \frac{\text{R}_3}{\text{R}_2})}{3 + \frac{\text{R}_3}{\text{R}_1} + \frac{\text{R}_3}{\text{R}_2}}$', font_size=48).shift(2*UP+3*LEFT)


        res_v2 = Tex(r'$\text{V}_1 = \frac{\text{V}_{\text{in}} (1 + \tfrac{\text{R}_3}{\text{R}_2})}{3 + \tfrac{\text{R}_3}{\text{R}_1} + \tfrac{\text{R}_3}{\text{R}_2}}$', font_size=48).shift(2*UP+3*RIGHT)

        res_v3 = Tex(r'$\text{V}_1 = \tfrac{\text{V}_{\text{in}} (1 + \frac{\text{R}_3}{\text{R}_2})}{3 + \frac{\text{R}_3}{\text{R}_1} + \frac{\text{R}_3}{\text{R}_2}}$', font_size=48).shift(2*DOWN+3*LEFT)

        res_v4 = Tex(r'$\text{V}_1 = \tfrac{\text{V}_{\text{in}} (1 + \tfrac{\text{R}_3}{\text{R}_2})}{3 + \tfrac{\text{R}_3}{\text{R}_1} + \tfrac{\text{R}_3}{\text{R}_2}}$', font_size=48).shift(2*DOWN+3*RIGHT)

        self.add(res_v1, res_v2, res_v3, res_v4)





