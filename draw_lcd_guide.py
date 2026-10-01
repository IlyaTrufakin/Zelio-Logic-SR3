"""Generates a high-resolution graphical diagram for Zelio Logic SR3 LCD display & HMI setup.
"""
from PIL import Image, ImageDraw, ImageFont

def create_lcd_diagram(output_path: str = "fbd_lcd_display_guide.png"):
    W, H = 2200, 1300
    img = Image.new("RGB", (W, H), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 34)
        subtitle_font = ImageFont.truetype("arial.ttf", 19)
        hdr_font = ImageFont.truetype("arialbd.ttf", 22)
        bold_font = ImageFont.truetype("arialbd.ttf", 17)
        reg_font = ImageFont.truetype("arial.ttf", 15)
        small_font = ImageFont.truetype("arialbd.ttf", 13)
        mono_font = ImageFont.truetype("consolab.ttf", 22)
        mono_small = ImageFont.truetype("consolab.ttf", 16)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = reg_font = small_font = bold_font = hdr_font = mono_font = mono_small = title_font

    # Top Header
    draw.rectangle([0, 0, W, 85], fill=(15, 23, 42))
    draw.text((45, 14), "Zelio Logic SR3 B262BD — Настройка экрана LCD и сервисных функций", fill=(255, 255, 255), font=title_font)
    draw.text((45, 54), "Отображение статуса, таймаутов, счетчика пусков и моточасов насоса через блок DISPLAY (FBD)", fill=(148, 163, 184), font=subtitle_font)

    # --- SECTION 1: VISUAL SCREENS (NORMAL VS ALARM) ---
    def draw_lcd_screen(x, y, title, lines, is_alarm=False):
        # Frame
        frame_color = (220, 38, 38) if is_alarm else (30, 41, 59)
        draw.rounded_rectangle([x, y, x+520, y+310], radius=16, fill=(15, 23, 42), outline=frame_color, width=4)
        # Title badge
        badge_bg = (239, 68, 68) if is_alarm else (59, 130, 246)
        draw.rounded_rectangle([x+20, y-15, x+300, y+15], radius=6, fill=badge_bg)
        draw.text((x+32, y-12), title, fill=(255, 255, 255), font=bold_font)

        # LCD Display area (greenish-gray or amber)
        lcd_bg = (254, 242, 242) if is_alarm else (220, 252, 231)
        lcd_border = (239, 68, 68) if is_alarm else (34, 197, 94)
        draw.rounded_rectangle([x+20, y+30, x+500, y+275], radius=8, fill=lcd_bg, outline=lcd_border, width=2)

        # Draw 4 LCD lines
        text_color = (185, 28, 28) if is_alarm else (20, 83, 45)
        for i, line in enumerate(lines):
            ly = y + 55 + i * 50
            # Grid dots / line indicator
            draw.text((x+35, ly), f"L{i+1}:", fill=(148, 163, 184), font=mono_small)
            draw.text((x+80, ly), line, fill=text_color, font=mono_font)

    # Normal Screen
    draw_lcd_screen(60, 130, "ЭКРАН 1: РАБОЧИЙ РЕЖИМ", [
        "PUMP: RUN  [Q1=ON]",
        "MODE: SHORT (4m) ",
        "STARTS: 00142    ",
        "HOURS:  0034.5 h "
    ], is_alarm=False)

    # Alarm Screen
    draw_lcd_screen(620, 130, "ЭКРАН 2: АВАРИЯ (СУХОЙ ХОД)", [
        "** ALARM: DRY RUN **",
        "PUMP STOPPED [B05]  ",
        "CHECK WATER / PIPE! ",
        "PRESS [I2] TO RESET "
    ], is_alarm=True)

    # --- SECTION 2: FBD DISPLAY BLOCKS WIRING ---
    # Container box
    draw.rounded_rectangle([1180, 110, W-50, 440], radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((1205, 125), "Подключение блоков индикации DISPLAY в схеме FBD", fill=(15, 23, 42), font=hdr_font)
    draw.text((1205, 155), "В библиотеке FBD выберите блок DISPLAY (HMI). Текст задается двойным кликом на блок.", fill=(100, 116, 139), font=reg_font)

    # Draw Display Block 1 (Work)
    def draw_fbd_disp(x, y, b_id, title, desc, active_cond):
        draw.rounded_rectangle([x, y, x+380, y+110], radius=8, fill=(240, 249, 255), outline=(2, 132, 199), width=2)
        draw.rectangle([x+2, y+2, x+378, y+28], fill=(2, 132, 199))
        draw.text((x+10, y+5), f"[{b_id}] DISPLAY ({title})", fill=(255, 255, 255), font=bold_font)
        draw.text((x+15, y+38), f"Условие активации: {active_cond}", fill=(15, 23, 42), font=small_font)
        draw.text((x+15, y+62), f"Выводит: {desc}", fill=(71, 85, 105), font=reg_font)
        draw.text((x+15, y+85), "Приоритет: Обычный", fill=(100, 116, 139), font=small_font)
        # In pin
        draw.ellipse([x-6, y+45-6, x+6, y+45+6], fill=(2, 132, 199), outline=(255, 255, 255), width=2)
        draw.text((x+10, y+38), "", fill=(2, 132, 199), font=small_font)

    draw_fbd_disp(1220, 195, "B10", "Рабочий экран", "Статус, Режим I3, Моточасы", "Инверсия Аварии (NOT B05)")
    draw_fbd_disp(1220, 315, "B11", "Аварийный экран", "Текст ошибки 'DRY RUN', подсказка I2", "Выход триггера Аварии (B05 Q)")

    draw_fbd_disp(1700, 195, "B07", "PRESET COUNT (Счетчик)", "Считает каждый пуск насоса", "Вход Pulse от выхода Q1")
    draw_fbd_disp(1700, 315, "B08", "HOUR COUNTER (Моточасы)", "Считает часы работы двигателя", "Вход Enable от выхода Q1")

    # --- SECTION 3: USEFUL RECOMMENDATIONS TABLE ---
    tbl_y = 475
    draw.rounded_rectangle([45, tbl_y, W-45, H-45], radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.rectangle([47, tbl_y+2, W-47, tbl_y+46], fill=(30, 41, 59))
    draw.text((65, tbl_y+12), "ПОЛЕЗНЫЕ СЕРВИСНЫЕ И ЗАЩИТНЫЕ ФУНКЦИИ ДЛЯ ДООСНАЩЕНИЯ ПРОГРАММЫ", fill=(255, 255, 255), font=hdr_font)

    features = [
        ("1. Защита от тактования (Anti-Cycling Timer)", 
         "Блок TIMER A/C (Ta=30..60с)", 
         "Если мембрана гидроаккумулятора порвется, насос начинает включаться каждые 5 секунд при открытом кране, что быстро сжигает пусковую обмотку. Блок задержки повторного пуска запрещает включение чаще 1 раза в минуту."),
        
        ("2. Учет моточасов и количества пусков", 
         "Блоки PRESET COUNT + HOUR COUNTER", 
         "Позволяет оценить реальный дебит скважины и ресурс насоса. По регламенту скважинные насосы требуют ТО или ревизии через 5000-10000 часов либо 100 000 пусков. Данные выводятся на ЖК-экран."),
        
        ("3. Мигающая подсветка LCD при аварии", 
         "Выход LCD BACKLIGHT + TIMER Li", 
         "Выход управления подсветкой экрана ПЛК можно подключить через генератор импульсов (TIMER Li, 1 Гц) при аварии B05. В темноте щитка мигающий экран сразу привлекает внимание хозяина дома."),
        
        ("4. Аппаратная защита ТТР (Варистор и Snubber)", 
         "Внешняя обвязка выхода ТТР (SSR)", 
         "Скважинный насос — высокоиндуктивная нагрузка с пусковым током в 5-7 раз выше номинального. Для полупроводникового реле обязательны: варистор 470В (20D471K) параллельно силовым клеммам ТТР и RC-цепочка (0.1 мкФ 630В + 100 Ом 2Вт)."),
        
        ("5. Ручная корректировка уставок с кнопок ПЛК", 
         "Кнопки Z1..Z4 на лицевой панели", 
         "В FBD можно привязать кнопки со стрелками Z1..Z4 к входам UP/DOWN счетчиков B03 (время аварии) и B01 (гистерезис). Это позволяет менять секунды прямо с панели без подключения кабеля к компьютеру.")
    ]

    row_y = tbl_y + 55
    for title, blk, desc in features:
        draw.text((65, row_y), title, fill=(2, 132, 199), font=bold_font)
        draw.text((580, row_y), blk, fill=(220, 38, 38), font=bold_font)
        
        # Word wrap description
        words = desc.split(' ')
        lines_desc = []
        cur = ""
        for w in words:
            if draw.textlength(cur + " " + w, font=reg_font) < 1150:
                cur += (" " if cur else "") + w
            else:
                lines_desc.append(cur)
                cur = w
        if cur:
            lines_desc.append(cur)
            
        for dl in lines_desc:
            draw.text((950, row_y), dl, fill=(51, 65, 85), font=reg_font)
            row_y += 24
            
        draw.line([(55, row_y + 8), (W-55, row_y + 8)], fill=(241, 245, 249), width=1)
        row_y += 18

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"LCD Diagram saved to {output_path}")

if __name__ == "__main__":
    create_lcd_diagram()
