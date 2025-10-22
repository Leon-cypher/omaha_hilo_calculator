"""
奧瑪哈高低牌牌型評估器
"""

from itertools import combinations
from collections import Counter
from card import Card

class HandEvaluator:
    """牌型評估器"""
    
    # 牌型強度常數
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_KIND = 8
    STRAIGHT_FLUSH = 9
    
    @staticmethod
    def get_best_high_hand(hole_cards, board_cards):
        """
        獲取最佳高牌組合
        奧瑪哈必須使用恰好2張手牌 + 3張公共牌
        """
        best_hand = None
        best_strength = 0
        
        # 遍歷所有可能的2張手牌組合
        for hole_combo in combinations(hole_cards, 2):
            # 遍歷所有可能的3張公共牌組合
            for board_combo in combinations(board_cards, 3):
                hand = list(hole_combo) + list(board_combo)
                strength = HandEvaluator._evaluate_high_hand(hand)
                
                if strength > best_strength:
                    best_strength = strength
                    best_hand = hand
        
        return best_hand, best_strength
    
    @staticmethod
    def get_best_low_hand(hole_cards, board_cards):
        """
        獲取最佳低牌組合
        低牌要求：5張牌都是8或以下，且沒有對子，A算作1
        """
        best_hand = None
        best_low_value = float('inf')
        
        # 遍歷所有可能的2張手牌組合
        for hole_combo in combinations(hole_cards, 2):
            # 遍歷所有可能的3張公共牌組合
            for board_combo in combinations(board_cards, 3):
                hand = list(hole_combo) + list(board_combo)
                low_value = HandEvaluator._evaluate_low_hand(hand)
                
                if low_value is not None and low_value < best_low_value:
                    best_low_value = low_value
                    best_hand = hand
        
        return best_hand, best_low_value if best_low_value != float('inf') else None
    
    @staticmethod
    def _evaluate_high_hand(cards):
        """評估高牌強度"""
        if len(cards) != 5:
            raise ValueError("手牌必須是5張")
        
        # 獲取牌面值和花色
        values = [card.value for card in cards]
        suits = [card.suit for card in cards]
        
        values.sort(reverse=True)
        value_counts = Counter(values)
        
        # 檢查是否同花
        is_flush = len(set(suits)) == 1
        
        # 檢查是否順子
        is_straight = HandEvaluator._is_straight(values)
        
        # 同花順
        if is_flush and is_straight:
            return HandEvaluator.STRAIGHT_FLUSH * 1000000 + max(values)
        
        # 四條
        if 4 in value_counts.values():
            four_kind = [val for val, count in value_counts.items() if count == 4][0]
            kicker = [val for val, count in value_counts.items() if count == 1][0]
            return HandEvaluator.FOUR_KIND * 1000000 + four_kind * 100 + kicker
        
        # 葫蘆
        if 3 in value_counts.values() and 2 in value_counts.values():
            three_kind = [val for val, count in value_counts.items() if count == 3][0]
            pair = [val for val, count in value_counts.items() if count == 2][0]
            return HandEvaluator.FULL_HOUSE * 1000000 + three_kind * 100 + pair
        
        # 同花
        if is_flush:
            return HandEvaluator.FLUSH * 1000000 + sum(val * (10 ** (4-i)) for i, val in enumerate(values))
        
        # 順子
        if is_straight:
            return HandEvaluator.STRAIGHT * 1000000 + max(values)
        
        # 三條
        if 3 in value_counts.values():
            three_kind = [val for val, count in value_counts.items() if count == 3][0]
            kickers = sorted([val for val, count in value_counts.items() if count == 1], reverse=True)
            return HandEvaluator.THREE_KIND * 1000000 + three_kind * 10000 + kickers[0] * 100 + kickers[1]
        
        # 兩對
        pairs = [val for val, count in value_counts.items() if count == 2]
        if len(pairs) == 2:
            pairs.sort(reverse=True)
            kicker = [val for val, count in value_counts.items() if count == 1][0]
            return HandEvaluator.TWO_PAIR * 1000000 + pairs[0] * 10000 + pairs[1] * 100 + kicker
        
        # 一對
        if 2 in value_counts.values():
            pair = [val for val, count in value_counts.items() if count == 2][0]
            kickers = sorted([val for val, count in value_counts.items() if count == 1], reverse=True)
            return HandEvaluator.PAIR * 1000000 + pair * 10000 + sum(kickers[i] * (100 ** (2-i)) for i in range(3))
        
        # 高牌
        score = HandEvaluator.HIGH_CARD * 1000000
        for i, val in enumerate(values):
            score += val * (15 ** (4-i))
        return score
    
    @staticmethod
    def _evaluate_low_hand(cards):
        """
        評估低牌
        返回None如果不符合低牌條件，否則返回低牌值（越小越好）
        """
        if len(cards) != 5:
            return None
        
        # 獲取低牌值（A=1, 其他牌面值不變）
        low_values = []
        for card in cards:
            if card.rank == 'A':
                low_values.append(1)
            elif card.value <= 8:  # 2-8
                low_values.append(card.value)
            else:  # 9, T, J, Q, K
                return None  # 有大牌，不符合低牌條件
        
        # 檢查是否有重複（對子）
        if len(set(low_values)) != 5:
            return None  # 有對子，不符合低牌條件
        
        # 計算低牌值（從大到小排序後計算）
        low_values.sort(reverse=True)
        low_value = 0
        for i, val in enumerate(low_values):
            low_value += val * (100 ** (4-i))
        
        return low_value
    
    @staticmethod
    def _is_straight(values):
        """檢查是否為順子"""
        if len(set(values)) != 5:
            return False
        
        values_sorted = sorted(values)
        
        # 檢查普通順子
        if values_sorted[-1] - values_sorted[0] == 4:
            return True
        
        # 檢查A-2-3-4-5順子
        if values_sorted == [2, 3, 4, 5, 14]:
            return True
        
        return False
    
    @staticmethod
    def hand_strength_description(strength):
        """獲取牌型強度描述"""
        hand_type = strength // 1000000
        
        descriptions = {
            HandEvaluator.HIGH_CARD: "高牌",
            HandEvaluator.PAIR: "一對",
            HandEvaluator.TWO_PAIR: "兩對",
            HandEvaluator.THREE_KIND: "三條",
            HandEvaluator.STRAIGHT: "順子",
            HandEvaluator.FLUSH: "同花",
            HandEvaluator.FULL_HOUSE: "葫蘆",
            HandEvaluator.FOUR_KIND: "四條",
            HandEvaluator.STRAIGHT_FLUSH: "同花順"
        }
        
        return descriptions.get(hand_type, f"未知牌型({hand_type})")