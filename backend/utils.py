import os
from pydub import AudioSegment

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')

# 1 – Convertir MP3 a WAV
def mp3_to_wav(mp3_file):
    wav_file = mp3_file.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')
    return wav_file

# Ejemplo:
# wav = mp3_to_wav(os.path.join(UPLOAD_FOLDER, 'test.mp3'))

# 2 – Extraer batería (prototipo simple: copia el audio)
def extract_drums(wav_file):
    drums_file = wav_file.replace('.wav', '_drums.wav')
    AudioSegment.from_wav(wav_file).export(drums_file, format='wav')
    return drums_file

# Ejemplo:
# drums = extract_drums(wav)

# 3 – Detectar golpes (simulado)
def detect_hits(drums_file):
    hits = [
        {'time': 0.5, 'type': 'kick'},
        {'time': 1.0, 'type': 'snare'},
        {'time': 1.5, 'type': 'hihat'}
    ]
    return hits

# Ejemplo:
# golpes = detect_hits(drums)

# 4 – Clasificar golpes (ya se incluyen tipos en detect_hits)
def classify_hits(hits):
    # Devuelve lista con tipos ya definidos
    for hit in hits:
        if hit['type'] not in ['kick', 'snare', 'hihat']:
            hit['type'] = 'unknown'
    return hits

# Ejemplo:
# golpes_clasificados = classify_hits(golpes)

# 5 – Calcular ritmo (BPM aproximado)
def calculate_bpm(hits):
    if len(hits) < 2:
        return 120  # Valor por defecto
    times = [hit['time'] for hit in hits]
    diffs = [t2 - t1 for t1, t2 in zip(times, times[1:])]
    avg_diff = sum(diffs) / len(diffs)
    bpm = round(60 / avg_diff)
    return bpm

# Ejemplo:
# bpm = calculate_bpm(golpes_clasificados)

# 6 – Ajustar tiempos al ritmo
def adjust_timing(hits, bpm=120):
    for hit in hits:
        hit['time'] = round(hit['time'] * bpm / 60, 2)
    return hits

# Ejemplo:
# golpes_ajustados = adjust_timing(golpes_clasificados, bpm)
