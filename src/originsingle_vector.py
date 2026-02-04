# single_vector.py
from manim import *
import numpy as np

class SingleVector:
    """简化的向量类 - 三个标签全部用 MathTex"""
    
    def __init__(self, vector=[3, 0, 0], color=BLUE, start_label='A', 
                 mid_label=r'\vec{a}', end_label='B', origin=ORIGIN):
        """
        创建一个向量
        
        参数:
        - vector: 向量的坐标 [x, y, z]
        - color: 颜色
        - start_label: 起点标签（默认'A'）
        - mid_label: 向量中间标签（默认'a'）
        - end_label: 终点标签（默认'B'）
        - origin: 原点位置
        """
        # 转换为numpy数组
        if isinstance(vector, list):
            vector = np.array(vector)
        if isinstance(origin, list):
            origin = np.array(origin)
        
        # 存储属性
        self.vector = vector
        self.origin = origin
        self.color = color
        self.start_label = start_label
        self.mid_label = mid_label
        self.end_label = end_label
        
        # 计算绝对坐标
        self.absolute_start = origin
        self.absolute_end = origin + vector
        self.absolute_mid = origin + vector / 2
        
        # 创建向量
        self.vector_obj = Arrow(
            start=self.absolute_start,
            end=self.absolute_end,
            color=color,
            buff=0,
            stroke_width=6
        )
        
        # 创建三个标签（全部用 MathTex）
        self.start_label_obj = MathTex(start_label, color=color)
        self.start_label_obj.scale(0.8).next_to(self.absolute_start, DOWN, buff=0.1)
        
        self.mid_label_obj = MathTex(mid_label, color=color)
        self.mid_label_obj.next_to(self.absolute_mid, UP, buff=0.1)
        
        self.end_label_obj = MathTex(end_label, color=color)
        self.end_label_obj.next_to(self.absolute_end, RIGHT, buff=0.15)
        
        # 创建起点标记点
        self.start_dot = Dot(self.absolute_start, color=color, radius=0.05)
    
    def show(self, scene, create_time=1, write_time=0.5):
        """在场景中显示向量"""
        # 显示起点
        scene.play(FadeIn(self.start_dot), run_time=create_time/2)
        scene.play(Write(self.start_label_obj), run_time=write_time/2)
        
        # 显示向量
        scene.play(GrowArrow(self.vector_obj), run_time=create_time)
        
        # 显示中间和终点标签
        scene.play(
            Write(self.mid_label_obj),
            Write(self.end_label_obj),
            run_time=write_time
        )
        
        scene.wait(0.5)
    
    def shift(self, direction):
        """移动整个向量"""
        # 移动所有图形对象
        self.vector_obj.shift(direction)
        self.start_dot.shift(direction)
        self.start_label_obj.shift(direction)
        self.mid_label_obj.shift(direction)
        self.end_label_obj.shift(direction)
        
        # 更新坐标
        dir_array = np.array(direction)
        self.origin += dir_array
        self.absolute_start += dir_array
        self.absolute_end += dir_array
        self.absolute_mid += dir_array
        
        return self
    
    def move_to(self, new_origin):
        """移动到新原点"""
        shift_amount = np.array(new_origin) - self.origin
        return self.shift(shift_amount)