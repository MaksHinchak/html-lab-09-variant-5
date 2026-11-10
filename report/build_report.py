from pathlib import Path
from shutil import copy2
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Preformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report/lab9-media-variant5.pdf'
DESKTOP=Path('/Users/maksimginchak/Desktop/Лабораторні/HTML/Лаба 9 Медіаресурси варіант 5.pdf')
pdfmetrics.registerFont(TTFont('ArialUA','/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('ArialUA',normal='ArialUA',bold='ArialBold')
pdfmetrics.registerFont(TTFont('CourierUA','/System/Library/Fonts/Supplemental/Courier New.ttf'))
BLUE=colors.HexColor('#174a7e'); LINE=colors.HexColor('#c9d8e2'); PALE=colors.HexColor('#f2f8fb')
body=ParagraphStyle('body',fontName='ArialUA',fontSize=10.5,leading=16,spaceAfter=8)
heading=ParagraphStyle('heading',fontName='ArialBold',fontSize=13,leading=18,textColor=BLUE,spaceBefore=5,spaceAfter=9)
example=ParagraphStyle('example',parent=heading,fontSize=14,leading=19,spaceAfter=11)
small=ParagraphStyle('small',parent=body,fontSize=10,leading=14)
cell=ParagraphStyle('cell',parent=body,fontSize=9,leading=13,spaceAfter=0)
white=ParagraphStyle('white',parent=cell,fontName='ArialBold',textColor=colors.white)
code=ParagraphStyle('code',fontName='CourierUA',fontSize=8,leading=10)
WIDTH=470.5512
story=[]
def p(s,style=body): return Paragraph(s,style)
def h(s): story.append(p(s,heading))
def paragraph(s,style=body): story.append(p(s,style))
def screenshot(name):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 story.append(Image(str(path),width=WIDTH,height=ht*WIDTH/w))
 story.append(Spacer(1,10))
def source(text):
 block=Preformatted(text.strip(),code)
 t=Table([[block]],colWidths=[WIDTH],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
 story.append(t);story.append(Spacer(1,10))
def page(): story.append(PageBreak())
def example_start(title):
 story.append(p(title,example))
 story.append(p('Сторінка: javascript.html. Скріншот реального сайту у Chrome, ширина вікна 1280 px.',small))


import json
results=json.loads((ROOT/'report/check-results.json').read_text())
def grid(rows,widths):
 t=Table([[p(escape(str(s)),white if i==0 else cell) for s in row] for i,row in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,10))
def image_fit(name,max_height):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 width=min(WIDTH,max_height*w/ht)
 story.append(Image(str(path),width=width,height=ht*width/w,hAlign='LEFT'));story.append(Spacer(1,10))


story.append(Spacer(1,680));page()
h('Завдання')
paragraph('Розробити власну бібліотеку медіаресурсів. Обов’язково використати audio, video та source. Створити меню бібліотеки з використанням елементів форм. Структура та наповнення визначаються самостійно. Роботу оформлено як продовження проєкту варіанта №5.')
h('Структура бібліотеки ByteMarket')
grid([['Розділ','Наповнення'],['Аудіо','«Сигнал готовності» - три висхідні ноти, 1.59 с. «Послідовність частот» - шість тонів, 3.18 с. Формат MP3.'],['Відео','«Переміщення фігур» та «Обертання та масштаб». Кожен ролик триває 4 с і має версії MP4 та WebM.'],['Графіка','Два зображення-постери показують початкові кадри роликів.'],['Меню','Дві форми з підписами label, списками select і кнопками запуску.']],[105,WIDTH-105])
paragraph('Звуки синтезовано, а відео створено програмно з геометричних фігур. Це власні локальні навчальні матеріали. Відеоролики демонструють рух та перетворення фігур і мають лише відеодоріжку. Файли та генератор scripts/build_media.py входять до репозиторію.')
h('Використані теги й атрибути')
grid([['Засіб','Призначення'],['audio, video','Стандартні браузерні програвачі.'],['source, src, type','Шлях до файлу та його MIME-тип. Для відео доступні два формати.'],['form, label, select, option, button','Меню вибору медіазаписів і запуск дії.'],['figure, figcaption','Групування програвача та підпис вибраного запису.'],['controls, preload, poster','Панель керування, завантаження метаданих, обкладинка відео.']],[160,WIDTH-160])
h('Файли та зміни')
paragraph('Додано media.html, assets/js/media.js, assets/css/media.css та assets/media/. На всіх 11 сторінках є пункт «Медіабібліотека». Пояснення містяться у report/Захист.md і Зміни_порівняно_з_лаб8.md. Результати браузерних перевірок записано в report/check-results.json.')
page()
h('Аудіобібліотека та меню форми')
image_fit('audio-library.png',340)
source('''<form id="audio-menu">
  <label for="audio-select">Аудіозапис</label>
  <select id="audio-select">
    <option value="0">Сигнал готовності</option>
    <option value="1">Послідовність частот</option>
  </select>
  <button type="submit">Відтворити аудіо</button>
</form>
<audio id="audio-player" controls preload="metadata">
  <source src="assets/media/ready.mp3" type="audio/mpeg">
</audio>''')
paragraph('Подія change оновлює адресу source, підпис і посилання для завантаження. Метод load перечитує нове джерело. Кнопка запускає play. Помилки відтворення обробляються з повідомленням у статусі. Панель controls дозволяє керувати відтворенням безпосередньо у програвачі.')
page()
h('Відеобібліотека')
image_fit('video-library.png',410)
source('''<video controls playsinline preload="metadata"
       width="720" height="480"
       poster="assets/media/movement-poster.png">
  <source src="assets/media/movement.mp4" type="video/mp4">
  <source src="assets/media/movement.webm" type="video/webm">
</video>''')
paragraph('Браузер обирає підтримуване джерело. MP4 закодовано H.264, WebM - VP9. Постер показує кадр до початку відтворення. Після вибору іншого ролика обидва source і poster оновлюються. Запуск одного програвача ставить інший на паузу. «Зупинити все» викликає pause і повертає currentTime до нуля.')
page()
h('Тестові приклади')
grid([['Перевірка','Результат'],['Обидва MP3','Тривалість 1.59 і 3.18 с. Відтворення починається після натискання.'],['Обидва MP4','Тривалість кожного 4 с. Відео завантажується та відтворюється.'],['WebM','Альтернативний формат успішно декодується, тривалість 4 с.'],['Перемикання списків','Джерела, постер, підпис і посилання завантаження відповідають вибору.'],['Спільне керування','Після запуску одного програвача інший призупинено.'],['Зупинити все','Обидва програвачі на паузі, час дорівнює нулю.'],['JavaScript вимкнено','Стандартні controls доступні для початкових файлів, меню-сценарії вимкнені.'],['Мобільний вигляд','На ширині 390 px програвачі й форми вміщуються в сторінку.'],['Навігація',f'{results["htmlPages"]} сторінок і {results["localLinks"]} локальних посилань перевірено. Помилок виконання у Chrome немає.']],[150,WIDTH-150])
h('Що показати під час захисту')
paragraph('Відкрити media.html через пункт «Медіабібліотека». Вибрати й відтворити кожен звуковий приклад. Перемкнути обидва відео, показати зміну постера й підпису. Запустити відео під час аудіо, щоб продемонструвати автоматичну паузу. Натиснути «Зупинити все». У коді показати audio, video, source та форму зі select.')
story.append(KeepTogether([p('Висновки',heading),p('Створено бібліотеку локальних аудіо- та відеоресурсів ByteMarket. Використано обов’язкові теги audio, video, source і меню на основі форм. Реалізовано перемикання записів, підписів та постерів, взаємну паузу і спільну зупинку. Перевірено відтворення всіх записів та мобільний вигляд. Порівняно з №8 додано медіаресурси й керування програвачами.'),p('Репозиторій',heading),p('<link href="https://github.com/MaksHinchak/html-lab-09-variant-5" color="#174a7e">https://github.com/MaksHinchak/html-lab-09-variant-5</link>')]))

def decorate(c,doc):
 c.setFont('ArialUA',9); c.setFillColor(colors.HexColor('#587083'))
 c.drawRightString(538.9134,34,str(doc.page))
 if doc.page==1:
  c.setFillColor(colors.black);c.setFont('ArialUA',12)
  for y,line in [(688.89,'Чернівецький національний університет'),(669.89,'імені Юрія Федьковича'),(650.89,'Навчально-науковий інститут фізико-технічних'),(631.89,'та комп’ютерних наук')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',17)
  for y,line in [(495.89,'ЗВІТ'),(470.89,'про виконання лабораторної роботи №9'),(445.89,'з дисципліни «Веб-програмування»')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',12);c.drawCentredString(A4[0]/2,423.89,'Тема: Бібліотека аудіо- та відеоресурсів')
  author_lines=[(303.39,'Виконав: студент групи 241-А'),(284.39,'Гінчак Максим Богданович'),(265.39,'Перевірив:'),(246.39,'асистент Нестеренко Володимир Васильович')]
  for y,line in author_lines: c.drawRightString(538.9134,y,line)
  c.drawCentredString(A4[0]/2,48,'Чернівці · 2026')

SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=62.3622,rightMargin=50.3622,topMargin=56,bottomMargin=46,title='Лабораторна робота №9. Бібліотека аудіо- та відеоресурсів. Варіант 5',author='Гінчак Максим Богданович').build(story,onFirstPage=decorate,onLaterPages=decorate)
r=PdfReader(OUT)
assert len(r.pages)==5,len(r.pages)
assert 'Висновки' in r.pages[-1].extract_text()
assert 'Репозиторій' in r.pages[-1].extract_text()
assert all('Висновки' not in p.extract_text() and 'Репозиторій' not in p.extract_text() for p in r.pages[:-1])
for index,page_obj in enumerate(r.pages):
 assert len(page_obj.extract_text())>50
 assert abs(float(page_obj.mediabox.width)-A4[0])<1
links=[a.get_object().get('/A',{}).get('/URI') for pg in r.pages for a in pg.get('/Annots',[])]
assert 'https://github.com/MaksHinchak/html-lab-09-variant-5' in links
copy2(OUT,DESKTOP)
assert OUT.read_bytes()==DESKTOP.read_bytes()
print(f'Created {len(r.pages)}-page A4 report:',DESKTOP)
