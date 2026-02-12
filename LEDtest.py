import machine

# ピン設定（Dピンあり、16行スキャン版）
r1 = machine.Pin(1, machine.Pin.OUT); g1 = machine.Pin(0, machine.Pin.OUT); b1 = machine.Pin(2, machine.Pin.OUT)
r2 = machine.Pin(4, machine.Pin.OUT); g2 = machine.Pin(3, machine.Pin.OUT); b2 = machine.Pin(5, machine.Pin.OUT)
a = machine.Pin(6, machine.Pin.OUT); b = machine.Pin(7, machine.Pin.OUT)
c = machine.Pin(8, machine.Pin.OUT); d = machine.Pin(9, machine.Pin.OUT)
clk = machine.Pin(10, machine.Pin.OUT); lat = machine.Pin(11, machine.Pin.OUT); oe = machine.Pin(12, machine.Pin.OUT)

def set_all_color(R, G, B):
    print(f"点灯中... (R:{R} G:{G} B:{B})")
    try:
        while True:
            for row in range(16): # 16行スキャン
                oe.value(1) # 消灯
                
                # 行選択（0-15）
                a.value(row & 0x01)
                b.value((row >> 1) & 0x01)
                c.value((row >> 2) & 0x01)
                d.value((row >> 3) & 0x01)
                
                # 32列分データを送る
                for _ in range(32):
                    r1.value(R); g1.value(G); b1.value(B)
                    r2.value(R); g2.value(G); b2.value(B)
                    clk.value(1)
                    clk.value(0)
                
                lat.value(1)
                lat.value(0)
                oe.value(0) # 点灯
    except KeyboardInterrupt:
        oe.value(1)
        print("停止しました")

# 好きな色で呼び出してみてください！
# 例：黄色にしたい場合
set_all_color(1, 0, 0)