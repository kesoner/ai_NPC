# Gemini 語音對話系統

這是一個基於 Google Gemini API 的語音對話系統，可以進行語音輸入並獲得 AI 回應。

## 功能特點

- 支援語音輸入和文字轉語音輸出
- 使用 Google Gemini API 進行對話
- 可自定義提示詞（prompts）
- 簡單的終端機介面操作

## 系統需求

- Python 3.x
- 麥克風（用於語音輸入）
- 喇叭（用於語音輸出）

## 安裝步驟

1. 克隆此專案到本地：
```bash
git clone [repository-url]
cd gemini_custom_prompt
```

2. 安裝所需套件：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
   - 在專案根目錄創建 `.env` 文件
   - 添加你的 Gemini API 金鑰：
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## 使用說明

1. 啟動程式：
```bash
python main.py
```

2. 在主選單中選擇操作：
   - 選項 1：開始語音對話
   - 選項 2：退出程式

3. 在語音對話模式中：
   - 按 Q 鍵結束錄音
   - 系統會自動將語音轉換為文字
   - 使用 Gemini API 生成回應
   - 將回應轉換為語音並播放

## 提示詞設定

- 提示詞文件位於 `prompts/C0` 目錄
- `固定_prompt.txt` 為固定提示詞
- 其他 `.txt` 文件為額外提示詞
- 所有提示詞會在初始化時載入

## 注意事項

- 確保網路連接正常
- 使用時請保持安靜環境
- 語音輸入結束後按 Q 鍵
- 音頻文件會自動生成和刪除

## 錯誤處理

- 如果遇到 API 錯誤，請檢查 API 金鑰是否正確
- 如果語音辨識失敗，請確保麥克風正常運作
- 如果音頻播放失敗，請檢查喇叭設定


## 聯絡方式

[聯絡資訊] 