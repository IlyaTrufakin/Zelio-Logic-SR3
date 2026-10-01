import sys, os, time
sys.path.insert(0, os.path.abspath('tools/zeliosoft2-mcp'))
from hidden_desktop import HiddenDesktopSession
import win32gui as wg

s = HiddenDesktopSession()
exe = r"C:\Program Files (x86)\Schneider Electric\Zelio2\ZelioSoft2 V5.4.3\Zelio2.exe"
file_path = r"C:\Program Files (x86)\Schneider Electric\Zelio2\ZelioSoft2 V5.4.3\Z2User\Examples\Heating_analog_fbd.zm2"
cmd = f'"{exe}" "{file_path}"'
info = s.launch(cmd, wait=6.0)
time.sleep(3)
hwnds = s.find_windows_for_pid(info['pid'])
for h in hwnds:
    txt = s._call(wg.GetWindowText, h)
    if 'ZelioSoft 2' in txt:
        s.main_hwnd = h
        break

if getattr(s, 'main_hwnd', None):
    s.screenshot(s.main_hwnd, 'zelio_heating_fbd.png')
    print('Screenshot saved to zelio_heating_fbd.png!')

s.close()
