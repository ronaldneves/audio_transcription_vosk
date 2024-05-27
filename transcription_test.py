import os
import wave 
import json 
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from pydub.utils import mediainfo

def conversor_taxa_audio(original, convertido):
    if not os.path.isfile(original):
        print(f"Erro: o arquivo {original} não foi encontrado.")
        return 

    try:    
        audio = AudioSegment.from_file(original)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(convertido, format = "wav")
        print(f"Arquivo convertido com sucesso: {convertido}")

        info = mediainfo(convertido)
        print(f"Amostragem do arquivo convertido: {info['sample_rate']}")
        print(f"Canais do arquivo {convertido}: {info['channels']} ")
    
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")


modelo_transcricao = 'model'
audio_original = 'teste2.wav'
audio_saida = 'output_teste_2.wav'

conversor_taxa_audio(audio_original, audio_saida)

if not os.path.exists(modelo_transcricao):
    print("Baixe o modelo de linguagem e coloque-o no diretório correto.")
    exit(1)

try:    
    model = Model(modelo_transcricao)
    print("Modelo carregado")

except Exception as e:
    print(f'Falha ao criar o modelo: {e}')
    exit(1)

try:
    wf = wave.open(audio_saida, "rb")
    print("Arquivo de audio carregado")

except FileNotFoundError:
    print(f'Arquivo {audio_saida} nao encontrado')
    exit(1)

except Exception as e:
    print(f'Falha ao abrir o arquivo de audio: {e}')
    exit(1)

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("O arquivo não é mono ou não está com 16000 Hz.")
    exit(1)

rec = KaldiRecognizer(model, wf.getframerate())

results = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        results.append(json.loads(rec.Result()))
    else:
        results.append(json.loads(rec.PartialResult()))


results.append(json.loads(rec.FinalResult()))

recognized_text = " ".join([res.get("text", "") for res in results])
print("Texto reconhecido:", recognized_text)