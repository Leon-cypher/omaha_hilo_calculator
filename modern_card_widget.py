"""
現代化撲克牌小部件 - 更貼近真實撲克牌外觀
"""

import tkinter as tk
from tkinter import Canvas

class ModernCardWidget:
    """現代化撲克牌小部件"""
    
    def __init__(self, parent_frame, card, callback=None, width=60, height=85):
        self.card = card
        self.callback = callback
        self.is_selected = False
        self.is_assigned = False
        self.width = width
        self.height = height
        
        # 顏色設定
        self.suit_colors = {
            '♠': '#000000',  # 黑桃 - 黑色
            '♣': '#000000',  # 梅花 - 黑色  
            '♥': '#dc143c',  # 紅心 - 紅色
            '♦': '#dc143c'   # 方塊 - 紅色
        }
        
        # 創建Frame容器
        self.frame = tk.Frame(parent_frame, bg='#2c3e50')
        
        # 創建Canvas作為卡牌
        self.canvas = Canvas(
            self.frame,
            width=width,
            height=height,
            bg='white',
            highlightthickness=2,
            highlightbackground='#333333',
            relief='raised',
            borderwidth=2
        )
        self.canvas.pack(padx=1, pady=1)
        
        # 繪製卡牌
        self.draw_card()
        
        # 綁定事件
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Enter>', self.on_hover_enter)
        self.canvas.bind('<Leave>', self.on_hover_leave)
        
    def draw_card(self):
        """繪製現代化卡牌 - 更接近真實撲克牌外觀"""
        self.canvas.delete("all")
        
        # 獲取顏色
        suit_color = self.suit_colors.get(self.card.suit, '#000000')
        
        # 繪製卡牌背景（白色，帶微妙陰影效果）
        self.create_rounded_rectangle(
            0, 0, self.width, self.height,
            radius=6, fill='white', outline='#d0d0d0', width=1
        )
        
        # 添加內部邊框增加立體感
        self.create_rounded_rectangle(
            1, 1, self.width-1, self.height-1,
            radius=5, fill='', outline='#f5f5f5', width=1
        )
        
        # 牌面值文字
        rank_text = '10' if self.card.rank == 'T' else self.card.rank
        
        # 根據卡片大小調整字體
        if self.width < 60:  # 小尺寸卡片
            rank_font_size = 9
            suit_font_size = 11
            center_font_size = 16 if self.card.suit in ['♠', '♣'] else 15
            corner_rank_size = 7
            corner_suit_size = 9
        else:  # 標準尺寸卡片
            rank_font_size = 11
            suit_font_size = 14
            center_font_size = 22 if self.card.suit in ['♠', '♣'] else 20
            corner_rank_size = 9
            corner_suit_size = 12
        
        # 左上角 - 使用更現代的字體和位置
        self.canvas.create_text(
            6, 4,
            text=rank_text,
            font=('Helvetica', rank_font_size, 'bold'),
            fill=suit_color,
            anchor='nw'
        )
        
        self.canvas.create_text(
            6, 14,
            text=self.card.suit,
            font=('Helvetica', suit_font_size, 'normal'),
            fill=suit_color,
            anchor='nw'
        )
        
        # 中央花色符號 - 更精緻的大小和位置
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=self.card.suit,
            font=('Helvetica', center_font_size, 'normal'),
            fill=suit_color,
            anchor='center'
        )
        
        # 右下角
        self.canvas.create_text(
            self.width - 6, self.height - 4,
            text=rank_text,
            font=('Helvetica', corner_rank_size, 'bold'),
            fill=suit_color,
            anchor='se'
        )
        
        self.canvas.create_text(
            self.width - 6, self.height - 14,
            text=self.card.suit,
            font=('Helvetica', corner_suit_size, 'normal'),
            fill=suit_color,
            anchor='se'
        )
        
        # 如果被選中，添加高亮效果
        if self.is_selected:
            self.create_rounded_rectangle(
                1, 1, self.width-1, self.height-1,
                radius=5, fill='', outline='#27ae60', width=2
            )
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """創建圓角矩形的輔助方法"""
        points = []
        
        # 簡化版圓角矩形，使用直線近似
        points.extend([x1 + radius, y1])
        points.extend([x2 - radius, y1])
        points.extend([x2, y1 + radius])
        points.extend([x2, y2 - radius])
        points.extend([x2 - radius, y2])
        points.extend([x1 + radius, y2])
        points.extend([x1, y2 - radius])
        points.extend([x1, y1 + radius])
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        """點擊事件處理"""
        if self.callback:
            self.callback(self)
    
    def on_hover_enter(self, event):
        """滑鼠進入"""
        if not self.is_selected:
            self.canvas.config(highlightbackground='#3498db', highlightthickness=2)
    
    def on_hover_leave(self, event):
        """滑鼠離開"""
        if not self.is_selected:
            self.canvas.config(highlightbackground='#333333', highlightthickness=2)
    
    def set_selected(self, selected):
        """設置選中狀態"""
        self.is_selected = selected
        if selected:
            self.canvas.config(bg='#e8f5e8', highlightbackground='#2ecc71', highlightthickness=3)
            self.draw_card()  # 重新繪製，會包含選中邊框
        else:
            self.canvas.config(bg='white', highlightbackground='#333333', highlightthickness=2)
            self.draw_card()
    
    def draw_selected_card(self):
        """繪製選中狀態的卡牌 - 已不需要，整合到draw_card中"""
        pass
    
    def set_assigned(self, assigned):
        """設置已分配狀態"""
        self.is_assigned = assigned
        if assigned:
            self.is_selected = False  # 分配時取消選擇
            self.canvas.config(bg='#f8f9fa', highlightbackground='#6c757d')
            self.canvas.delete("all")
            self.draw_assigned_card()
        else:
            self.canvas.config(bg='white', highlightbackground='#333333')
            self.draw_card()
    
    def draw_assigned_card(self):
        """繪製已分配狀態的卡牌"""
        # 獲取顏色（灰色版本）
        original_color = self.suit_colors.get(self.card.suit, '#000000')
        suit_color = '#6c757d'  # 統一灰色
        
        # 繪製卡牌背景
        self.create_rounded_rectangle(
            0, 0, self.width, self.height,
            radius=6, fill='#f8f9fa', outline='#dee2e6', width=1
        )
        
        rank_text = '10' if self.card.rank == 'T' else self.card.rank
        
        # 根據卡片大小調整字體
        if self.width < 60:  # 小尺寸卡片
            rank_font_size = 9
            suit_font_size = 11
            center_font_size = 16 if self.card.suit in ['♠', '♣'] else 15
            corner_rank_size = 7
            corner_suit_size = 9
        else:  # 標準尺寸卡片
            rank_font_size = 11
            suit_font_size = 14
            center_font_size = 22 if self.card.suit in ['♠', '♣'] else 20
            corner_rank_size = 9
            corner_suit_size = 12
        
        # 左上角
        self.canvas.create_text(
            6, 4,
            text=rank_text,
            font=('Helvetica', rank_font_size, 'bold'),
            fill=suit_color,
            anchor='nw'
        )
        
        self.canvas.create_text(
            6, 14,
            text=self.card.suit,
            font=('Helvetica', suit_font_size, 'normal'),
            fill=suit_color,
            anchor='nw'
        )
        
        # 中央
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=self.card.suit,
            font=('Helvetica', center_font_size, 'normal'),
            fill=suit_color,
            anchor='center'
        )
        
        # 右下角
        self.canvas.create_text(
            self.width - 6, self.height - 4,
            text=rank_text,
            font=('Helvetica', corner_rank_size, 'bold'),
            fill=suit_color,
            anchor='se'
        )
        
        self.canvas.create_text(
            self.width - 6, self.height - 14,
            text=self.card.suit,
            font=('Helvetica', corner_suit_size, 'normal'),
            fill=suit_color,
            anchor='se'
        )
    
    def grid(self, **kwargs):
        """網格佈局"""
        self.frame.grid(**kwargs)
    
    def pack(self, **kwargs):
        """包裝佈局"""
        self.frame.pack(**kwargs)