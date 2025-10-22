"""
奧瑪哈高低牌勝率計算器 - 主程式
"""

import sys
from equity_calculator import OmahaHiLoEquityCalculator

def print_separator():
    print("=" * 60)

def print_hand_analysis(result):
    """打印手牌分析結果"""
    if 'error' in result:
        print(f"錯誤: {result['error']}")
        return
    
    print(f"手牌: {' '.join(result['hand_cards'])}")
    print(f"公共牌: {' '.join(result['board_cards'])}")
    print(f"最佳高牌: {' '.join(result['best_hi_hand'])} ({result['hi_hand_type']})")
    
    if result['has_low']:
        print(f"最佳低牌: {' '.join(result['best_lo_hand'])}")
    else:
        print("無低牌")

def print_equity_results(results):
    """打印勝率計算結果"""
    if 'error' in results:
        print(f"錯誤: {results['error']}")
        return
    
    print(f"模擬次數: {results['simulations']:,}")
    print()
    
    for player_name, stats in results.items():
        if player_name == 'simulations':
            continue
            
        print(f"{player_name.upper()}:")
        print(f"  總勝率: {stats['equity']:.2f}%")
        print(f"  高牌獲勝: {stats['hi_win_rate']:.2f}% ({stats['hi_wins']:,} 次)")
        print(f"  低牌獲勝: {stats['lo_win_rate']:.2f}% ({stats['lo_wins']:,} 次)")
        print(f"  獲得整個底池: {stats['scoop_rate']:.2f}% ({stats['scoops']:,} 次)")
        print(f"  平分底池: {stats['split_rate']:.2f}% ({stats['splits']:,} 次)")
        print()

def main():
    calculator = OmahaHiLoEquityCalculator()
    
    print("🎯 5張奧瑪哈高低牌勝率計算器")
    print_separator()
    print("牌面表示法: 2-9, T(10), J, Q, K, A")
    print("花色表示法: s(♠), h(♥), d(♦), c(♣)")
    print("例如: As = A♠, Kh = K♥, Qd = Q♦, Jc = J♣")
    print("注意: 每位玩家需要5張手牌！")
    print_separator()
    
    while True:
        print("\n選擇功能:")
        print("1. 兩手牌對戰勝率計算")
        print("2. 手牌強度分析")
        print("3. 多人勝率計算")
        print("4. 退出")
        
        choice = input("\n請選擇 (1-4): ").strip()
        
        if choice == '1':
            print_separator()
            print("兩手牌對戰勝率計算")
            print("請輸入5張手牌，用空格分隔")
            
            hand1 = input("玩家1手牌: ").strip()
            if not hand1:
                continue
                
            hand2 = input("玩家2手牌: ").strip()
            if not hand2:
                continue
                
            board = input("已知公共牌 (可選，0-5張): ").strip()
            
            try:
                simulations = int(input("模擬次數 (預設10000): ").strip() or "10000")
            except ValueError:
                simulations = 10000
            
            print("\n計算中...")
            results = calculator.calculate_hand_vs_hand(hand1, hand2, board, simulations)
            
            print_separator()
            print_equity_results(results)
        
        elif choice == '2':
            print_separator()
            print("手牌強度分析")
            
            hand = input("請輸入5張手牌: ").strip()
            if not hand:
                continue
                
            board = input("請輸入5張公共牌: ").strip()
            if not board:
                continue
            
            result = calculator.analyze_hand_strength(hand, board)
            
            print_separator()
            print_hand_analysis(result)
        
        elif choice == '3':
            print_separator()
            print("多人勝率計算")
            
            try:
                num_players = int(input("玩家數量 (2-9): ").strip())
                if num_players < 2 or num_players > 9:
                    print("玩家數量必須在2-9之間")
                    continue
            except ValueError:
                print("請輸入有效的數字")
                continue
            
            players_hands = []
            for i in range(num_players):
                hand = input(f"玩家{i+1}手牌 (5張): ").strip()
                if not hand:
                    break
                players_hands.append(hand)
            
            if len(players_hands) != num_players:
                print("輸入不完整")
                continue
            
            board = input("已知公共牌 (可選，0-5張): ").strip()
            
            try:
                simulations = int(input("模擬次數 (預設10000): ").strip() or "10000")
            except ValueError:
                simulations = 10000
            
            print("\n計算中...")
            
            # 解析手牌
            try:
                from card import parse_cards
                parsed_hands = [parse_cards(hand) for hand in players_hands]
                parsed_board = parse_cards(board) if board.strip() else []
                
                results = calculator.calculate_equity(parsed_hands, parsed_board, simulations)
                
                print_separator()
                print("多人勝率結果:")
                print(f"模擬次數: {simulations:,}")
                print()
                
                for i, player_name in enumerate(sorted(results.keys())):
                    stats = results[player_name]
                    print(f"玩家{i+1} ({players_hands[i]}):")
                    print(f"  總勝率: {stats['equity']:.2f}%")
                    print(f"  高牌獲勝: {stats['hi_win_rate']:.2f}%")
                    print(f"  低牌獲勝: {stats['lo_win_rate']:.2f}%")
                    print(f"  獲得整個底池: {stats['scoop_rate']:.2f}%")
                    print()
                    
            except Exception as e:
                print(f"錯誤: {e}")
        
        elif choice == '4':
            print("感謝使用！")
            break
        
        else:
            print("無效選擇，請重新輸入")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式已中斷")
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        sys.exit(1)