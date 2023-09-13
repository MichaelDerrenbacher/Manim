from typing import Callable
from manim import *
from colour import Color
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.scene.scene import Scene
from manim.utils.rate_functions import smooth


"""
ValueTracker are invisible mobjects that store numbers
    can animate modification of a parameter
"""
class static_plot(Scene):
    def construct(self):
        ax = Axes(tips=False, 
                  x_range=[-2, 2, 1], 
                  y_range=[0, -40, -20], 
                  x_length=10, 
                  y_length=6, 
                  axis_config={"include_numbers": True},
                  x_axis_config={"scaling": LogBase(custom_labels=True),
                                 "numbers_to_include": [0.01, 0.1, 1, 10, 100],},
                  y_axis_config={"numbers_to_include": [-0.001, -20, -40]},  # heheheh
                  )
        
        bode = ax.plot(lambda x: 20*(np.log10(1)-np.log10(np.sqrt(x**2 + 1))), color=VIR_5)
        plane = NumberPlane(
                        x_range=[0, 10, 1],
                        y_range=[0, 6, 1.5],

                        background_line_style={
                            "stroke_color": WHITE,
                            "stroke_width": 2,
                            "stroke_opacity": 0.3},

                        faded_line_ratio=5,
                        faded_line_style={
                            "stroke_color": WHITE,
                            "stroke_width": 1,
                            "stroke_opacity": 0.2}
        )
        
        self.add(plane, ax, bode)


class dynamic_plot(Scene):
    def construct(self):

        wo = ValueTracker(1)

        ax = Axes(tips=False, 
                  x_range=[-2, 2, 1], 
                  y_range=[0, -40, -20], 
                  x_length=10, 
                  y_length=6, 
                  axis_config={"include_numbers": True},
                  x_axis_config={"scaling": LogBase(custom_labels=True),
                                 "numbers_to_include": [0.01, 0.1, 1, 10, 100],},
                  y_axis_config={"numbers_to_include": [-0.001, -20, -40]},  # heheheh
                  )
        
        bode = ax.plot(lambda x: 20*(np.log10(1)-np.log10(np.sqrt((x/wo.get_value())**2 + 1))), color=VIR_5)
        plane = NumberPlane(
                        x_range=[0, 10, 2.5],
                        y_range=[0, 6, 1.5],

                        background_line_style={
                            "stroke_color": WHITE,
                            "stroke_width": 2,
                            "stroke_opacity": 0.3},

                        faded_line_ratio=5,
                        faded_line_style={
                            "stroke_color": WHITE,
                            "stroke_width": 1,
                            "stroke_opacity": 0.2}
        )
        x_label = Text("Frequency (Hz)", font_size=24).next_to(ax, DOWN)
        y_label = Text("Vout/Vin\n(dB)", font_size=24).next_to(ax, LEFT)
        
        plot = VGroup(plane, ax, bode, x_label, y_label)

        self.add(plane, ax, bode, x_label, y_label)

        self.play(AnimationGroup(FadeIn(plot)))
        self.wait(1)


        bode.add_updater(
            lambda mob: mob.become(ax.plot(lambda x: 20*(np.log10(1)-np.log10(np.sqrt((x/wo.get_value())**2 + 1))), color=VIR_5))
        )

        self.play(wo.animate.set_value(2))
        self.wait(0.1)
        self.play(wo.animate.set_value(0.5), rate_func=smooth)
        self.wait(0.2)
        self.play(wo.animate.set_value(1), rate_func=smooth)
        self.wait(0.1)

        #YAY



class dynamic_plot_clean(Scene):
    def construct(self):
        def semilogx(x_min, x_max, x_step, y_min, y_max, y_step, x_label="", y_label=""):
            """
            Make axis with x log scale and y linear scale
            """
            x_axis_numbers = np.logspace(x_min, x_max, int(((x_max-x_min)/x_step))+1)
            y_axis_numbers = np.linspace(y_min, y_max-0.001, int(((y_max-y_min)/y_step))+1) 
            #                                           ^ hack to make y_max number appear on axis

            # semilog x axes
            ax = Axes(
                tips=False,
                x_range=[x_min, x_max, x_step],
                y_range=[y_max, y_min, -y_step],  # flipped order to get axis on bottom
                x_length=10,
                y_length=6,
                axis_config={"include_numbers": True},
                x_axis_config={"scaling": LogBase(custom_labels=True),
                               "numbers_to_include": x_axis_numbers,},
                y_axis_config={"numbers_to_include": y_axis_numbers},
            )
            
            # background grid (is there a way to make this log scale?)
            plane = NumberPlane(
                x_range=[0, 10, 2.5],
                y_range=[0, 6, 1.5],

                background_line_style={
                    "stroke_color": WHITE,
                    "stroke_width": 2,
                    "stroke_opacity": 0.3},

                faded_line_ratio=5,
                faded_line_style={
                    "stroke_color": WHITE,
                    "stroke_width": 1,
                    "stroke_opacity": 0.2}
            )

            # x/y labels
            x_label_obj = Tex(x_label, font_size=48).next_to(ax, DOWN)
            y_label_obj = Tex(y_label, font_size=64).next_to(ax, LEFT)

            return [ax, plane, x_label_obj, y_label_obj]


        def calc_mag(w, wo):
            """
            RC circuit magnitiude equation
                20*log(1/(1+jw/wo))
            """
            return 20*(np.log10(1)-np.log10(np.sqrt((w/wo)**2 + 1)))  # could remove log10(1) term but keeping incase gain needed

        #------------------------------------------------
        # plot creation
        #------------------------------------------------
        # create animated variable
        wo = ValueTracker(1)

        # create plot
        [ax, plane, x_label, y_label] = semilogx(x_min=-2,
                                                 x_max=2,
                                                 x_step=1,
                                                 y_min=-40,
                                                 y_max=0,
                                                 y_step=20,
                                                 x_label=r"Frequency",
                                                 y_label=r'$\frac{\text{V}_\text{out}}{\text{V}_\text{in}}$')

        bode = ax.plot(lambda x: calc_mag(w=x, wo=wo.get_value()), color=BLUE)
        plot = VGroup(plane, ax, bode, x_label, y_label)

        #------------------------------------------------
        # create equations
        #------------------------------------------------
        # transfer function
        mag_eqn = Tex(r'$\frac{\text{V}_\text{out}}{\text{V}_\text{in}} = \frac{1}{1+s\text{RC}}$', font_size=48)

        # 1/omega label
        rc_label = Tex(r'$\text{RC }= $', font_size=32)

        # 1/omega value
        rc_number = DecimalNumber(
            1/wo.get_value(),
            num_decimal_places=3,
            font_size=32
        ).next_to(rc_label, RIGHT)
        
        rc_number.add_updater(
            lambda mob: mob.set_value(1/wo.get_value()).next_to(rc_label, RIGHT)
        )

        # RC = omega_value equation
        bottom_eqn = VGroup(rc_number, rc_label)

        equations = VGroup(mag_eqn, bottom_eqn)

        image = ImageMobject("rc_circuit.png")

        #------------------------------------------------
        # positioning/scaling 
        #------------------------------------------------
        image.height = 2.5
        plot.scale(0.65)
        plot.move_to([2.75, 0, 0])
        mag_eqn.move_to([-4, -.75, 0])
        bottom_eqn.next_to(mag_eqn, 3*DOWN)
        image.move_to([-4, 2, 0])

        # add all the groups to scene
        self.add(plot, equations, image)

        #------------------------------------------------
        # animations
        #------------------------------------------------
        self.play(AnimationGroup(FadeIn(plot, equations, image)))
        self.wait(1)

        bode.add_updater(
            lambda mob: mob.become(ax.plot(lambda x: calc_mag(w=x, wo=wo.get_value()), color=BLUE))
        )

        self.play(wo.animate.set_value(2))
        self.wait(0.1)
        self.play(wo.animate.set_value(0.5), rate_func=smooth)
        self.wait(0.2)
        self.play(wo.animate.set_value(1), rate_func=smooth)
        self.wait(0.1)
