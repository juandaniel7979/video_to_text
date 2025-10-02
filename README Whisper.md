## Video a texto con Whisper (Windows/Linux/Mac)

Herramienta de línea de comandos para:

- Extraer audio de un video con `ffmpeg`.
- Transcribir con `openai-whisper`.
- Exportar a `.txt`, `.srt` y `.vtt`.

### Requisitos

- ffmpeg instalado y disponible en `PATH`.
  - Windows: use el instalador de `Gyan.dev` o `Chocolatey`: `choco install ffmpeg`.
  - Linux: `sudo apt install ffmpeg` o equivalente.
  - macOS: `brew install ffmpeg`.
- Python 3.9+.
- (Opcional) GPU con CUDA para acelerar Whisper (instale PyTorch con CUDA de acuerdo a su GPU).

### Instalación

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows PowerShell
pip install -U pip
pip install -r requirements.txt
```

Si desea soporte GPU, instale PyTorch según su entorno desde `https://pytorch.org` y luego `pip install -U openai-whisper`.

### Uso

```bash
python transcribe.py ruta\\al\\video.mp4 --basename salida --srt --txt
```

Parámetros útiles:

- `--audio-out`: ruta del audio extraído (por extensión define codec: `.mp3`, `.wav`, `.m4a`).
- `--model`: `tiny`, `base`, `small`, `medium`, `large`.
- `--language`: fuerza idioma, p. ej. `es`, `en`.
- `--txt`, `--srt`, `--vtt`: formatos de salida. Si no especifica, por defecto guarda TXT y SRT.
- `--basename`: nombre base para archivos de salida.

Ejemplos:

```bash
python transcribe.py video.mp4 --basename transcripcion --srt --txt
python transcribe.py video.mp4 --audio-out audio.wav --model small --vtt
```

Los archivos generados quedarán como `transcripcion.txt`, `transcripcion.srt`, `transcripcion.vtt`.

### Notas

- Para resultados más rápidos en CPU, use modelos `tiny` o `base`. Para mejor calidad, use `small`/`medium`/`large`.
- Si ffmpeg no se encuentra, asegúrese de que el ejecutable esté en el `PATH` del sistema.


