from stt_converter import SpeechToText
from tts_converter import text_to_speech
import requests
import json
from dotenv import load_dotenv
import os
import time
from playsound import playsound

# 載入環境變數
load_dotenv()

class TerminalApp:
    def __init__(self):
        self.stt = SpeechToText()
        self.api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCXRgg9MKDCkN_VvsxiY1jobRqo3SjdIKQ')
        self.is_first_conversation = True
        self.prompts = self._load_prompts()
        self.initial_response = None
        # 創建音頻檔案目錄
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

    def _load_prompts(self):
        """載入所有提示詞"""
        prompts = []
        prompt_dir = r"D:\code by corsor\gemini_custom_prompt\prompts\C0"
        
        # 檢查資料夾是否存在
        if not os.path.exists(prompt_dir):
            print(f"錯誤：找不到提示詞資料夾 {prompt_dir}")
            return prompts
        
        # 先讀取固定提示詞文件
        fixed_prompt_path = os.path.join(prompt_dir, "固定_prompt.txt")
        if os.path.exists(fixed_prompt_path):
            try:
                with open(fixed_prompt_path, 'r', encoding='utf-8') as f:
                    fixed_prompt = f.read().strip()
                    prompts.append(fixed_prompt)
                    print("\n已載入固定提示詞：")
                    print(fixed_prompt)
                    print("-" * 50)
            except Exception as e:
                print(f"警告：讀取固定提示詞文件時發生錯誤: {str(e)}")
        else:
            print("警告：找不到固定提示詞文件 固定_prompt.txt")
        
        # 讀取資料夾中其他的 .txt 文件
        for file_name in os.listdir(prompt_dir):
            if file_name.endswith('.txt') and file_name != "固定_prompt.txt":
                file_path = os.path.join(prompt_dir, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        prompt_content = f.read().strip()
                        prompts.append(prompt_content)
                        print(f"\n已載入提示詞文件 {file_name} 的內容：")
                        print(prompt_content)
                        print("-" * 50)
                except Exception as e:
                    print(f"警告：讀取文件 {file_name} 時發生錯誤: {str(e)}")
        
        if not prompts:
            print("錯誤：沒有找到任何提示詞文件")
        else:
            print(f"\n總共載入了 {len(prompts)} 個提示詞文件")
        
        return prompts

    def _initialize_gemini(self):
        """初始化 Gemini，發送所有提示詞"""
        if self.is_first_conversation:
            print("\n正在初始化 Gemini...")
            system_prompt = "\n".join(self.prompts)
            print("\n發送給 Gemini 的初始化提示詞：")
            print(system_prompt)
            print("-" * 50)
            self._call_gemini_api(system_prompt)
            print("初始化完成！")
            self.is_first_conversation = False
            

    def _call_gemini_api(self, prompt):
        """呼叫 Gemini API"""
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}'
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            
            # 從回應中提取文字
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                if 'content' in response_data['candidates'][0]:
                    if 'parts' in response_data['candidates'][0]['content']:
                        if len(response_data['candidates'][0]['content']['parts']) > 0:
                            if 'text' in response_data['candidates'][0]['content']['parts'][0]:
                                return response_data['candidates'][0]['content']['parts'][0]['text']
            
            return "抱歉，我無法理解您的問題。"
        except requests.exceptions.RequestException as e:
            return f"錯誤: {str(e)}"

    def get_gemini_response(self, prompt):
        # 組合所有提示詞和使用者輸入
        system_prompt = "\n".join(self.prompts)
        full_prompt = f"{system_prompt}\n\n使用者: {prompt}\n助手:"
        print("-" * 50)
        
        return self._call_gemini_api(full_prompt)

    def process_voice_input(self):
        print("\n=== 語音輸入模式 ===")
        print("請開始說話（按 Q 鍵結束錄音）...")
        
        # 錄音並轉換為文字
        text = self.stt.from_microphone()
        if not text:
            print("沒有偵測到語音輸入")
            return
            
        print(f"\n辨識結果: {text}")
        
        # 獲取 Gemini 回應
        print("\n正在獲取 Gemini 回應...")
        response_text = self.get_gemini_response(text)
        print(f"\nGemini 回應: {response_text}")
        
        # 將回應轉換為語音並播放
        print("\n正在轉換為語音...")
        audio_path = os.path.join(self.audio_dir, "response.mp3")
        
        # 確保音頻文件成功生成
        if text_to_speech(response_text, audio_path):
            print(f"音頻檔案已生成：{audio_path}")
            
            # 檢查文件是否存在
            if os.path.exists(audio_path):
                print("\n正在播放回應...")
                try:
                    playsound(audio_path)
                    print("播放完成！")
                    # 播放完畢後刪除音檔
                    try:
                        os.remove(audio_path)
                        print("音檔已刪除")
                    except Exception as e:
                        print(f"刪除音檔時發生錯誤: {str(e)}")
                except Exception as e:
                    print(f"播放音檔時發生錯誤: {str(e)}")
            else:
                print(f"錯誤：音頻文件未成功生成")
        else:
            print("錯誤：語音轉換失敗")

    def run(self):
        print("=== 語音對話系統 ===")
        print("1. 開始語音對話")
        print("2. 退出")
        
        while True:
            choice = input("\n請選擇操作 (1-2): ")
            
            if choice == "1":
                self.process_voice_input()
            elif choice == "2":
                print("再見！")
                break
            else:
                print("無效的選擇，請重新輸入")

if __name__ == "__main__":
    app = TerminalApp()
    app.run() 