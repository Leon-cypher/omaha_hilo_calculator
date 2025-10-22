"""
5張奧瑪哈高低牌勝率計算器 - 網頁版
使用Flask創建適合手機使用的網頁界面
"""

from flask import Flask, render_template, request, jsonify
import json
from equity_calculator import OmahaHiLoEquityCalculator
from card import Card, parse_cards

app = Flask(__name__)
calculator = OmahaHiLoEquityCalculator()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_equity():
    """計算勝率API"""
    try:
        data = request.get_json()
        
        # 解析玩家手牌
        players_hands = []
        for i, hand_str in enumerate(data.get('players_hands', [])):
            if hand_str.strip():
                try:
                    hand = parse_cards(hand_str.strip())
                    if len(hand) != 5:
                        return jsonify({
                            'error': f'玩家{i+1}的手牌必須是5張，目前是{len(hand)}張'
                        }), 400
                    players_hands.append(hand)
                except Exception as e:
                    return jsonify({
                        'error': f'玩家{i+1}的手牌格式錯誤: {str(e)}'
                    }), 400
        
        if len(players_hands) < 2:
            return jsonify({'error': '至少需要2個玩家'}), 400
        
        # 解析公共牌
        board_cards = []
        board_str = data.get('board_cards', '').strip()
        if board_str:
            try:
                board_cards = parse_cards(board_str)
                if len(board_cards) > 5:
                    return jsonify({'error': '公共牌不能超過5張'}), 400
            except Exception as e:
                return jsonify({'error': f'公共牌格式錯誤: {str(e)}'}), 400
        
        # 獲取模擬次數
        simulations = data.get('simulations', 10000)
        if simulations < 1000 or simulations > 50000:
            simulations = 10000
        
        # 計算勝率
        results = calculator.calculate_equity(players_hands, board_cards, simulations)
        
        # 格式化結果
        formatted_results = {
            'simulations': simulations,
            'players': []
        }
        
        for i, (player_name, stats) in enumerate(results.items()):
            if player_name == 'simulations':
                continue
            formatted_results['players'].append({
                'player': f'玩家{i+1}',
                'hand': ' '.join([str(card) for card in players_hands[i]]),
                'equity': round(stats['equity'], 2),
                'hi_win_rate': round(stats['hi_win_rate'], 2),
                'lo_win_rate': round(stats['lo_win_rate'], 2),
                'scoop_rate': round(stats['scoop_rate'], 2),
                'split_rate': round(stats['split_rate'], 2)
            })
        
        return jsonify(formatted_results)
        
    except Exception as e:
        return jsonify({'error': f'計算錯誤: {str(e)}'}), 500

@app.route('/api/analyze_hand', methods=['POST'])
def analyze_hand():
    """分析單手牌強度API"""
    try:
        data = request.get_json()
        hand_str = data.get('hand', '').strip()
        board_str = data.get('board', '').strip()
        
        if not hand_str or not board_str:
            return jsonify({'error': '請輸入手牌和公共牌'}), 400
        
        result = calculator.analyze_hand_strength(hand_str, board_str)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'分析錯誤: {str(e)}'}), 500

if __name__ == '__main__':
    # 創建templates資料夾
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("🎯 5張奧瑪哈高低牌勝率計算器 - 網頁版")
    print("服務器啟動於: http://localhost:5000")
    print("在手機瀏覽器中訪問此網址即可使用！")
    
    app.run(debug=True, host='0.0.0.0', port=5000)