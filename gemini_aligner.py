# gemini_aligner.py
import os
import google.generativeai as genai
import json
import re

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

GEMINI_PROMPT_TEMPLATE = '''
你是一個英文學習助教，專門協助標記句子中的關鍵單字或片語。

請執行以下任務：
1. 根據提供的 "word_or_phrase"，找出它在 "sentence" 中出現的位置。
2. 忽略所有標點符號與所有格（如 John’s 視為 John）。
3. 計算詞語在句子中的詞彙起始與結束位置（以單字為單位，從 1 開始編號）。
4. 若為片語，請連續比對詞彙。
5. 若找不到完全匹配的詞形，請判斷是否為詞形變化（如 go → went），若是請照樣標記，並在 match_form 中說明實際出現的詞。
6. 若無法辨識或不確定，請回傳 status 為 "人工處理"。

請以 JSON 格式回傳：
{
  "mark_start": <整數>,
  "mark_end": <整數>,
  "status": "OK" 或 "人工處理",
  "match_form": "實際出現的詞形（若不同）"
}

word_or_phrase: {{word_or_phrase}}
sentence: {{sentence}}
'''

def call_gemini_for_alignment(word_or_phrase, sentence):
    prompt = GEMINI_PROMPT_TEMPLATE.replace("{{word_or_phrase}}", word_or_phrase).replace("{{sentence}}", sentence)

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    try:
        content = response.text.strip()
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_text = match.group()
            return json.loads(json_text)
        else:
            return {"status": "人工處理"}
    except Exception as e:
        print("[Gemini Error]", e)
        return {"status": "人工處理"}

# 測試
if __name__ == '__main__':
    result = call_gemini_for_alignment("in the end", "We worked hard, and in the end, we succeeded.")
    print(result)
