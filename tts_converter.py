from gtts import gTTS
import os

def text_to_speech(text, output_file="output.mp3"):
    try:
        # 使用 gTTS 將文字轉換為語音
        tts = gTTS(text=text, lang='zh-tw', slow=False)
        
        # 儲存音頻檔案
        tts.save(output_file)
        print(f"音頻檔案已儲存為 {output_file}")
        return True
    except Exception as e:
        print(f"轉換語音時發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    # 從 app.py 的輸出讀取文字
    with open("output.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # 轉換為語音
    text_to_speech(text) 