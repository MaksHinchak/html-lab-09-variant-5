"""Generate local educational audio and video examples using Pillow and ffmpeg."""
from pathlib import Path
from tempfile import TemporaryDirectory
import math
import struct
import subprocess
import wave
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'assets/media'
MEDIA.mkdir(exist_ok=True)
FONT = '/Library/Fonts/Arial Unicode.ttf'

def run(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

with TemporaryDirectory() as directory:
    temp = Path(directory)
    for name, frequencies in [('ready', [523.25, 659.25, 783.99]), ('sequence', [330, 440, 550, 660, 550, 440])]:
        samples = []
        rate = 22050
        for frequency in frequencies:
            length = int(rate * .45)
            for i in range(length):
                envelope = min(i / (rate * .02), (length - 1 - i) / (rate * .05), 1)
                samples.append(int(8500 * envelope * math.sin(2 * math.pi * frequency * i / rate)))
            samples.extend([0] * int(rate * .08))
        with wave.open(str(temp / f'{name}.wav'), 'wb') as output:
            output.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
            output.writeframes(struct.pack('<' + 'h' * len(samples), *samples))
        run('-i', str(temp / f'{name}.wav'), '-codec:a', 'libmp3lame', '-q:a', '4', str(MEDIA / f'{name}.mp3'))

    title_font = ImageFont.truetype(FONT, 26)
    text_font = ImageFont.truetype(FONT, 18)
    for name, title in [('movement', 'Переміщення фігур'), ('transforms', 'Обертання та масштаб')]:
        frames = temp / name
        frames.mkdir()
        for frame in range(60):
            phase = 2 * math.pi * frame / 60
            image = Image.new('RGB', (720, 480), 'white')
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, 720, 85), fill='#0c3158')
            draw.text((26, 10), 'ByteMarket', font=title_font, fill='white')
            draw.text((26, 49), title + ' · варіант 5', font=text_font, fill='#b6eee4')
            def point(x, y):
                return (255 + x * 48, 250 - y * 48)
            color = '#0000ff'
            for index, (x, y) in enumerate([(-2, 1), (1, 1)]):
                if name == 'movement' and index == 0:
                    x += .4 * math.sin(phase)
                radius = 48 * (1 - .25 * (1 - math.cos(phase)) / 2 if name == 'transforms' and index == 1 else 1)
                px, py = point(x, y)
                draw.ellipse((px-radius, py-radius, px+radius, py+radius), fill=color, outline='black', width=1)
            for x, y, width, height in [(-3,-1,2,1),(2,1,1,1),(3,0,1,1),(0,-2,1,1),(1,-3,2,1),(4,-2,1,1)]:
                if name == 'movement' and x == 2:
                    y += .35 * math.sin(phase)
                draw.rectangle((point(x,y+height),point(x+width,y)), fill=color, outline='black')
            angle = phase if name == 'transforms' else 0
            diamond=[]
            for x,y in [(-1,0),(0,1),(1,0),(0,-1)]:
                diamond.append(point(3+x*math.cos(angle)-y*math.sin(angle),-1+x*math.sin(angle)+y*math.cos(angle)))
            draw.polygon(diamond, fill=color, outline='black')
            draw.line((point(-4,0),point(6,0)), fill='black', width=2)
            draw.line((point(0,-3.5),point(0,2.8)), fill='black', width=2)
            draw.text((552,251),'X',font=text_font,fill='black')
            draw.text((262,110),'Y',font=text_font,fill='black')
            draw.text((26,443),'Власний навчальний ролик · 4 с · без звукової доріжки',font=text_font,fill='#174a7e')
            image.save(frames/f'{frame:03d}.png')
            if frame == 0:
                image.save(MEDIA/f'{name}-poster.png')
        run('-framerate','15','-i',str(frames/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','23','-movflags','+faststart',str(MEDIA/f'{name}.mp4'))
        run('-i',str(MEDIA/f'{name}.mp4'),'-c:v','libvpx-vp9','-crf','35','-b:v','0',str(MEDIA/f'{name}.webm'))
print('Generated 2 MP3 recordings and 2 videos in MP4/WebM, with posters.')
