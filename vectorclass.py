from manim import *
import numpy as np

class VectorDiagramConfig:
    """向量图配置类"""
    def __init__(
        self,
        vec_a=np.array([3, 0, 0]),
        vec_b=np.array([3, 3*np.sqrt(3), 0]),
        shift_amount=DOWN * 2 + LEFT * 2,
        colors=None,
        labels=None,
        show_explanation=True
    ):
        self.vec_a = vec_a
        self.vec_b = vec_b
        self.vec_2a = 2 * vec_a
        self.shift_amount = shift_amount
        
        # 颜色配置
        default_colors = {
            'a': BLUE,
            'b': RED,
            '2a': YELLOW,
            'segment': GREEN,
            'point': ORANGE,
            'line_to_origin': PURPLE
        }
        self.colors = {**default_colors, **(colors or {})}
        
        # 标签配置
        default_labels = {
            'a': r"\vec{a}",
            'b': r"\vec{b}",
            '2a': r"2\vec{a}",
            'point': "P",
            'line': r"\overrightarrow{OP}"
        }
        self.labels = {**default_labels, **(labels or {})}
        
        self.show_explanation = show_explanation


class FlexibleVectorDiagram(Scene):
    """灵活的向量图类"""
    
    def __init__(self, config=None, **kwargs):
        super().__init__(**kwargs)
        self.config = config if config else VectorDiagramConfig()
        self.alpha_tracker = ValueTracker(0.1)
        self.elements = {}
    
    def setup(self):
        """初始化所有元素"""
        self._setup_vectors()
        self._setup_lines()
        self._setup_labels()
        self._setup_animation_elements()
    
    def _setup_vectors(self):
        """设置向量"""
        self.elements['vec_a'] = Vector(
            self.config.vec_a, 
            color=self.config.colors['a']
        )
        self.elements['vec_b'] = Vector(
            self.config.vec_b, 
            color=self.config.colors['b']
        )
        self.elements['vec_2a'] = Vector(
            self.config.vec_2a, 
            color=self.config.colors['2a']
        )
        
        # 位移
        for key in ['vec_a', 'vec_b', 'vec_2a']:
            self.elements[key].shift(self.config.shift_amount)
    
    def _setup_lines(self):
        """设置线段"""
        self.elements['segment'] = Line(
            start=self.config.vec_b,
            end=self.config.vec_2a,
            color=self.config.colors['segment']
        ).shift(self.config.shift_amount)
        
        # 计算关键点
        self.origin = ORIGIN + self.config.shift_amount
        self.start_point = self.config.vec_b + self.config.shift_amount
        self.end_point = self.config.vec_2a + self.config.shift_amount
    
    def _setup_labels(self):
        """设置标签"""
        # 向量标签
        self.elements['label_a'] = MathTex(
            self.config.labels['a'],
            color=self.config.colors['a']
        ).next_to(self.elements['vec_a'].get_end(), UP, buff=0.1)
        
        self.elements['label_b'] = MathTex(
            self.config.labels['b'],
            color=self.config.colors['b']
        ).next_to(self.elements['vec_b'].get_end(), RIGHT, buff=0.1)
        
        self.elements['label_2a'] = MathTex(
            self.config.labels['2a'],
            color=self.config.colors['2a']
        ).next_to(self.elements['vec_2a'].get_end(), DOWN, buff=0.1)
    
    def _setup_animation_elements(self):
        """设置动画元素"""
        def get_point_position():
            return self.start_point + self.alpha_tracker.get_value() * (self.end_point - self.start_point)
        
        # 移动点
        self.elements['moving_point'] = always_redraw(
            lambda: Dot(
                get_point_position(),
                color=self.config.colors['point'],
                radius=DEFAULT_DOT_RADIUS * 1.2
            )
        )
        
        # 点标签
        self.elements['point_label'] = always_redraw(
            lambda: MathTex(self.config.labels['point']).scale(0.8).next_to(
                get_point_position(), UP, buff=0.1
            )
        )
        
        # 连接线
        self.elements['line_to_origin'] = always_redraw(
            lambda: Line(
                start=self.origin,
                end=get_point_position(),
                color=self.config.colors['line_to_origin'],
                stroke_width=4,
                stroke_opacity=0.8
            )
        )
        
        # 连接线标签
        self.elements['line_label'] = always_redraw(
            lambda: MathTex(self.config.labels['line']).scale(0.7).next_to(
                (self.origin + get_point_position()) / 2, LEFT, buff=0.1
            ).set_color(self.config.colors['line_to_origin'])
        )
    
    def animate_setup(self, sequence=None):
        """执行设置动画序列"""
        if sequence is None:
            sequence = [
                ('vectors', 2, 0.3),
                ('labels', 1.5, 0.3),
                ('segment', 1, None),
                ('connection', 1, None),
                ('point', 1, None)
            ]
        
        for step in sequence:
            element_type, duration, lag_ratio = step
            
            if element_type == 'vectors':
                self.play(
                    LaggedStart(
                        Create(self.elements['vec_a']),
                        Create(self.elements['vec_b']),
                        Create(self.elements['vec_2a']),
                        lag_ratio=lag_ratio
                    ),
                    run_time=duration
                )
            
            elif element_type == 'labels':
                self.play(
                    LaggedStart(
                        Write(self.elements['label_a']),
                        Write(self.elements['label_b']),
                        Write(self.elements['label_2a']),
                        lag_ratio=lag_ratio
                    ),
                    run_time=duration
                )
            
            elif element_type == 'segment':
                self.play(
                    Create(self.elements['segment']),
                    run_time=duration
                )
                self.wait(0.5)
            
            elif element_type == 'connection':
                self.play(
                    Create(self.elements['line_to_origin']),
                    Write(self.elements['line_label']),
                    run_time=duration
                )
                self.wait(0.5)
            
            elif element_type == 'point':
                self.play(
                    FadeIn(self.elements['moving_point'], scale=0.5),
                    Write(self.elements['point_label']),
                    run_time=duration
                )
                self.wait(0.5)
    
    def move_point(self, target_values, durations=None, rate_funcs=None):
        """移动点序列"""
        if isinstance(target_values, (int, float)):
            target_values = [target_values]
        
        if durations is None:
            durations = [2] * len(target_values)
        elif isinstance(durations, (int, float)):
            durations = [durations] * len(target_values)
        
        if rate_funcs is None:
            rate_funcs = [smooth] * len(target_values)
        elif not isinstance(rate_funcs, list):
            rate_funcs = [rate_funcs] * len(target_values)
        
        for target, duration, rate_func in zip(target_values, durations, rate_funcs):
            self.play(
                self.alpha_tracker.animate.set_value(target),
                rate_func=rate_func,
                run_time=duration
            )
    
    def construct(self):
        """主构造方法"""
        self.setup()
        self.animate_setup()
        
        # 示例动画序列
        self.move_point(
            target_values=[1, 0.5, 0.25, 0.75, 0.33, 0.67],
            durations=[3, 2, 1.5, 1.5, 1.5, 1.5],
            rate_funcs=[linear, smooth, smooth, smooth, smooth, smooth]
        )
        
        if self.config.show_explanation:
            self._add_explanation()
        
        self.wait(2)
    
    def _add_explanation(self):
        """添加解释"""
        explanation = MathTex(
            r"P(t) &= \vec{b} + t(2\vec{a} - \vec{b}) \\",
            r"&= (1-t)\vec{b} + 2t\vec{a} \\",
            r"t &\in [0, 1]"
        ).scale(0.6).to_edge(DOWN)
        
        explanation.set_color_by_tex_to_color_map({
            r"\vec{a}": self.config.colors['a'],
            r"\vec{b}": self.config.colors['b'],
            r"t": self.config.colors['2a']
        })
        
        self.play(Write(explanation), run_time=2)


# ====================== 使用示例 ======================
class CustomVectorDiagram1(FlexibleVectorDiagram):
    """自定义示例1：修改颜色和标签"""
    def construct(self):
        # 创建配置
        config = VectorDiagramConfig(
            colors={
                'a': TEAL,
                'b': PINK,
                '2a': GOLD,
                'segment': LIGHT_BROWN,
                'point': MAROON,
                'line_to_origin': LIGHT_PURPLE
            },
            labels={
                'a': r"\mathbf{u}",
                'b': r"\mathbf{v}",
                '2a': r"2\mathbf{u}",
                'point': r"Q",
                'line': r"\overrightarrow{OQ}"
            }
        )
        
        self.config = config
        super().construct()


class CustomVectorDiagram2(FlexibleVectorDiagram):
    """自定义示例2：修改向量和动画序列"""
    def construct(self):
        config = VectorDiagramConfig(
            vec_a=np.array([2, 1, 0]),
            vec_b=np.array([-1, 3, 0]),
            shift_amount=UP * 1
        )
        
        self.config = config
        self.setup()
        
        # 自定义动画序列
        custom_sequence = [
            ('vectors', 2, 0.2),
            ('segment', 1, None),
            ('labels', 1, 0.2),
            ('connection', 1, None),
            ('point', 1, None)
        ]
        
        self.animate_setup(sequence=custom_sequence)
        
        # 自定义移动序列
        self.move_point(
            target_values=[0, 0.5, 1, 0.25, 0.75],
            durations=[2, 1.5, 2, 1, 1],
            rate_funcs=[smooth, smooth, linear, smooth, smooth]
        )
        
        self.wait(3)