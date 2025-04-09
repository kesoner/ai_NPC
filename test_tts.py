from gtts import gTTS

def text_to_speech(text, output_file="test_output.mp3"):
    """將文字轉換為語音"""
    tts = gTTS(text=text, lang='zh-tw', slow=False)
    tts.save(output_file)
    print(f"測試音頻檔案已儲存為 {output_file}")

if __name__ == "__main__":
    # 測試用
    test_text = "你好，這是一個測試。我是MAX，很高興認識你。"
    text_to_speech(test_text) 