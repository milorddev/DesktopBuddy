import win32con
import win32gui
import win32api
import win32process

def isRealWindow(hWnd):
    '''Return True if given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowSizes():
    '''
    Return a list of tuples (handler, (width, height)) for each real window.
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        
        pid = win32process.GetWindowThreadProcessId(hWnd)
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
        proc_name = win32process.GetModuleFileNameEx(handle, 0)
        
        rect = win32gui.GetWindowRect(hWnd)
        obj = {"process":proc_name, "rect": rect, "topleft": (rect[0],rect[1]), "width": rect[2]-rect[0]}
        #windows.append((proc_name, (rect[2] - rect[0], rect[3] - rect[1]), rect))
        #windows.append((proc_name,rect))
        windows.append(obj)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

'''
for win in getWindowSizes():
    print(win)
'''
