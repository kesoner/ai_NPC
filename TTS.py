from gtts import gTTS
import os

def text_to_speech(text, output_file="output.mp3"):
    """
    將文字轉換為語音並保存為MP3檔案
    
    Args:
        text (str): 要轉換的文字
        output_file (str): 輸出檔案名稱，預設為 output.mp3
    """
    try:
        # 創建 gTTS 物件
        tts = gTTS(text=text, lang='zh-tw')
        
        # 保存為MP3檔案
        tts.save(output_file)
        
        print(f"語音已成功保存為 {output_file}")
        return True
    except Exception as e:
        print(f"轉換過程中發生錯誤: {str(e)}")
        return False 