import vectorclass
# 最简单的方式
class MyScene(CustomVectorDiagram1):
    def construct(self):
        super().construct()

# 自定义参数
# class MyCustomScene(Scene):
#     def construct(self):
#         diagram = MovingPointVectorDiagram(
#             vec_a=np.array([2, 0, 0]),
#             vec_b=np.array([1, 4, 0]),
#             shift_amount=UP
#         )
#         diagram.construct()

# 使用灵活配置
# class MyFlexibleScene(FlexibleVectorDiagram):
#     def construct(self):
#         config = VectorDiagramConfig(
#             colors={'a': RED, 'b': BLUE},
#             labels={'point': 'X'}
#         )
#         self.config = config
#         super().construct()