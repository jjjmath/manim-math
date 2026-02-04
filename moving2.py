from manim import *
from src.originsingle_vector import SingleVector
from src.moving_point import MovingPoint
class MovingOnLine(Scene):
    """在线段上移动"""
    
    def construct(self):
        # 创建一条线段
        line = Line([-3, 0, 0], [3, 0, 0], color=GRAY)
        self.play(Create(line))
        point2=Dot([-1,3,0],color=RED)
        self.add(point2)
        # 在线段上创建动点
        point = MovingPoint(
            line=line,             # 在线段上
            color=GREEN,
            point_label='Q'
        )
        point.show(self)
        
        connecting_line = always_redraw(
            lambda: Line(
                point2.get_center(),
                point.get_center()+(point.get_center()-point2.get_center()),  
                color=BLUE,
                stroke_width=3
            )
        )
        
        self.add(connecting_line)
        
        # 移动点
        positions = [0, 0.3, 0.7, 0.5, 1, 0.2]
        for pos in positions:
            point.move_to(pos, self, run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        # 移动点
        positions = [0, 0.3, 0.7, 0.5, 1, 0.2]
        point.move_along(positions, self)
        
        self.wait(2)