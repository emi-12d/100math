from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
import math

def generate_pdf(operator='+', digits=1):
    """
    指定された四則演算と桁数で、問題と解答の100ます計算PDFを2種類生成する関数

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
    
    # --- ファイル名設定 ---
    base_filename = f"hyakumasu_{setting['title']}_{digits}keta"
    problem_filename = f"{base_filename}.pdf"
    answer_filename = f"{base_filename}_ans.pdf"

    # --- PDFとフォントの準備 ---
    c_problem = canvas.Canvas(problem_filename, pagesize=A4)
    c_answer = canvas.Canvas(answer_filename, pagesize=A4)
    width, height = A4

    try:
        pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))
        font_name = 'IPAexGothic'
    except Exception as e:
        print("警告: フォントファイル 'ipaexg.ttf' が見つかりません。")
        font_name = "Helvetica"

    # --- 桁数に応じたレイアウト調整 (A4幅に収まるように修正済み) ---
    if digits <= 1:
        grid_size = 40
        font_size = 16
    elif digits == 2:
        grid_size = 48
        font_size = 14
    else: # 3桁以上
        grid_size = 52
        font_size = 12
    
    # --- 問題の数字を生成 ---
    min_val = 1 if digits == 1 else 10**(digits - 1)
    max_val = (10**digits) - 1

    top_numbers = [random.randint(min_val, max_val) for _ in range(10)]
    left_numbers = []

    if operator in ['+', '*']:
        left_numbers = [random.randint(min_val, max_val) for _ in range(10)]
    elif operator == '-':
        left_numbers = [num + random.randint(min_val, max_val) for num in top_numbers]
        random.shuffle(left_numbers)
    elif operator == '/':
        # 注: このわり算のロジックでは、答えが整数にならない組み合わせが生成されることがあります。
        # 解答PDFでは、小数点第2位までの近似値が記載されます。
        answers_for_gen = [random.randint(1, 9) for _ in range(10)]
        left_numbers = [t * a for t, a in zip(top_numbers, answers_for_gen)]
        random.shuffle(left_numbers)

    # --- 全ての解答を先に計算 ---
    answers = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            l_num = left_numbers[i]
            t_num = top_numbers[j]
            if operator == '+':
                answers[i][j] = l_num + t_num
            elif operator == '-':
                answers[i][j] = l_num - t_num
            elif operator == '*':
                answers[i][j] = l_num * t_num
            elif operator == '/':
                if t_num != 0:
                    answers[i][j] = l_num / t_num
                else:
                    answers[i][j] = " - " # ゼロ除算エラー防止

    # --- 描画処理を共通化 ---
    canvases = [
        {'c': c_problem, 'title': f"{setting['title']} 100ますけいさん ({digits}桁)", 'include_answers': False},
        {'c': c_answer,  'title': f"{setting['title']} 100ますけいさん ({digits}桁) - 解答", 'include_answers': True}
    ]

    for canvas_info in canvases:
        c = canvas_info['c']
        
        # フォントサイズ設定
        c.setFont(font_name, font_size)

        # ページタイトル
        title_font_size = 18
        c.setFont(font_name, title_font_size)
        c.drawCentredString(width / 2, height - 60, canvas_info['title'])
        c.setFont(font_name, font_size)

        # マス目と数字の描画
        margin_x = (width - grid_size * 11) / 2
        start_x = margin_x
        start_y = height - 120

        for i in range(11):
            for j in range(11):
                x = start_x + j * grid_size
                y = start_y - i * grid_size
                
                center_x = x + grid_size / 2
                center_y = y + grid_size / 2 - (font_size / 3)

                c.grid([x, x + grid_size], [y, y + grid_size])

                if i == 0 and j == 0:
                    c.drawCentredString(center_x, center_y, setting['symbol'])
                elif i == 0 and j > 0:
                    c.drawCentredString(center_x, center_y, str(top_numbers[j-1]))
                elif i > 0 and j == 0:
                    c.drawCentredString(center_x, center_y, str(left_numbers[i-1]))
                # 解答を描画する場合
                elif i > 0 and j > 0 and canvas_info['include_answers']:
                    ans = answers[i-1][j-1]
                    # 答えが小数の場合、フォーマットを調整
                    if isinstance(ans, float) and not ans.is_integer():
                         # 小数点以下が長くなりすぎないように丸める
                        ans_str = f"{ans:.2f}".rstrip('0').rstrip('.')
                    else:
                        ans_str = str(int(ans))
                    
                    # 答えの桁数に応じてフォントを少し小さくする
                    ans_font_size = font_size
                    if len(ans_str) > 5:
                        ans_font_size = font_size - 4
                    elif len(ans_str) > 3:
                        ans_font_size = font_size - 2
                    
                    c.setFont(font_name, ans_font_size)
                    c.drawCentredString(center_x, center_y, ans_str)
                    c.setFont(font_name, font_size) # フォントサイズを戻す

        c.save()

    print(f"'{problem_filename}' と '{answer_filename}' を作成しました。")


# --- 関数を実行 ---
if __name__ == '__main__':
    # 1桁の足し算
    generate_pdf(operator='+', digits=1)
    
    # 2桁の引き算
    generate_pdf(operator='-', digits=2)
    
    # 2桁の掛け算
    generate_pdf(operator='*', digits=2)
    
    # 割る数が2桁の割り算
    generate_pdf(operator='/', digits=2)
