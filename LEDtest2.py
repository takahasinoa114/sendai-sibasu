import machine
import time

# ピン設定
r1 = machine.Pin(0, machine.Pin.OUT); g1 = machine.Pin(1, machine.Pin.OUT); b1 = machine.Pin(2, machine.Pin.OUT)
r2 = machine.Pin(3, machine.Pin.OUT); g2 = machine.Pin(4, machine.Pin.OUT); b2 = machine.Pin(5, machine.Pin.OUT)
a = machine.Pin(6, machine.Pin.OUT); b = machine.Pin(7, machine.Pin.OUT)
c = machine.Pin(8, machine.Pin.OUT); d = machine.Pin(9, machine.Pin.OUT)
clk = machine.Pin(10, machine.Pin.OUT); lat = machine.Pin(11, machine.Pin.OUT); oe = machine.Pin(12, machine.Pin.OUT)

# 全消灯
oe.value(1)

def test_dot():
    # 0行目を選択
    a.value(0); b.value(0); c.value(0); d.value(0)
    
    # 1ドット目だけ「赤」を送る
    # 1回だけCLKを叩く
    r1.value(1); g1.value(0); b1.value(0) # ここで赤(R1)だけを1にする
    clk.value(1); clk.value(0)
    
    # 残りの31ドットは全部オフにする
    r1.value(0); g1.value(0); b1.value(0)
    for _ in range(31):
        clk.value(1); clk.value(0)
        
    lat.value(1); lat.value(0)
    oe.value(0) # 点灯
    print("左上の1ドットだけ赤く光っていますか？")

test_dot()