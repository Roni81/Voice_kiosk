from gtts import gTTS
import os
import pygame

class KoreanTTS:

    def __init__(self):

        self.language = 'ko'

        pygame.mixer.init()

    

    
    def text_to_speech(self, text, file_name = 'out_put.mp3', keep_file = False):
        '''
        텍스트를 음성으로 변환
        save = True 면 저장, False는 재생 후 삭제
        '''

        try:

            # TTS 생성
            tts = gTTS(text=text, lang=self.language)
            tts.save(file_name)

            # 음성 파일 출력
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)


            # 파일 삭제

            if not keep_file:
                os.remove(file_name)


        except Exception as e:
            print(f"Error: {str(e)}")
            


