class SimpleChatbot:
    def __init__(self):
        self.responses = {
            "안녕": "안녕하세요! 무엇을 도와드릴까요?",
            "날씨": "죄송합니다. 현재 날씨 정보는 제공할 수 없습니다.",
            "시간": "현재 시각을 알려드릴 수 있습니다.",
        }
        
    def get_response(self, user_input):
        for key in self.responses:
            if key in user_input:
                return self.responses[key]
        return "죄송합니다. 이해하지 못했습니다. 다시 말씀해주시겠어요?"