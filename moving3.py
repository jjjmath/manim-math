from manim import *
from src.originsingle_vector import SingleVector
from src.moving_point import MovingPoint
class MultiplePoints(Scene):
    """多个动点"""
    
    def construct(self):
        # 创建向量
        vector = SingleVector([3, 1, 0], BLUE, 'A', r'\overrightarrow{AB}', 'B')
        vector.show(self)
        
        # 创建两个动点
        point1 = MovingPoint(vector, RED, 'P_1', UP)
        point2 = MovingPoint(vector, GREEN, 'P_2', DOWN)
        
        point1.show(self)
        point2.show(self)
        
        # 同时移动两个点
        self.play(
            point1.position_tracker.animate.set_value(0.7),
            point2.position_tracker.animate.set_value(0.3),
            run_time=3
        )
        
        self.wait(1)
        
        # 交换位置
        self.play(
            point1.position_tracker.animate.set_value(0.3),
            point2.position_tracker.animate.set_value(0.7),
            run_time=2
        )
        
        self.wait(2)