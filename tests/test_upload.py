import os
from backend.app import mp3_to_wav, UPLOAD_FOLDER

def test_upload():
    test_file = os.path.join(UPLOAD_FOLDER, 'test.mp3')
    assert os.path.exists(test_file), "El archivo MP3 debe existir"
    wav_file = mp3_to_wav(test_file)
    assert os.path.exists(wav_file), "El archivo WAV debe crearse"

# Ejemplo de ejecución:
# test_upload()
# print("Test de subida pasado")
