from django.http import JsonResponse
from django.shortcuts import render
from .services.audio_service import AudioTranscriber
from .services.chat_service import ChatService
from .services.tts_service import KoreanTTS
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def chat_view(request):
    if request.method == 'POST':
        try:
            audio_file = request.FILES.get('audio')
            duration = float(request.POST.get('duration', 5))

            # 서비스 초기화
            transcriber = AudioTranscriber()
            chatbot = ChatService()
            tts = KoreanTTS()
            
            # 오디오 바이트 읽기
            audio_bytes = audio_file.read()
            
            # 수정된 메서드 호출 ✅
            text = transcriber.process_audio(audio_bytes, duration) 

            # 5. 텍스트 유효성 검사
            if not text.strip():
                return JsonResponse({
                    'success': False,
                    'error': '인식된 텍스트가 없습니다'
                })

            # 6. 챗봇 응답 생성
            response = chatbot.get_response(text)
            clean_res = chatbot.clean_text(response)
            
            # 7. TTS 변환
            audio_response = tts.text_to_speech(clean_res)

            return JsonResponse({
                'success': True,
                'text': text,
                'response': clean_res,
                'audio_url': audio_response
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'처리 실패: {str(e)}'
            })

    # GET 요청 처리
    return render(request, 'index.html')