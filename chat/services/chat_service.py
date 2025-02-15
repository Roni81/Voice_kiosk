import requests
import re

class ChatService:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"


    def clean_text(self, text):
        # 특수문자 및 이모지 제거
        clean = re.sub(r'[^\w\s가-힣.]', '', text)
        # 불필요한 공백 제거
        clean = ' '.join(clean.split())
        return clean
        
    def get_response(self, text):



        try:
            # API 호출하여 응답 받기
            # 명확한 한국어 지시사항을 포함한 프롬프트
            prompt = f"""아래는 사용자와 AI 어시스턴트의 대화입니다.
            어시스턴트는 반드시 한국어로만 자연스럽게 대답합니다.
            특수문자나 이모지를 사용하지 않고 순수하게 텍스트로만 대화합니다.
            
            사용자: {text}
            어시스턴트: """

            headers = {'Content-Type': 'application/json'}
            data = {
                "model": "llama2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.api_url, json=data, headers=headers)
        
            # 응답 텍스트 추출
            if response.status_code == 200:
                bot_response = response.json()['response']
            
                return bot_response
            else:
                return f"에러: API 응답 코드 {response.status_code}"
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return "죄송합니다. 오류가 발생했습니다."
    
    # def clear_history(self):
    #     """대화 기록 초기화"""
    #     self.conversation_history = []