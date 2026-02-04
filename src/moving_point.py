# moving_point.py
from manim import *
import numpy as np

class MovingPoint:
    """在向量或线段上移动的点 - 最简实现"""
    
    def __init__(self, line=None, color=RED, point_label='P', label_position=UP):
        """
        创建一个在向量/线段上移动的点
        
        参数:
        - line: 向量或线段对象（SingleVector 或 Line/Arrow）
        - color: 点颜色
        - point_label: 点标签
        - label_position: 标签位置（UP, DOWN, LEFT, RIGHT）
        """
        self.line = line
        self.color = color
        self.point_label = point_label
        
        # 位置跟踪器（0=起点，1=终点）
        self.position_tracker = ValueTracker(0)
        
        # 计算起点和终点
        if isinstance(line, Arrow):
            self.start_point = line.get_start()
            self.end_point = line.get_end()
        elif hasattr(line, 'vector_obj'):  # SingleVector 对象
            self.start_point = line.origin
            self.end_point = line.origin + line.vector
        elif isinstance(line, Line):
            self.start_point = line.get_start()
            self.end_point = line.get_end()
        else:
            # 默认创建一条线段
            self.start_point = ORIGIN
            self.end_point = RIGHT * 3
        
        # 创建动态点
        self.point = always_redraw(
            lambda: Dot(
                self.start_point + 
                self.position_tracker.get_value() * 
                (self.end_point - self.start_point),
                color=color,
                radius=0.08
            )
        )
        
        # 创建点标签
        self.label = always_redraw(
            lambda: MathTex(point_label).scale(0.8).next_to(
                self.point.get_center(), label_position, buff=0.1
            ).set_color(color)
        )
    
    def show(self, scene):
        """显示动点"""
        scene.add(self.point, self.label)
    
    def move_to(self, position, scene=None, run_time=2):
        """
        移动到指定位置（0=起点，1=终点）
        
        参数:
        - position: 位置值（0到1之间）
        - scene: 场景对象（用于动画）
        - run_time: 动画时间
        """
        if scene:
            scene.play(
                self.position_tracker.animate.set_value(position),
                run_time=run_time
            )
        else:
            self.position_tracker.set_value(position)
    
    def move_along(self, positions, scene, run_times=None):
        """
        沿路径移动一系列位置
        
        参数:
        - positions: 位置列表 [0.2, 0.5, 0.8, ...]
        - scene: 场景对象
        - run_times: 每个位置的时间列表
        """
        if run_times is None:
            run_times = [2] * len(positions)
        
        for pos, time in zip(positions, run_times):
            self.move_to(pos, scene, time)
    def get_center(self):
        """获取点的中心位置（方便外部访问）"""
        return self.point.get_center()