"""
撲克牌基礎類別
"""

class Card:
    """撲克牌類別"""
    
    SUITS = ['♠', '♥', '♦', '♣']  # 黑桃、紅心、方塊、梅花
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    
    def __init__(self, rank, suit):
        if rank not in self.RANKS:
            raise ValueError(f"無效的牌面: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"無效的花色: {suit}")
        
        self.rank = rank
        self.suit = suit
        self.value = self.RANKS.index(rank) + 2  # 2=2, 3=3, ..., A=14
        self.low_value = 14 if rank == 'A' else self.value  # A在低牌中為1
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return f"Card('{self.rank}', '{self.suit}')"
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))

class Deck:
    """牌堆類別"""
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """重置牌堆"""
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
    
    def remove_cards(self, cards):
        """從牌堆中移除指定牌"""
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)
    
    def get_remaining_cards(self):
        """獲取剩餘的牌"""
        return self.cards.copy()

def parse_card(card_str):
    """
    解析牌的字符串表示
    例如: 'As' -> Card('A', '♠')
    """
    if len(card_str) != 2:
        raise ValueError(f"牌的格式錯誤: {card_str}")
    
    rank = card_str[0].upper()
    suit_char = card_str[1].lower()
    
    suit_map = {
        's': '♠', 'spade': '♠', 'spades': '♠',
        'h': '♥', 'heart': '♥', 'hearts': '♥', 
        'd': '♦', 'diamond': '♦', 'diamonds': '♦',
        'c': '♣', 'club': '♣', 'clubs': '♣'
    }
    
    if suit_char not in suit_map:
        raise ValueError(f"無效的花色: {suit_char}")
    
    return Card(rank, suit_map[suit_char])

def parse_cards(cards_str):
    """
    解析多張牌的字符串
    例如: 'As Kh Qd Jc' -> [Card('A', '♠'), Card('K', '♥'), ...]
    """
    if not cards_str.strip():
        return []
    
    card_strings = cards_str.strip().split()
    return [parse_card(card_str) for card_str in card_strings]