from manim import *
from src.originsingle_vector import SingleVector
from src.moving_point import MovingPoint

class TestMovingPoint(Scene):
    def construct(self):
        # 1. 创建向量
        vector = SingleVector(
            vector=[4, 2, 0],
            color= BLUE, 
            start_label='O',
            mid_label=r'\vec{v}',
            end_label='A',
            origin=ORIGIN
            )
        vector.show(self)
        
        # 2. 创建动点
        point = MovingPoint(
            line=vector,           # 在向量上移动
            color=RED,             # 点颜色
            point_label='P',       # 点标签
            label_position=UP      # 标签在上方
        )
        
        # 3. 显示动点
        point.show(self)
        
        self.wait(1)
        
        # 4. 移动点
        point.move_to(0.5, self, run_time=2)   # 移动到中点
        self.wait(1)
        
        point.move_to(0.8, self, run_time=1)   # 移动到0.8位置
        self.wait(1)
        
        point.move_to(0.2, self, run_time=1)   # 移动到0.2位置
        self.wait(2)
