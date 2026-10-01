import os
from PIL import Image, ImageDraw, ImageFont

def create_lcd_params_guide():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zelio_lcd_params_guide.png")
    W, H = 1920, 1150
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_hdr = ImageFont.truetype("arialbd.ttf", 18)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_reg = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_mono = ImageFont.truetype("consolab.ttf", 20)
        font_mono_small = ImageFont.truetype("consolab.ttf", 14)
        font_btn = ImageFont.truetype("arialbd.ttf", 13)
    except:
        font_title = font_hdr = font_bold = font_reg = font_small = font_mono = font_mono_small = font_btn = ImageFont.load_default()

    # 1. HEADER
    draw.rectangle([0, 0, W, 70], fill=(15, 65, 125))
    draw.text((30, 20), "НАСТРОЙКА ПАРАМЕТРОВ С ЭКРАНА ZELIO LOGIC SR3 B262BD (ЧЕРЕЗ БЛОК DISPLAY)", fill=(255, 255, 255), font=font_title)

    # 2. LEFT PANEL: DISPLAY BLOCK CONFIGURATION IN ZELIOSOFT 2
    pan1_x, pan1_y, pan1_w, pan1_h = 30, 90, 980, 1020
    draw.rounded_rectangle([pan1_x, pan1_y, pan1_x + pan1_w, pan1_y + pan1_h], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.rectangle([pan1_x + 2, pan1_y + 2, pan1_x + pan1_w - 2, pan1_y + 44], fill=(30, 58, 102))
    draw.text((pan1_x + 15, pan1_y + 12), "ШАГ 1: НАСТРОЙКА БЛОКА B023 DISPLAY В ZELIOSOFT 2", fill=(255, 255, 255), font=font_hdr)

    # Sub-text
    draw.text((pan1_x + 20, pan1_y + 60), "1. Дважды кликните по желтому блоку B023 DISPLAY на вашей схеме.", fill=(15, 23, 42), font=font_bold)
    draw.text((pan1_x + 20, pan1_y + 82), "2. Откроется окно настройки экрана (сетка 4 строки по 18 символов).", fill=(71, 85, 105), font=font_reg)

    # Virtual LCD Screen mockup (4 lines x 18 chars)
    scr_x, scr_y, scr_w, scr_h = pan1_x + 30, pan1_y + 115, 520, 250
    draw.rounded_rectangle([scr_x, scr_y, scr_x + scr_w, scr_h + scr_y], radius=10, fill=(15, 23, 42), outline=(100, 116, 139), width=3)
    # LCD active area (light green matrix)
    draw.rounded_rectangle([scr_x + 15, scr_y + 15, scr_x + scr_w - 15, scr_y + scr_h - 15], radius=6, fill=(220, 252, 231), outline=(34, 197, 94), width=2)

    lcd_lines = [
        ("L1:", "Ta (Пуск) : ", "03.0", "s", "B024 Ta"),
        ("L2:", "Tb (Докач): ", "05.0", "s", "B024 Tb"),
        ("L3:", "T1 (СухХод):", "240 ", "s", "B018 Ta"),
        ("L4:", "T2 (Полив) :", "090 ", "m", "B021 N")
    ]

    for i, (l_num, txt, val, unit, src) in enumerate(lcd_lines):
        ly = scr_y + 35 + i * 48
        draw.text((scr_x + 28, ly), l_num, fill=(100, 116, 139), font=font_mono_small)
        draw.text((scr_x + 65, ly), txt, fill=(20, 83, 45), font=font_mono)
        # Highlight editable value box
        vx = scr_x + 230
        draw.rounded_rectangle([vx - 4, ly - 2, vx + 60, ly + 26], radius=3, fill=(187, 247, 208), outline=(22, 163, 74), width=1)
        draw.text((vx, ly), val, fill=(15, 23, 42), font=font_mono)
        draw.text((vx + 68, ly), unit, fill=(20, 83, 45), font=font_mono)

    # Explanation next to LCD
    call_x = scr_x + scr_w + 20
    draw.rounded_rectangle([call_x, scr_y + 10, pan1_x + pan1_w - 25, scr_y + scr_h], radius=6, fill=(240, 249, 255), outline=(56, 189, 248), width=2)
    draw.text((call_x + 12, scr_y + 20), "ЧТО ВВОДИТЬ В СТРОКИ:", fill=(3, 105, 161), font=font_bold)
    draw.text((call_x + 12, scr_y + 48), "• Строка 1: Текст 'Ta:' + перетащить", fill=(15, 23, 42), font=font_small)
    draw.text((call_x + 24, scr_y + 68), "уставку Ta из блока B024 (фильтр 3с)", fill=(71, 85, 105), font=font_small)
    draw.text((call_x + 12, scr_y + 94), "• Строка 2: Текст 'Tb:' + перетащить", fill=(15, 23, 42), font=font_small)
    draw.text((call_x + 24, scr_y + 114), "уставку Tb из блока B024 (докачка 5с)", fill=(71, 85, 105), font=font_small)
    draw.text((call_x + 12, scr_y + 140), "• Строка 3: Текст 'T1:' + уставка Ta", fill=(15, 23, 42), font=font_small)
    draw.text((call_x + 24, scr_y + 160), "из блока B018 (сухой ход 240с / 4м)", fill=(71, 85, 105), font=font_small)
    draw.text((call_x + 12, scr_y + 186), "• Строка 4: Текст 'T2:' + уставка N", fill=(15, 23, 42), font=font_small)
    draw.text((call_x + 24, scr_y + 206), "из счетчика B021 (полив 90 мин)", fill=(71, 85, 105), font=font_small)

    # CRITICAL CHECKBOX CALLOUT
    chk_y = pan1_y + 390
    draw.rounded_rectangle([pan1_x + 25, chk_y, pan1_x + pan1_w - 25, chk_y + 140], radius=8, fill=(254, 242, 242), outline=(239, 68, 68), width=2)
    draw.text((pan1_x + 40, chk_y + 14), "САМЫЙ ВАЖНЫЙ ПУНКТ: ВКЛЮЧЕНИЕ 'MODIFICATION AUTHORIZED'", fill=(185, 28, 28), font=font_bold)
    draw.text((pan1_x + 40, chk_y + 40), "1. Кликните мышкой на каждое вставленное число на экране (оно выделится синей рамкой).", fill=(15, 23, 42), font=font_reg)
    draw.text((pan1_x + 40, chk_y + 64), "2. Внизу окна настроек ОБЯЗАТЕЛЬНО ПОСТАВЬТЕ ГАЛОЧКУ:", fill=(15, 23, 42), font=font_reg)

    # Big Checkbox Mockup
    cb_x, cb_y = pan1_x + 50, chk_y + 92
    draw.rectangle([cb_x, cb_y, cb_x + 26, cb_y + 26], fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.line([(cb_x + 4, cb_y + 12), (cb_x + 10, cb_y + 20), (cb_x + 22, cb_y + 6)], fill=(22, 163, 74), width=3)
    draw.text((cb_x + 36, cb_y + 3), "[v]  Modification authorized  (Разрешить модификацию с дисплея)", fill=(22, 101, 52), font=font_bold)

    # How to connect B023 on the schematic
    sch_box_y = pan1_y + 555
    draw.rounded_rectangle([pan1_x + 25, sch_box_y, pan1_x + pan1_w - 25, sch_box_y + 430], radius=8, fill=(250, 252, 255), outline=(180, 200, 225), width=1)
    draw.text((pan1_x + 40, sch_box_y + 15), "КАК ПОДКЛЮЧИТЬ БЛОК B023 DISPLAY НА СХЕМЕ FBD:", fill=(30, 60, 120), font=font_bold)
    draw.text((pan1_x + 40, sch_box_y + 42), "У блока DISPLAY слева есть один вход — 'Command' (разрешение показа экрана).", fill=(71, 85, 105), font=font_reg)
    draw.text((pan1_x + 40, sch_box_y + 65), "Чтобы этот экран показывался ВСЕГДА в нормальном режиме работы насоса:", fill=(71, 85, 105), font=font_reg)

    # Diagram snippet
    snip_x, snip_y = pan1_x + 50, sch_box_y + 100
    # Block B009 NOT
    draw.rectangle([snip_x, snip_y, snip_x + 60, snip_y + 54], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.text((snip_x + 12, snip_y - 18), "B009", fill=(0, 0, 0), font=font_bold)
    draw.text((snip_x + 14, snip_y + 16), "NOT", fill=(22, 163, 74), font=font_bold)
    draw.text((snip_x - 120, snip_y + 16), "от B012 (Авария) -->", fill=(100, 116, 139), font=font_small)

    # Block B023 DISPLAY
    draw.rectangle([snip_x + 220, snip_y - 10, snip_x + 340, snip_y + 64], fill=(254, 240, 138), outline=(202, 138, 4), width=2)
    draw.text((snip_x + 245, snip_y - 28), "B023", fill=(0, 0, 0), font=font_bold)
    draw.text((snip_x + 235, snip_y + 20), "DISPLAY", fill=(15, 23, 42), font=font_bold)

    # Wire between B009 and B023
    draw.line([(snip_x + 60, snip_y + 27), (snip_x + 220, snip_y + 27)], fill=(2, 132, 199), width=3)
    draw.polygon([(snip_x + 214, snip_y + 22), (snip_x + 220, snip_y + 27), (snip_x + 214, snip_y + 32)], fill=(2, 132, 199))
    draw.text((snip_x + 75, snip_y + 8), "Команда показа (1=ВКЛ)", fill=(2, 132, 199), font=font_small)

    draw.text((pan1_x + 40, sch_box_y + 190), "• Вход B023 подключается к выходу B009 NOT (сигнал 'Аварии НЕТ').", fill=(15, 23, 42), font=font_bold)
    draw.text((pan1_x + 40, sch_box_y + 215), "  Пока аварии нет — на экране горит этот главный экран с параметрами и уставками.", fill=(71, 85, 105), font=font_reg)
    draw.text((pan1_x + 40, sch_box_y + 238), "  А если сработала авария — B009 выдает 0, экран гаснет и уступает место аварийному!", fill=(71, 85, 105), font=font_reg)
    draw.text((pan1_x + 40, sch_box_y + 270), "• Альтернатива: можно подать постоянную '1' с блока ON (вкладка IN внизу экрана).", fill=(100, 116, 139), font=font_reg)

    # 3. RIGHT PANEL: HARDWARE BUTTONS & LIVE ADJUSTMENT
    pan2_x, pan2_y, pan2_w, pan2_h = 1040, 90, 850, 1020
    draw.rounded_rectangle([pan2_x, pan2_y, pan2_x + pan2_w, pan2_y + pan2_h], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.rectangle([pan2_x + 2, pan2_y + 2, pan2_x + pan2_w - 2, pan2_y + 44], fill=(22, 101, 52))
    draw.text((pan2_x + 15, pan2_y + 12), "ШАГ 2: КАК МЕНЯТЬ УСТАВКИ КНОПКАМИ НА КОРПУСЕ ZELIO", fill=(255, 255, 255), font=font_hdr)

    # Step by Step flow on front panel
    steps = [
        ("ДЕЙСТВИЕ 1: ВЫХОД НА ЭКРАН ПАРАМЕТРОВ",
         "Если на реле отображается экран входов/выходов, нажмите одновременно:",
         [("Shift", "белая клавиша"), ("+", ""), ("Menu/OK", "зеленая круглая")],
         "Реле переключится на ваш настроенный экран B023 с параметрами."),

        ("ДЕЙСТВИЕ 2: ВХОД В РЕЖИМ РЕДАКТИРОВАНИЯ (PARAM)",
         "Нажмите белую клавишу Shift. В нижней строке экрана появится меню.",
         [("Shift", "нажать один раз"), ("->", ""), ("Param", "кнопка под надписью Param")],
         "На первой цифре уставки (03.0) замигает курсор!"),

        ("ДЕЙСТВИЕ 3: ИЗМЕНЕНИЕ ЗНАЧЕНИЯ И НАВИГАЦИЯ",
         "Используйте стрелки на передней панели:",
         [("▲ / ▼", "Увеличить / Уменьшить цифру (+ / -)"),
          ("◄ / ►", "Смена разряда и переход на след. строку")],
         "Вы можете свободно переходить между Ta (3с), Tb (5с), T1 (240с) и T2 (90м)."),

        ("ДЕЙСТВИЕ 4: СОХРАНЕНИЕ НОВЫХ ЗНАЧЕНИЙ",
         "Когда нужное значение выставлено, нажмите кнопку подтверждения:",
         [("Menu/OK", "зеленая кнопка")],
         "Новое значение МГНОВЕННО сохраняется в энергонезависимую память EEPROM и применяется на лету без остановки насоса!"),

        ("ДЕЙСТВИЕ 5: ВЫХОД ИЗ РЕЖИМА РЕДАКТИРОВАНИЯ",
         "Для выхода нажмите клавишу Shift:",
         [("Shift", "нажать для выхода")],
         "Курсор перестанет мигать, экран вернется в обычный режим чтения.")
    ]

    sy = pan2_y + 60
    for num, (title, desc, btns, note) in enumerate(steps):
        draw.rounded_rectangle([pan2_x + 20, sy, pan2_x + pan2_w - 20, sy + 160], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((pan2_x + 35, sy + 10), title, fill=(15, 23, 42), font=font_bold)
        draw.text((pan2_x + 35, sy + 34), desc, fill=(71, 85, 105), font=font_reg)

        # Buttons graphic
        bx = pan2_x + 35
        for b_name, b_desc in btns:
            if b_name in ["+", "->"]:
                draw.text((bx + 6, sy + 64), b_name, fill=(100, 116, 139), font=font_bold)
                bx += 26
                continue
            bw = int(draw.textlength(b_name, font=font_btn)) + 24
            is_green = "OK" in b_name
            bg_col = (220, 252, 231) if is_green else (241, 245, 249)
            brd_col = (34, 197, 94) if is_green else (100, 116, 139)
            draw.rounded_rectangle([bx, sy + 58, bx + bw, sy + 88], radius=4, fill=bg_col, outline=brd_col, width=2)
            draw.text((bx + 12, sy + 64), b_name, fill=(15, 23, 42), font=font_btn)
            if b_desc:
                draw.text((bx + bw + 8, sy + 66), f"({b_desc})", fill=(100, 116, 139), font=font_small)
                bx += bw + int(draw.textlength(f"({b_desc})", font=font_small)) + 16
            else:
                bx += bw + 12

        draw.text((pan2_x + 35, sy + 104), note, fill=(22, 101, 52), font=font_small)
        sy += 175

    # EEPROM note box at bottom right
    eeprom_y = pan2_y + pan2_h - 100
    draw.rounded_rectangle([pan2_x + 20, eeprom_y, pan2_x + pan2_w - 20, eeprom_y + 80], radius=6, fill=(254, 252, 232), outline=(234, 179, 8), width=2)
    draw.text((pan2_x + 35, eeprom_y + 12), "ВАЖНО: ПАМЯТЬ НЕ СБРАСЫВАЕТСЯ ПРИ ВЫКЛЮЧЕНИИ ПИТАНИЯ!", fill=(161, 98, 7), font=font_bold)
    draw.text((pan2_x + 35, eeprom_y + 36), "Все измененные с кнопок уставки (Ta, Tb, 240с, 90мин) сохраняются в EEPROM.", fill=(113, 63, 18), font=font_small)
    draw.text((pan2_x + 35, eeprom_y + 54), "При отключении электричества и повторном включении реле запустится с вашими новыми уставками!", fill=(113, 63, 18), font=font_small)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"LCD parameters guide saved to {output_path}")

if __name__ == "__main__":
    create_lcd_params_guide()
