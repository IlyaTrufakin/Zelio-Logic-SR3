import sys
import os
import time

sys.path.insert(0, os.path.abspath('tools/zeliosoft2-mcp'))
from hidden_desktop import HiddenDesktopSession
import win32gui as wg

s = HiddenDesktopSession()
exe = r"C:\Program Files (x86)\Schneider Electric\Zelio2\ZelioSoft2 V5.4.3\Zelio2.exe"
file_path = os.path.abspath("WellPump_SR3B262BD.zm2")
cmd = f'"{exe}" "{file_path}"'
print("Launching:", cmd)
info = s.launch(cmd, wait=6.0)
print("PID:", info['pid'])
time.sleep(3)
hwnds = s.find_windows_for_pid(info['pid'])
print("Windows for PID count:", len(hwnds))
for h in hwnds:
    txt = s._call(wg.GetWindowText, h)
    cls = s._call(wg.GetClassName, h)
    print(f"HWND {h}: title={txt!r}, class={cls!r}")
    if txt.startswith("ZelioSoft 2"):
        s.main_hwnd = h

if getattr(s, 'main_hwnd', None):
    print("Main HWND found:", s.main_hwnd)
    s.screenshot(s.main_hwnd, "zelio_screen.png")
    print("Screenshot saved to zelio_screen.png")

else:
    print("Main window not found yet, dumping all desktop windows:")
    all_h = s.list_windows()
    for h in all_h:
        txt = s._call(wg.GetWindowText, h)
        print(f"Desktop HWND {h}: title={txt!r}")

s.close()
