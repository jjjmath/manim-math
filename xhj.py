from manim import *
class AnimatedGraph(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 1],
            axis_config={"color": BLUE},
        )

        # Create the graph of the function y = x^2
        graph = axes.plot(lambda x: x**2, color=RED)

        # Create labels for the axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        # Create a title for the graph
        title = Text("Graph of $y = x^2$", font_size=24).to_edge(UP)

        # Animate the creation of the graph
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(title))
        self.wait(2)