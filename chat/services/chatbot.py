from openai import OpenAI
import os

class Chatbot:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        
    def get_response(self, user_input):
        # 대화 기록에 사용자 입력 추가
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # API 호출하여 응답 받기
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            # 응답 텍스트 추출
            bot_response = response.choices[0].message.content
            
            # 대화 기록에 봇 응답 추가
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            return bot_response
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return "죄송합니다. 오류가 발생했습니다."
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []