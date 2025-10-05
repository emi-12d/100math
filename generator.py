from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random

def generate_pdf(operator='+', digits=3):
    """
    指定された四則演算と桁数で100ます計算PDFを生成する関数

    Args:
        operator (str): 演算子 ('+', '-', '*', '/')
        digits (int): 問題の数字の桁数 (例: 1, 2, 3)
    """
    # --- 基本設定 ---
    settings = {
        '+': {'title': 'たしざん', 'symbol': '＋'},
        '-': {'title': 'ひきざん', 'symbol': '－'},
        '*': {'title': 'かけざん', 'symbol': '×'},
        '/': {'title': 'わりざん', 'symbol': '÷'}
    }
    if operator not in settings:
        print(f"エラー: 対応していない演算子です -> '{operator}'")
        return
    if not isinstance(digits, int) or digits < 1:
        print(f"エラー: 桁数は1以上の整数で指定してください -> '{digits}'")
        return

    setting = settings[operator]
    filename = f"hyakumasu_{setting['title']}_{digits}keta.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # --- フォント設定 ---
    try:
        pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))
        font_name = 'IPAexGothic'
    except Exception as e:
        print("警告: フォントファイル 'ipaexg.ttf' が見つかりません。")
        font_name = "Helvetica"

    # --- 桁数に応じたレイアウト調整 ---
    if digits <= 2:
        grid_size = 45
        font_size = 16
    elif digits == 3:
        grid_size = 55
        font_size = 14
    else: # 4桁以上
        grid_size = 70
        font_size = 12
        
    c.setFont(font_name, font_size)

    # --- ページタイトル ---
    title_font_size = 18
    c.setFont(font_name, title_font_size)
    c.drawCentredString(width / 2, height - 60, f"{setting['title']} 100ますけいさん ({digits}桁)")
    c.setFont(font_name, font_size) # フォントサイズを元に戻す

    # --- 問題の数字を生成 ---
    min_val = 1 if digits == 1 else 10**(digits - 1)
    max_val = (10**digits) - 1

    top_numbers = []
    left_numbers = []

    if operator in ['+', '*']:
        top_numbers = [random.randint(min_val, max_val) for _ in range(10)]
        left_numbers = [random.randint(min_val, max_val) for _ in range(10)]
    
    elif operator == '-':
        # 引き算: 答えが負にならないように調整
        top_numbers = [random.randint(min_val, max_val) for _ in range(10)]
        left_numbers = [num + random.randint(min_val, max_val) for num in top_numbers]
        random.shuffle(left_numbers)

    elif operator == '/':
        # 割り算: 答えが必ず整数になるように調整
        # 割る数を指定された桁数で、答えを1桁で生成
        top_numbers = [random.randint(min_val, max_val) for _ in range(10)]
        answers = [random.randint(1, 9) for _ in range(10)]
        left_numbers = [t * a for t, a in zip(top_numbers, answers)]
        random.shuffle(left_numbers)

    # --- マス目と数字の描画 ---
    margin_x = (width - grid_size * 11) / 2
    start_x = margin_x
    start_y = height - 120

    for i in range(11):
        for j in range(11):
            x = start_x + j * grid_size
            y = start_y - i * grid_size
            
            # 中央揃えで文字を描画するための中心座標
            center_x = x + grid_size / 2
            center_y = y + grid_size / 2 - (font_size / 3)

            # 枠線
            c.grid([x, x + grid_size], [y, y + grid_size])

            # 数字や記号
            if i == 0 and j == 0:
                c.drawCentredString(center_x, center_y, setting['symbol'])
            elif i == 0 and j > 0:
                c.drawCentredString(center_x, center_y, str(top_numbers[j-1]))
            elif i > 0 and j == 0:
                c.drawCentredString(center_x, center_y, str(left_numbers[i-1]))

    c.save()
    print(f"'{filename}' を作成しました。")


# --- 関数を実行 ---
if __name__ == '__main__':
    # 1桁の足し算
    generate_pdf(operator='+', digits=1)
    
    # 2桁の引き算
    generate_pdf(operator='-', digits=2)
    
    # 2桁の掛け算
    generate_pdf(operator='*', digits=2)
    
    # 割る数が2桁の割り算
    generate_pdf(operator='/', digits=3)