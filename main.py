import argparse
import sys

import generator

# パーサを作る
parser = argparse.ArgumentParser(description="100マス計算")

# 必須の位置引数を2つ定義
# これらは指定しないと自動でエラーになる
parser.add_argument("operator", help="演算子 (+, -, *, /) を指定")
parser.add_argument("left_digits", type=int, help="左側の数字の桁数を指定")
parser.add_argument("top_digits", type=int, help="上側の数字の桁数を指定")

# 引数をパース
# ここで引数が足りなければ、argparseが自動でエラーを出して終了する
args = parser.parse_args()

operator = args.operator
left_digits = args.left_digits
top_digits = args.top_digits

# 念のため、演算子の種類をチェックする処理を追加
allowed_operators = ["+", "-", "*", "/"]
if operator not in allowed_operators:
    print(f"エラー: 演算子 '{operator}' は無効です。", file=sys.stderr)
    print(f"許可されている演算子: {', '.join(allowed_operators)}", file=sys.stderr)
    sys.exit(1)  # エラーで終了

# 桁数が5以上の場合にエラーを出す
if left_digits >= 5 or top_digits >= 5:
    print(
        'エラー: 4桁までの整数のみに対応しています。\ndigitには4以下の数値を入力してください。\nExample : `python main.py "+" 4`',
        file=sys.stderr,
    )
    sys.exit(1)  # エラーで終了

print(f"演算子: {operator}")
print(f"桁数: {left_digits, top_digits}")

generator.generate_asymmetric_number_of_characters_Hundred_Square_Calculations_pdf(operator, left_digits, top_digits)
