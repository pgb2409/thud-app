import os
from pydub import AudioSegment
import json
import uuid

# Carpeta de uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads/output')
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def mp3_to_wav(mp3_file):
    wav_file = mp3_file.replace('.mp3', '.wav')
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')
    return wav_file

def extract_drums(wav_file):
    # Función simulada para extraer batería
    # Retorna ruta de archivo de batería (WAV)
    drums_file = wav_file.replace('.wav', '_drums.wav')
    # En un prototipo simple, solo copiamos el archivo
    AudioSegment.from_wav(wav_file).export(drums_file, format='wav')
    return drums_file

def detect_hits(drums_file):
    # Función simulada para detectar golpes
    # Retorna lista de golpes con tiempo y tipo
    hits = [
        {'time': 0.5, 'type': 'kick'},
        {'time': 1.0, 'type': 'snare'},
        {'time': 1.5, 'type': 'hihat'}
    ]
    return hits

def adjust_timing(hits, bpm=120):
    # Ajusta los tiempos de los golpes al ritmo
    for hit in hits:
        hit['time'] = round(hit['time'] * bpm / 60, 2)
    return hits

def generate_score(hits):
    # Genera partitura simulada en JSON, MusicXML y MIDI
    score_id = uuid.uuid4().hex
    score = {
        'json': json.dumps(hits),
        'musicxml': f"<score-partwise id='{score_id}'></score-partwise>",
        'midi': f"{score_id}.midi"
    }
    return score

# Función principal para procesar archivo
def process_file(filename):
    mp3_path = os.path.join(UPLOAD_FOLDER, filename)
    wav_path = mp3_to_wav(mp3_path)
    drums_path = extract_drums(wav_path)
    hits = detect_hits(drums_path)
    hits = adjust_timing(hits)
    score = generate_score(hits)
    return score

# Ejemplo de prueba
if __name__ == '__main__':
    test_file = 'test.mp3'  # Cambiar por un MP3 real en uploads/
    if os.path.exists(os.path.join(UPLOAD_FOLDER, test_file)):
        resultado = process_file(test_file)
        print("Resultado del procesamiento:", resultado)
    else:
        print(f"No se encontró el archivo {test_file} en uploads/")
import shutil
from app import processed_files, pending_files

def save_score_files(filename, score):
    output_folder = os.path.join(os.path.dirname(__file__), '../uploads/output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Guardar JSON
    json_path = os.path.join(output_folder, filename.replace('.mp3', '.json'))
    with open(json_path, 'w') as f:
        f.write(score['json'])
    
    # Guardar MusicXML
    xml_path = os.path.join(output_folder, filename.replace('.mp3', '.musicxml'))
    with open(xml_path, 'w') as f:
        f.write(score['musicxml'])
    
    # Guardar MIDI (simulado)
    midi_path = os.path.join(output_folder, score['midi'])
    # Para prototipo, copiamos el MP3 como archivo MIDI de prueba
    shutil.copy(os.path.join(os.path.dirname(__file__), '../uploads', filename), midi_path)
    
    # Actualizar estado en app.py
    processed_files[filename] = {
        'json': score['json'],
        'musicxml': score['musicxml'],
        'midi': score['midi']
    }
    if filename in pending_files:
        pending_files.remove(filename)
import json
from midiutil import MIDIFile

def create_score(hits, output_prefix='../uploads/output/score'):
    """
    Recibe la lista de golpes ajustados y genera:
    - JSON
    - MusicXML (simplificado)
    - MIDI
    """
    if not hits:
        return None

    # 1 – JSON
    json_path = f'{output_prefix}.json'
    with open(json_path, 'w') as f:
        json.dump(hits, f, indent=2)

    # 2 – MusicXML (muy simple prototipo)
    musicxml_path = f'{output_prefix}.xml'
    musicxml_content = '<?xml version="1.0"?>\n<score-partwise version="3.1">\n  <part id="P1">\n'
    for i, hit in enumerate(hits):
        note_type = 'quarter'
        if hit['type'] == 'kick':
            step = 'C'
        elif hit['type'] == 'snare':
            step = 'D'
        else:
            step = 'E'
        musicxml_content += f'    <note>\n      <pitch><step>{step}</step><octave>4</octave></pitch>\n      <duration>1</duration>\n      <type>{note_type}</type>\n    </note>\n'
    musicxml_content += '  </part>\n</score-partwise>'
    with open(musicxml_path, 'w') as f:
        f.write(musicxml_content)

    # 3 – MIDI
    midi_path = f'{output_prefix}.mid'
    midi = MIDIFile(1)
    midi.addTempo(track=0, time=0, tempo=120)
    for hit in hits:
        if hit['type'] == 'kick':
            pitch = 36
        elif hit['type'] == 'snare':
            pitch = 38
        else:
            pitch = 42
        midi.addNote(track=0, channel=0, pitch=pitch, time=hit['time'], duration=0.5, volume=100)
    with open(midi_path, 'wb') as f:
        midi.writeFile(f)

    return {
        'json': json_path,
        'musicxml': musicxml_path,
        'midi': midi_path
    }

# Ejemplo de uso:
# from utils import adjust_timing, classify_hits, detect_hits
# golpes = detect_hits('../uploads/example_drums.wav')
# golpes_clasificados = classify_hits(golpes)
# golpes_ajustados = adjust_timing(golpes_clasificados, bpm=120)
# archivos = create_score(golpes_ajustados)
# print('Archivos generados:', archivos)
