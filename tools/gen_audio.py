"""Synthesize the 112 英聽 audio from the transcripts in bank/112_listening.json.

Uses the Windows SAPI voice Microsoft Zira (the only English voice on this
machine). Male lines ("M:") use the same voice made deeper: synthesized
28% faster at a low pitch, then resampled 1.28x slower, which lowers the
pitch and formants (~180 Hz -> ~125 Hz) while keeping the original length.
Output: ../public/audio/listening/112/aNN.wav (16 kHz mono).
"""
import json
import os
import subprocess
import tempfile
import wave
from xml.sax.saxutils import escape

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'public', 'audio', 'listening', '112')
RATE = 16000
MALE_STRETCH = 1.28

PS = r'''
Add-Type -AssemblyName System.Speech
$jobs = Get-Content -Raw -Encoding UTF8 $args[0] | ConvertFrom-Json
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(16000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
foreach ($j in $jobs) {
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $s.SelectVoice('Microsoft Zira Desktop')
  $s.SetOutputToWaveFile($j.file, $fmt)
  $s.SpeakSsml($j.ssml)
  $s.Dispose()
}
'''


def ssml(text, male):
    body = escape(text)
    if male:
        body = f"<prosody pitch='x-low' rate='+28%'>{body}</prosody>"
    return f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>{body}</speak>"


def read(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64)


def silence(sec):
    return np.zeros(int(RATE * sec))


def main():
    bank = json.load(open(os.path.join(HERE, 'bank', '112_listening.json'), encoding='utf-8'))
    tmp = tempfile.mkdtemp()
    jobs, plan = [], {}
    for qno, segs in bank['transcripts'].items():
        plan[qno] = []
        for k, (who, text) in enumerate(segs):
            if who == 'Q':
                text = 'Question. ' + text
            f = os.path.join(tmp, f'{int(qno):02d}_{k:02d}.wav')
            jobs.append({'file': f, 'ssml': ssml(text, who == 'M')})
            plan[qno].append((who, f))
    job_file = os.path.join(tmp, 'jobs.json')
    with open(job_file, 'w', encoding='utf-8') as fh:
        json.dump(jobs, fh, ensure_ascii=False)
    ps_file = os.path.join(tmp, 'tts.ps1')
    with open(ps_file, 'w', encoding='utf-8-sig') as fh:
        fh.write(PS)
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps_file, job_file], check=True)

    os.makedirs(OUT, exist_ok=True)
    durations = {}
    for qno, parts in plan.items():
        audio = [silence(0.4)]
        for k, (who, f) in enumerate(parts):
            a = read(f)
            if who == 'M':
                a = np.interp(np.arange(0, len(a) - 1, 1 / MALE_STRETCH), np.arange(len(a)), a)
            if k:
                audio.append(silence(1.0 if who == 'Q' else 0.5))
            audio.append(a)
        audio.append(silence(0.4))
        pcm = np.clip(np.concatenate(audio), -32768, 32767).astype('<i2')
        path = os.path.join(OUT, f'a{int(qno):02d}.wav')
        with wave.open(path, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(RATE)
            w.writeframes(pcm.tobytes())
        durations[qno] = round(len(pcm) / RATE, 1)
    print('durations (s):', durations)
    print('total seconds:', round(sum(durations.values()), 1))


if __name__ == '__main__':
    main()
