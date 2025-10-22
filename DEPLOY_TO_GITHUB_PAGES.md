# 🚀 部署到 GitHub Pages 指南

## 📁 文件說明

### 🎯 核心文件
- `vue-omaha-calc.html` - **Vue 版本**（推薦用於 GitHub Pages）
- `web_standalone.html` - 純 JavaScript 版本
- 原始 Python 文件 - 桌面版本

## 🌐 部署到 GitHub Pages

### 步驟 1：創建 GitHub 存儲庫
1. 在 GitHub 創建新的公開存儲庫
2. 存儲庫名稱建議：`omaha-hilo-calculator`

### 步驟 2：上傳文件
```bash
# 初始化 Git
git init
git add .
git commit -m "Initial commit - Omaha Hi-Lo Calculator"

# 連接到 GitHub 存儲庫
git remote add origin https://github.com/YOUR_USERNAME/omaha-hilo-calculator.git
git branch -M main
git push -u origin main
```

### 步驟 3：啟用 GitHub Pages
1. 進入存儲庫設定（Settings）
2. 滾動到 "Pages" 部分
3. Source 選擇 "Deploy from a branch"
4. Branch 選擇 "main" 
5. Folder 選擇 "/ (root)"
6. 點擊 "Save"

### 步驟 4：設定主頁
將 `vue-omaha-calc.html` 重命名為 `index.html`：
```bash
# 在存儲庫根目錄
mv vue-omaha-calc.html index.html
git add .
git commit -m "Set Vue version as main page"
git push
```

## 📱 訪問您的應用

部署完成後，您的應用將可在以下網址訪問：
```
https://YOUR_USERNAME.github.io/omaha-hilo-calculator/
```

## 🎮 功能特點

### ✅ 完整功能
- 支援 2-9 個玩家
- 5 張手牌奧瑪哈規則
- 高低分池計算
- 蒙特卡羅模擬（2000-20000次）
- 響應式設計（手機友好）

### 📊 計算結果
- 總勝率 (Equity)
- 高牌獲勝率
- 低牌獲勝率  
- Scoop 率（獨得整個底池）
- Split 率（平分底池）

### 🎯 使用方式
1. 選擇玩家數量
2. 輸入每個玩家的 5 張手牌
3. 可選：輸入已知公共牌
4. 選擇模擬次數
5. 點擊「計算勝率」

### 🃏 牌面格式
```
As Kh Qd Jc Ts
花色：s(♠) h(♥) d(♦) c(♣)
牌值：A, 2-9, T, J, Q, K
```

## 🔄 更新應用

要更新應用，只需：
1. 修改 HTML 文件
2. 提交並推送到 GitHub：
```bash
git add .
git commit -m "Update calculator features"
git push
```

GitHub Pages 會自動重新部署！

## 🎉 分享給朋友

部署完成後，直接分享 GitHub Pages 網址給您的牌友們：
- 無需安裝任何應用
- 直接用手機瀏覽器開啟
- 支援離線使用（加載一次後）
- 跨平台兼容（iOS、Android、桌面）

---

**享受您的專業級奧瑪哈高低牌勝率計算器！** 🎊