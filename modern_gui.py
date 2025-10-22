"""
5張奧瑪哈高低牌勝率計算器 - 現代化界面
使用更真實的撲克牌外觀
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from equity_calculator import OmahaHiLoEquityCalculator
from card import Card
import random
from modern_card_widget import ModernCardWidget

class ModernOmahaGUI:
    """現代化5張奧瑪哈界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 5張奧瑪哈高低牌勝率計算器 - 現代版")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')  # 更深的背景色
        
        # 計算器實例
        self.calculator = OmahaHiLoEquityCalculator()
        
        # 遊戲狀態
        self.num_players = 2
        self.selected_cards = []
        self.card_widgets = []
        self.player_hands = [[] for _ in range(9)]
        self.board_cards = []
        
        # 創建界面
        self.create_interface()
        self.initialize_deck()
    
    def create_interface(self):
        """創建現代化界面"""
        # 標題和控制面板
        self.create_header()
        
        # 主要內容區域
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 左側 - 牌桌區域
        self.create_table_area(main_frame)
        
        # 右側 - 牌堆區域
        self.create_deck_area(main_frame)
    
    def create_header(self):
        """創建標題和控制面板"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        # 標題
        title_label = tk.Label(header_frame,
                              text="🎯 5張奧瑪哈高低牌勝率計算器",
                              font=('微軟正黑體', 18, 'bold'),
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(header_frame,
                                 text="現代化撲克牌界面 - 更真實的視覺體驗",
                                 font=('微軟正黑體', 11),
                                 bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack()
        
        # 控制面板
        control_frame = tk.Frame(header_frame, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=5)
        
        # 左側控制
        left_controls = tk.Frame(control_frame, bg='#2c3e50')
        left_controls.pack(side='left', fill='x', expand=True)
        
        # 玩家數量
        tk.Label(left_controls, text="玩家數量:", 
                font=('微軟正黑體', 11), bg='#2c3e50', fg='#ecf0f1').pack(side='left')
        
        self.player_var = tk.StringVar(value="2")
        player_spinbox = tk.Spinbox(left_controls, from_=2, to=9, 
                                   textvariable=self.player_var,
                                   font=('微軟正黑體', 10), width=5,
                                   command=self.update_player_count)
        player_spinbox.pack(side='left', padx=(5, 20))
        
        # 選擇狀態顯示
        self.selection_label = tk.Label(left_controls, text="已選擇: 0 張", 
                                       font=('微軟正黑體', 11, 'bold'),
                                       bg='#2c3e50', fg='#f39c12')
        self.selection_label.pack(side='left', padx=10)
        
        # 右側按鈕
        right_controls = tk.Frame(control_frame, bg='#2c3e50')
        right_controls.pack(side='right')
        
        tk.Button(right_controls, text="❌ 取消選擇", 
                 font=('微軟正黑體', 9), bg='#e67e22', fg='white',
                 command=self.clear_selection).pack(side='left', padx=2)
        
        self.reset_button = tk.Button(right_controls, text="🔄 重置", 
                                     font=('微軟正黑體', 10, 'bold'),
                                     bg='#e74c3c', fg='white', width=8,
                                     command=self.reset_game)
        self.reset_button.pack(side='left', padx=2)
        
        self.auto_deal_button = tk.Button(right_controls, text="🃏 自動發牌", 
                                         font=('微軟正黑體', 10, 'bold'),
                                         bg='#3498db', fg='white', width=10,
                                         command=self.auto_deal)
        self.auto_deal_button.pack(side='left', padx=2)
        
        self.calculate_button = tk.Button(right_controls, text="🎲 計算勝率", 
                                         font=('微軟正黑體', 10, 'bold'),
                                         bg='#27ae60', fg='white', width=10,
                                         command=self.calculate_equity)
        self.calculate_button.pack(side='left', padx=2)
        
        # 進度條
        self.progress = ttk.Progressbar(right_controls, mode='indeterminate', length=100)
        self.progress.pack(side='left', padx=5)
    
    def create_table_area(self, parent):
        """創建牌桌區域"""
        table_frame = tk.LabelFrame(parent, text="🎴 牌桌區域", 
                                   font=('微軟正黑體', 12, 'bold'),
                                   bg='#34495e', fg='#ecf0f1',
                                   padx=10, pady=10)
        table_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # 公共牌區域
        self.create_board_area(table_frame)
        
        # 玩家區域
        self.create_player_areas(table_frame)
    
    def create_board_area(self, parent):
        """創建公共牌區域"""
        board_frame = tk.LabelFrame(parent, text="🃏 公共牌", 
                                   font=('微軟正黑體', 11, 'bold'),
                                   bg='#27ae60', fg='white',
                                   padx=10, pady=10)
        board_frame.pack(fill='x', pady=(0, 10))
        
        # 控制按鈕
        button_frame = tk.Frame(board_frame, bg='#27ae60')
        button_frame.pack(fill='x', pady=5)

        # 分配至公共牌按鈕
        assign_board_button = tk.Button(button_frame,
                                     text="📥 分配至公共牌",
                                     font=('微軟正黑體', 10, 'bold'),
                                     bg='white', fg='#27ae60',
                                     command=lambda: self.assign_selected_cards('board'))
        assign_board_button.pack(side='left', padx=10)

        # 公共牌顯示區域
        self.board_display = tk.Frame(board_frame, bg='#27ae60', height=90)
        self.board_display.pack(fill='x', pady=5)
        self.board_display.pack_propagate(False)
    
    def create_player_areas(self, parent):
        """創建玩家區域"""
        self.players_frame = tk.Frame(parent, bg='#34495e')
        self.players_frame.pack(fill='both', expand=True)
        
        self.player_buttons = []
        self.player_displays = []
        
        # 初始化2個玩家
        self.update_player_areas()
    
    def update_player_areas(self):
        """更新玩家區域 - 改為緊湊的垂直列表"""
        # 清除現有玩家區域
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        
        self.player_buttons = []
        self.player_displays = []
        
        # 創建滾動區域
        canvas = tk.Canvas(self.players_frame, bg='#34495e')
        scrollbar = ttk.Scrollbar(self.players_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 打包滾動組件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        player_colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6', 
                        '#1abc9c', '#e67e22', '#34495e', '#16a085', '#8e44ad']
        
        for i in range(self.num_players):
            player_color = player_colors[i % len(player_colors)]
            
            # 創建緊湑的水平玩家條
            player_row = tk.Frame(scrollable_frame, bg='#2c3e50', relief='raised', bd=1)
            player_row.pack(fill='x', padx=5, pady=2)
            
            # 玩家標籤（左側）
            player_label = tk.Label(player_row, 
                                   text=f"🎴 玩家{i+1}",
                                   font=('微軟正黑體', 10, 'bold'),
                                   bg=player_color, fg='white',
                                   width=12, padx=5, pady=5)
            player_label.pack(side='left', padx=2, pady=2)
            
            # 分配按鈕（左側）
            assign_button = tk.Button(player_row,
                                     text=f"📥 分配",
                                     font=('微軟正黑體', 9),
                                     bg='white', fg=player_color,
                                     width=8,
                                     command=lambda idx=i: self.assign_selected_cards(f'player_{idx}'))
            assign_button.pack(side='left', padx=2, pady=2)
            self.player_buttons.append(assign_button)
            
            # 手牌顯示區域（右側，水平排列）
            hand_display = tk.Frame(player_row, bg='#2c3e50', height=60)
            hand_display.pack(side='left', fill='x', expand=True, padx=5, pady=2)
            hand_display.pack_propagate(False)  # 固定高度
            self.player_displays.append(hand_display)
    
    def create_deck_area(self, parent):
        """創建現代化牌堆區域"""
        deck_frame = tk.LabelFrame(parent, text="🃏 撲克牌堆", 
                                  font=('微軟正黑體', 12, 'bold'),
                                  bg='#34495e', fg='#ecf0f1',
                                  padx=10, pady=10)
        deck_frame.pack(side='right', fill='both', expand=False, padx=(5, 0))
        
        # 說明標籤
        info_label = tk.Label(deck_frame, 
                             text="點擊撲克牌選擇 (橫向現代佈局)",
                             font=('微軟正黑體', 10),
                             bg='#34495e', fg='#bdc3c7')
        info_label.pack(pady=(0, 10))
        
        # 創建容器frame
        container_frame = tk.Frame(deck_frame, bg='#34495e')
        container_frame.pack(fill='both', expand=True)
        
        # 創建滾動區域（同時支援水平和垂直滾動）
        canvas = tk.Canvas(container_frame, bg='#2c3e50', width=900, height=400)
        v_scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(container_frame, orient="horizontal", command=canvas.xview)
        self.deck_content = tk.Frame(canvas, bg='#2c3e50')
        
        self.deck_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.deck_content, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # 配置網格權重
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)
    
    def initialize_deck(self):
        """初始化52張現代化撲克牌 - 橫向緊湊佈局"""
        self.card_widgets = []
        
        # 清除現有內容
        for widget in self.deck_content.winfo_children():
            widget.destroy()
        
        # 創建花色分組顯示 - 橫向佈局
        main_frame = tk.Frame(self.deck_content, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        for suit_idx, suit in enumerate(Card.SUITS):
            # 每個花色一行
            suit_color = '#dc143c' if suit in ['♥', '♦'] else '#ecf0f1'
            suit_frame = tk.Frame(main_frame, bg='#2c3e50')
            suit_frame.pack(fill='x', pady=5)
            
            # 花色標籤（更加美觀）
            suit_label = tk.Label(suit_frame, 
                                 text=f" {suit} ", 
                                 font=('Helvetica', 18, 'normal'),
                                 bg='#34495e', fg=suit_color,
                                 padx=12, pady=8, width=4,
                                 relief='raised', borderwidth=1)
            suit_label.pack(side='left', padx=(0, 10))
            
            # 該花色的13張牌橫向排列
            cards_frame = tk.Frame(suit_frame, bg='#2c3e50')
            cards_frame.pack(side='left', fill='x', expand=True)
            
            for rank in Card.RANKS:
                card = Card(rank, suit)
                # 使用稍大一點的尺寸讓牌更清晰
                card_widget = ModernCardWidget(cards_frame, card, self.on_card_click, width=55, height=75)
                card_widget.frame.pack(side='left', padx=2, pady=1)
                self.card_widgets.append(card_widget)
    
    def on_card_click(self, card_widget):
        """處理卡牌點擊：選擇、取消選擇、或取消分配"""
        if card_widget.is_assigned:
            # 如果牌已被分配，則取消分配
            
            # 從玩家手牌中移除
            for i in range(self.num_players):
                if card_widget in self.player_hands[i]:
                    self.player_hands[i].remove(card_widget)
                    break  # 找到後即可跳出循環
            
            # 從公共牌中移除
            if card_widget in self.board_cards:
                self.board_cards.remove(card_widget)

            card_widget.set_assigned(False)
            self.update_display()

        elif card_widget.is_selected:
            # 如果牌已被選擇，則取消選擇
            card_widget.set_selected(False)
            self.selected_cards.remove(card_widget)
            self.update_selection_display()
        else:
            # 否則，選擇該牌
            card_widget.set_selected(True)
            self.selected_cards.append(card_widget)
            self.update_selection_display()
    

    
    def auto_assign_board_cards(self, count):
        """自動分配指定數量的公共牌"""
        available_widgets = [cw for cw in self.card_widgets if not hasattr(cw, 'is_assigned') or not cw.is_assigned]
        
        if len(available_widgets) < count:
            messagebox.showwarning("警告", f"沒有足夠的牌來分配{count}張公共牌")
            return
        
        selected_cards = random.sample(available_widgets, count)
        
        for card_widget in selected_cards:
            self.board_cards.append(card_widget)
            card_widget.set_assigned(True)
            card_widget.is_assigned = True
    
    def assign_selected_cards(self, target):
        """分配選中的卡牌到目標區域"""
        if not self.selected_cards:
            messagebox.showwarning("警告", "請先選擇要分配的牌！")
            return
        
        if target.startswith('player_'):
            player_idx = int(target.split('_')[1])
            available_slots = 5 - len(self.player_hands[player_idx])
            
            if len(self.selected_cards) > available_slots:
                messagebox.showwarning("警告", f"玩家{player_idx+1}只能再要{available_slots}張牌！")
                return
            
            for card_widget in self.selected_cards:
                self.player_hands[player_idx].append(card_widget)
                card_widget.set_assigned(True)
                card_widget.is_assigned = True
        
        elif target == 'board':
            # 檢查是否超過5張公共牌
            if len(self.board_cards) + len(self.selected_cards) > 5:
                messagebox.showwarning("警告", f"公共牌總數不能超過5張！")
                return

            for card_widget in self.selected_cards:
                self.board_cards.append(card_widget)
                card_widget.set_assigned(True)
                card_widget.is_assigned = True

        self.selected_cards.clear()
        self.update_display()
    
    def update_selection_display(self):
        """更新選擇狀態顯示"""
        count = len(self.selected_cards)
        self.selection_label.config(text=f"已選擇: {count} 張")
    
    def update_display(self):
        """更新整體顯示"""
        self.update_selection_display()
        
        # 更新公共牌顯示
        for widget in self.board_display.winfo_children():
            widget.destroy()
        
        if self.board_cards:
            # 直接在公共牌區域顯示卡牌圖案
            for card_widget in self.board_cards:
                # 創建一個新的、不可點擊的卡牌來顯示
                display_card = ModernCardWidget(self.board_display, card_widget.card, None, width=55, height=75)
                display_card.frame.pack(side='left', padx=2, pady=2)
        else:
            tk.Label(self.board_display, text="(無公共牌)", 
                    font=('微軟正黑體', 10, 'bold'),
                    bg='#27ae60', fg='white').pack(pady=25)
        
        # 更新玩家手牌顯示
        for i in range(self.num_players):
            display = self.player_displays[i]
            
            for widget in display.winfo_children():
                widget.destroy()
            
            if self.player_hands[i]:
                # 顯示手牌圖像
                for card_widget in self.player_hands[i]:
                    display_card = ModernCardWidget(display, card_widget.card, None, width=55, height=75)
                    display_card.frame.pack(side='left', padx=1, pady=1)
            else:
                # 顯示手牌為空
                tk.Label(display, text="(點擊牌堆選牌，\n再點擊下方分配按鈕)", 
                        font=('微軟正黑體', 9, 'italic'),
                        bg=display.master.cget('bg'), fg='#ecf0f1').pack(pady=15)
    
    def update_player_count(self):
        """更新玩家數量"""
        try:
            new_count = int(self.player_var.get())
            if 2 <= new_count <= 9:
                old_count = self.num_players
                self.num_players = new_count
                
                # 清除多餘玩家的手牌
                for i in range(new_count, old_count):
                    for card_widget in self.player_hands[i]:
                        card_widget.set_assigned(False)
                        card_widget.is_assigned = False
                    self.player_hands[i].clear()
                
                self.update_player_areas()
                self.update_display()
        except ValueError:
            pass
    
    def clear_selection(self):
        """清除所有選擇"""
        for card_widget in self.selected_cards:
            card_widget.set_selected(False)
        self.selected_cards.clear()
        self.update_selection_display()
    
    def reset_game(self):
        """重置遊戲"""
        for card_widget in self.card_widgets:
            card_widget.set_assigned(False)
            card_widget.set_selected(False)
            card_widget.is_assigned = False
        
        self.selected_cards.clear()
        self.board_cards.clear()
        for i in range(9):
            self.player_hands[i].clear()
        
        self.update_display()
        messagebox.showinfo("重置", "遊戲已重置！")
    
    def auto_deal(self):
        """自動發牌"""
        self.reset_game()
        
        available_widgets = [cw for cw in self.card_widgets]
        random.shuffle(available_widgets)
        
        card_index = 0
        
        # 給每個玩家發5張牌
        for i in range(self.num_players):
            for j in range(5):
                if card_index < len(available_widgets):
                    card_widget = available_widgets[card_index]
                    self.player_hands[i].append(card_widget)
                    card_widget.set_assigned(True)
                    card_widget.is_assigned = True
                    card_index += 1
        
        # 發隨機數量的公共牌 (0, 3, 4, or 5)
        num_board_cards = random.choice([0, 3, 4, 5])
        for _ in range(num_board_cards):
            if card_index < len(available_widgets):
                card_widget = available_widgets[card_index]
                self.board_cards.append(card_widget)
                card_widget.set_assigned(True)
                card_widget.is_assigned = True
                card_index += 1

        self.update_display()
        messagebox.showinfo("自動發牌", f"自動發牌完成！\n發了 {self.num_players} 位玩家的手牌和 {num_board_cards} 張公共牌。")
    
    def calculate_equity(self):
        """計算勝率"""
        # 檢查手牌數
        for i in range(self.num_players):
            if len(self.player_hands[i]) != 5:
                messagebox.showwarning("警告", f"玩家{i+1}必須恰好5張手牌！")
                return
        
        # 檢查公共牌數（允許0-5張）
        board_count = len(self.board_cards)
        if board_count > 5:
            messagebox.showwarning("警告", "公共牌不能超過5張！")
            return
        
        # 顯示計算信息
        board_count = len(self.board_cards)
        if board_count == 0:
            calculation_type = "翻牌前"
        elif board_count == 3:
            calculation_type = "翻牌後"
        elif board_count == 4:
            calculation_type = "轉牌後"
        elif board_count == 5:
            calculation_type = "河牌後"
        else:
            calculation_type = f"{board_count} 張公共牌"
        
        # 確認是否繼續（如果是翻牌前）
        if board_count == 0:
            confirm = messagebox.askyesno(
                "翻牌前計算", 
                f"將進行{calculation_type}勝率計算\n"
                f"({self.num_players}個玩家，無公共牌)\n"
                f"這將使用蒙特卡羅模擬，需要較長時間。\n\n"
                f"是否繼續？"
            )
            if not confirm:
                return
        
        # 轉換為Card物件
        player_hands = []
        for i in range(self.num_players):
            hand = [cw.card for cw in self.player_hands[i]]
            player_hands.append(hand)
        
        board = [cw.card for cw in self.board_cards] if self.board_cards else []
        
        # 開始計算
        self.calculate_button.config(state='disabled', text=f'計算{calculation_type}勝率中...')
        self.progress.start()
        
        def calculate():
            try:
                simulations = 10000
                results = self.calculator.calculate_equity(player_hands, board, simulations)
                self.root.after(0, lambda: self.show_results(results, calculation_type))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("錯誤", f"計算錯誤: {str(e)}"))
            finally:
                self.root.after(0, self.calculation_finished)
        
        thread = threading.Thread(target=calculate)
        thread.daemon = True
        thread.start()
    
    def show_results(self, results, calculation_type):
        """顯示計算結果"""
        result_window = tk.Toplevel(self.root)
        result_window.title(f"🎲 5張奧瑪哈勝率計算結果 - {calculation_type}")
        result_window.geometry("700x600")
        result_window.configure(bg='#2c3e50')
        
        from tkinter import scrolledtext
        
        results_text = scrolledtext.ScrolledText(
            result_window,
            font=('Consolas', 11),
            bg='#34495e',
            fg='#ecf0f1',
            wrap='word'
        )
        results_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        output = f"""🎲 5張奧瑪哈高低牌勝率計算結果 - {calculation_type}
{'='*65}
玩家數量: {self.num_players}
計算類型: {calculation_type}
模擬次數: 10,000 次

💡 總勝率說明：表示該玩家在長期中平均能獲得多少比例的底池
   在奧瑪哈高低牌中，底池通常分為高牌底池(50%)和低牌底池(50%)
   總勝率 = 所有可能結果的加權平均 (所有玩家總勝率應為100%)

"""
        
        for i in range(self.num_players):
            player_key = f'player_{i+1}'
            if player_key in results:
                stats = results[player_key]
                hand_text = " ".join([f"{cw.card.rank}{cw.card.suit}" for cw in self.player_hands[i]])
                
                output += f"""🏆 玩家{i+1} 手牌: {hand_text}
  總勝率(底池期望值): {stats['equity']:.2f}%
  ├─ 高牌獲勝率: {stats['hi_win_rate']:.2f}% ({stats['hi_wins']:,} 次)
  ├─ 低牌獲勝率: {stats['lo_win_rate']:.2f}% ({stats['lo_wins']:,} 次)
  └─ 底池分配情況:
     • 獲得整個底池(100%): {stats['scoop_rate']:.2f}% ({stats['scoops']:,} 次)
     • 平分底池(50%): {stats['split_rate']:.2f}% ({stats['splits']:,} 次)
     • 獲得3/4底池(75%): {stats['three_quarter_rate']:.2f}% ({stats['three_quarters']:,} 次)
     • 獲得1/4底池(25%): {stats['quarter_rate']:.2f}% ({stats['quarters']:,} 次)

"""
        
        board_text = " ".join([f"{cw.card.rank}{cw.card.suit}" for cw in self.board_cards]) if self.board_cards else "(無公共牌 - 翻牌前)"
        output += f"🃏 公共牌: {board_text}\n"
        
        results_text.insert('end', output)
    
    def calculation_finished(self):
        """計算完成"""
        self.calculate_button.config(state='normal', text='🎲 計算勝率')
        self.progress.stop()

def main():
    root = tk.Tk()
    app = ModernOmahaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()