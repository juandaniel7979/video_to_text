import os
import subprocess
import torch
import whisper
from tqdm import tqdm
import math

def extract_audio(video_path, audio_path="audio.mp3"):
    """
    Extrae el audio de un archivo de video usando ffmpeg.
    """
    command = [
        "ffmpeg", "-i", video_path,
        "-vn", "-acodec", "mp3",
        audio_path, "-y"
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return audio_path

def transcribe_with_progress(audio_path, model_size="small", output_format="srt", chunk_length=60):
    """
    Transcribe un archivo de audio por fragmentos, mostrando progreso.
    """
    # Detectar dispositivo
    device = "cuda" if torch.cuda.is_available() else "cpu"
    fp16 = device == "cuda"
    model = whisper.load_model(model_size, device=device)

    # Calcular duración total del audio
    import ffmpeg
    probe = ffmpeg.probe(audio_path)
    duration = float(probe['format']['duration'])
    total_chunks = math.ceil(duration / chunk_length)

    print(f"🎧 Duración: {duration:.2f} s | Dividido en {total_chunks} fragmentos")

    # Resultados acumulados
    full_text = ""
    full_segments = []

    # Procesar con barra de progreso
    for i in tqdm(range(total_chunks), desc="Transcribiendo"):
        start = i * chunk_length
        end = min((i + 1) * chunk_length, duration)
        out_file = f"chunk_{i}.mp3"

        # Extraer fragmento
        command = [
            "ffmpeg", "-i", audio_path,
            "-ss", str(start), "-to", str(end),
            "-acodec", "mp3", out_file, "-y"
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Transcribir fragmento
        result = model.transcribe(out_file, fp16=fp16)
        os.remove(out_file)

        # Guardar resultados
        full_text += result["text"] + " "
        for seg in result["segments"]:
            seg["start"] += start
            seg["end"] += start
            full_segments.append(seg)

    # Guardar TXT
    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        f.write(full_text.strip())

    # Guardar SRT
    if output_format == "srt":
        with open("transcripcion.srt", "w", encoding="utf-8") as f:
            for i, seg in enumerate(full_segments, start=1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print("✅ Transcripción completada")
    return full_text

def format_timestamp(seconds: float) -> str:
    """
    Convierte segundos a formato SRT (HH:MM:SS,mmm).
    """
    millisec = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02}:{mins:02}:{secs:02},{millisec:03}"


if __name__ == "__main__":
    video_file = "video.mp4"   # 🔹 Cambia por tu archivo
    audio_file = "audio.mp3"

    

    # 1. Extraer audio
    extract_audio(video_file, audio_file)

    # 2. Transcribir con barra de progreso
    transcribe_with_progress(audio_file, model_size="medium", output_format="srt", chunk_length=60)
