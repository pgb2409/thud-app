from backend.worker import create_score

def test_score_generation():
    golpes = [
        {'time': 0.5, 'type': 'kick'},
        {'time': 1.0, 'type': 'snare'},
        {'time': 1.5, 'type': 'hihat'}
    ]
    archivos = create_score(golpes)
    assert 'json' in archivos and 'musicxml' in archivos and 'midi' in archivos, "Deben generarse los 3 formatos"

# Ejemplo de ejecución:
# test_score_generation()
# print("Test de partitura pasado")
