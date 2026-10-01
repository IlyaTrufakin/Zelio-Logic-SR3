"""Generates a polished, pixel-perfect, high-resolution graphical schematic of the FBD program
for Schneider Zelio Logic SR3 B262BD pump control.
"""
from PIL import Image, ImageDraw, ImageFont

def create_fbd_diagram(output_path: str = "fbd_pump_schematic.png"):
    W, H = 2400, 1500
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
        hdr_font = ImageFont.truetype("arialbd.ttf", 22)
        bold_font = ImageFont.truetype("arialbd.ttf", 17)
        reg_font = ImageFont.truetype("arial.ttf", 15)
        small_font = ImageFont.truetype("arialbd.ttf", 13)
        code_font = ImageFont.truetype("consolab.ttf", 16)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = reg_font = small_font = bold_font = hdr_font = code_font = title_font

    # --- TOP HEADER ---
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42))
    draw.text((50, 16), "Zelio Logic SR3 B262BD — Графическая схема программы в формате FBD", fill=(255, 255, 255), font=title_font)
    draw.text((50, 60), "Автоматика скважинного насоса: датчик НО, кнопка пуска/сброса, тумблер таймаутов, ТТР и лампа работы", fill=(148, 163, 184), font=subtitle_font)

    # Terminal pill
    def draw_terminal(x, y, w, h, text, subtext, color=(16, 185, 129), is_input=True):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=color, outline=(5, 150, 105), width=2)
        draw.text((x + 18, y + 10), text, fill=(255, 255, 255), font=hdr_font)
        draw.text((x + 18, y + 36), subtext, fill=(240, 253, 244), font=small_font)
        px = x + w if is_input else x
        py = y + h // 2
        draw.ellipse([px-7, py-7, px+7, py+7], fill=(15, 23, 42), outline=(255, 255, 255), width=2)
        return (px, py)

    # FBD Block
    def draw_fbd_block(x, y, w, h, b_id, title, subtitle, settings, in_labels, out_labels, bg=(238, 242, 255), border=(79, 70, 229)):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=bg, outline=border, width=2)
        # Header bar
        draw.rectangle([x+2, y+2, x+w-2, y+34], fill=border)
        draw.text((x + 12, y + 6), f"[{b_id}] {title}", fill=(255, 255, 255), font=bold_font)
        if subtitle:
            draw.text((x + 14, y + 40), subtitle, fill=(100, 116, 139), font=small_font)

        # Settings box (offset to the right so it never touches left pin labels)
        if settings:
            sy = y + 62
            for s in settings:
                draw.text((x + 75, sy), s, fill=(15, 23, 42), font=code_font)
                sy += 22

        # Input pins (left)
        in_ports = {}
        if in_labels:
            step = (h - 45) / (len(in_labels) + 1)
            for i, lbl in enumerate(in_labels):
                py = int(y + 45 + step * (i + 1))
                draw.ellipse([x-6, py-6, x+6, py+6], fill=border, outline=(255, 255, 255), width=2)
                draw.text((x + 10, py - 9), lbl, fill=(79, 70, 229), font=small_font)
                in_ports[lbl] = (x, py)


        # Output pins (right)
        out_ports = {}
        if out_labels:
            step = (h - 45) / (len(out_labels) + 1)
            for i, lbl in enumerate(out_labels):
                py = int(y + 40 + step * (i + 1))
                draw.ellipse([x+w-6, py-6, x+w+6, py+6], fill=border, outline=(255, 255, 255), width=2)
                draw.text((x + w - 12 - draw.textlength(lbl, font=small_font), py - 9), lbl, fill=(79, 70, 229), font=small_font)
                out_ports[lbl] = (x+w, py)

        return in_ports, out_ports

    def draw_logic_gate(x, y, w, h, g_type, in_count=2, bg=(241, 245, 249), border=(100, 116, 139)):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=bg, outline=border, width=2)
        draw.text((x + w//2 - draw.textlength(g_type, font=bold_font)//2, y + h//2 - 10), g_type, fill=(15, 23, 42), font=bold_font)
        in_p = []
        step = h / (in_count + 1)
        for i in range(in_count):
            py = int(y + step * (i + 1))
            draw.ellipse([x-5, py-5, x+5, py+5], fill=border)
            in_p.append((x, py))
        out_p = (x + w, y + h // 2)
        draw.ellipse([x+w-5, out_p[1]-5, x+w+5, out_p[1]+5], fill=border)
        return in_p, out_p

    def draw_wire(pts, color=(30, 41, 59), width=2, arrow=True):
        for i in range(len(pts)-1):
            draw.line([pts[i], pts[i+1]], fill=color, width=width)
        if arrow:
            x, y = pts[-1]
            px, py = pts[-2]
            if x > px:
                draw.polygon([(x, y), (x-9, y-5), (x-9, y+5)], fill=color)
            elif y > py:
                draw.polygon([(x, y), (x-5, y-9), (x+5, y-9)], fill=color)
            elif y < py:
                draw.polygon([(x, y), (x-5, y+9), (x+5, y+9)], fill=color)
            elif x < px:
                draw.polygon([(x, y), (x+9, y-5), (x+9, y+5)], fill=color)

    def draw_junction(pt, color=(30, 41, 59), radius=5):
        draw.ellipse([pt[0]-radius, pt[1]-radius, pt[0]+radius, pt[1]+radius], fill=color)

    # =========================================================================
    # 1. INPUT TERMINALS
    # =========================================================================
    p_i1 = draw_terminal(50, 160, 240, 65, "I1 : ДАТЧИК ДАВЛ.", "НО контакт (2...3 бар)", color=(2, 132, 199))
    p_i2 = draw_terminal(50, 370, 240, 65, "I2 : ПУСК / СБРОС", "Кнопка (НО импульс)", color=(2, 132, 199))
    p_i3 = draw_terminal(50, 770, 240, 65, "I3 : ТУМБЛЕР РЕЖ.", "0=Короткий, 1=Длинный", color=(2, 132, 199))

    # =========================================================================
    # 2. PRESSURE INVERTER & B01 TIMER A/C
    # =========================================================================
    not_i1_in, not_i1_out = draw_logic_gate(350, 168, 60, 50, "NOT", in_count=1)
    draw_wire([p_i1, not_i1_in[0]])

    b01_in, b01_out = draw_fbd_block(480, 130, 280, 140, "B01", "TIMER A/C", "Фильтр гистерезиса",
                                    ["Ta = 3.0 s (Вкл)", "Tb = 5.0 s (Выкл)"],
                                    ["Cmd"], ["Out"],
                                    bg=(238, 242, 255), border=(79, 70, 229))
    draw_wire([not_i1_out, b01_in["Cmd"]])

    # NOT gate for stop when pressure satisfied
    not_p_in, not_p_out = draw_logic_gate(810, 260, 60, 45, "NOT", in_count=1)
    j_b01 = (785, b01_out["Out"][1])
    draw_junction(j_b01)
    draw_wire([b01_out["Out"], j_b01, (785, not_p_in[0][1]), not_p_in[0]])

    # OR1: Start trigger (Auto B01 OR Manual I2)
    or1_in, or1_out = draw_logic_gate(830, 145, 65, 65, "OR", in_count=2)
    draw_wire([j_b01, (800, j_b01[1]), (800, or1_in[0][1]), or1_in[0]])
    draw_wire([p_i2, (310, p_i2[1]), (310, 395), (810, 395), (810, or1_in[1][1]), or1_in[1]])
    j_i2 = (310, p_i2[1])
    draw_junction(j_i2)

    # AND1: Start AND (No Alarm)
    and1_in, and1_out = draw_logic_gate(940, 155, 65, 65, "AND", in_count=2)
    draw_wire([or1_out, and1_in[0]])

    # OR2: Stop trigger (Pressure satisfied OR Alarm)
    or2_in, or2_out = draw_logic_gate(940, 260, 65, 65, "OR", in_count=2)
    draw_wire([not_p_out, or2_in[0]])

    # =========================================================================
    # 3. B02 BISTABLE (MAIN PUMP) & OUTPUTS
    # =========================================================================
    b02_in, b02_out = draw_fbd_block(1060, 160, 250, 150, "B02", "BISTABLE", "Главный триггер насоса",
                                    ["Выход Q: Насос ВКЛ"],
                                    ["Set", "Reset"], ["Q"],
                                    bg=(254, 243, 199), border=(217, 119, 6))
    draw_wire([and1_out, b02_in["Set"]])
    draw_wire([or2_out, b02_in["Reset"]])

    # Outputs (Right top)
    p_q1 = draw_terminal(2050, 150, 280, 65, "Q1 : ТТР НАСОСА", "Выход +24V на ТТР (насос)", color=(225, 29, 72), is_input=False)
    p_q2 = draw_terminal(2050, 250, 280, 65, "Q2 : ЛАМПА РАБОТЫ", "Горит когда качает (Q2=Q1)", color=(234, 88, 12), is_input=False)

    j_q_main = (1600, b02_out["Q"][1])
    draw_wire([b02_out["Q"], (2050, b02_out["Q"][1])])
    draw_junction(j_q_main)
    draw_wire([j_q_main, (1600, p_q2[1]), p_q2])

    # =========================================================================
    # 4. TIMEOUT SELECTION PANEL (I3)
    # =========================================================================
    draw.rounded_rectangle([320, 520, 1950, 940], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    draw.text((350, 535), "БЛОК ЗАЩИТЫ ОТ СУХОГО ХОДА И ПОРЫВА С ВЫБОРОМ ТАЙМАУТА ПО ВХОДУ I3", fill=(30, 41, 59), font=hdr_font)

    # Inverter for I3
    not_i3_in, not_i3_out = draw_logic_gate(380, 590, 60, 45, "NOT", in_count=1)
    j_i3 = (320, p_i3[1])
    draw_junction(j_i3)
    draw_wire([p_i3, j_i3, (320, not_i3_in[0][1]), not_i3_in[0]])

    # Wire Q running down
    j_q_down1 = (1350, b02_out["Q"][1])
    draw_junction(j_q_down1)

    # --- Short timeout (I3 = 0, 4 min) ---
    and_short_in, and_short_out = draw_logic_gate(500, 580, 65, 65, "AND", in_count=2)
    draw_wire([(1350, 588), and_short_in[0]])
    draw_junction((1350, 588))
    draw_wire([not_i3_out, and_short_in[1]])

    b03_in, b03_out = draw_fbd_block(630, 560, 330, 120, "B03", "TIMER A/C", "Короткий таймаут (I3=0)",
                                    ["Функция: A (Delay ON)", "Ta = 240.0 s (4 мин)"],
                                    ["Cmd"], ["Out"],
                                    bg=(254, 226, 226), border=(220, 38, 38))
    draw_wire([and_short_out, b03_in["Cmd"]])

    # --- Long timeout (I3 = 1, 90 min) ---
    and_long_in, and_long_out = draw_logic_gate(500, 760, 65, 65, "AND", in_count=2)
    draw_wire([(1350, 768), and_long_in[0]])
    draw_junction((1350, 768))
    draw_wire([j_i3, (320, and_long_in[1][1]), and_long_in[1]])

    b04_in, b04_out = draw_fbd_block(630, 740, 330, 120, "B04", "TIMER Li", "Минутный генератор (период 60 с)",
                                    ["Thigh = 30.0 s", "Tlow  = 30.0 s"],
                                    ["Cmd"], ["Out"],
                                    bg=(224, 242, 254), border=(2, 132, 199))
    draw_wire([and_long_out, b04_in["Cmd"]])

    b06_in, b06_out = draw_fbd_block(1030, 740, 300, 130, "B06", "PRESET COUNT", "Счетчик минут (I3=1)",
                                    ["Preset = 90 (минут)", "Счет импульсов B04"],
                                    ["Pulse", "Reset"], ["Out"],
                                    bg=(224, 242, 254), border=(2, 132, 199))

    draw_wire([b04_out["Out"], b06_in["Pulse"]])

    # Reset B06 when pump turns OFF
    not_q_in, not_q_out = draw_logic_gate(900, 850, 60, 45, "NOT", in_count=1)
    draw_wire([(1350, 872), not_q_in[0]])
    draw_junction((1350, 872))
    draw_wire([not_q_out, (980, 872), (980, b06_in["Reset"][1]), b06_in["Reset"]])

    # =========================================================================
    # 5. ALARM LATCH B05 & INTERLOCKS
    # =========================================================================
    or3_in, or3_out = draw_logic_gate(1380, 660, 65, 75, "OR", in_count=2)
    draw_wire([b03_out["Out"], (1340, b03_out["Out"][1]), (1340, or3_in[0][1]), or3_in[0]])
    draw_wire([b06_out["Out"], (1340, b06_out["Out"][1]), (1340, or3_in[1][1]), or3_in[1]])

    b05_in, b05_out = draw_fbd_block(1500, 640, 300, 140, "B05", "BISTABLE", "Триггер Аварии",
                                    ["Блокирует насос Q1", "Сброс кнопкой I2"],
                                    ["Set", "Reset"], ["Q"],
                                    bg=(254, 226, 226), border=(220, 38, 38))
    draw_wire([or3_out, b05_in["Set"]])

    # Wire I2 to Reset of B05
    draw_wire([j_i2, (310, 480), (1460, 480), (1460, b05_in["Reset"][1]), b05_in["Reset"]])
    draw_junction((310, 480))

    # Alarm output wire to OR2 stop and to Inhibit AND1
    j_al_wire = (1850, b05_out["Q"][1])
    draw_junction(j_al_wire)
    draw_wire([b05_out["Q"], j_al_wire, (1850, 360), (910, 360), (910, or2_in[1][1]), or2_in[1]])

    # NOT for Inhibit start on AND1 (placed cleanly below header bar)
    not_al_in, not_al_out = draw_logic_gate(810, 98, 60, 45, "NOT", in_count=1)
    draw_wire([(910, 360), (910, 120), not_al_in[0]])
    draw_wire([not_al_out, (920, 120), (920, and1_in[1][1]), and1_in[1]])


    # Terminal LCD Backlight
    p_lcd = draw_terminal(2050, 670, 280, 65, "LCD BACKLIGHT", "Подсветка при аварии", color=(217, 119, 6), is_input=False)
    draw_wire([j_al_wire, (2050, j_al_wire[1])])

    # =========================================================================
    # 6. BOTTOM SUMMARY TABLE
    # =========================================================================
    draw.rounded_rectangle([40, 980, W-40, H-40], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    draw.rectangle([42, 982, W-42, 1028], fill=(241, 245, 249))
    draw.text((60, 992), "СВОДНАЯ ТАБЛИЦА НАСТРОЕК БЛОКОВ В ZELIOSOFT 2 (Двойной клик на блоке в редакторе FBD)", fill=(15, 23, 42), font=bold_font)

    cols = [
        ("Блок", 60),
        ("Тип функции", 200),
        ("Параметры и уставки (вводить в окне свойств)", 400),
        ("Назначение в схеме скважинного насоса", 1000),
        ("Логика работы", 1620)
    ]
    for c_title, cx in cols:
        draw.text((cx, 1042), c_title, fill=(71, 85, 105), font=bold_font)

    draw.line([(40, 1070), (W-40, 1070)], fill=(226, 232, 240), width=1)

    rows = [
        ("B01", "TIMER A/C", "Функция: A/C,  Ta = 3.0 s,  Tb = 5.0 s", "Гистерезис и фильтрация гидроударов", "3 с задержка пуска (антидребезг), 5 с задержка останова (докачка бака)"),
        ("B02", "BISTABLE", "Тип: RS-триггер (Set / Reset)", "Главный триггер включения насоса Q1", "Set: запрос на воду без аварии; Reset: давление в норме или Авария"),
        ("B03", "TIMER A/C", "Функция: A (Delay ON),  Ta = 240.0 s (4 мин)", "Короткий таймаут аварии (тумблер I3 = 0)", "Если при I3=0 насос молотит > 4 мин без набора 3 бар -> Авария"),
        ("B04", "TIMER Li", "Thigh = 30.0 s,  Tlow = 30.0 s (период 60 с)", "Минутный тактовый генератор", "Формирует 1 импульс в минуту для подсчета времени полива"),
        ("B06", "PRESET COUNT", "Preset = 90,  Счет по переднему фронту", "Длинный таймаут аварии (тумблер I3 = 1)", "Разрешает непрерывную работу до 90 минут при поливе и наборе ванны"),
        ("B05", "BISTABLE", "Тип: RS-триггер аварийной блокировки", "Защита от сухого хода и порыва трубы", "Взводится по таймауту B03 или B06. Сбрасывается кнопкой I2"),
        ("Q1", "Выход 1", "Транзисторный выход 24 В DC, 0.5 А", "Управление твердотельным реле (ТТР)", "Подает сигнал +24В на вход ТТР single-phase SSR насоса"),
        ("Q2", "Выход 2", "Транзисторный выход 24 В DC, 0.5 А", "Сигнальная лампа работы насоса", "Включается строго синхронно с насосом Q1 (горит при работе)"),
    ]

    ry = 1082
    for r_id, r_type, r_set, r_role, r_logic in rows:
        bg_row = (248, 250, 252) if ((ry - 1082) // 40) % 2 == 0 else (255, 255, 255)
        draw.rectangle([45, ry-4, W-45, ry+34], fill=bg_row)
        draw.text((60, ry), r_id, fill=(30, 41, 59), font=bold_font)
        draw.text((200, ry), r_type, fill=(79, 70, 229), font=bold_font)
        draw.text((400, ry), r_set, fill=(15, 23, 42), font=code_font)
        draw.text((1000, ry), r_role, fill=(51, 65, 85), font=reg_font)
        draw.text((1620, ry), r_logic, fill=(71, 85, 105), font=reg_font)
        ry += 40

    img.save(output_path, "PNG")
    print(f"Diagram saved to {output_path} ({W}x{H})")
    return output_path

if __name__ == "__main__":
    create_fbd_diagram()
