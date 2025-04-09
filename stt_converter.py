import speech_recognition as sr
import threading
import keyboard
import queue
import time
from typing import Optional, Union

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.text_result = None
        self.stop_recording = False
        self.audio = None

    def _listen_for_q_key(self):
        """監聽 Q 鍵"""
        keyboard.wait('q')
        self.stop_recording = True

    def _audio_callback(self, _, audio):
        """音頻回調函數"""
        if not self.stop_recording:
            self.audio_queue.put(audio)

    def from_microphone(self) -> str:
        """從麥克風錄音並轉換為文字，按 Q 鍵結束錄音"""
        try:
            # 創建一個線程來監聽 Q 鍵
            def check_stop_key():
                keyboard.wait('q')
                self.stop_recording = True

            with sr.Microphone() as source:
                print("正在調整環境噪音...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("\n請開始說話（按 Q 鍵結束錄音）...")
                
                # 重置停止標誌
                self.stop_recording = False
                
                # 啟動按鍵監聽線程
                key_thread = threading.Thread(target=check_stop_key)
                key_thread.daemon = True
                key_thread.start()

                # 開始錄音
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
                
                try:
                    # 使用 Google 的語音辨識服務
                    text = self.recognizer.recognize_google(audio, language='zh-TW')
                    return text
                except sr.UnknownValueError:
                    print("\n無法辨識語音")
                    return ""
                except sr.RequestError as e:
                    print(f"\n語音辨識服務錯誤: {str(e)}")
                    return ""

        except Exception as e:
            print(f"\n發生錯誤: {str(e)}")
            return ""

    def from_file(self, audio_file: str) -> str:
        """從音頻檔案轉換為文字"""
        try:
            with sr.AudioFile(audio_file) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language='zh-TW')
            return text
        except sr.UnknownValueError:
            print("\n無法辨識語音")
            return ""
        except sr.RequestError as e:
            print(f"\n語音辨識服務錯誤: {str(e)}")
            return ""
        except Exception as e:
            print(f"\n發生錯誤: {str(e)}")
            return ""

    def start_recording(self) -> None:
        """開始錄音（非阻塞式）"""
        if not self.is_recording:
            self.is_recording = True
            # 這裡可以添加錄音開始的回調函數

    def stop_recording(self) -> str:
        """停止錄音並返回辨識結果"""
        if self.is_recording:
            self.is_recording = False
            return self.from_microphone()
        return ""

if __name__ == "__main__":
    # 測試用
    stt = SpeechToText()
    print("準備開始錄音...")
    time.sleep(1)  # 給使用者準備時間
    text = stt.from_microphone()
    
    # 將結果寫入檔案供後續使用
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(text) 