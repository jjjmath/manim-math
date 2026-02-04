from manim import *
import numpy as np

class BasicVectors(Scene):
    def construct(self):
        # 创建两个向量
        vec1 = Vector([3, 0, 0], color=BLUE)
        vec2 = Vector([3, 3*np.sqrt(3), 0], color=RED)
        vec3 = Vector([6, 0, 0], color=YELLOW)  # 2a
        line = Line(start=[3, 3*np.sqrt(3), 0], end=[6, 0, 0], color=GREEN)
        
        # 整体移动
        shift_amount = DOWN*2 + LEFT*2
        origin = np.array([0, 0, 0]) + shift_amount  # 原点位置
        
        vec1.shift(shift_amount)
        vec2.shift(shift_amount)
        vec3.shift(shift_amount)
        line.shift(shift_amount)
        
        # 标签
        vec1_label = MathTex(r"\vec{a}", color=BLUE).next_to(vec1.get_end(), UP)
        vec2_label = MathTex(r"\vec{b}", color=RED).next_to(vec2.get_end(), RIGHT)
        vec3_label = MathTex(r"2\vec{a}", color=YELLOW).next_to(vec3.get_end(), DOWN)
        
        # 创建动画轨迹的点
        # 直线的起点和终点（考虑shift后的位置）
        start_point = np.array([3, 3*np.sqrt(3), 0]) + shift_amount
        end_point = np.array([6, 0, 0]) + shift_amount
        
        # 创建alpha跟踪器
        alpha = ValueTracker(0)
        
        # 创建沿着直线移动的点
        point = always_redraw(
            lambda: Dot(
                start_point + alpha.get_value() * (end_point - start_point),
                color=ORANGE,
                radius=0.08
            )
        )
        
        # 点的标签
        point_label = always_redraw(
            lambda: MathTex("P").next_to(
                start_point + alpha.get_value() * (end_point - start_point),
                UP, buff=0.1
            ).scale(0.8)
        )
        
        # 创建从原点到P点的线段（跟随P点移动）
        line1 = always_redraw(
            lambda: Line(
                start=origin,
                end=start_point + alpha.get_value() * (end_point - start_point),
                color=PURPLE,
                stroke_width=6
            )
        )
        
        # 添加到场景
        self.play(Create(vec1), Write(vec1_label))
        self.wait(0.5)
        self.play(Create(vec2), Write(vec2_label))
        self.wait(1)
        self.play(Create(vec3), Write(vec3_label))
        self.wait(1)
        self.play(Create(line))
        self.wait(1)
        
        # 添加线段
        self.play(Create(line1))    
        self.wait(1)
        
        # 添加点
        self.add(point, point_label)
        
        # 让点沿着直线移动
        self.play(alpha.animate.set_value(1), run_time=3)
        self.play(alpha.animate.set_value(0.5), run_time=3)
        self.wait(2)