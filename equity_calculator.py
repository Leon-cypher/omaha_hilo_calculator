"""
奧瑪哈高低牌勝率計算器
"""

import random
from itertools import combinations
from collections import defaultdict
from card import Card, Deck, parse_cards
from hand_evaluator import HandEvaluator

class OmahaHiLoEquityCalculator:
    """奧瑪哈高低牌勝率計算器"""
    
    def __init__(self):
        self.deck = Deck()
        self.hand_evaluator = HandEvaluator()
    
    def calculate_equity(self, players_hands, board_cards=None, num_simulations=10000):
        """
        計算多個玩家的勝率
        
        Args:
            players_hands: 玩家手牌列表，每個元素是4張牌的列表
            board_cards: 已知的公共牌（可以是0-5張）
            num_simulations: 模擬次數
        
        Returns:
            dict: 每個玩家的勝率統計
        """
        if not players_hands:
            raise ValueError("至少需要一個玩家")
        
        # 驗證手牌
        for i, hand in enumerate(players_hands):
            if len(hand) != 5:
                raise ValueError(f"玩家 {i+1} 的手牌必須是5張")
        
        if board_cards is None:
            board_cards = []
        
        if len(board_cards) > 5:
            raise ValueError("公共牌不能超過5張")
        
        # 重置牌堆並移除已知牌
        self.deck.reset()
        known_cards = []
        for hand in players_hands:
            known_cards.extend(hand)
        known_cards.extend(board_cards)
        self.deck.remove_cards(known_cards)
        
        # 初始化結果統計
        results = {
            f'player_{i+1}': {
                'hi_wins': 0,
                'lo_wins': 0, 
                'scoops': 0,  # 獨贏整個底池
                'splits': 0,  # 平分底池 (50%)
                'quarters': 0,  # 獲得1/4底池
                'three_quarters': 0,  # 獲得3/4底池
                'total_value': 0  # 總價值（勝率）
            }
            for i in range(len(players_hands))
        }
        
        # 進行蒙特卡羅模擬
        for _ in range(num_simulations):
            # 隨機補完公共牌到5張
            remaining_board = 5 - len(board_cards)
            if remaining_board > 0:
                available_cards = self.deck.get_remaining_cards()
                random_board = random.sample(available_cards, remaining_board)
                full_board = board_cards + random_board
            else:
                full_board = board_cards
            
            # 評估每個玩家的最佳高牌和低牌
            player_results = []
            for i, hand in enumerate(players_hands):
                hi_hand, hi_strength = self.hand_evaluator.get_best_high_hand(hand, full_board)
                lo_hand, lo_strength = self.hand_evaluator.get_best_low_hand(hand, full_board)
                
                player_results.append({
                    'player': f'player_{i+1}',
                    'hi_strength': hi_strength,
                    'lo_strength': lo_strength,
                    'has_low': lo_strength is not None
                })
            
            # 找出高牌獲勝者
            max_hi_strength = max(p['hi_strength'] for p in player_results)
            hi_winners = [p for p in player_results if p['hi_strength'] == max_hi_strength]
            
            # 找出低牌獲勝者（如果有人符合低牌條件）
            lo_players = [p for p in player_results if p['has_low']]
            lo_winners = []
            if lo_players:
                min_lo_strength = min(p['lo_strength'] for p in lo_players)
                lo_winners = [p for p in lo_players if p['lo_strength'] == min_lo_strength]
            
            # 分配獎勵和統計勝利類型
            hi_pot_value = 0.5 if lo_winners else 1.0  # 如果沒有低牌，高牌得整個底池
            lo_pot_value = 0.5 if lo_winners else 0.0   # 只有在有低牌時才有低牌底池
            
            # 計算每個玩家在這一手的收益
            for player_result in player_results:
                player_name = player_result['player']
                is_hi_winner = player_result in hi_winners
                is_lo_winner = player_result in lo_winners
                pot_share = 0
                
                # 高牌獎勵
                if is_hi_winner:
                    results[player_name]['hi_wins'] += 1
                    hi_share = hi_pot_value / len(hi_winners)
                    pot_share += hi_share
                
                # 低牌獎勵
                if is_lo_winner:
                    results[player_name]['lo_wins'] += 1
                    lo_share = lo_pot_value / len(lo_winners)
                    pot_share += lo_share
                
                results[player_name]['total_value'] += pot_share
                
                # 統計勝利類型
                if is_hi_winner and is_lo_winner:
                    # 同時贏得高牌和低牌 - Scoop
                    results[player_name]['scoops'] += 1
                        
                elif is_hi_winner and not is_lo_winner:
                    # 只贏得高牌
                    if len(hi_winners) == 1:
                        if lo_winners:
                            # 獨得高牌，有低牌玩家存在 - 獲得50%
                            results[player_name]['splits'] += 1
                        else:
                            # 沒有低牌玩家，獨得整個底池
                            results[player_name]['scoops'] += 1
                    else:
                        # 與他人分享高牌
                        if lo_winners:
                            # 有低牌玩家存在，分享高牌50% - 獲得25%或更少
                            results[player_name]['quarters'] += 1
                        else:
                            # 沒有低牌玩家，與他人分享整個底池
                            if len(hi_winners) == 2:
                                results[player_name]['splits'] += 1
                            else:
                                results[player_name]['quarters'] += 1
                            
                elif is_lo_winner and not is_hi_winner:
                    # 只贏得低牌
                    if len(lo_winners) == 1:
                        # 獨得低牌50%
                        results[player_name]['splits'] += 1
                    else:
                        # 與他人分享低牌50% - 獲得25%或更少
                        results[player_name]['quarters'] += 1
                        
                # 檢查是否獲得3/4底池的情況
                # 當一個玩家獲得其中一個底池的全部，而另一個底池被多人分享時
                if pot_share == 0.75:
                    results[player_name]['three_quarters'] += 1
                elif pot_share > 0.5 and pot_share < 0.75:
                    # 例如獨得一個底池，但與另一人分享另一個底池 (0.5 + 0.25 = 0.75)
                    # 或者其他大於50%但小於75%的情況
                    results[player_name]['three_quarters'] += 1
        
        # 計算百分比
        for player_name in results:
            player_stats = results[player_name]
            player_stats['hi_win_rate'] = player_stats['hi_wins'] / num_simulations * 100
            player_stats['lo_win_rate'] = player_stats['lo_wins'] / num_simulations * 100
            player_stats['scoop_rate'] = player_stats['scoops'] / num_simulations * 100
            player_stats['split_rate'] = player_stats['splits'] / num_simulations * 100
            player_stats['quarter_rate'] = player_stats['quarters'] / num_simulations * 100
            player_stats['three_quarter_rate'] = player_stats['three_quarters'] / num_simulations * 100
            player_stats['equity'] = player_stats['total_value'] / num_simulations * 100
        
        return results
    
    def calculate_hand_vs_hand(self, hand1_str, hand2_str, board_str="", num_simulations=10000):
        """
        計算兩手牌對戰的勝率
        
        Args:
            hand1_str: 玩家1手牌字符串，例如 "As Kh Qd Jc Tc"
            hand2_str: 玩家2手牌字符串
            board_str: 公共牌字符串，例如 "2s 3h 4d"
            num_simulations: 模擬次數
        
        Returns:
            dict: 勝率結果
        """
        try:
            hand1 = parse_cards(hand1_str)
            hand2 = parse_cards(hand2_str)
            board = parse_cards(board_str) if board_str.strip() else []
            
            if len(hand1) != 5 or len(hand2) != 5:
                raise ValueError("每個玩家必須有5張手牌")
            
            results = self.calculate_equity([hand1, hand2], board, num_simulations)
            
            return {
                'player1': results['player_1'],
                'player2': results['player_2'],
                'simulations': num_simulations
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_hand_strength(self, hand_str, board_str):
        """
        分析單手牌在給定公共牌下的最佳組合
        
        Args:
            hand_str: 手牌字符串
            board_str: 公共牌字符串（必須是5張）
        
        Returns:
            dict: 手牌分析結果
        """
        try:
            hand = parse_cards(hand_str)
            board = parse_cards(board_str)
            
            if len(hand) != 5:
                raise ValueError("手牌必須是5張")
            if len(board) != 5:
                raise ValueError("分析時公共牌必須是5張")
            
            # 獲取最佳高牌和低牌
            hi_hand, hi_strength = self.hand_evaluator.get_best_high_hand(hand, board)
            lo_hand, lo_strength = self.hand_evaluator.get_best_low_hand(hand, board)
            
            result = {
                'hand_cards': [str(card) for card in hand],
                'board_cards': [str(card) for card in board],
                'best_hi_hand': [str(card) for card in hi_hand] if hi_hand else None,
                'hi_hand_type': self.hand_evaluator.hand_strength_description(hi_strength),
                'hi_strength': hi_strength,
                'has_low': lo_strength is not None
            }
            
            if lo_strength is not None:
                result['best_lo_hand'] = [str(card) for card in lo_hand]
                result['lo_strength'] = lo_strength
            
            return result
            
        except Exception as e:
            return {'error': str(e)}