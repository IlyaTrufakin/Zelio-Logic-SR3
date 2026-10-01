"""Updated generator for Well Pump Automation program (.zm2) for Zelio Logic SR3.
Includes:
1. Pressure sensor NO connected to Input 1 (I1):
   - P < 2 bar: contact OPEN (I1 = 0) -> calls for pump via /I1.
   - P >= 3 bar: contact CLOSED (I1 = 1) -> pump stops.
2. External forced start & reset button connected to Input 2 (I2):
   - Pressing I2 resets alarm latch M2.
3. Selector switch connected to Input 3 (I3):
   - I3 = 0 (No signal): SHORT timeout mode (4 minutes / 240s) for standard home use.
   - I3 = 1 (Signal present): LONG timeout mode (90 minutes) for garden irrigation, bath, heavy use.
4. Output 1 (Q1): Solid State Relay (SSR) controlling pump motor.
5. Output 2 (Q2): Pump running lamp (Q2 = Q1, lights up when pump is running).
6. Hysteresis in seconds:
   - T1 = 3.0s (On-delay filter: anti-chatter / water hammer debounce).
   - T2 = 5.0s (Off-delay filter: pressure stabilization & tank top-up).
   - T4 = 30.0s (Anti-cycling min pause between pump starts).
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path("tools/zeliosoft2-mcp").resolve()))
from zm2builder import ZM2Builder

def build_pump_program(output_file: str = "WellPump_SR3B262BD.zm2"):
    template_path = Path("tools/zeliosoft2-mcp/templates/SR2B201BD.zm2")
    builder = ZM2Builder(template_path)

    # =========================================================================
    # 1. АВТОМАТИЧЕСКИЙ РЕЖИМ (ДАТЧИК НО НА ВХОДЕ I1)
    # Датчик НО: при P < 2 бар контакт разомкнут (I1 = 0).
    # Запрос на накачку идет через инверсный контакт /I1.
    # =========================================================================

    # R1: T1 (3.0s) Задержка на включение (давление < 2 бар: /I1, нет аварии /M2, нет паузы /M5)
    builder.add_row(
        contacts=[(1, "I", 1, True), (2, "M", 2, True), (3, "M", 5, True)],
        coil=("T", 1, "command")
    )

    # R2: Включение авто-режима M1 (Set по окончании T1, если нет аварии /M2)
    builder.add_row(
        contacts=[(1, "T", 1), (2, "M", 2, True)],
        coil=("M", 1, "set")
    )

    # R3: T2 (5.0s) Задержка на выключение / докачка (давление достигло 3 бар: I1=1 при работающем M1)
    builder.add_row(
        contacts=[(1, "M", 1), (2, "I", 1)],
        coil=("T", 2, "command")
    )

    # R4: Условие сброса авто-режима: (T2 сработал ИЛИ возникла авария M2)
    # Де Морган: M12 = /T2 AND /M2 -> сброс M1 по /M12
    builder.add_row(
        contacts=[(1, "T", 2, True), (2, "M", 2, True)],
        coil=("M", 12, "direct")
    )

    # R5: Сброс авто-режима M1 (Reset по /M12)
    builder.add_row(
        contacts=[(1, "M", 12, True)],
        coil=("M", 1, "reset")
    )

    # =========================================================================
    # 2. КНОПКА ПРИНУДИТЕЛЬНОГО ПУСКА / СБРОСА АВАРИИ НА ВХОДЕ I2
    # =========================================================================

    # R6: Импульс с кнопки I2 включает принудительный пуск M3
    builder.add_row(
        contacts=[(1, "I", 2)],
        coil=("M", 3, "set")
    )

    # R7: Сброс аварии M2 кнопкой I2 (или кнопкой Z2 на панели)
    # Де Морган: M13 = /I2 AND /Z2 -> сброс аварии по /M13
    builder.add_row(
        contacts=[(1, "I", 2, True), (2, "Z", 2, True)],
        coil=("M", 13, "direct")
    )
    # R8: Сброс аварии M2 (Reset)
    builder.add_row(
        contacts=[(1, "M", 13, True)],
        coil=("M", 2, "reset")
    )

    # R9: Сброс принудительного режима M3 при наборе давления 3 бар (T2) или аварии (M2) или кнопке Z2
    # Де Морган: M11 = /T2 AND /M2 AND /Z2 -> сброс M3 по /M11
    builder.add_row(
        contacts=[(1, "T", 2, True), (2, "M", 2, True), (3, "Z", 2, True)],
        coil=("M", 11, "direct")
    )
    # R10: Сброс M3 (Reset)
    builder.add_row(
        contacts=[(1, "M", 11, True)],
        coil=("M", 3, "reset")
    )

    # =========================================================================
    # 3. ВЫХОД Q1 (ТВЕРДОТЕЛЬНОЕ РЕЛЕ НАСОСА)
    # =========================================================================

    # R11: Объединение запросов Auto (M1) ИЛИ Manual (M3):
    # Де Морган: M10 = /M1 AND /M3 (активен, когда оба выключены)
    builder.add_row(
        contacts=[(1, "M", 1, True), (2, "M", 3, True)],
        coil=("M", 10, "direct")
    )

    # R12: Выход Q1 активен, когда есть запрос (/M10) И нет аварии (/M2)
    builder.add_row(
        contacts=[(1, "M", 10, True), (2, "M", 2, True)],
        coil=("Q", 1, "direct")
    )

    # =========================================================================
    # 4. ВЫХОД Q2 (СИГНАЛЬНАЯ ЛАМПА РАБОТЫ НАСОСА)
    # =========================================================================

    # R13: Лампа работы насоса Q2 (горит строго при работающем насосе Q1)
    builder.add_row(
        contacts=[(1, "Q", 1)],
        coil=("Q", 2, "direct")
    )

    # =========================================================================
    # 5. АНТИЦИКЛИРОВАНИЕ: ЗАЩИТНАЯ ПАУЗА МЕЖДУ ПУСКАМИ (T4 = 30.0s)
    # =========================================================================

    # R14: T4 (30.0s) Таймер паузы, отсчитывает время после остановки насоса (/Q1)
    builder.add_row(
        contacts=[(1, "Q", 1, True)],
        coil=("T", 4, "command")
    )

    # R15: M5 = Блокировка повторного включения активна, пока Q1=0 и T4 еще не досчитал (/T4)
    builder.add_row(
        contacts=[(1, "Q", 1, True), (2, "T", 4, True)],
        coil=("M", 5, "direct")
    )

    # =========================================================================
    # 6. ВЫБОР ТАЙМАУТА АВАРИИ ПЕРЕКЛЮЧАТЕЛЕМ НА ВХОДЕ I3
    # I3 = 0 (нет сигнала): КОРОТКИЙ таймаут T3 = 240 сек (4 минуты, бытовой/гидробак)
    # I3 = 1 (есть сигнал): ДЛИННЫЙ таймаут C3 = 90 минут (полив / ванна)
    # =========================================================================

    # --- ВЕТКА 1: КОРОТКИЙ ТАЙМАУТ (I3 = 0) ---
    # R16: T3 (240s = 4 мин) работает при Q1=1 и I3=0 (/I3)
    builder.add_row(
        contacts=[(1, "Q", 1), (2, "I", 3, True)],
        coil=("T", 3, "command")
    )

    # R17: M16 = Сигнал срабатывания короткого таймаута T3
    builder.add_row(
        contacts=[(1, "T", 3)],
        coil=("M", 16, "direct")
    )

    # --- ВЕТКА 2: ДЛИННЫЙ ТАЙМАУТ (I3 = 1) ---
    # R18: T5 (60.0s) Минутный генератор импульсов при Q1=1 и I3=1 (переключатель включен)
    builder.add_row(
        contacts=[(1, "Q", 1), (2, "I", 3), (3, "T", 5, True)],
        coil=("T", 5, "command")
    )

    # R19: C3 +1 каждую минуту непрерывной работы в длинном режиме
    builder.add_row(
        contacts=[(1, "T", 5)],
        coil=("C", 3, "inc")
    )

    # R20: Сброс счетчика C3 при остановке насоса (/Q1)
    builder.add_row(
        contacts=[(1, "Q", 1, True)],
        coil=("C", 3, "reset")
    )

    # R21: M17 = Сигнал срабатывания длинного таймаута (C3 достиг 90 минут)
    builder.add_row(
        contacts=[(1, "C", 3)],
        coil=("M", 17, "direct")
    )

    # --- ОБЪЕДИНЕНИЕ АВАРИЙНЫХ СИГНАЛОВ ---
    # R22: M14 = /M16 AND /M17 (Де Морган: ни короткий M16, ни длинный M17 не сработал)
    builder.add_row(
        contacts=[(1, "M", 16, True), (2, "M", 17, True)],
        coil=("M", 14, "direct")
    )

    # R23: Взвод аварии M2 при срабатывании любого таймаута (Set по /M14)
    builder.add_row(
        contacts=[(1, "M", 14, True)],
        coil=("M", 2, "set")
    )

    # =========================================================================
    # 7. СТАТИСТИКА: СЧЕТЧИКИ ПУСКОВ И АВАРИЙ
    # =========================================================================

    # R24: C1 +1 при каждом включении насоса Q1
    builder.add_row(
        contacts=[(1, "Q", 1), (2, "M", 6, True)],
        coil=("C", 1, "inc")
    )
    # R25: Память фронта Q1 (Set)
    builder.add_row(
        contacts=[(1, "Q", 1)],
        coil=("M", 6, "set")
    )
    # R26: Сброс памяти фронта Q1 (Reset)
    builder.add_row(
        contacts=[(1, "Q", 1, True)],
        coil=("M", 6, "reset")
    )

    # R27: C2 +1 при возникновении аварии M2
    builder.add_row(
        contacts=[(1, "M", 2), (2, "M", 7, True)],
        coil=("C", 2, "inc")
    )
    # R28: Память фронта M2 (Set)
    builder.add_row(
        contacts=[(1, "M", 2)],
        coil=("M", 7, "set")
    )
    # R29: Сброс памяти фронта M2 (Reset)
    builder.add_row(
        contacts=[(1, "M", 2, True)],
        coil=("M", 7, "reset")
    )

    # =========================================================================
    # 8. УСТАВКИ ТАЙМЕРОВ И СЧЕТЧИКОВ
    # =========================================================================
    builder.set_timer_preset(1, 3.0)     # T1 = 3.0 с (Задержка включения / антидребезг в секундах)
    builder.set_timer_preset(2, 5.0)     # T2 = 5.0 с (Задержка выключения / докачка бака в секундах)
    builder.set_timer_preset(3, 240.0)   # T3 = 240.0 с (КОРОТКИЙ ТАЙМАУТ: 4 минуты при I3=0)
    builder.set_timer_preset(4, 30.0)    # T4 = 30.0 с (Антициклирование / пауза между пусками)
    builder.set_timer_preset(5, 60.0)    # T5 = 60.0 с (Минутный генератор для длинного режима)

    builder.set_counter_preset(1, 9999)  # C1 = Счетчик пусков насоса
    builder.set_counter_preset(2, 9999)  # C2 = Счетчик аварий сухого хода
    builder.set_counter_preset(3, 90)    # C3 = ДЛИННЫЙ ТАЙМАУТ: 90 минут при I3=1 (Полив / Ванна)

    out_path = builder.save(output_file)
    print(f"Program generated successfully: {out_path.resolve()} ({out_path.stat().st_size} bytes)")
    return out_path

if __name__ == "__main__":
    build_pump_program()
