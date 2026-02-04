from manim import *
import numpy as np

class BasicVectors(Scene):
    def construct(self):
        # ====================== 常量定义 ======================
        VEC_A = np.array([3, 0, 0])  # 向量a
        VEC_B = np.array([3, 3*np.sqrt(3), 0])  # 向量b
        VEC_2A = 2 * VEC_A  # 向量2a
        SHIFT_AMOUNT = DOWN * 2 + LEFT * 2  # 位移向量
        
        # ====================== 创建图形元素 ======================
        # 1. 创建向量
        vec_a = Vector(VEC_A, color=BLUE)
        vec_b = Vector(VEC_B, color=RED)
        vec_2a = Vector(VEC_2A, color=YELLOW)
        
        # 2. 创建线段
        line_segment = Line(start=VEC_B, end=VEC_2A, color=GREEN)
        
        # 3. 位移所有元素
        for mobject in [vec_a, vec_b, vec_2a, line_segment]:
            mobject.shift(SHIFT_AMOUNT)
        
        # 4. 计算关键点
        origin = ORIGIN + SHIFT_AMOUNT  # 原点（位移后）
        start_point = VEC_B + SHIFT_AMOUNT  # 线段起点（b的终点）
        end_point = VEC_2A + SHIFT_AMOUNT  # 线段终点（2a的终点）
        
        # ====================== 标签和标注 ======================
        # 向量标签
        vec_a_label = MathTex(r"\vec{a}", color=BLUE).next_to(
            vec_a.get_end(), UP, buff=0.1
        )
        vec_b_label = MathTex(r"\vec{b}", color=RED).next_to(
            vec_b.get_end(), RIGHT, buff=0.1
        )
        vec_2a_label = MathTex(r"2\vec{a}", color=YELLOW).next_to(
            vec_2a.get_end(), DOWN, buff=0.1
        )
        
        # ====================== 动画相关 ======================
        # 1. Alpha跟踪器
        alpha_tracker = ValueTracker(0.1)
        
        # 2. 动态计算P点位置
        def get_point_position():
            """计算P点的当前位置"""
            return start_point + alpha_tracker.get_value() * (end_point - start_point)
        
        # 3. 移动的P点
        moving_point = always_redraw(
            lambda: Dot(
                get_point_position(),
                color=ORANGE,
                radius=DEFAULT_DOT_RADIUS * 1.2
            )
        )
        
        # 4. P点标签
        point_label = always_redraw(
            lambda: MathTex("P").scale(0.8).next_to(
                get_point_position(), UP, buff=0.1
            )
        )
        
        # 5. 从原点到P点的线段
        line_to_origin = always_redraw(
            lambda: Line(
                start=origin,
                end=get_point_position(),
                color=PURPLE,
                stroke_width=4,
                stroke_opacity=0.8
            )
        )
        
        # 6. 线段标签（可选）
        line_label = always_redraw(
            lambda: MathTex(r"\overrightarrow{OP}").scale(0.7).next_to(
                (origin + get_point_position()) / 2, LEFT, buff=0.1
            ).set_color(PURPLE)
        )
        
        # ====================== 动画序列 ======================
        # 第一阶段：显示基本图形
        self.play(
            LaggedStart(
                Create(vec_a),
                Create(vec_b),
                Create(vec_2a),
                lag_ratio=0.3
            ),
            run_time=2
        )
        
        self.play(
            LaggedStart(
                Write(vec_a_label),
                Write(vec_b_label),
                Write(vec_2a_label),
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        
        # 第二阶段：显示线段
        self.play(
            Create(line_segment),
            run_time=1
        )
        self.wait(0.5)
        
        # 第三阶段：显示动态线段
        self.play(
            Create(line_to_origin),
            Write(line_label),
            run_time=1
        )
        self.wait(0.5)
        
        # 第四阶段：添加移动点
        self.play(
            FadeIn(moving_point, scale=0.5),
            Write(point_label),
            run_time=1
        )
        
        # 第五阶段：移动点
        # 从0移动到1
        self.play(
            alpha_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=3
        )
        
        # 从1移动到0.5
        self.play(
            alpha_tracker.animate.set_value(0.5),
            rate_func=smooth,
            run_time=2
        )
        
        # 暂停观察
        self.wait(1)
        
        # 可选：添加数学表达式说明
        explanation = MathTex(
            r"P(t) &= \vec{b} + t(2\vec{a} - \vec{b}) \\",
            r"&= (1-t)\vec{b} + t(2\vec{a}) \\",
            r"t &\in [0, 1]"
        ).scale(0.6)
        
        explanation.to_edge(DOWN)
        explanation.set_color_by_tex_to_color_map({
            r"\vec{a}": BLUE,
            r"\vec{b}": RED,
            r"t": YELLOW
        })
        
        self.play(
            Write(explanation),
            run_time=2
        )
        self.wait(2)
        
        # 可选：高亮展示特定位置
        # 返回到0.75位置
        # self.play(
        #     alpha_tracker.animate.set_value(0.75),
        #     rate_func=smooth,
        #     run_time=2
        # )
        # self.wait(2)
