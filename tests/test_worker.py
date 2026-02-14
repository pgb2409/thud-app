from backend.utils import detect_hits, classify_hits, adjust_timing, calculate_bpm, extract_drums, mp3_to_wav

def test_worker_pipeline():
    mp3 = '../uploads/test.mp3'
    wav = mp3_to_wav(mp3)
    drums = extract_drums(wav)
    hits = detect_hits(drums)
    hits_clasificados = classify_hits(hits)
    bpm = calculate_bpm(hits_clasificados)
    hits_ajustados = adjust_timing(hits_clasificados, bpm)
    assert len(hits_ajustados) > 0, "Debe detectar al menos un golpe"

# Ejemplo de ejecución:
# test_worker_pipeline()
# print("Test de procesamiento pasado")
