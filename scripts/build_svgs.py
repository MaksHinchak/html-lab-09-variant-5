from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / 'assets/svg'


def chart(animated=False):
    prefix = 'animated' if animated else 'static'
    title = 'Анімований малюнок варіанта 5' if animated else 'Статичний малюнок варіанта 5'
    defs = f'''  <defs>
    <symbol id="{prefix}-box" viewBox="0 0 1 1" preserveAspectRatio="none">
      <rect width="1" height="1" />
    </symbol>
    <marker id="{prefix}-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0 0 L6 3 L0 6 Z" fill="black" />
    </marker>
  </defs>'''
    def box(name, x, y, width=1):
        return f'<use id="{prefix}-{name}" data-figure="{name}" href="#{prefix}-box" x="{x}" y="{y}" width="{width}" height="1" />'
    if not animated:
        figures = [
            f'<circle id="{prefix}-left-circle" data-figure="left-circle" cx="-2" cy="1" r="1" />',
            f'<circle id="{prefix}-right-circle" data-figure="right-circle" cx="1" cy="1" r="1" />',
            box('left-bar', -3, -1, 2), box('top-box', 2, 1), box('step-box', 3, 0),
            box('bottom-left-box', 0, -2), box('bottom-bar', 1, -3, 2), box('bottom-right-box', 4, -2),
            f'<polygon id="{prefix}-diamond" data-figure="diamond" points="2,-1 3,0 4,-1 3,-2" />'
        ]
    else:
        figures = [
            '''<circle id="animated-left-circle" data-figure="left-circle" cx="-2" cy="1" r="1">
      <animate attributeName="fill" values="#0000ff;#ff6b35;#0000ff" dur="4s" repeatCount="indefinite" />
    </circle>''',
            '''<g transform="translate(1 1)">
      <g id="animated-scale">
        <animateTransform attributeName="transform" type="scale" values="1;0.72;1" dur="5s" repeatCount="indefinite" />
        <circle id="animated-right-circle" data-figure="right-circle" r="1" />
      </g>
    </g>''',
            box('left-bar', -3, -1, 2),
            '<g id="animated-translate">\n      <animateTransform attributeName="transform" type="translate" values="0 0;0 0.5;0 0" dur="5s" repeatCount="indefinite" />\n      '+box('top-box', 2, 1)+'\n    </g>',
            box('step-box', 3, 0), box('bottom-left-box', 0, -2), box('bottom-bar', 1, -3, 2),
            '<g transform="translate(4.5 -1.5)">\n      <g id="animated-skew">\n        <animateTransform attributeName="transform" type="skewX" values="0;25;-25;0" dur="7s" repeatCount="indefinite" />\n        '+box('bottom-right-box', -.5, -.5)+'\n      </g>\n    </g>',
            '''<g transform="translate(3 -1)">
      <g id="animated-rotate">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite" />
        <polygon id="animated-diamond" data-figure="diamond" points="-1,0 0,1 1,0 0,-1" />
      </g>
    </g>'''
        ]
    axes = [f'  <g id="{prefix}-axes" style="fill: none;" stroke="black" stroke-width="2">',
            f'    <line x1="38" y1="245" x2="736" y2="245" marker-end="url(#{prefix}-arrow)" />',
            f'    <line x1="290" y1="493" x2="290" y2="35" marker-end="url(#{prefix}-arrow)" />']
    for x in [-3, -2, -1, 1, 2, 3, 4, 5]:
        px = 290 + x*72
        axes.append(f'    <line x1="{px}" y1="235" x2="{px}" y2="255" />')
    for y in [-3, -2, -1, 1, 2]:
        py = 245 - y*72
        axes.append(f'    <line x1="280" y1="{py}" x2="300" y2="{py}" />')
    axes.append('  </g>')
    labels = ['  <g style="fill: black;" font-family="Times New Roman, serif" font-size="23">',
              '    <text x="748" y="274">X</text>', '    <text x="310" y="45">Y</text>',
              '    <text x="278" y="274" text-anchor="end">0</text>']
    for x in [-3, -1, 1, 2, 3, 4, 5]:
        labels.append(f'    <text x="{290+x*72}" y="274" text-anchor="middle">{x}</text>')
    for y in [-3, -2, -1, 1, 2]:
        labels.append(f'    <text x="277" y="{253-y*72}" text-anchor="end">{y}</text>')
    labels.append('  </g>')
    return f'''<svg id="{prefix}-drawing" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 540" width="100%" height="100%" role="img" aria-labelledby="{prefix}-title {prefix}-desc">
  <title id="{prefix}-title">{title}</title>
  <desc id="{prefix}-desc">Два кола, шість прямокутників і ромб синього кольору на осях X та Y. Центри кіл: (-2, 1) і (1, 1), радіус 1. Вершини ромба: (2, -1), (3, 0), (4, -1), (3, -2).</desc>
{defs}
  <g id="{prefix}-shapes" transform="translate(290 245) scale(72 -72)" style="fill: #0000ff;" stroke="black" stroke-width="0.025">
    '''+'\n    '.join(figures)+'\n  </g>\n'+'\n'.join(axes+labels)+'\n</svg>'


def curved_text():
    return '''<svg id="curved-text-drawing" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 280" width="100%" height="100%" role="img" aria-labelledby="curve-title curve-desc">
  <title id="curve-title">Текст уздовж кривої Безьє</title>
  <desc id="curve-desc">Напис SVG, ByteMarket, варіант 5 розташований уздовж вигнутої лінії над трьома векторними мікросхемами.</desc>
  <defs>
    <path id="headline-curve" d="M80 205 C180 25 600 25 700 205" />
    <symbol id="chip-symbol" viewBox="0 0 80 80">
      <rect x="18" y="18" width="44" height="44" rx="6" fill="#174a7e" />
      <rect x="30" y="30" width="20" height="20" rx="3" fill="#67d6c0" />
      <g stroke="#174a7e" stroke-width="4">
        <line x1="5" y1="30" x2="18" y2="30" /><line x1="5" y1="50" x2="18" y2="50" />
        <line x1="62" y1="30" x2="75" y2="30" /><line x1="62" y1="50" x2="75" y2="50" />
      </g>
    </symbol>
  </defs>
  <ellipse cx="390" cy="185" rx="220" ry="72" fill="#eef7fa" />
  <use href="#headline-curve" style="fill: none;" stroke="#90afc1" stroke-width="2" stroke-dasharray="6 6" />
  <text fill="#0c3158" font-family="Georgia, serif" font-size="28" letter-spacing="1">
    <!-- SVG 2: href and startOffset are standard textPath attributes. -->
    <!--suppress HtmlUnknownAttribute,HtmlDeprecatedAttribute -->
    <textPath href="#headline-curve" startOffset="50%" style="text-anchor: middle;">SVG · ByteMarket · Варіант 5</textPath>
  </text>
  <polyline points="270,190 390,225 510,190" fill="none" stroke="#157983" stroke-width="3" />
  <use href="#chip-symbol" x="230" y="145" width="80" height="80" />
  <use href="#chip-symbol" x="350" y="145" width="80" height="80" />
  <use href="#chip-symbol" x="470" y="145" width="80" height="80" />
</svg>'''


if __name__ == '__main__':
    svgs = {'variant5-static.svg': chart(), 'variant5-animated.svg': chart(True), 'curved-text.svg': curved_text()}
    for name, content in svgs.items():
        (SVG_DIR/name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+content+'\n')
    template = (ROOT/'scripts/svg-page.template.html').read_text()
    for marker, filename in [('STATIC', 'variant5-static.svg'), ('ANIMATED', 'variant5-animated.svg'), ('CURVE', 'curved-text.svg')]:
        template = template.replace('{{'+marker+'}}', svgs[filename])
    assert '{{' not in template
    (ROOT/'svg.html').write_text(template)
    print('Created 3 SVG files and svg.html')
