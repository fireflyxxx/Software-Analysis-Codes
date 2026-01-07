import unittest
from hypothesis import given, settings, Verbosity, strategies as st
from dataclasses import dataclass
from typing import List

# ==========================================
# 1. 模拟业务逻辑 (System Under Test)
# ==========================================

@dataclass
class CartItem:
    name: str
    price: int
    quantity: int

def calculate_total(items: List[CartItem]) -> int:
    """
    模拟一个购物车结算函数。
    Bug逻辑：如果商品总价超过 1000，且包含价格为 0 的赠品，系统崩溃。
    """
    total = 0
    has_free_gift = False
    
    for item in items:
        total += item.price * item.quantity
        if item.price == 0:
            has_free_gift = True
            
    # 模拟 Bug：高额订单不能包含赠品，否则触发异常
    if total > 1000 and has_free_gift:
        raise ValueError("CRITICAL_BUG: High value cart cannot handle free gifts!")
        
    return total

# ==========================================
# 2. Hypothesis 测试代码
# ==========================================

class TestShoppingCart(unittest.TestCase):
    
    # 定义生成策略：生成复杂的购物车对象列表
    # 价格在 0 到 2000 之间，数量 1-10
    item_strategy = st.builds(
        CartItem, 
        name=st.just("Item"), 
        price=st.integers(min_value=0, max_value=2000),
        quantity=st.integers(min_value=1, max_value=10)
    )

    @settings(max_examples=500, verbosity=Verbosity.verbose)
    @given(st.lists(item_strategy, min_size=1))
    def test_cart_calculation(self, items):
        """
        属性测试：验证结算函数不会抛出异常。
        Hypothesis 会找到触发 Bug 的列表，然后尝试约减。
        预期约减结果：一个价格>1000的商品 + 一个价格为0的商品。
        """
        # 调用业务逻辑
        calculate_total(items)

if __name__ == '__main__':
    unittest.main()