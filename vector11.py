from manim import *
from src.originsingle_vector import SingleVector as sv

class vecetor_example(Scene):
    def construct(self):
        vector1 = sv(vector=[3, 0, 0], color=YELLOW,origin=[-2,-2,0],start_label='O',label=r"\vec{v}",end_label='A')
        vector1.show(self, create_time=2, write_time=1)
       
        vector2 = sv(vector=[0, 2, 0], color=GREEN,origin=[-2,-2,0],label=r"\vec{u}",end_label='B')
        vector2.show(self, create_time=2, write_time=1) 
        
        vector3 = sv(vector=[3, 2, 0], color=RED,origin=[-2,-2,0],label=r"\vec{v}+\vec{u}",end_label='C')     
        vector3.show(self, create_time=2, write_time=1) 
        vector4 = sv(vector=[3, 0, 0], color=YELLOW,origin=[-2,0,0],label=r"\vec{v}")
        
        vector4.show(self, create_time=2, write_time=1)
        vector5 = sv(vector=[0, 2, 0], color=GREEN,origin=[1,-2,0],label=r"\vec{u}")
        vector5.show(self, create_time=2, write_time=1) 