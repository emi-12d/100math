import argparse
import generator

parser = argparse.ArgumentParser(description='100マス計算')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('arg1', help='演算子の指定')    # 必須の引数を追加
parser.add_argument('arg2', help='桁数')

args = parser.parse_args() 
print(args.arg1)
print(args.arg2)
operator=args.arg1
digits=int(args.arg2)

generator.generate_pdf(operator, digits)

  

