from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
import os

def generate_asymmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator='+', left_digits=1, top_digits=1):
    """
    指定された四則演算と桁数で、桁数の違う数字の演算ができる100ます計算PDFを生成する
    left_digits: 左側の数字の桁数
    top_digits: 上側の数字の桁数
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
    if not (isinstance(left_digits, int) and left_digits >= 1 and isinstance(top_digits, int) and top_digits >= 1):
        print(f"エラー: 桁数は1以上の整数で指定してください -> 左:{left_digits}, 上:{top_digits}")
        return

    setting = settings[operator]
    
    # --- ファイル名設定 ---
    base_filename = f"hyakumasu_{setting['title']}_{left_digits}x{top_digits}keta"
    problem_filename = f"{base_filename}.pdf"
    answer_filename = f"{base_filename}_ans.pdf"

    # --- PDFとフォントの準備 ---
    c_problem = canvas.Canvas(problem_filename, pagesize=A4)
    c_answer = canvas.Canvas(answer_filename, pagesize=A4)
    width, height = A4

    try:
        font_path = os.path.join('ipaexg00102', 'ipaexg.ttf')
        pdfmetrics.registerFont(TTFont('IPAexGothic', font_path))
        font_name = 'IPAexGothic'
    except Exception:
        print(f"警告: フォントファイル '{font_path}' が見つかりません。")
        font_name = "Helvetica"

    # --- 桁数に応じたレイアウト調整 (大きい方の桁数に合わせる) ---
    max_digits = max(left_digits, top_digits)
    if max_digits <= 1:
        grid_size = 40
        font_size = 16
    elif max_digits == 2:
        grid_size = 48
        font_size = 14
    else: # 3桁以上
        grid_size = 52
        font_size = 12
    
    # --- 問題の数字を生成 ---
    def get_numbers(digits):
        min_val = 1 if digits == 1 else 10**(digits - 1)
        max_val = (10**digits) - 1
        population = range(min_val, max_val + 1)
        # NOTE: 1桁の場合, 2桁以上の時は重複を無しにしないといけない
        if digits != 1:
            return random.sample(population, 10)
        else:
            # NOTE: 0~9の数字を重複なしで並べ替える
            return random.sample([i for i in range(10)],10)

    left_numbers = get_numbers(left_digits)
    print("left_digits",left_numbers)
    top_numbers = get_numbers(top_digits)
    print("top_digits",top_numbers)

    # --- 全ての解答を先に計算 ---
    answers = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            l_num, t_num = left_numbers[i], top_numbers[j]
            if operator == '+': answers[i][j] = l_num + t_num
            elif operator == '-': answers[i][j] = l_num - t_num
            elif operator == '*': answers[i][j] = l_num * t_num
            elif operator == '/': answers[i][j] = l_num / t_num if t_num != 0 else " - "

    # --- 描画処理 ---
    title_str = f"{setting['title']} 100ますけいさん ({left_digits}桁 × {top_digits}桁)"
    canvases = [
        {'c': c_problem, 'title': title_str, 'include_answers': False},
        {'c': c_answer,  'title': f"{title_str} - 解答", 'include_answers': True}
    ]

    for canvas_info in canvases:
        c = canvas_info['c']
        c.setFont(font_name, font_size)
        c.setFont(font_name, 18)
        c.drawCentredString(width / 2, height - 60, canvas_info['title'])
        c.setFont(font_name, font_size)

        margin_x = (width - grid_size * 11) / 2
        start_x, start_y = margin_x, height - 120

        for i in range(11):
            for j in range(11):
                x, y = start_x + j * grid_size, start_y - i * grid_size
                center_x, center_y = x + grid_size / 2, y + grid_size / 2 - (font_size / 3)
                c.grid([x, x + grid_size], [y, y + grid_size])

                if i == 0 and j == 0:
                    c.drawCentredString(center_x, center_y, setting['symbol'])
                elif i == 0 and j > 0:
                    c.drawCentredString(center_x, center_y, str(top_numbers[j-1]))
                elif i > 0 and j == 0:
                    c.drawCentredString(center_x, center_y, str(left_numbers[i-1]))
                elif i > 0 and j > 0 and canvas_info['include_answers']:
                    ans = answers[i-1][j-1]
                    ans_str = str(ans)
                    if isinstance(ans, float) and not ans.is_integer():
                        ans_str = f"{ans:.2f}".rstrip('0').rstrip('.')
                    elif not isinstance(ans, str):
                        ans_str = str(int(ans))
                    
                    ans_font_size = font_size
                    if len(ans_str) > 5: ans_font_size -= 4
                    elif len(ans_str) > 3: ans_font_size -= 2
                    
                    c.setFont(font_name, ans_font_size)
                    c.drawCentredString(center_x, center_y, ans_str)
                    c.setFont(font_name, font_size)
        c.save()

    print(f"'{problem_filename}' と '{answer_filename}' を作成しました。")

def generate_symmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator='+', digits=1):
    """
    指定された四則演算と桁数で、桁数が同じ問題の100ます計算PDFを生成する関数
    （内部的に非対称関数を呼び出します）
    """
    generate_asymmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator, left_digits=digits, top_digits=digits)


# --- 実行例 ---
if __name__ == '__main__':
    # 【非対称】左2桁、上1桁の足し算
    generate_asymmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator='+', left_digits=2, top_digits=1)

    # 【非対称】左3桁、上2桁の引き算
    generate_asymmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator='-', left_digits=3, top_digits=2)
    
    # 【対称】2桁の掛け算 (対称関数を呼び出し)
    generate_symmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator='*', digits=2)

