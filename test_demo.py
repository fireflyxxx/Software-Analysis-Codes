from hypothesis import given , settings , Verbosity , Phase
2 import hypothesis . strategies as st
3 import unittest
4
5 class TestShrinking ( unittest . TestCase ):
6 # 开 启 Verbose 模 式 ， 便 于 观 察 基 础 日 志
7 @settings (
8 verbosity = Verbosity .verbose ,
9 phases =[ Phase. generate ] # 仅 执 行 生 成 阶 段 ， 跳 过 shrinking
10 )
11 @given (st.lists(st. integers ()))
12 def test_list_contains_no_zero (self , xs):
13 # 核 心 性 质 ： 任 何 生 成 的 列 表 中 都 不 应 该 包 含 0
14 # 一 旦 包 含 0 ， 测 试 即 失 败 ， 触 发 Shrinking
15 assert 0 not in xs
16
17 if __name__ == '__main__ ':
18 unittest .main ()