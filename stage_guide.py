"""
階段選擇功能說明
"""

def explain_stage_selection():
    """解釋新的階段選擇功能"""
    print("🎯 新增階段選擇功能說明")
    print("=" * 40)
    
    print("🎮 界面新功能：")
    print("在公共牌區域新增了4個階段按鈕：")
    print()
    
    stages = [
        {
            'name': '翻牌前',
            'cards': 0,
            'color': '紅色',
            'description': '無公共牌，純手牌勝率計算',
            'use_case': '決定是否進入牌局、位置策略'
        },
        {
            'name': '翻牌後', 
            'cards': 3,
            'color': '橙色',
            'description': '3張公共牌，大部分牌力已確定',
            'use_case': '下注策略、聽牌計算'
        },
        {
            'name': '轉牌後',
            'cards': 4, 
            'color': '藍色',
            'description': '4張公共牌，接近最終結果',
            'use_case': '最後一張牌的勝率分析'
        },
        {
            'name': '河牌後',
            'cards': 5,
            'color': '紫色', 
            'description': '5張公共牌，確定最終結果',
            'use_case': '攤牌勝負分析、學習複盤'
        }
    ]
    
    for i, stage in enumerate(stages, 1):
        print(f"{i}. 🎴 {stage['name']} ({stage['color']}按鈕)")
        print(f"   公共牌數量: {stage['cards']} 張")
        print(f"   特點: {stage['description']}")
        print(f"   使用場景: {stage['use_case']}")
        print()
    
    print("🎯 使用方法：")
    print("1. 點擊階段按鈕 (翻牌前/翻牌後/轉牌後/河牌後)")
    print("2. 系統會自動:")
    print("   • 清除之前的公共牌")
    print("   • 如果不是翻牌前，隨機分配對應數量的公共牌")
    print("   • 更新界面顯示當前階段")
    print("3. 分配玩家手牌 (每人5張)")
    print("4. 點擊「計算勝率」")
    
    print("\n⚡ 快捷功能：")
    print("• 🔄 自動發牌: 根據當前階段自動分配所有牌")
    print("• 🗑️ 清除公共牌: 移除公共牌並回到翻牌前")
    print("• 📥 手動分配: 仍可手動選擇特定的公共牌")
    
    print("\n✅ 改進的好處：")
    print("• 一鍵設置不同計算階段")
    print("• 清楚顯示當前處於哪個階段")
    print("• 避免忘記分配公共牌的困擾")
    print("• 支援快速切換不同場景分析")
    
    print("\n🎲 實用範例：")
    print("想分析「A♠A♥2♠3♥K♦ vs K♠K♥J♠9♥T♦」：")
    print("1. 點「翻牌前」按鈕 → 分析起手牌勝率")
    print("2. 點「翻牌後」按鈕 → 看翻牌如何影響勝率")
    print("3. 點「轉牌後」按鈕 → 分析轉牌帶來的變化")
    print("4. 點「河牌後」按鈕 → 確認最終結果")

if __name__ == "__main__":
    explain_stage_selection()