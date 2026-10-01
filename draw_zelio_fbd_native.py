"""Generates an authentic, pixel-perfect ZelioSoft 2 native FBD editor screenshot
with crystal-clear, color-coded, labeled wiring and zero collisions.
Explicitly labels all input/output pins (I1, O1, SET, RESET, Q) so it is 100% obvious
where to connect every single wire in ZelioSoft 2.
"""
from PIL import Image, ImageDraw, ImageFont

def create_native_zelio_fbd_screenshot(output_path: str = "zelio_pump_fbd_native.png"):
    W, H = 2100, 1380
    img = Image.new("RGB", (W, H), (235, 238, 242))
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        title_font = ImageFont.truetype("segoeui.ttf", 16)
        menu_font = ImageFont.truetype("segoeui.ttf", 15)
        bold_font = ImageFont.truetype("arialbd.ttf", 15)
        block_hdr_font = ImageFont.truetype("arialbd.ttf", 14)
        block_sub_font = ImageFont.truetype("arialbd.ttf", 12)
        param_font = ImageFont.truetype("consolab.ttf", 13)
        lbl_font = ImageFont.truetype("arialbd.ttf", 13)
        reg_font = ImageFont.truetype("arial.ttf", 13)
        small_font = ImageFont.truetype("arial.ttf", 11)
        wire_tag_font = ImageFont.truetype("arialbd.ttf", 12)
        tab_font = ImageFont.truetype("arialbd.ttf", 15)
        logo_font = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        title_font = menu_font = bold_font = block_hdr_font = block_sub_font = param_font = lbl_font = reg_font = small_font = wire_tag_font = tab_font = logo_font = ImageFont.load_default()

    # 1. WINDOW TITLE BAR
    draw.rectangle([0, 0, W, 36], fill=(255, 255, 255))
    draw.line([(0, 36), (W, 36)], fill=(210, 215, 222), width=1)
    draw.rectangle([10, 8, 28, 26], fill=(16, 185, 129))
    draw.text((15, 9), "Z", fill=(255, 255, 255), font=bold_font)
    draw.text((36, 8), "ZelioSoft 2 - [WellPump_FBD_SR3B262BD.zm2 - Edit] — Понятная схема соединений", fill=(15, 23, 42), font=title_font)
    draw.text((W-110, 6), "—   ▢   ✕", fill=(71, 85, 105), font=title_font)

    # 2. MENU BAR
    draw.rectangle([0, 37, W, 68], fill=(245, 247, 250))
    draw.line([(0, 68), (W, 68)], fill=(218, 222, 229), width=1)
    menus = ["File", "Edit", "Mode", "Module", "Zelio2 COM", "Transfer", "Options", "Display", "Directories", "Tools", "Draw", "Window", "?"]
    mx = 14
    for m in menus:
        draw.text((mx, 44), m, fill=(30, 41, 59), font=menu_font)
        mx += int(draw.textlength(m, font=menu_font)) + 18

    # 3. TOP TOOLBAR
    draw.rectangle([0, 69, W, 122], fill=(225, 232, 240))
    draw.line([(0, 122), (W, 122)], fill=(180, 195, 210), width=2)

    def draw_tool_btn(bx, by, icon_type):
        draw.rounded_rectangle([bx, by, bx+34, by+34], radius=4, fill=(240, 244, 248), outline=(180, 195, 210), width=1)
        if icon_type == "new":
            draw.rectangle([bx+10, by+8, bx+24, by+26], fill=(255, 255, 255), outline=(100, 116, 139))
        elif icon_type == "open":
            draw.rectangle([bx+8, by+12, bx+26, by+24], fill=(245, 158, 11), outline=(217, 119, 6))
        elif icon_type == "save":
            draw.rectangle([bx+9, by+9, bx+25, by+25], fill=(59, 130, 246), outline=(37, 99, 235))
            draw.rectangle([bx+13, by+9, bx+21, by+15], fill=(255, 255, 255))
        elif icon_type == "help":
            draw.ellipse([bx+8, by+8, bx+26, by+26], fill=(239, 68, 68))
            draw.text((bx+13, by+8), "?", fill=(255, 255, 255), font=bold_font)

    draw_tool_btn(12, 78, "new")
    draw_tool_btn(52, 78, "open")
    draw_tool_btn(92, 78, "save")
    draw_tool_btn(142, 78, "help")

    # Zoom dropdown
    draw.rounded_rectangle([195, 82, 275, 110], radius=3, fill=(255, 255, 255), outline=(180, 195, 210), width=1)
    draw.text((205, 87), "100%", fill=(15, 23, 42), font=menu_font)
    draw.polygon([(260, 93), (268, 93), (264, 99)], fill=(71, 85, 105))

    draw.text((330, 78), "EDIT MODE", fill=(0, 110, 190), font=logo_font)
    draw.rounded_rectangle([520, 80, 554, 112], radius=4, fill=(255, 245, 230), outline=(230, 150, 50), width=1)
    draw.line([(527, 105), (547, 85)], fill=(200, 100, 20), width=3)
    draw.rounded_rectangle([564, 80, 598, 112], radius=4, fill=(240, 244, 248), outline=(180, 195, 210), width=1)
    draw.text((574, 86), "S", fill=(30, 41, 59), font=bold_font)

    # 4. BOTTOM BAR & TABS
    bar_y = H - 90
    draw.rectangle([0, bar_y, W, H], fill=(15, 65, 125))

    tabs = ["IN", "FBD", "SFC", "LOGIC", "OUT", "AFB"]
    tx = 25
    for i, t in enumerate(tabs):
        active = (t == "FBD")
        bg_col = (255, 255, 255) if active else (240, 245, 252)
        txt_col = (15, 65, 125) if active else (30, 41, 59)
        draw.rounded_rectangle([tx, bar_y + 12, tx + 95, bar_y + 44], radius=4, fill=bg_col)
        draw.text((tx + 47 - draw.textlength(t, font=tab_font)//2, bar_y + 18), t, fill=txt_col, font=tab_font)
        tx += 110

    stat_y = H - 38
    draw.rectangle([0, stat_y, W, H], fill=(10, 45, 90))
    draw.rectangle([20, stat_y + 4, 60, stat_y + 32], fill=(20, 55, 105), outline=(50, 100, 170))
    draw.line([(28, stat_y + 12), (52, stat_y + 12)], fill=(255, 255, 255), width=2)
    draw.line([(28, stat_y + 24), (52, stat_y + 24)], fill=(255, 255, 255), width=2)
    draw.text((75, stat_y + 9), "Ready", fill=(200, 220, 245), font=reg_font)

    draw.rounded_rectangle([W - 190, stat_y + 5, W - 20, stat_y + 31], radius=3, fill=(18, 52, 98), outline=(60, 110, 180), width=1)
    draw.text((W - 170, stat_y + 8), "SR3 B262BD", fill=(255, 255, 255), font=bold_font)

    # 5. CANVAS
    canvas_x = 24
    canvas_y = 138
    canvas_w = W - 48
    canvas_h = bar_y - canvas_y - 14

    draw.rectangle([canvas_x, canvas_y, canvas_x + canvas_w, canvas_y + canvas_h], fill=(255, 255, 255), outline=(0, 0, 0), width=2)

    in_rail_w = 90
    draw.rectangle([canvas_x, canvas_y, canvas_x + in_rail_w, canvas_y + canvas_h], fill=(245, 247, 250), outline=(210, 215, 222), width=1)

    out_rail_w = 90
    draw.rectangle([canvas_x + canvas_w - out_rail_w, canvas_y, canvas_x + canvas_w, canvas_y + canvas_h], fill=(245, 247, 250), outline=(210, 215, 222), width=1)

    # Input drawers
    inputs_pos = {}
    def draw_zelio_input(idx_num, y_center, label, full_title, is_switch=False):
        iy = y_center - 24
        ix = canvas_x + 12
        draw.rectangle([ix, iy, ix + 65, iy + 48], fill=(230, 235, 242), outline=(30, 41, 59), width=1)
        draw.text((ix + 4, iy + 14), label, fill=(15, 23, 42), font=bold_font)
        if not is_switch:
            draw.rectangle([ix + 32, iy + 8, ix + 56, iy + 40], fill=(255, 255, 255), outline=(100, 116, 139))
            draw.ellipse([ix + 37, iy + 14, ix + 51, iy + 34], fill=(250, 204, 21), outline=(202, 138, 4), width=2)
        else:
            draw.rectangle([ix + 32, iy + 8, ix + 56, iy + 40], fill=(255, 255, 255), outline=(100, 116, 139))
            draw.rectangle([ix + 38, iy + 12, ix + 50, iy + 26], fill=(59, 130, 246), outline=(37, 99, 235))

        tx = canvas_x + in_rail_w
        ty = y_center
        draw.polygon([(tx - 6, ty - 6), (tx, ty), (tx - 6, ty + 6)], fill=(0, 0, 0))
        draw.text((tx + 10, ty - 24), full_title, fill=(71, 85, 105), font=small_font)
        inputs_pos[label] = (tx, ty)
        return (tx, ty)

    p_i1 = draw_zelio_input(1, 230, "I1", "Датчик (НО, 2..3 бар)")
    p_i2 = draw_zelio_input(2, 430, "I2", "Кнопка Пуск / Сброс аварии")
    p_i3 = draw_zelio_input(3, 760, "I3", "Тумблер таймаута (0=4мин, 1=90мин)", is_switch=True)

    for idx, iy in [(4, 960), (5, 1080)]:
        draw.rectangle([canvas_x + 12, iy - 20, canvas_x + 77, iy + 20], fill=(240, 244, 248), outline=(200, 210, 220))
        draw.text((canvas_x + 18, iy - 10), f"I{idx}", fill=(160, 175, 190), font=bold_font)

    # Output drawers
    outputs_pos = {}
    def draw_zelio_output(idx_num, y_center, label, full_title):
        iy = y_center - 24
        ix = canvas_x + canvas_w - out_rail_w + 12
        draw.rectangle([ix, iy, ix + 65, iy + 48], fill=(230, 235, 242), outline=(30, 41, 59), width=1)
        draw.text((ix + 35, iy + 14), label, fill=(15, 23, 42), font=bold_font)
        draw.rectangle([ix + 8, iy + 12, ix + 28, iy + 36], fill=(255, 255, 255), outline=(37, 99, 235), width=2)
        tx = canvas_x + canvas_w - out_rail_w
        ty = y_center
        draw.polygon([(tx + 6, ty - 6), (tx, ty), (tx + 6, ty + 6)], fill=(0, 0, 0))
        draw.text((tx - draw.textlength(full_title, font=small_font) - 12, ty - 18), full_title, fill=(71, 85, 105), font=small_font)
        outputs_pos[label] = (tx, ty)
        return (tx, ty)

    p_q1 = draw_zelio_output(1, 270, "Q1", "Твердотельное реле (ТТР) насоса")
    p_q2 = draw_zelio_output(2, 400, "Q2", "Сигнальная лампа работы насоса")
    p_lcd = draw_zelio_output(3, 910, "LCD", "Подсветка экрана при аварии")

    # 6. DRAW ZELIOSOFT FBD BLOCKS WITH EXPLICIT PIN LABELS

    # Bistable
    def draw_zelio_bistable(x, y, b_id, title_comment=""):
        bw, bh = 84, 88
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=bold_font)
        if title_comment:
            draw.text((x - 10, y + bh + 4), title_comment, fill=(100, 116, 139), font=small_font)

        draw.text((x + 10, y + 10), "SET", fill=(0, 80, 180), font=block_hdr_font)
        draw.text((x + 52, y + 36), "Q", fill=(0, 80, 180), font=block_hdr_font)
        draw.text((x + 10, y + 60), "RESET", fill=(0, 80, 180), font=block_sub_font)

        draw.polygon([(x - 6, y + 18 - 5), (x, y + 18), (x - 6, y + 18 + 5)], fill=(0, 0, 0))
        draw.polygon([(x - 6, y + 68 - 5), (x, y + 68), (x - 6, y + 68 + 5)], fill=(0, 0, 0))
        draw.polygon([(x + bw, y + 44 - 5), (x + bw + 6, y + 44), (x + bw, y + 44 + 5)], fill=(0, 0, 0))

        return {
            "set": (x, y + 18),
            "reset": (x, y + 68),
            "q": (x + bw + 6, y + 44)
        }

    # Timer A+C with explicit I1 (Top) and O1 (Top)
    def draw_zelio_timer_ac(x, y, b_id, ta_str, tb_str="", title_comment=""):
        bw, bh = 94, 110
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=bold_font)
        if title_comment:
            draw.text((x - 15, y + bh + 4), title_comment, fill=(100, 116, 139), font=small_font)

        draw.line([(x + 14, y + 26), (x + 30, y + 26), (x + 30, y + 14), (x + 64, y + 14), (x + 64, y + 26), (x + 80, y + 26)], fill=(0, 100, 200), width=2)
        draw.line([(x + 30, y + 10), (x + 30, y + 32)], fill=(220, 38, 38), width=1)
        draw.line([(x + 64, y + 10), (x + 64, y + 32)], fill=(220, 38, 38), width=1)

        draw.text((x + 12, y + 34), "TIMER A+C", fill=(0, 80, 180), font=small_font)
        if tb_str:
            draw.text((x + 10, y + 54), f"Ta={ta_str}", fill=(15, 23, 42), font=param_font)
            draw.text((x + 10, y + 74), f"Tb={tb_str}", fill=(15, 23, 42), font=param_font)
        else:
            draw.text((x + 10, y + 62), f"Ta={ta_str}", fill=(15, 23, 42), font=param_font)

        # Draw green triangles
        for gy in [y + 20, y + 42, y + 64, y + 86]:
            draw.polygon([(x + bw - 1, gy - 4), (x + bw + 6, gy), (x + bw - 1, gy + 4)], fill=(16, 185, 129))

        # Explicit Labels
        draw.text((x + 6, y + 12), "I1", fill=(30, 41, 59), font=small_font)
        draw.text((x + bw - 22, y + 12), "O1", fill=(16, 185, 129), font=small_font)

        # Input arrows
        draw.polygon([(x - 6, y + 20 - 5), (x, y + 20), (x - 6, y + 20 + 5)], fill=(0, 0, 0))
        draw.polygon([(x - 6, y + 46 - 4), (x, y + 46), (x - 6, y + 46 + 4)], fill=(180, 190, 200)) # I2 unused

        # Output arrow
        draw.polygon([(x + bw + 6, y + 20 - 5), (x + bw + 12, y + 20), (x + bw + 6, y + 20 + 5)], fill=(0, 0, 0))

        return {
            "cmd": (x, y + 20),
            "out": (x + bw + 12, y + 20)
        }

    # Timer Li
    def draw_zelio_timer_li(x, y, b_id, title_comment=""):
        bw, bh = 94, 102
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=bold_font)
        if title_comment:
            draw.text((x - 15, y + bh + 4), title_comment, fill=(100, 116, 139), font=small_font)

        draw.line([(x+14, y+28), (x+26, y+28), (x+26, y+14), (x+46, y+14), (x+46, y+28), (x+66, y+28), (x+66, y+14), (x+80, y+14)], fill=(0, 100, 200), width=2)
        draw.text((x + 16, y + 36), "TIMER Li", fill=(0, 80, 180), font=small_font)
        draw.text((x + 12, y + 62), "T = 60 s", fill=(15, 23, 42), font=param_font)

        for gy in [y + 20, y + 42, y + 64, y + 86]:
            draw.polygon([(x + bw - 1, gy - 4), (x + bw + 6, gy), (x + bw - 1, gy + 4)], fill=(16, 185, 129))

        draw.text((x + 6, y + 12), "I1", fill=(30, 41, 59), font=small_font)
        draw.text((x + bw - 22, y + 12), "O1", fill=(16, 185, 129), font=small_font)

        draw.polygon([(x - 6, y + 20 - 5), (x, y + 20), (x - 6, y + 20 + 5)], fill=(0, 0, 0))
        draw.polygon([(x + bw + 6, y + 20 - 5), (x + bw + 12, y + 20), (x + bw + 6, y + 20 + 5)], fill=(0, 0, 0))

        return {"cmd": (x, y + 20), "out": (x + bw + 12, y + 20)}

    # Preset Counter
    def draw_zelio_counter(x, y, b_id, preset_val, title_comment=""):
        bw, bh = 94, 106
        draw.rectangle([x, y, x + bw, y + bh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        draw.text((x + 10, y - 18), b_id, fill=(0, 0, 0), font=bold_font)
        if title_comment:
            draw.text((x - 15, y + bh + 4), title_comment, fill=(100, 116, 139), font=small_font)

        draw.rectangle([x + 12, y + 14, x + 76, y + 36], fill=(240, 245, 250), outline=(100, 116, 139))
        draw.text((x + 16, y + 18), f"N={preset_val}", fill=(0, 80, 180), font=bold_font)
        draw.text((x + 10, y + 42), "PRESET CNT", fill=(0, 0, 0), font=small_font)

        draw.text((x + 10, y + 62), "I1(Pulse)", fill=(71, 85, 105), font=small_font)
        draw.text((x + 10, y + 84), "I3(Reset)", fill=(71, 85, 105), font=small_font)
        draw.text((x + bw - 20, y + 28), "O1", fill=(16, 185, 129), font=small_font)

        draw.polygon([(x - 6, y + 68 - 4), (x, y + 68), (x - 6, y + 68 + 4)], fill=(0, 0, 0))
        draw.polygon([(x - 6, y + 90 - 4), (x, y + 90), (x - 6, y + 90 + 4)], fill=(0, 0, 0))
        draw.polygon([(x + bw, y + 46 - 4), (x + bw + 6, y + 46), (x + bw, y + 46 + 4)], fill=(0, 0, 0))

        return {"pulse": (x, y + 68), "reset": (x, y + 90), "out": (x + bw + 6, y + 46)}

    # Logic Gate
    def draw_zelio_gate(x, y, g_type, title=""):
        gw, gh = 46, 50
        draw.rectangle([x, y, x + gw, y + gh], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        if title:
            draw.text((x + 6, y - 16), title, fill=(0, 0, 0), font=small_font)

        if g_type == "NOT":
            draw.polygon([(x + 10, y + 10), (x + 30, y + 25), (x + 10, y + 40)], fill=(220, 252, 231), outline=(22, 163, 74), width=1)
            draw.text((x + 14, y + 17), "1", fill=(22, 163, 74), font=bold_font)
            draw.ellipse([x + 31, y + 22, x + 37, y + 28], fill=(255, 255, 255), outline=(22, 163, 74), width=1)
            draw.text((x + 10, y + gh + 2), "NOT", fill=(0, 0, 0), font=small_font)
            in_pts = [(x, y + 25)]
            out_pt = (x + gw + 6, y + 25)
            draw.polygon([(x - 6, y + 25 - 4), (x, y + 25), (x - 6, y + 25 + 4)], fill=(0, 0, 0))
            draw.polygon([(x + gw, y + 25 - 4), (x + gw + 6, y + 25), (x + gw, y + 25 + 4)], fill=(0, 0, 0))
        elif g_type == "AND":
            draw.text((x + 17, y + 12), "&", fill=(0, 80, 180), font=bold_font)
            draw.text((x + 11, y + gh + 2), "AND", fill=(0, 0, 0), font=small_font)
            in_pts = [(x, y + 16), (x, y + 34)]
            out_pt = (x + gw + 6, y + 25)
            draw.polygon([(x - 6, y + 16 - 4), (x, y + 16), (x - 6, y + 16 + 4)], fill=(0, 0, 0))
            draw.polygon([(x - 6, y + 34 - 4), (x, y + 34), (x - 6, y + 34 + 4)], fill=(0, 0, 0))
            draw.polygon([(x + gw, y + 25 - 4), (x + gw + 6, y + 25), (x + gw, y + 25 + 4)], fill=(0, 0, 0))
        elif g_type == "OR":
            draw.text((x + 9, y + 12), "≥1", fill=(0, 80, 180), font=bold_font)
            draw.text((x + 13, y + gh + 2), "OR", fill=(0, 0, 0), font=small_font)
            in_pts = [(x, y + 16), (x, y + 34)]
            out_pt = (x + gw + 6, y + 25)
            draw.polygon([(x - 6, y + 16 - 4), (x, y + 16), (x - 6, y + 16 + 4)], fill=(0, 0, 0))
            draw.polygon([(x - 6, y + 34 - 4), (x, y + 34), (x - 6, y + 34 + 4)], fill=(0, 0, 0))
            draw.polygon([(x + gw, y + 25 - 4), (x + gw + 6, y + 25), (x + gw, y + 25 + 4)], fill=(0, 0, 0))

        return {"in": in_pts, "out": out_pt}

    # COLOR-CODED WIRE HELPER WITH BRIDGE WHITE HALO
    def draw_color_wire(pts, color=(0, 0, 0), width=2, dot_start=False, dot_end=False, tag=""):
        # First draw white underlay to cleanly separate from any crossing wires
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(255, 255, 255), width=width+4)
        # Then draw colored wire
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=width)
        if dot_start:
            x, y = pts[0]
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=color)
        if dot_end:
            x, y = pts[-1]
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=color)
        if tag and len(pts) >= 2:
            # Place tag text along the first horizontal segment
            tx = (pts[0][0] + pts[1][0]) // 2 - draw.textlength(tag, font=wire_tag_font) // 2
            ty = pts[0][1] - 16
            draw.rounded_rectangle([tx - 4, ty - 2, tx + draw.textlength(tag, font=wire_tag_font) + 4, ty + 16], radius=3, fill=(255, 255, 255), outline=color, width=1)
            draw.text((tx, ty), tag, fill=color, font=wire_tag_font)

    # --- PLACE ALL BLOCKS ON CANVAS (GENEROUS SPACING) ---

    # Color Palette for Signals
    C_BLUE = (2, 132, 199)    # Pressure signal / Hysteresis
    C_ORANGE = (217, 119, 6)  # I2 Push button / Reset
    C_GREEN = (22, 163, 74)   # Pump Running Q1 / Q2
    C_PURPLE = (124, 58, 237) # I3 Timeout mode selector
    C_RED = (220, 38, 38)     # Alarm & Lockout

    # 1. NOT gate after I1
    g_not_i1 = draw_zelio_gate(270, 206, "NOT", title="B000")
    # 2. B001 Timer A/C (Hysteresis 3s / 5s)
    b01 = draw_zelio_timer_ac(380, 184, "B001", "3.0 s", "5.0 s", "Фильтр гистерезиса")

    # 3. Logic gates before B002
    g_or_start = draw_zelio_gate(590, 218, "OR")
    g_not_alarm = draw_zelio_gate(590, 130, "NOT", title="Защита")
    g_and_start = draw_zelio_gate(710, 218, "AND")

    g_not_stop = draw_zelio_gate(590, 320, "NOT")
    g_or_stop = draw_zelio_gate(710, 320, "OR")

    # 4. B002 Bistable (Main pump latch)
    b02 = draw_zelio_bistable(830, 236, "B002", "Главный триггер насоса")

    # --- DUAL TIMEOUT BLOCK (B003, B004, B006) ---
    draw.rounded_rectangle([220, 540, 1260, 930], radius=8, fill=(250, 252, 255), outline=(180, 200, 225), width=1)
    draw.text((410, 550), "БЛОК ЗАЩИТЫ ОТ СУХОГО ХОДА И ПОРЫВА ТРУБЫ (ТАЙМАУТ ПО I3)", fill=(30, 60, 120), font=bold_font)

    # Short timeout branch (I3=0)
    g_not_i3 = draw_zelio_gate(310, 600, "NOT")
    g_and_short = draw_zelio_gate(440, 600, "AND")
    b03 = draw_zelio_timer_ac(570, 580, "B003", "240.0 s", title_comment="Короткий таймаут (4 мин)")

    # Long timeout branch (I3=1)
    g_and_long = draw_zelio_gate(440, 750, "AND")
    b04 = draw_zelio_timer_li(570, 730, "B004", "Минутный генератор (60с)")
    g_not_cnt_rst = draw_zelio_gate(740, 810, "NOT")
    b06 = draw_zelio_counter(850, 730, "B006", "90", "Счетчик полива (90 мин)")

    # OR gate for Alarm trigger
    g_or_alarm = draw_zelio_gate(1100, 660, "OR")

    # B005 Bistable (Alarm latch)
    b05 = draw_zelio_bistable(1320, 646, "B005", "Триггер Аварии сухого хода")

    # --- WIRE CONNECTIONS WITH DEDICATED TRACKS & COLORS ---

    # 1. BLUE: I1 -> NOT -> B001 Cmd (I1 pin)
    draw_color_wire([p_i1, g_not_i1["in"][0]], color=C_BLUE, width=2)
    draw_color_wire([g_not_i1["out"], b01["cmd"]], color=C_BLUE, width=2)

    # 2. BLUE: B001 Out (O1 pin) -> OR start & NOT stop
    b01_split_x = 520
    draw_color_wire([b01["out"], (b01_split_x, b01["out"][1])], color=C_BLUE, width=2)
    draw_color_wire([(b01_split_x, b01["out"][1]), (b01_split_x, g_or_start["in"][0][1]), g_or_start["in"][0]], color=C_BLUE, width=2, dot_start=True)
    draw_color_wire([(b01_split_x, b01["out"][1]), (b01_split_x, g_not_stop["in"][0][1]), g_not_stop["in"][0]], color=C_BLUE, width=2)

    # 3. ORANGE: I2 (Push button) -> OR start & down to B005 Reset
    i2_split_x = 190
    draw_color_wire([p_i2, (i2_split_x, p_i2[1])], color=C_ORANGE, width=2)
    draw_color_wire([(i2_split_x, p_i2[1]), (i2_split_x, g_or_start["in"][1][1]), g_or_start["in"][1]], color=C_ORANGE, width=2, dot_start=True)
    # Track down to bottom at y = 970 (well below everything)
    draw_color_wire([(i2_split_x, p_i2[1]), (i2_split_x, 970), (1280, 970), (1280, b05["reset"][1]), b05["reset"]], color=C_ORANGE, width=2)

    # 4. BLUE: Start path to B002 SET
    draw_color_wire([g_or_start["out"], g_and_start["in"][1]], color=C_BLUE, width=2)
    draw_color_wire([g_and_start["out"], (790, g_and_start["out"][1]), (790, b02["set"][1]), b02["set"]], color=C_BLUE, width=2)

    # 5. BLUE: Stop path to B002 RESET
    draw_color_wire([g_not_stop["out"], g_or_stop["in"][0]], color=C_BLUE, width=2)
    draw_color_wire([g_or_stop["out"], (790, g_or_stop["out"][1]), (790, b02["reset"][1]), b02["reset"]], color=C_BLUE, width=2)

    # 6. GREEN: B002 Output Q (Pump running) -> Q1, Q2, and Dual Timeout
    q_split_x = 980
    draw_color_wire([b02["q"], (q_split_x, b02["q"][1])], color=C_GREEN, width=3, tag="Насос ВКЛ")
    draw_color_wire([(q_split_x, b02["q"][1]), (q_split_x, p_q1[1]), p_q1], color=C_GREEN, width=3, dot_start=True)
    draw_color_wire([(q_split_x, b02["q"][1]), (q_split_x, p_q2[1]), p_q2], color=C_GREEN, width=3, dot_start=True)

    # Feed pump signal down into Dual-Timeout at dedicated lane x = 390
    draw_color_wire([(q_split_x, b02["q"][1]), (q_split_x, 490), (390, 490), (390, g_and_short["in"][1][1]), g_and_short["in"][1]], color=C_GREEN, width=2, dot_start=True)
    draw_color_wire([(390, 490), (390, g_and_long["in"][1][1]), g_and_long["in"][1]], color=C_GREEN, width=2, dot_start=True)

    # 7. PURPLE: I3 (Timeout mode switch)
    i3_split_x = 270
    draw_color_wire([p_i3, (i3_split_x, p_i3[1])], color=C_PURPLE, width=2, tag="Режим I3")
    draw_color_wire([(i3_split_x, p_i3[1]), (i3_split_x, g_not_i3["in"][0][1]), g_not_i3["in"][0]], color=C_PURPLE, width=2, dot_start=True)
    draw_color_wire([(i3_split_x, p_i3[1]), (i3_split_x, g_and_long["in"][0][1]), g_and_long["in"][0]], color=C_PURPLE, width=2)

    # Short branch: NOT I3 -> AND -> B003 Cmd (I1 pin)
    draw_color_wire([g_not_i3["out"], g_and_short["in"][0]], color=C_PURPLE, width=2)
    draw_color_wire([g_and_short["out"], b03["cmd"]], color=C_PURPLE, width=2)

    # Long branch: AND -> B004 Cmd (I1 pin) & NOT Reset
    draw_color_wire([g_and_long["out"], b04["cmd"]], color=C_PURPLE, width=2)
    draw_color_wire([g_and_long["out"], (510, g_and_long["out"][1]), (510, 835), g_not_cnt_rst["in"][0]], color=C_PURPLE, width=2, dot_start=True)
    draw_color_wire([g_not_cnt_rst["out"], (810, g_not_cnt_rst["out"][1]), (810, b06["reset"][1]), b06["reset"]], color=C_PURPLE, width=2)

    # B004 Out (O1 pin) -> B006 Pulse (I1 pin)
    draw_color_wire([b04["out"], (790, b04["out"][1]), (790, b06["pulse"][1]), b06["pulse"]], color=C_PURPLE, width=2)

    # 8. RED: Alarms from B003 Out (O1 pin) & B006 Out (O1 pin) -> OR Alarm
    draw_color_wire([b03["out"], (1040, b03["out"][1]), (1040, g_or_alarm["in"][0][1]), g_or_alarm["in"][0]], color=C_RED, width=2)
    draw_color_wire([b06["out"], (1040, b06["out"][1]), (1040, g_or_alarm["in"][1][1]), g_or_alarm["in"][1]], color=C_RED, width=2)
    draw_color_wire([g_or_alarm["out"], (1240, g_or_alarm["out"][1]), (1240, b05["set"][1]), b05["set"]], color=C_RED, width=2)

    # 9. RED: B005 Q Output (Alarm Lockout)
    alm_split_x = 1480
    draw_color_wire([b05["q"], (alm_split_x, b05["q"][1])], color=C_RED, width=3, tag="АВАРИЯ")
    # to LCD Backlight
    draw_color_wire([(alm_split_x, b05["q"][1]), (alm_split_x, p_lcd[1]), p_lcd], color=C_RED, width=3, dot_start=True)
    # up to stop pump (OR stop)
    draw_color_wire([(alm_split_x, b05["q"][1]), (alm_split_x, 370), (660, 370), (660, g_or_stop["in"][1][1]), g_or_stop["in"][1]], color=C_RED, width=2, dot_start=True)
    # up to block pump start (NOT alarm)
    draw_color_wire([(alm_split_x, 370), (alm_split_x, 155), (g_not_alarm["in"][0][0], 155), g_not_alarm["in"][0]], color=C_RED, width=2, dot_start=True)
    draw_color_wire([g_not_alarm["out"], (670, g_not_alarm["out"][1]), (670, g_and_start["in"][0][1]), g_and_start["in"][0]], color=C_RED, width=2)

    # 10. COLOR LEGEND (BOX AT BOTTOM LEFT)
    leg_x, leg_y = 60, canvas_y + canvas_h - 100
    draw.rounded_rectangle([leg_x, leg_y, leg_x + 680, leg_y + 85], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((leg_x + 15, leg_y + 8), "Цветовая маркировка цепей схемы (для безошибочного подключения):", fill=(15, 23, 42), font=bold_font)

    items = [
        (C_BLUE, "Цепь давления / пуска"),
        (C_GREEN, "Цепь насоса (Q1 / Q2)"),
        (C_ORANGE, "Кнопка I2 (Пуск/Сброс)"),
        (C_PURPLE, "Таймаут I3 (4м / 90м)"),
        (C_RED, "Сигнал Аварии (Стоп/LCD)")
    ]
    lx = leg_x + 15
    for col, txt in items:
        draw.rectangle([lx, leg_y + 40, lx + 20, leg_y + 54], fill=col)
        draw.text((lx + 26, leg_y + 38), txt, fill=(15, 23, 42), font=small_font)
        lx += int(draw.textlength(txt, font=small_font)) + 40

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Color-coded native Zelio FBD diagram saved to {output_path}")

if __name__ == "__main__":
    create_native_zelio_fbd_screenshot()
