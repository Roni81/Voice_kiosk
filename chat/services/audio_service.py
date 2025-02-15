import torch
import sounddevice as sd
import numpy as np
import whisper
import wave
import scipy.io.wavfile as wavfile
from tempfile import NamedTemporaryFile
from faster_whisper import WhisperModel


class AudioTranscriber:
    def __init__(self):
        # whisper 모델로드 (크기 선택 가능: Tiny, Base, Small, Medium, Large)
        # GPU 사용 가능 여부 확인
        self.model = WhisperModel(
            "base",
            device = 'cpu',
            compute_type = 'int8',
            cpu_threads = 4
            )
        
        self.samplerate = 16000
        self.channels = 1
    def record_audio(self, duration=5):
        '''
        지정된 시간(초) 동안 오디오 녹음
        '''
        print(f'녹음 시작 ... {duration}초 동안 말씀해 주세요')
        audio_data = sd.rec(
            int(duration * self.samplerate),
            samplerate= self.samplerate,
            channels=self.channels,
            dtype=np.float32
        )
        # sd.rec(샘플 갯수, 샘플레이트, 채널, 데이터 타입(numpy float)
            
        sd.wait()
        print('녹음 완료')

        return audio_data
    

    def save_audio(self, audio_data, filename):
        '''
        녹음된 오디오를 wav파일로 저장
        '''

        audio_data_int = (audio_data * 32767).astype(np.int16)
        wavfile.write(filename, self.samplerate, audio_data_int)

    
    def transcribe(self, audio_file):
        '''
        오디오 파일을 텍스트로 변환
        '''
        segments, info = self.model.transcribe(audio_file, language='ko')
        return " ".join([segment.text for segment in segments])

    def process_audio(self, audio_bytes: bytes, duration: float):
        """업로드된 오디오 바이트 처리 메서드"""
        with NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            # 1. 바이트 데이터를 임시 파일에 저장
            temp_audio.write(audio_bytes)
            temp_audio.flush()
            
            # 2. 음성 인식 실행
            segments, info = self.model.transcribe(temp_audio.name, language='ko')
            transcribed_text = " ".join([segment.text for segment in segments])
            
        return transcribed_text




