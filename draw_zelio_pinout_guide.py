"""Generates an ultra-clear, high-resolution visual pinout & connection guide
for ZelioSoft 2 FBD blocks (TIMER A+C, BISTABLE, TIMER Li, PRESET COUNT).
Cleaned up to guarantee zero text collisions and maximum readability.
"""
from PIL import Image, ImageDraw, ImageFont

def create_pinout_guide(output_path: str = "zelio_fbd_pinout_guide.png"):
    W, H = 2200, 1400
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 34)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
        hdr_font = ImageFont.truetype("arialbd.ttf", 22)
        bold_font = ImageFont.truetype("arialbd.ttf", 16)
        reg_font = ImageFont.truetype("arial.ttf", 15)
        small_font = ImageFont.truetype("arial.ttf", 13)
        pin_font = ImageFont.truetype("arialbd.ttf", 15)
    except Exception:
        title_font = subtitle_font = hdr_font = bold_font = reg_font = small_font = pin_font = ImageFont.load_default()

    # Top Header
    draw.rectangle([0, 0, W, 90], fill=(15, 23, 42))
    draw.text((45, 14), "ZelioSoft 2 FBD — Точная распиновка блоков и правила подключения", fill=(255, 255, 255), font=title_font)
    draw.text((45, 56), "Куда именно подключать входные и выходные провода на таймерах, триггерах и счетчиках", fill=(148, 163, 184), font=subtitle_font)

    # CARD HELPER
    def draw_card(x, y, w, h, title, subtitle):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        draw.rectangle([x+2, y+2, x+w-2, y+48], fill=(30, 41, 59))
        draw.text((x+20, y+12), title, fill=(255, 255, 255), font=hdr_font)
        draw.text((x+20, y+56), subtitle, fill=(100, 116, 139), font=reg_font)

    # --- CARD 1: TIMER A+C (TOP LEFT) ---
    c1_x, c1_y, c1_w, c1_h = 50, 120, 1020, 580
    draw_card(c1_x, c1_y, c1_w, c1_h, "1. БЛОК TIMER A+C (Таймер задержки вкл/выкл)", "Используется для B001 (гистерезис 3с/5с) и B003 (короткий таймаут 4 мин)")

    # Draw Zoomed TIMER A+C block
    bx, by, bw, bh = c1_x + 400, c1_y + 120, 200, 270
    draw.rectangle([bx, by, bx+bw, by+bh], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((bx + 40, by - 26), "TIMER A+C", fill=(0, 0, 0), font=hdr_font)

    # Waveform inside
    draw.line([(bx+25, by+65), (bx+60, by+65), (bx+60, by+35), (bx+130, by+35), (bx+130, by+65), (bx+175, by+65)], fill=(0, 100, 200), width=3)
    draw.line([(bx+60, by+25), (bx+60, by+75)], fill=(220, 38, 38), width=2)
    draw.line([(bx+130, by+25), (bx+130, by+75)], fill=(220, 38, 38), width=2)
    draw.text((bx + 35, by + 85), "Ta = 3.0 s", fill=(15, 23, 42), font=bold_font)
    draw.text((bx + 35, by + 115), "Tb = 5.0 s", fill=(15, 23, 42), font=bold_font)

    # PINS LEFT & RIGHT
    p_in = [by + 40, by + 95, by + 150, by + 205]
    for i, py in enumerate(p_in):
        draw.polygon([(bx-14, py-10), (bx, py), (bx-14, py+10)], fill=(0, 0, 0))
        draw.text((bx + 8, py - 9), f"I{i+1}", fill=(71, 85, 105), font=small_font)
        draw.polygon([(bx+bw-2, py-12), (bx+bw+16, py), (bx+bw-2, py+12)], fill=(16, 185, 129))
        draw.text((bx + bw - 28, py - 9), f"O{i+1}", fill=(71, 85, 105), font=small_font)

    # Callout Left (I1)
    draw.rounded_rectangle([c1_x + 20, by + 10, bx - 30, by + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((c1_x + 30, by + 18), "▶ ВХОД I1: COMMANDE", fill=(20, 83, 45), font=bold_font)
    draw.text((c1_x + 30, by + 40), "Вход запуска (команда)", fill=(15, 23, 42), font=reg_font)
    draw.text((c1_x + 30, by + 58), "ПОДКЛЮЧАТЬ СЮДА!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx - 30, by + 40), (bx - 14, by + 40)], fill=(22, 163, 74), width=3)

    # Unused Inputs
    draw.text((c1_x + 50, by + 90), "• I2: Сброс (Reset) — пустой", fill=(100, 116, 139), font=reg_font)
    draw.text((c1_x + 50, by + 145), "• I3: Внешняя уставка Ta — пустой", fill=(100, 116, 139), font=reg_font)
    draw.text((c1_x + 50, by + 200), "• I4: Внешняя уставка Tb — пустой", fill=(100, 116, 139), font=reg_font)

    # Callout Right (O1)
    draw.rounded_rectangle([bx + bw + 35, by + 10, c1_x + c1_w - 20, by + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((bx + bw + 45, by + 18), "◀ ВЫХОД O1: SORTIE", fill=(20, 83, 45), font=bold_font)
    draw.text((bx + bw + 45, by + 40), "Дискретный выход таймера (Q)", fill=(15, 23, 42), font=reg_font)
    draw.text((bx + bw + 45, by + 58), "СНИМАТЬ СИГНАЛ ОТСЮДА!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx + bw + 16, by + 40), (bx + bw + 35, by + 40)], fill=(22, 163, 74), width=3)

    draw.text((bx + bw + 45, by + 110), "• O2/O3: Числовые выходы Ta/Tb", fill=(100, 116, 139), font=reg_font)
    draw.text((bx + bw + 45, by + 130), "(в секундах, нужны только для дисплея)", fill=(148, 163, 184), font=small_font)

    # Bottom summary box Card 1
    draw.rounded_rectangle([c1_x + 20, c1_y + 440, c1_x + c1_w - 20, c1_y + 550], radius=8, fill=(240, 249, 255), outline=(2, 132, 199), width=1)
    draw.text((c1_x + 35, c1_y + 455), "Главное правило для TIMER A+C:", fill=(2, 132, 199), font=bold_font)
    draw.text((c1_x + 35, c1_y + 482), "1. ВХОД — САМЫЙ ВЕРХНИЙ ПИН СЛЕВА (I1 COMMANDE).", fill=(15, 23, 42), font=reg_font)
    draw.text((c1_x + 35, c1_y + 510), "2. ВЫХОД — САМЫЙ ВЕРХНИЙ ЗЕЛЕНЫЙ ТРЕУГОЛЬНИК СПРАВА (O1 SORTIE).", fill=(15, 23, 42), font=reg_font)

    # --- CARD 2: BISTABLE (TOP RIGHT) ---
    c2_x, c2_y, c2_w, c2_h = 1130, 120, 1020, 580
    draw_card(c2_x, c2_y, c2_w, c2_h, "2. БЛОК BISTABLE (RS-триггер с памятью)", "Используется для B002 (пуск/останов насоса) и B005 (авария сухого хода)")

    bx2, by2, bw2, bh2 = c2_x + 400, c2_y + 130, 180, 240
    draw.rectangle([bx2, by2, bx2+bw2, by2+bh2], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((bx2 + 35, by2 - 26), "BISTABLE", fill=(0, 0, 0), font=hdr_font)

    draw.text((bx2 + 25, by2 + 30), "SET", fill=(0, 80, 180), font=hdr_font)
    draw.text((bx2 + 115, by2 + 105), "Q", fill=(0, 80, 180), font=hdr_font)
    draw.text((bx2 + 25, by2 + 175), "RESET", fill=(0, 80, 180), font=hdr_font)

    draw.polygon([(bx2-14, by2+42-10), (bx2, by2+42), (bx2-14, by2+42+10)], fill=(0, 0, 0))
    draw.polygon([(bx2-14, by2+188-10), (bx2, by2+188), (bx2-14, by2+188+10)], fill=(0, 0, 0))
    draw.polygon([(bx2+bw2, by2+115-10), (bx2+bw2+14, by2+115), (bx2+bw2, by2+115+10)], fill=(0, 0, 0))

    # SET Callout
    draw.rounded_rectangle([c2_x + 20, by2 + 10, bx2 - 30, by2 + 75], radius=6, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c2_x + 30, by2 + 18), "▶ ВЕРХНИЙ ПИН: SET", fill=(180, 83, 9), font=bold_font)
    draw.text((c2_x + 30, by2 + 40), "Вход включения (импульс 1 -> Q=1)", fill=(15, 23, 42), font=reg_font)
    draw.text((c2_x + 30, by2 + 58), "Включает насос / взводит аварию", fill=(180, 83, 9), font=small_font)
    draw.line([(bx2 - 30, by2 + 42), (bx2 - 14, by2 + 42)], fill=(217, 119, 6), width=3)

    # RESET Callout
    draw.rounded_rectangle([c2_x + 20, by2 + 155, bx2 - 30, by2 + 220], radius=6, fill=(254, 226, 226), outline=(220, 38, 38), width=2)
    draw.text((c2_x + 30, by2 + 163), "▶ НИЖНИЙ ПИН: RESET", fill=(185, 28, 28), font=bold_font)
    draw.text((c2_x + 30, by2 + 185), "Вход сброса (импульс 1 -> Q=0)", fill=(15, 23, 42), font=reg_font)
    draw.text((c2_x + 30, by2 + 203), "Выключает насос / сбрасывает аварию", fill=(185, 28, 28), font=small_font)
    draw.line([(bx2 - 30, by2 + 188), (bx2 - 14, by2 + 188)], fill=(220, 38, 38), width=3)

    # Q Callout
    draw.rounded_rectangle([bx2 + bw2 + 35, by2 + 85, c2_x + c2_w - 20, by2 + 150], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((bx2 + bw2 + 45, by2 + 93), "◀ ПРАВЫЙ ПИН: ВЫХОД Q", fill=(20, 83, 45), font=bold_font)
    draw.text((bx2 + bw2 + 45, by2 + 115), "Дискретный выход триггера", fill=(15, 23, 42), font=reg_font)
    draw.text((bx2 + bw2 + 45, by2 + 133), "Управляет выходами Q1 и Q2", fill=(22, 163, 74), font=small_font)
    draw.line([(bx2 + bw2 + 14, by2 + 115), (bx2 + bw2 + 35, by2 + 115)], fill=(22, 163, 74), width=3)

    # Bottom summary box Card 2
    draw.rounded_rectangle([c2_x + 20, c2_y + 440, c2_x + c2_w - 20, c2_y + 550], radius=8, fill=(240, 249, 255), outline=(2, 132, 199), width=1)
    draw.text((c2_x + 35, c2_y + 455), "Логика работы BISTABLE:", fill=(2, 132, 199), font=bold_font)
    draw.text((c2_x + 35, c2_y + 482), "• В B002: SET включает насос (вода нужна). RESET выключает насос (набрали 3 бар или авария).", fill=(15, 23, 42), font=reg_font)
    draw.text((c2_x + 35, c2_y + 510), "• В B005: SET взводит аварию (сухой ход). RESET сбрасывает аварию (кнопка I2).", fill=(15, 23, 42), font=reg_font)

    # --- CARD 3: TIMER Li (BOTTOM LEFT) ---
    c3_x, c3_y, c3_w, c3_h = 50, 740, 1020, 580
    draw_card(c3_x, c3_y, c3_w, c3_h, "3. БЛОК TIMER Li (Импульсный генератор / мигалка)", "Используется для B004 (формирует 1 импульс каждую минуту в режиме полива)")

    bx3, by3, bw3, bh3 = c3_x + 400, c3_y + 130, 200, 260
    draw.rectangle([bx3, by3, bx3+bw3, by3+bh3], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((bx3 + 50, by3 - 26), "TIMER Li", fill=(0, 0, 0), font=hdr_font)

    draw.line([(bx3+25, by3+65), (bx3+55, by3+65), (bx3+55, by3+35), (bx3+95, by3+35), (bx3+95, by3+65), (bx3+135, by3+65), (bx3+135, by3+35), (bx3+175, by3+35)], fill=(0, 100, 200), width=3)
    draw.text((bx3 + 35, by3 + 85), "Thigh = 30.0 s", fill=(15, 23, 42), font=bold_font)
    draw.text((bx3 + 35, by3 + 115), "Tlow  = 30.0 s", fill=(15, 23, 42), font=bold_font)
    draw.text((bx3 + 35, by3 + 145), "Период: 60 сек", fill=(2, 132, 199), font=bold_font)

    for py in [by3 + 40, by3 + 95, by3 + 150, by3 + 205]:
        draw.polygon([(bx3-14, py-10), (bx3, py), (bx3-14, py+10)], fill=(0, 0, 0))
        draw.polygon([(bx3+bw3-2, py-12), (bx3+bw3+16, py), (bx3+bw3-2, py+12)], fill=(16, 185, 129))

    # Callout Left
    draw.rounded_rectangle([c3_x + 20, by3 + 10, bx3 - 30, by3 + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((c3_x + 30, by3 + 18), "▶ ВХОД I1: COMMANDE", fill=(20, 83, 45), font=bold_font)
    draw.text((c3_x + 30, by3 + 40), "Разрешение работы генератора", fill=(15, 23, 42), font=reg_font)
    draw.text((c3_x + 30, by3 + 58), "ПОДКЛЮЧАТЬ СЮДА!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx3 - 30, by3 + 40), (bx3 - 14, by3 + 40)], fill=(22, 163, 74), width=3)

    # Callout Right
    draw.rounded_rectangle([bx3 + bw3 + 35, by3 + 10, c3_x + c3_w - 20, by3 + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((bx3 + bw3 + 45, by3 + 18), "◀ ВЫХОД O1: SORTIE", fill=(20, 83, 45), font=bold_font)
    draw.text((bx3 + bw3 + 45, by3 + 40), "Выход тактовых импульсов (1/мин)", fill=(15, 23, 42), font=reg_font)
    draw.text((bx3 + bw3 + 45, by3 + 58), "ИДЕТ НА ВХОД СЧЕТЧИКА B006!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx3 + bw3 + 16, by3 + 40), (bx3 + bw3 + 35, by3 + 40)], fill=(22, 163, 74), width=3)

    # Bottom summary box Card 3
    draw.rounded_rectangle([c3_x + 20, c3_y + 440, c3_x + c3_w - 20, c3_y + 550], radius=8, fill=(240, 249, 255), outline=(2, 132, 199), width=1)
    draw.text((c3_x + 35, c3_y + 455), "Главное правило для TIMER Li:", fill=(2, 132, 199), font=bold_font)
    draw.text((c3_x + 35, c3_y + 482), "1. ВХОД — САМЫЙ ВЕРХНИЙ ПИН СЛЕВА (I1 COMMANDE).", fill=(15, 23, 42), font=reg_font)
    draw.text((c3_x + 35, c3_y + 510), "2. ВЫХОД — САМЫЙ ВЕРХНИЙ ЗЕЛЕНЫЙ ТРЕУГОЛЬНИК СПРАВА (O1 SORTIE).", fill=(15, 23, 42), font=reg_font)

    # --- CARD 4: PRESET COUNT (BOTTOM RIGHT) ---
    c4_x, c4_y, c4_w, c4_h = 1130, 740, 1020, 580
    draw_card(c4_x, c4_y, c4_w, c4_h, "4. БЛОК PRESET COUNT (Счетчик минут полива)", "Используется для B006 (отсчитывает 90 минут непрерывной работы при поливе)")

    bx4, by4, bw4, bh4 = c4_x + 400, c4_y + 130, 200, 260
    draw.rectangle([bx4, by4, bx4+bw4, by4+bh4], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((bx4 + 25, by4 - 26), "PRESET COUNT", fill=(0, 0, 0), font=hdr_font)

    # Display inside
    draw.rectangle([bx4 + 25, by4 + 25, bx4 + 175, by4 + 75], fill=(240, 245, 250), outline=(100, 116, 139))
    draw.text((bx4 + 45, by4 + 38), "N = 90", fill=(0, 80, 180), font=hdr_font)
    draw.text((bx4 + 35, by4 + 95), "Preset: 90", fill=(15, 23, 42), font=bold_font)
    draw.text((bx4 + 35, by4 + 125), "Счетчик минут", fill=(100, 116, 139), font=reg_font)

    # Pins Left
    draw.polygon([(bx4-14, by4+40-10), (bx4, by4+40), (bx4-14, by4+40+10)], fill=(0, 0, 0))
    draw.text((bx4 + 8, by4 + 31), "I1", fill=(71, 85, 105), font=small_font)
    draw.polygon([(bx4-14, by4+95-10), (bx4, by4+95), (bx4-14, by4+95+10)], fill=(0, 0, 0))
    draw.text((bx4 + 8, by4 + 86), "I2", fill=(71, 85, 105), font=small_font)
    draw.polygon([(bx4-14, by4+150-10), (bx4, by4+150), (bx4-14, by4+150+10)], fill=(0, 0, 0))
    draw.text((bx4 + 8, by4 + 141), "I3", fill=(71, 85, 105), font=small_font)

    # Pins Right
    draw.polygon([(bx4+bw4-2, by4+40-12), (bx4+bw4+16, by4+40), (bx4+bw4-2, by4+40+12)], fill=(16, 185, 129))
    draw.text((bx4 + bw4 - 28, by4 + 31), "O1", fill=(71, 85, 105), font=small_font)
    draw.polygon([(bx4+bw4-2, by4+95-12), (bx4+bw4+16, by4+95), (bx4+bw4-2, by4+95+12)], fill=(16, 185, 129))
    draw.text((bx4 + bw4 - 28, by4 + 86), "O2", fill=(71, 85, 105), font=small_font)

    # Pulse Callout
    draw.rounded_rectangle([c4_x + 20, by4 + 10, bx4 - 30, by4 + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((c4_x + 30, by4 + 18), "▶ ВЕРХНИЙ: I1 PULSE", fill=(20, 83, 45), font=bold_font)
    draw.text((c4_x + 30, by4 + 40), "Вход счета импульсов", fill=(15, 23, 42), font=reg_font)
    draw.text((c4_x + 30, by4 + 58), "ПОДКЛЮЧАТЬ ОТ ВЫХОДА B004!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx4 - 30, by4 + 40), (bx4 - 14, by4 + 40)], fill=(22, 163, 74), width=3)

    # Reset Callout
    draw.rounded_rectangle([c4_x + 20, by4 + 120, bx4 - 30, by4 + 185], radius=6, fill=(254, 226, 226), outline=(220, 38, 38), width=2)
    draw.text((c4_x + 30, by4 + 128), "▶ ТРЕТИЙ: I3 RESET", fill=(185, 28, 28), font=bold_font)
    draw.text((c4_x + 30, by4 + 150), "Вход обнуления счетчика", fill=(15, 23, 42), font=reg_font)
    draw.text((c4_x + 30, by4 + 168), "Сбрасывает в 0 при выкл. насоса", fill=(185, 28, 28), font=small_font)
    draw.line([(bx4 - 30, by4 + 150), (bx4 - 14, by4 + 150)], fill=(220, 38, 38), width=3)

    # Output Callout
    draw.rounded_rectangle([bx4 + bw4 + 35, by4 + 10, c4_x + c4_w - 20, by4 + 75], radius=6, fill=(220, 252, 231), outline=(22, 163, 74), width=2)
    draw.text((bx4 + bw4 + 45, by4 + 18), "◀ ВЫХОД O1: SORTIE", fill=(20, 83, 45), font=bold_font)
    draw.text((bx4 + bw4 + 45, by4 + 40), "Срабатывает при счете 90", fill=(15, 23, 42), font=reg_font)
    draw.text((bx4 + bw4 + 45, by4 + 58), "ВЗВОДИТ АВАРИЮ В B005!", fill=(22, 163, 74), font=bold_font)
    draw.line([(bx4 + bw4 + 16, by4 + 40), (bx4 + bw4 + 35, by4 + 40)], fill=(22, 163, 74), width=3)

    # Bottom summary box Card 4
    draw.rounded_rectangle([c4_x + 20, c4_y + 440, c4_x + c4_w - 20, c4_y + 550], radius=8, fill=(240, 249, 255), outline=(2, 132, 199), width=1)
    draw.text((c4_x + 35, c4_y + 455), "Главное правило для PRESET COUNT:", fill=(2, 132, 199), font=bold_font)
    draw.text((c4_x + 35, c4_y + 482), "1. ВХОД СЧЕТА — САМЫЙ ВЕРХНИЙ ПИН СЛЕВА (I1 PULSE).", fill=(15, 23, 42), font=reg_font)
    draw.text((c4_x + 35, c4_y + 510), "2. ВХОД СБРОСА — ТРЕТИЙ ПИН СЛЕВА (I3 RESET). ВЫХОД — ВЕРХНИЙ СПРАВА (O1).", fill=(15, 23, 42), font=reg_font)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Clean Pinout guide saved to {output_path}")

if __name__ == "__main__":
    create_pinout_guide()
