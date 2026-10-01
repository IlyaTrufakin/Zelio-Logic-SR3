import os
from PIL import Image, ImageDraw, ImageFont

def create_optimized_zelio_diagram():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zelio_fbd_optimized.png")
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 23)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
        font_reg = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_param = ImageFont.truetype("arialbd.ttf", 13)
        font_box = ImageFont.truetype("arialbd.ttf", 15)
        font_pin = ImageFont.truetype("arialbd.ttf", 12)
    except:
        font_title = font_bold = font_reg = font_small = font_param = font_box = font_pin = ImageFont.load_default()

    # 1. HEADER
    draw.rectangle([0, 0, W, 68], fill=(15, 65, 125))
    draw.text((30, 20), "Schneider Zelio Logic SR3 B262BD — ИДЕАЛЬНАЯ СХЕМА FBD (БЕЗ ЛОЖНЫХ СРАБАТЫВАНИЙ И ДЁРГАНИЙ)", fill=(255, 255, 255), font=font_title)

    # 2. CANVAS
    cx, cy, cw, ch = 30, 85, W - 60, H - 150
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255), outline=(180, 195, 210), width=2)

    # Rails
    in_rail_w = 90
    draw.rectangle([cx, cy, cx + in_rail_w, cy + ch], fill=(245, 247, 250), outline=(210, 215, 222), width=1)
    out_rail_w = 90
    draw.rectangle([cx + cw - out_rail_w, cy, cx + cw, cy + ch], fill=(245, 247, 250), outline=(210, 215, 222), width=1)

    # Input drawer
    def draw_zelio_input(label, y_center, full_title, is_switch=False):
        iy = y_center - 24
        ix = cx + 12
        draw.rectangle([ix, iy, ix + 65, iy + 48], fill=(230, 235, 242), outline=(30, 41, 59), width=1)
        draw.text((ix + 4, iy + 14), label, fill=(15, 23, 42), font=font_bold)
        draw.rectangle([ix + 32, iy + 8, ix + 56, iy + 40], fill=(255, 255, 255), outline=(100, 116, 139))
        if not is_switch:
            draw.ellipse([ix + 37, iy + 14, ix + 51, iy + 34], fill=(250, 204, 21), outline=(202, 138, 4), width=2)
        else:
            draw.rectangle([ix + 38, iy + 12, ix + 50, iy + 26], fill=(124, 58, 237), outline=(91, 33, 182))

        tx = cx + in_rail_w
        ty = y_center
        draw.polygon([(tx - 6, ty - 6), (tx, ty), (tx - 6, ty + 6)], fill=(0, 0, 0))
        draw.text((ix, iy - 20), full_title, fill=(30, 50, 80), font=font_bold)
        return (tx, ty)

    # Output drawer
    def draw_zelio_output(label, y_center, full_title):
        iy = y_center - 24
        ix = cx + cw - out_rail_w + 12
        draw.rectangle([ix, iy, ix + 65, iy + 48], fill=(230, 235, 242), outline=(30, 41, 59), width=1)
        draw.text((ix + 35, iy + 14), label, fill=(15, 23, 42), font=font_bold)
        draw.rectangle([ix + 8, iy + 12, ix + 28, iy + 36], fill=(255, 255, 255), outline=(37, 99, 235), width=2)
        tx = cx + cw - out_rail_w
        ty = y_center
        draw.polygon([(tx + 6, ty - 6), (tx, ty), (tx + 6, ty + 6)], fill=(0, 0, 0))
        draw.text((tx - draw.textlength(full_title, font=font_small) - 12, ty - 18), full_title, fill=(71, 85, 105), font=font_small)
        return (tx, ty)

    # Place Inputs
    p_i1 = draw_zelio_input("I1", 170, "I1: Датчик давления (НО)")
    p_i2 = draw_zelio_input("I2", 340, "I2: Кнопка Сброса аварии (и пуска после аварии)")
    p_i3 = draw_zelio_input("I3", 640, "I3: Режим таймаута", is_switch=True)

    # Place Outputs
    p_q1 = draw_zelio_output("Q1", 200, "Q1: ТТР насоса (SSR 24VDC)")
    p_q2 = draw_zelio_output("Q2", 300, "Q2: Сигнальная лампа работы насоса")
    p_lcd = draw_zelio_output("LCD", 860, "B022: Подсветка дисплея при Аварии")

    # Gate drawer
    def draw_gate(x, y, g_type, b_id=""):
        gw, gh = 48, 52
        draw.rectangle([x, y, x + gw, y + gh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        if b_id:
            draw.text((x + 8, y - 18), b_id, fill=(0, 0, 0), font=font_bold)
        if g_type == "NOT":
            draw.polygon([(x + 10, y + 10), (x + 32, y + 26), (x + 10, y + 42)], fill=(220, 252, 231), outline=(22, 163, 74), width=1)
            draw.text((x + 15, y + 17), "1", fill=(22, 163, 74), font=font_bold)
            draw.ellipse([x + 33, y + 23, x + 39, y + 29], fill=(255, 255, 255), outline=(22, 163, 74), width=1)
            draw.text((x + 10, y + gh + 2), "NOT", fill=(0, 0, 0), font=font_small)
            draw.polygon([(x - 6, y + 26 - 4), (x, y + 26), (x - 6, y + 26 + 4)], fill=(0, 0, 0))
            draw.polygon([(x + gw, y + 26 - 4), (x + gw + 6, y + 26), (x + gw, y + 26 + 4)], fill=(0, 0, 0))
            return {"in": [(x, y + 26)], "out": (x + gw + 6, y + 26)}
        elif g_type == "AND":
            draw.text((x + 17, y + 12), "&", fill=(0, 80, 180), font=font_bold)
            draw.text((x + 10, y + gh + 2), "AND", fill=(0, 0, 0), font=font_small)
            in_pts = []
            for py in [y + 11, y + 21, y + 31, y + 41]:
                draw.polygon([(x - 6, py - 3), (x, py), (x - 6, py + 3)], fill=(0, 0, 0))
                in_pts.append((x, py))
            draw.polygon([(x + gw, y + 26 - 4), (x + gw + 6, y + 26), (x + gw, y + 26 + 4)], fill=(0, 0, 0))
            return {"in": in_pts, "out": (x + gw + 6, y + 26)}
        elif g_type == "OR":
            draw.text((x + 10, y + 12), "≥1", fill=(0, 80, 180), font=font_bold)
            draw.text((x + 13, y + gh + 2), "OR", fill=(0, 0, 0), font=font_small)
            draw.polygon([(x - 6, y + 16 - 4), (x, y + 16), (x - 6, y + 16 + 4)], fill=(0, 0, 0))
            draw.polygon([(x - 6, y + 36 - 4), (x, y + 36), (x - 6, y + 36 + 4)], fill=(0, 0, 0))
            draw.polygon([(x + gw, y + 26 - 4), (x + gw + 6, y + 26), (x + gw, y + 26 + 4)], fill=(0, 0, 0))
            return {"in": [(x, y + 16), (x, y + 36)], "out": (x + gw + 6, y + 26)}

    # Timer A-C
    def draw_timer_ac(x, y, b_id, ta_str, tb_str="", note=""):
        bw, bh = 94, 110
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=font_bold)
        draw.text((x + 12, y + 32), "TIMER A-C", fill=(0, 80, 180), font=font_small)
        draw.text((x + 10, y + 52), f"Ta={ta_str}", fill=(15, 23, 42), font=font_param)
        if tb_str:
            draw.text((x + 10, y + 72), f"Tb={tb_str}", fill=(15, 23, 42), font=font_param)
        if note:
            draw.text((x - 10, y + bh + 4), note, fill=(100, 116, 139), font=font_small)
        for gy in [y + 20, y + 42, y + 64, y + 86]:
            draw.polygon([(x + bw - 1, gy - 4), (x + bw + 6, gy), (x + bw - 1, gy + 4)], fill=(16, 185, 129))
        draw.text((x + 6, y + 12), "I1", fill=(30, 41, 59), font=font_pin)
        draw.text((x + bw - 22, y + 12), "O1", fill=(16, 185, 129), font=font_pin)
        draw.polygon([(x - 6, y + 20 - 5), (x, y + 20), (x - 6, y + 20 + 5)], fill=(0, 0, 0))
        draw.polygon([(x + bw + 6, y + 20 - 5), (x + bw + 12, y + 20), (x + bw + 6, y + 20 + 5)], fill=(0, 0, 0))
        return {"cmd": (x, y + 20), "out": (x + bw + 12, y + 20)}

    # Timer Li
    def draw_timer_li(x, y, b_id, t_str, note=""):
        bw, bh = 94, 95
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=font_bold)
        draw.text((x + 14, y + 30), "TIMER Li", fill=(0, 80, 180), font=font_small)
        draw.text((x + 12, y + 54), f"T = {t_str}", fill=(15, 23, 42), font=font_param)
        if note:
            draw.text((x - 10, y + bh + 4), note, fill=(100, 116, 139), font=font_small)
        for gy in [y + 20, y + 42, y + 64, y + 86]:
            draw.polygon([(x + bw - 1, gy - 4), (x + bw + 6, gy), (x + bw - 1, gy + 4)], fill=(16, 185, 129))
        draw.text((x + 6, y + 12), "I1", fill=(30, 41, 59), font=font_pin)
        draw.text((x + bw - 22, y + 12), "O1", fill=(16, 185, 129), font=font_pin)
        draw.polygon([(x - 6, y + 20 - 5), (x, y + 20), (x - 6, y + 20 + 5)], fill=(0, 0, 0))
        draw.polygon([(x + bw + 6, y + 20 - 5), (x + bw + 12, y + 20), (x + bw + 6, y + 20 + 5)], fill=(0, 0, 0))
        return {"cmd": (x, y + 20), "out": (x + bw + 12, y + 20)}

    # Preset Counter
    def draw_counter(x, y, b_id, preset_val, note=""):
        bw, bh = 94, 106
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=font_bold)
        draw.rectangle([x + 12, y + 14, x + 76, y + 36], fill=(240, 245, 250), outline=(100, 116, 139))
        draw.text((x + 16, y + 18), f"N={preset_val}", fill=(0, 80, 180), font=font_bold)
        draw.text((x + 10, y + 42), "PRESET CNT", fill=(0, 0, 0), font=font_small)
        draw.text((x + 10, y + 62), "I1 (Pulse)", fill=(71, 85, 105), font=font_small)
        draw.text((x + 10, y + 84), "I3 (Reset)", fill=(71, 85, 105), font=font_small)
        draw.text((x + bw - 22, y + 26), "O1", fill=(16, 185, 129), font=font_pin)
        draw.polygon([(x - 6, y + 68 - 4), (x, y + 68), (x - 6, y + 68 + 4)], fill=(0, 0, 0))
        draw.polygon([(x - 6, y + 90 - 4), (x, y + 90), (x - 6, y + 90 + 4)], fill=(0, 0, 0))
        draw.polygon([(x + bw, y + 46 - 4), (x + bw + 6, y + 46), (x + bw, y + 46 + 4)], fill=(0, 0, 0))
        if note:
            draw.text((x - 10, y + bh + 4), note, fill=(100, 116, 139), font=font_small)
        return {"pulse": (x, y + 68), "reset": (x, y + 90), "out": (x + bw + 6, y + 46)}

    # Bistable
    def draw_bistable(x, y, b_id, note=""):
        bw, bh = 84, 88
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=font_bold)
        draw.text((x + 10, y + 10), "SET", fill=(0, 80, 180), font=font_bold)
        draw.text((x + 52, y + 36), "Q", fill=(0, 80, 180), font=font_bold)
        draw.text((x + 10, y + 60), "RESET", fill=(0, 80, 180), font=font_bold)
        draw.polygon([(x - 6, y + 18 - 5), (x, y + 18), (x - 6, y + 18 + 5)], fill=(0, 0, 0))
        draw.polygon([(x - 6, y + 68 - 5), (x, y + 68), (x - 6, y + 68 + 5)], fill=(0, 0, 0))
        draw.polygon([(x + bw, y + 44 - 5), (x + bw + 6, y + 44), (x + bw, y + 44 + 5)], fill=(0, 0, 0))
        if note:
            draw.text((x - 10, y + bh + 4), note, fill=(100, 116, 139), font=font_small)
        return {"set": (x, y + 18), "reset": (x, y + 68), "q": (x + bw + 6, y + 44)}

    # Wire helper
    def draw_wire(pts, color=(0, 0, 0), width=2, dot_start=False, dot_end=False, label=""):
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(255, 255, 255), width=width+4)
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=width)
        if dot_start:
            x, y = pts[0]
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=color)
        if dot_end:
            x, y = pts[-1]
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=color)
        if label and len(pts) >= 2:
            tx = (pts[0][0] + pts[1][0]) // 2 - draw.textlength(label, font=font_small) // 2
            ty = pts[0][1] - 16
            draw.rounded_rectangle([tx - 4, ty - 2, tx + draw.textlength(label, font=font_small) + 4, ty + 16], radius=3, fill=(255, 255, 255), outline=color, width=1)
            draw.text((tx, ty), label, fill=color, font=font_small)

    # Signal Colors
    C_BLUE = (2, 132, 199)    # Pressure demand
    C_ORANGE = (217, 119, 6)  # I2 Push button / Reset
    C_GREEN = (22, 163, 74)   # Pump Running Q1 / Q2
    C_PURPLE = (124, 58, 237) # I3 Mode selector
    C_RED = (220, 38, 38)     # Alarm lockout
    C_CYAN = (8, 145, 178)    # Direct sensor feedback to timer reset

    # --- TOP ROW: PUMP CONTROL LOGIC (B005, B024, B010) ---
    b005 = draw_gate(270, 144, "NOT", b_id="B005")
    b024 = draw_timer_ac(440, 120, "B024", "3.0 s", "5.0 s", note="Гистерезис (Ta=3с, Tb=5с)")

    b010 = draw_gate(710, 200, "AND", b_id="B010")

    # Callout: Eliminated blocks (B007, B008, B011, B013)
    del_box_x, del_box_y = 860, 95
    draw.rounded_rectangle([del_box_x, del_box_y, del_box_x + 650, del_box_y + 95], radius=6, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((del_box_x + 15, del_box_y + 10), "УДАЛЕНЫ БЛОКИ B007, B008, B011 И B013!", fill=(185, 28, 28), font=font_box)
    draw.text((del_box_x + 15, del_box_y + 33), "1. Кнопка I2 подключается ТОЛЬКО на сброс триггера B012 RESET!", fill=(127, 29, 29), font=font_small)
    draw.text((del_box_x + 15, del_box_y + 51), "   Она больше НЕ дёргает насос, когда в системе уже есть 3 бара!", fill=(185, 28, 28), font=font_bold)
    draw.text((del_box_x + 15, del_box_y + 71), "2. Выход B024 O1 подключен НАПРЯМУЮ в B010 AND, а B010 AND — в Q1 и Q2!", fill=(22, 101, 52), font=font_bold)

    # Wiring Top Path:
    # 1. I1 -> B005 NOT
    draw_wire([p_i1, b005["in"][0]], color=C_BLUE, width=2)
    # 2. B005 NOT -> B024 Cmd
    b005_split_x = 350
    draw_wire([b005["out"], (b005_split_x, b005["out"][1]), b024["cmd"]], color=C_BLUE, width=2)
    # 3. B024 Out -> B010 AND (Top, pin 0)
    draw_wire([b024["out"], (650, b024["out"][1]), (650, b010["in"][0][1]), b010["in"][0]], color=C_BLUE, width=2)

    # 4. I2 -> goes ONLY down to B012 RESET!
    i2_split_x = 180
    draw_wire([p_i2, (i2_split_x, p_i2[1]), (i2_split_x, 960), (1130, 960), (1130, 694)], color=C_ORANGE, width=2, label="СБРОС АВАРИИ I2 (ТОЛЬКО НА B012 RESET)")

    # 5. B010 AND Out -> Q1, Q2, and Feedback loop down to Dry-Run protection
    q_out_x = 840
    draw_wire([b010["out"], (q_out_x, b010["out"][1])], color=C_GREEN, width=3)
    draw_wire([(q_out_x, b010["out"][1]), (q_out_x, p_q1[1]), p_q1], color=C_GREEN, width=3, dot_start=True)
    draw_wire([(q_out_x, b010["out"][1]), (q_out_x, p_q2[1]), p_q2], color=C_GREEN, width=3, dot_start=True)

    # Feedback Pump Running to bottom area (x = 330)
    fb_y = 440
    draw_wire([(q_out_x, b010["out"][1]), (q_out_x, fb_y)], color=C_GREEN, width=2, dot_start=True)
    draw_wire([(q_out_x, fb_y), (330, fb_y)], color=C_GREEN, width=2, label="НАСОС РАБОТАЕТ")

    # --- BOTTOM AREA: DRY-RUN PROTECTION & TIMEOUT SELECTION ---
    draw.rounded_rectangle([170, 480, 1570, 940], radius=8, fill=(250, 252, 255), outline=(180, 200, 225), width=1)
    draw.text((430, 492), "БЛОК ЗАЩИТЫ ОТ СУХОГО ХОДА И ПОРЫВА ТРУБЫ (ВЫБОР ТАЙМАУТА ПО I3)", fill=(30, 60, 120), font=font_bold)

    # Short branch (I3=0)
    b015 = draw_gate(250, 560, "NOT", b_id="B015")
    b016 = draw_gate(410, 560, "AND", b_id="B016")
    b018 = draw_timer_ac(550, 530, "B018", "240.0 s", note="Короткий таймаут (4 мин)")

    # Long branch (I3=1)
    b017 = draw_gate(410, 740, "AND", b_id="B017")
    b019 = draw_timer_li(550, 710, "B019", "60 s", note="Минутный генератор (60с)")
    b020 = draw_gate(710, 810, "NOT", b_id="B020")
    b021 = draw_counter(830, 710, "B021", "90", note="Счетчик полива (90 мин)")

    # OR Alarm
    b014 = draw_gate(1040, 640, "OR", b_id="B014")

    # Alarm Bistable B012
    b012 = draw_bistable(1180, 626, "B012", note="Триггер АВАРИИ")
    b009 = draw_gate(1420, 640, "NOT", b_id="B009")

    # Connect I2 end to B012 RESET
    draw_wire([(1130, 694), b012["reset"]], color=C_ORANGE, width=2)

    # --- WIRING BOTTOM PATH ---
    # I3 branch
    i3_split_x = 200
    draw_wire([p_i3, (i3_split_x, p_i3[1])], color=C_PURPLE, width=2)
    draw_wire([(i3_split_x, p_i3[1]), (i3_split_x, b015["in"][0][1]), b015["in"][0]], color=C_PURPLE, width=2, dot_start=True)
    draw_wire([(i3_split_x, p_i3[1]), (i3_split_x, b017["in"][1][1]), b017["in"][1]], color=C_PURPLE, width=2)

    # B015 NOT -> B016 AND (Input 0, top)
    draw_wire([b015["out"], b016["in"][0]], color=C_PURPLE, width=2)

    # Pump Running Feedback -> B016 AND (Input 1) & B017 AND (Input 0, top)
    draw_wire([(330, fb_y), (330, b016["in"][1][1]), b016["in"][1]], color=C_GREEN, width=2, dot_start=True)
    draw_wire([(330, fb_y), (330, b017["in"][0][1]), b017["in"][0]], color=C_GREEN, width=2)

    # CRITICAL FIX: Direct pressure feedback from B005 NOT -> B016 (Input 2) & B017 (Input 2)!
    p_sens_x = 370
    draw_wire([(b005_split_x, b005["out"][1]), (p_sens_x, b005["out"][1])], color=C_CYAN, width=2, dot_start=True)
    draw_wire([(p_sens_x, b005["out"][1]), (p_sens_x, 500)], color=C_CYAN, width=2)
    draw_wire([(p_sens_x, 500), (p_sens_x, b016["in"][2][1]), b016["in"][2]], color=C_CYAN, width=2, dot_start=True)
    draw_wire([(p_sens_x, 500), (p_sens_x, b017["in"][2][1]), b017["in"][2]], color=C_CYAN, width=2)
    draw.rounded_rectangle([200, 448, 360, 468], radius=3, fill=(255, 255, 255), outline=C_CYAN, width=1)
    draw.text((206, 451), "СБРОС АВАРИИ ПРИ I1=1", fill=C_CYAN, font=font_small)

    # B016 AND Out -> B018 Cmd
    draw_wire([b016["out"], b018["cmd"]], color=C_PURPLE, width=2)

    # B017 AND Out -> B019 Cmd & B020 NOT (Reset counter)
    draw_wire([b017["out"], b019["cmd"]], color=C_PURPLE, width=2)
    draw_wire([b017["out"], (480, b017["out"][1]), (480, 836), b020["in"][0]], color=C_PURPLE, width=2, dot_start=True)
    draw_wire([b020["out"], (790, b020["out"][1]), (790, b021["reset"][1]), b021["reset"]], color=C_PURPLE, width=2)

    # B019 Out -> B021 Pulse
    draw_wire([b019["out"], (780, b019["out"][1]), (780, b021["pulse"][1]), b021["pulse"]], color=C_PURPLE, width=2)

    # B018 Out -> B014 OR (Top)
    draw_wire([b018["out"], (960, b018["out"][1]), (960, b014["in"][0][1]), b014["in"][0]], color=C_RED, width=2)
    # B021 Out -> B014 OR (Bottom)
    draw_wire([b021["out"], (960, b021["out"][1]), (960, b014["in"][1][1]), b014["in"][1]], color=C_RED, width=2)

    # B014 OR Out -> B012 SET (Top pin)
    draw_wire([b014["out"], (1120, b014["out"][1]), (1120, b012["set"][1]), b012["set"]], color=C_RED, width=2)

    # B012 Q Output (ALARM)
    alm_x = 1320
    draw_wire([b012["q"], (alm_x, b012["q"][1])], color=C_RED, width=3, label="АВАРИЯ")
    # -> B022 LCD Backlight
    draw_wire([(alm_x, b012["q"][1]), (alm_x, p_lcd[1]), p_lcd], color=C_RED, width=3, dot_start=True)
    # -> B009 NOT
    draw_wire([(alm_x, b012["q"][1]), (alm_x, b009["in"][0][1]), b009["in"][0]], color=C_RED, width=3)

    # B009 NOT Out (НЕТ АВАРИИ = 1) -> up to B010 AND (Bottom, pin 3)
    draw_wire([b009["out"], (1500, b009["out"][1]), (1500, 360)], color=C_RED, width=2)
    draw_wire([(1500, 360), (670, 360)], color=C_RED, width=2, label="Разрешение работы (Аварии НЕТ)")
    draw_wire([(670, 360), (670, b010["in"][3][1]), b010["in"][3]], color=C_RED, width=2)

    # --- TIMING EXPLANATION BOX (TOP RIGHT) ---
    t_box_x, t_box_y = 960, 205
    draw.rounded_rectangle([t_box_x, t_box_y, t_box_x + 600, t_box_y + 225], radius=6, fill=(240, 249, 255), outline=(56, 189, 248), width=2)
    draw.text((t_box_x + 15, t_box_y + 12), "КАК РАБОТАЕТ КНОПКА I2 И ЗАЩИТА ОТ ЛОЖНОЙ АВАРИИ:", fill=(3, 105, 161), font=font_box)
    draw.text((t_box_x + 15, t_box_y + 40), "• Кнопка I2 теперь подключена ТОЛЬКО на B012 RESET (Сброс аварии).", fill=(15, 23, 42), font=font_small)
    draw.text((t_box_x + 15, t_box_y + 58), "  Если в баке уже есть 3 бара — нажатие I2 насос НЕ ДЁРГАЕТ вообще!", fill=(22, 101, 52), font=font_bold)
    draw.text((t_box_x + 15, t_box_y + 82), "• А если была АВАРИЯ (давление 0) — нажатие I2 сбрасывает B012,", fill=(15, 23, 42), font=font_small)
    draw.text((t_box_x + 15, t_box_y + 102), "  и насос ТУТ ЖЕ автоматически начинает качать, пока не наберёт 3 бара!", fill=(3, 105, 161), font=font_bold)
    draw.text((t_box_x + 15, t_box_y + 126), "• Прямой провод с B005 NOT на 3-й вход B016/B017 гарантирует:", fill=(15, 23, 42), font=font_small)
    draw.text((t_box_x + 15, t_box_y + 146), "  в момент набора давления (I1=1) таймер аварии B018 обнуляется в 0,", fill=(22, 101, 52), font=font_bold)
    draw.text((t_box_x + 15, t_box_y + 168), "  а насос спокойно докачивает 5 секунд Tb в бак без риска ложной аварии!", fill=(71, 85, 105), font=font_small)
    draw.text((t_box_x + 15, t_box_y + 190), "• Полная защита от сухого хода: при I1=0 таймер надежно отключит насос за 4 мин.", fill=(185, 28, 28), font=font_bold)

    # --- COLOR LEGEND ---
    leg_x, leg_y = 50, H - 55
    draw.rectangle([leg_x, leg_y, W - 100, leg_y + 40], fill=(255, 255, 255), outline=(203, 213, 225))
    items = [
        (C_BLUE, "Цепь требования воды (I1, B005, B024)"),
        (C_GREEN, "Цепь включения насоса (B010, Q1, Q2)"),
        (C_CYAN, "Мгновенный сброс таймера аварии при I1=1"),
        (C_ORANGE, "Кнопка I2 (Сброс аварии B012 RESET)"),
        (C_RED, "Цепь аварии (B012, B009, LCD)")
    ]
    lx = leg_x + 15
    for col, txt in items:
        draw.rectangle([lx, leg_y + 12, lx + 18, leg_y + 26], fill=col)
        draw.text((lx + 24, leg_y + 11), txt, fill=(15, 23, 42), font=font_small)
        lx += int(draw.textlength(txt, font=font_small)) + 25

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Optimized FBD saved to {output_path}")

if __name__ == "__main__":
    create_optimized_zelio_diagram()
