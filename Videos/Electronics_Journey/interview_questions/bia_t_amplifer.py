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
16 VIRIDIS
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



class Setup1(Scene):
    def construct(self):
        cir = ImageMobject("images/circuit_full.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)
        cir_ac_1 = ImageMobject("images/circuit_AC_1.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)
        cir_ac_2 = ImageMobject("images/circuit_AC_2.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)
        cir_ac_3 = ImageMobject("images/circuit_AC_3.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)

        cir_dc_1 = ImageMobject("images/circuit_DC_1.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)
        cir_dc_2 = ImageMobject("images/circuit_DC_2.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)
        cir_dc_3 = ImageMobject("images/circuit_DC_3.png").move_to(1.5*UP).scale(1.5).set_z_index(-1)


        self.play(FadeIn(cir))
        self.wait(2)



        v_in1 = Tex('$V_{in1}$', font_size=36, color=VIR_1).move_to(UP*2.6+LEFT*3)
        v_in2 = Tex('$V_{in2}$', font_size=36, color=VIR_2).move_to(UP*0.5+LEFT*1.4)

        v_out = Tex('$V_{out}$', font_size=36, color=VIR_3).move_to(UP*1.4+RIGHT*4.6)

        v_m = Tex('$V_-$', font_size=36, color=VIR_5).move_to(UP*1.8+RIGHT*1.7)
        v_p = Tex('$V_+$', font_size=36, color=VIR_6).move_to(UP*1.0+RIGHT*1.7)


        c1 = Tex('$C_1$', font_size=36, color=VIR_7).move_to(UP*3.8+LEFT*2.1)
        r1 = Tex('$R_1$', font_size=36, color=VIR_8).move_to(UP*3.8+LEFT*0.6)
        r2 = Tex('$R_2$', font_size=36, color=VIR_9).move_to(UP*3.8+RIGHT*2.4)
        r3 = Tex('$R_3$', font_size=36, color=VIR_10).move_to(UP*1.7+LEFT*0.6)
        c2 = Tex('$C_2$', font_size=36, color=VIR_11).move_to(UP*0.35+RIGHT*1.35)

        voltages = VGroup(v_in1, v_in2, v_out, v_m, v_p)
        designators = VGroup(c1, r1, r2, r3, c2)


        text_1 = Tex(r'$ \text{Frequency} \rightarrow 0 $', font_size=48, color=WHITE).move_to(DOWN*2.5+RIGHT*0)
        text_2 = Tex(r'$ \text{Frequency} \rightarrow \infty $ ', font_size=48, color=WHITE).move_to(DOWN*2.5+RIGHT*0)

        vout_v1_1 = Tex(r'$ \frac{V_{out}}{V_{in1}} \right|_{V_{in2} = 0}$', font_size=48, color=WHITE).move_to(DOWN*1.5+LEFT*1)
        question_1 =  Tex(r'= ?', font_size=48, color=WHITE).next_to(vout_v1_1, RIGHT)
        vout_v1_1[0][0:4].set_fill(color=VIR_3)
        vout_v1_1[0][5:9].set_fill(color=VIR_1)
        vout_v1_1[0][11:15].set_fill(color=VIR_2)


        self.play(AnimationGroup(*[FadeIn(element) for element in designators], lag_ratio=0.2))
        self.play(AnimationGroup(*[FadeIn(element) for element in voltages], lag_ratio=0.2))
        self.wait(2)


        # AC
        self.play(FadeIn(cir_ac_1),
                  # FadeOut(cir),
                  FadeOut(v_in2),
                  FadeIn(vout_v1_1),
                  FadeIn(question_1))
        self.wait(2)

        self.play(FadeIn(cir_ac_2),
                  # FadeOut(cir_ac_1),
                  FadeIn(text_1))
        self.wait(2)

        self.play(FadeIn(cir_ac_3),
                  #FadeOut(cir_ac_2),
                  ReplacementTransform(text_1, text_2))
        self.wait(2)

        self.play(#FadeIn(cir_ac_1),
                  FadeOut(cir_ac_2),
                  FadeOut(cir_ac_3),
                  #FadeOut(cir_ac_3),
                  FadeOut(text_2))
        self.wait(2)



        # self.play(vout_v1_1.animate.shift(LEFT*5),
        #           question_1.animate.shift(LEFT*5))




        self.wait(2)


        # v_p_eqn = Tex(r'$ V_+ = 0 \therefore V_- = 0 $', font_size=48, color=WHITE).move_to(DOWN*1.5+LEFT*1)
        # # v_m_eqn = Tex(r'$ $', font_size=48, color=WHITE).next_to(v_p_eqn, RIGHT)
        # v_p_eqn[0][0:2].set_fill(color=VIR_6)
        # v_p_eqn[0][5:7].set_fill(color=VIR_5)
        #
        #
        # self.play(FadeIn(v_p_eqn))
        # self.wait(2)


        eqn_1 = Tex(r'$ = -V_{in1}\frac{Z_2}{Z_1} $', font_size=48, color=WHITE).move_to(DOWN*1.5+RIGHT*0.5)
        eqn_1[0][2:6].set_fill(color=VIR_1)

        self.play(vout_v1_1.animate.shift(LEFT),
                  ReplacementTransform(question_1, eqn_1))
        self.wait(2)

        # self.play(#FadeOut(v_p_eqn),
        #           eqn_1.animate.shift(UP))
        # self.wait(2)

        eqn_2 = Tex(r'$ Z_2 = R_2 $', font_size=48, color=WHITE).move_to(DOWN*2.5+LEFT*1)
        eqn_2[0][3:6].set_fill(color=VIR_9)

        self.play(FadeIn(eqn_2))
        self.wait(2)

        eqn_3 = Tex(r'$ Z_1 = \frac{1}{sC_1} + R_1$', font_size=48, color=WHITE).move_to(DOWN*3.5+LEFT*1.6)
        eqn_3[0][6:8].set_fill(color=VIR_7)
        eqn_3[0][9:12].set_fill(color=VIR_8)

        self.play(FadeIn(eqn_3))
        self.wait(2)


        eqn_4 = Tex(r'$ = \frac{sR_1C_1}{sC_1}$', font_size=48, color=WHITE).move_to(DOWN*3.5+RIGHT*1)
        eqn_4[0][2:4].set_fill(color=VIR_8)
        eqn_4[0][4:6].set_fill(color=VIR_7)
        eqn_4[0][8:10].set_fill(color=VIR_7)

        self.play(FadeIn(eqn_4))
        self.wait(2)


        eqn_5 = Tex(r'$ = -V_{in1}\frac{sR_2C_1}{sR_1C_1+1} $', font_size=48, color=WHITE).move_to(DOWN*1.5+RIGHT*1.1)
        eqn_5[0][2:6].set_fill(color=VIR_1)
        eqn_5[0][7:9].set_fill(color=VIR_9)
        eqn_5[0][9:11].set_fill(color=VIR_7)
        eqn_5[0][13:15].set_fill(color=VIR_8)
        eqn_5[0][15:17].set_fill(color=VIR_7)


        self.play(ReplacementTransform(eqn_1, eqn_5),
                  FadeOut(eqn_2),
                  FadeOut(eqn_3),
                  FadeOut(eqn_4))
        self.wait(2)


        self.play(FadeOut(cir_ac_1),
                  # FadeOut(cir_ac_2),
                  # FadeOut(cir_ac_3),
                  FadeOut(vout_v1_1),
                  # FadeOut(question_1),
                  FadeIn(v_in2),
                  FadeOut(eqn_5))
        self.wait(2)




class Setup2(Scene):
    def construct(self):
        cir = ImageMobject("images/circuit_full.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_1 = ImageMobject("images/circuit_AC_1.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_2 = ImageMobject("images/circuit_AC_2.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_3 = ImageMobject("images/circuit_AC_3.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)

        cir_dc_1 = ImageMobject("images/circuit_DC_1.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_dc_2 = ImageMobject("images/circuit_DC_2.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_dc_3 = ImageMobject("images/circuit_DC_3.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in1 = Tex('$V_{in1}$', font_size=36, color=VIR_1).move_to(UP * 2.6 + LEFT * 3)
        v_in2 = Tex('$V_{in2}$', font_size=36, color=VIR_2).move_to(UP * 0.5 + LEFT * 1.4)

        v_out = Tex('$V_{out}$', font_size=36, color=VIR_3).move_to(UP * 1.4 + RIGHT * 4.6)

        v_m = Tex('$V_-$', font_size=36, color=VIR_5).move_to(UP * 1.8 + RIGHT * 1.7)
        v_p = Tex('$V_+$', font_size=36, color=VIR_6).move_to(UP * 1.0 + RIGHT * 1.7)

        c1 = Tex('$C_1$', font_size=36, color=VIR_7).move_to(UP * 3.8 + LEFT * 2.1)
        r1 = Tex('$R_1$', font_size=36, color=VIR_8).move_to(UP * 3.8 + LEFT * 0.6)
        r2 = Tex('$R_2$', font_size=36, color=VIR_9).move_to(UP * 3.8 + RIGHT * 2.4)
        r3 = Tex('$R_3$', font_size=36, color=VIR_10).move_to(UP * 1.7 + LEFT * 0.6)
        c2 = Tex('$C_2$', font_size=36, color=VIR_11).move_to(UP * 0.35 + RIGHT * 1.35)

        voltages = VGroup(v_in1, v_in2, v_out, v_m, v_p)
        designators = VGroup(c1, r1, r2, r3, c2)

        text_1 = Tex(r'$ \text{Frequency} \rightarrow 0 $', font_size=48, color=WHITE).move_to(
            DOWN * 2.5 + RIGHT * 0)
        text_2 = Tex(r'$ \text{Frequency} \rightarrow \infty $ ', font_size=48, color=WHITE).move_to(
            DOWN * 2.5 + RIGHT * 0)

        vout_v1_1 = Tex(r'$ \frac{V_{out}}{V_{in1}} \right|_{V_{in2} = 0}$', font_size=48, color=WHITE).move_to(
            DOWN * 1.5 + LEFT * 1)
        question_1 = Tex(r'= ?', font_size=48, color=WHITE).next_to(vout_v1_1, RIGHT)
        vout_v1_1[0][0:4].set_fill(color=VIR_3)
        vout_v1_1[0][5:9].set_fill(color=VIR_1)
        vout_v1_1[0][11:15].set_fill(color=VIR_2)

        vout_v2_1 = Tex(r'$ \frac{V_{out}}{V_{in2}} \right|_{V_{in1} = 0}$', font_size=48, color=WHITE).move_to(
            DOWN * 1.5 + LEFT * 1)
        question_2 = Tex(r'= ?', font_size=48, color=WHITE).next_to(vout_v2_1, RIGHT)
        vout_v2_1[0][0:4].set_fill(color=VIR_3)
        vout_v2_1[0][5:9].set_fill(color=VIR_2)
        vout_v2_1[0][11:15].set_fill(color=VIR_1)

        self.play(AnimationGroup(*[FadeIn(element) for element in designators], lag_ratio=0.2))
        self.play(AnimationGroup(*[FadeIn(element) for element in voltages], lag_ratio=0.2))
        self.wait(2)


        # DC
        self.play(FadeIn(cir_dc_1),
                  # FadeOut(cir),
                  FadeOut(v_in1),
                  FadeIn(vout_v2_1),
                  FadeIn(question_2))
        self.wait(2)

        self.play(FadeIn(cir_dc_2),
                  # FadeOut(cir_ac_1),
                  FadeIn(text_1))
        self.wait(2)

        self.play(FadeIn(cir_dc_3),
                  #FadeOut(cir_ac_2),
                  ReplacementTransform(text_1, text_2))
        self.wait(2)

        self.play(#FadeIn(cir_dc_1),
                  FadeOut(cir_dc_2),
                  FadeOut(cir_dc_3),
                  #FadeOut(cir_dc_3),
                  FadeOut(text_2))
        self.wait(2)




        # V+ = V-
        eqn_1 = Tex(r'$V_+ = V- = V_{in2} \frac{\frac{1}{sC_2}}{R_3+\frac{1}{sC_2}} = V_{in2} \frac{1}{sR_3C_2+1}$', font_size=48, color=WHITE).move_to(DOWN * 2.5 + LEFT * 0.25)
        eqn_1[0][0:2].set_fill(color=VIR_6)
        eqn_1[0][3:5].set_fill(color=VIR_5)

        eqn_1[0][6:10].set_fill(color=VIR_2)
        eqn_1[0][13:15].set_fill(color=VIR_11)
        eqn_1[0][16:18].set_fill(color=VIR_10)
        eqn_1[0][22:24].set_fill(color=VIR_11)

        eqn_1[0][25:29].set_fill(color=VIR_2)
        eqn_1[0][32:34].set_fill(color=VIR_10)
        eqn_1[0][34:36].set_fill(color=VIR_11)

        self.play(FadeIn(eqn_1))
        self.wait(2)



        eqn_2 = Tex(r'$V_{out} = V_- + R_2 \frac{V_-}{\frac{1}{sC_1}+R_1} = V_- \left( \frac{sC_1R_2}{sR_1C_1+1} + 1 \right)$', font_size=48, color=WHITE).move_to(DOWN * 3.5 + LEFT * 0.25)
        eqn_2[0][0:4].set_fill(color=VIR_3)
        eqn_2[0][5:7].set_fill(color=VIR_5)
        eqn_2[0][8:10].set_fill(color=VIR_9)
        eqn_2[0][10:12].set_fill(color=VIR_5)
        eqn_2[0][16:18].set_fill(color=VIR_7)
        eqn_2[0][19:21].set_fill(color=VIR_8)
        eqn_2[0][22:24].set_fill(color=VIR_5)
        eqn_2[0][26:28].set_fill(color=VIR_7)
        eqn_2[0][28:30].set_fill(color=VIR_9)
        eqn_2[0][32:34].set_fill(color=VIR_8)
        eqn_2[0][34:36].set_fill(color=VIR_7)


        self.play(FadeIn(eqn_2))
        self.wait(2)


        eqn_3 = Tex(r'$ = V_{in2} \left( \frac{1}{sR_3C_2+1} \right) \left( \frac{sC_1R_2}{sR_1C_1+1} + 1 \right)$', font_size=48, color=WHITE).move_to(DOWN * 1.5 + RIGHT * 1.8)
        eqn_3[0][1:5].set_fill(color=VIR_2)
        eqn_3[0][9:11].set_fill(color=VIR_10)
        eqn_3[0][11:13].set_fill(color=VIR_11)
        eqn_3[0][18:20].set_fill(color=VIR_7)
        eqn_3[0][20:22].set_fill(color=VIR_9)
        eqn_3[0][24:26].set_fill(color=VIR_8)
        eqn_3[0][26:28].set_fill(color=VIR_7)

        self.play(ReplacementTransform(question_2, eqn_3),
                  FadeOut(eqn_1),
                  FadeOut(eqn_2),
                  vout_v2_1.animate.shift(2*LEFT))
        self.wait(2)

        eqn_f = Tex(r'$V_{out} = V_{in2} \left( \frac{1}{sR_3C_2+1} \right) \left( \frac{sC_1R_2}{sR_1C_1+1} + 1 \right) -V_{in1}\frac{sR_2C_1}{sR_1C_1+1}  $', font_size=48, color=WHITE).move_to(DOWN * 1.5)
        eqn_f[0][0:4].set_fill(color=VIR_3)
        x = 4
        eqn_f[0][1+x:5+x].set_fill(color=VIR_2)
        eqn_f[0][9+x:11+x].set_fill(color=VIR_10)
        eqn_f[0][11+x:13+x].set_fill(color=VIR_11)
        eqn_f[0][18+x:20+x].set_fill(color=VIR_7)
        eqn_f[0][20+x:22+x].set_fill(color=VIR_9)
        eqn_f[0][24+x:26+x].set_fill(color=VIR_8)
        eqn_f[0][26+x:28+x].set_fill(color=VIR_7)
        y = 36
        eqn_f[0][2+y:6+y].set_fill(color=VIR_1)
        eqn_f[0][7+y:9+y].set_fill(color=VIR_9)
        eqn_f[0][9+y:11+y].set_fill(color=VIR_7)
        eqn_f[0][13+y:15+y].set_fill(color=VIR_8)
        eqn_f[0][15+y:17+y].set_fill(color=VIR_7)

        self.play(FadeIn(eqn_f),
                  FadeOut(eqn_3),
                  FadeOut(vout_v2_1),
                  FadeOut(cir_dc_1),
                  FadeIn(v_in1))
        # self.add(Circle())

        self.wait(2)

        text_3 = Tex(r"$\text{If } V_{in1} \text{ is AC, and } V_{in2} \text{ is DC:}$").move_to(DOWN * 2.5)
        self.play(FadeIn(text_3))
        self.wait(2)

        eqn_f2 = Tex(r'$V_{out} = V_{in2} - V_{in1}\frac{R_2}{R_1}  $', font_size=48, color=WHITE).move_to(DOWN * 3.5)
        eqn_f2[0][0:4].set_fill(color=VIR_3)
        eqn_f2[0][5:9].set_fill(color=VIR_2)
        eqn_f2[0][10:14].set_fill(color=VIR_1)
        eqn_f2[0][14:16].set_fill(color=VIR_9)
        eqn_f2[0][17:19].set_fill(color=VIR_8)
        self.play(FadeIn(eqn_f2))

        self.wait(2)


        self.play(# FadeOut(eqn_3),
                  FadeOut(eqn_f),
                  FadeOut(eqn_f2),
                  FadeOut(text_3))
        self.wait(2)

        # self.play(FadeIn(text_1))


class Setup3(Scene):
    def construct(self):
        ac_res = ImageMobject("images/AC_res.png").move_to(1.5 * UP).scale(1.1).set_z_index(-1)
        self.play(FadeIn(ac_res))
        self.wait(2)

        problem_1 = Text("Which input would you say this transfer function corresponds to?", font_size=30).move_to(DOWN*1.5)
        self.play(FadeIn(problem_1))
        self.wait(2)
        self.play(FadeOut(problem_1))
        self.wait(2)


        self.play(FadeOut(ac_res))
        self.wait(2)


        dc_res = ImageMobject("images/DC_res.png").move_to(1.5 * UP).scale(1.1).set_z_index(-1)
        self.play(FadeIn(dc_res))
        self.play(FadeIn(problem_1))
        self.wait(2)
        self.play(FadeOut(problem_1))
        self.wait(2)


class Setup4(Scene):
    def construct(self):
        cir = ImageMobject("images/circuit_full.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_1 = ImageMobject("images/circuit_AC_1.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_2 = ImageMobject("images/circuit_AC_2.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_ac_3 = ImageMobject("images/circuit_AC_3.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)

        cir_dc_1 = ImageMobject("images/circuit_DC_1.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_dc_2 = ImageMobject("images/circuit_DC_2.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)
        cir_dc_3 = ImageMobject("images/circuit_DC_3.png").move_to(1.5 * UP).scale(1.5).set_z_index(-1)

        self.play(FadeIn(cir))
        self.wait(2)

        v_in1 = Tex('$V_{in1}$', font_size=36, color=VIR_1).move_to(UP * 2.6 + LEFT * 3)
        v_in2 = Tex('$V_{in2}$', font_size=36, color=VIR_2).move_to(UP * 0.5 + LEFT * 1.4)

        v_out = Tex('$V_{out}$', font_size=36, color=VIR_3).move_to(UP * 1.4 + RIGHT * 4.6)

        v_m = Tex('$V_-$', font_size=36, color=VIR_5).move_to(UP * 1.8 + RIGHT * 1.7)
        v_p = Tex('$V_+$', font_size=36, color=VIR_6).move_to(UP * 1.0 + RIGHT * 1.7)

        c1 = Tex('$C_1$', font_size=36, color=VIR_7).move_to(UP * 3.8 + LEFT * 2.1)
        r1 = Tex('$R_1$', font_size=36, color=VIR_8).move_to(UP * 3.8 + LEFT * 0.6)
        r2 = Tex('$R_2$', font_size=36, color=VIR_9).move_to(UP * 3.8 + RIGHT * 2.4)
        r3 = Tex('$R_3$', font_size=36, color=VIR_10).move_to(UP * 1.7 + LEFT * 0.6)
        c2 = Tex('$C_2$', font_size=36, color=VIR_11).move_to(UP * 0.35 + RIGHT * 1.35)

        voltages = VGroup(v_in1, v_in2, v_out, v_m, v_p)
        designators = VGroup(c1, r1, r2, r3, c2)

        self.play(AnimationGroup(*[FadeIn(element) for element in designators], lag_ratio=0.2))
        self.play(AnimationGroup(*[FadeIn(element) for element in voltages], lag_ratio=0.2))
        self.wait(2)


        problem_1 = Text("There are two input voltages to this circuit:\n  Which would you call the AC input?\n  Which would you call the DC input?", font_size=30).move_to(DOWN*1.5)
        self.play(FadeIn(problem_1))
        self.wait(2)
        self.play(FadeOut(problem_1))
        self.wait(2)

        problem_2 = Text("What do you think this circuit is for?", font_size=30).move_to(DOWN*1.5)
        self.play(FadeIn(problem_2))
        self.wait(2)
        self.play(FadeOut(problem_2))
        self.wait(2)

        problem_3 = Text("Can you derive the transfer function of the AC input?", font_size=30).move_to(DOWN*1.5)
        self.play(FadeIn(problem_3))
        self.wait(2)
        self.play(FadeOut(problem_3))
        self.wait(2)

        problem_4 = Text("Can you derive the transfer function of the DC input?", font_size=30).move_to(DOWN*1.5)
        self.play(FadeIn(problem_4))
        self.wait(2)
        self.play(FadeOut(problem_4))
        self.wait(2)