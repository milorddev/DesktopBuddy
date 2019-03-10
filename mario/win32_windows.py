import win32con
import win32gui
import win32api
import win32process
from tkinter import *
from multiprocessing.dummy import Pool as ThreadPool 

def get_windows():

    def cleanupList(windows):
        result = []
        for i in windows:
            if i['process'] == "" or not i['visible'] == 1:
                continue
            else:
                result.append(i)
        return result
    
    def sort_windows(windows):
        global firstOne
        sorted_windows = []
        # Find the first entry
        '''
        for window in windows:
            if window["hwnd_above"] == 0:
                sorted_windows.append(window)
                break
        '''
        if firstOne:
            sorted_windows.append(firstOne)
        else:
            raise(IndexError("Could not find first entry"))

        # Follow the trail
        #genSearch = item for item in window if item['hwnd_above'] == sorted_windows[-1]["hwnd"]
        
        while True:
            for window in windows:
                if sorted_windows[-1]["hwnd"] == window["hwnd_above"]:
                    sorted_windows.append(window)
                    break
            else:
                break
        
        return sorted_windows

    def isRealWindow(hWnd):
        #Return True if given window is a real Windows application window.
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

    def enum_handler(hwnd, results):
        global firstOne
        #if not isRealWindow(hWnd):
            #return
        
        window_placement = win32gui.GetWindowPlacement(hwnd)
        rect = win32gui.GetWindowRect(hwnd) #(left, top, right, bottom)
        process = win32gui.GetWindowText(hwnd)
        visible = win32gui.IsWindowVisible(hwnd) == 1
        obj = {
            "hwnd":hwnd,
            "hwnd_above":win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV), # Window handle to above window
            "process":process,
            "visible":visible,
            "minimized":window_placement[1] == win32con.SW_SHOWMINIMIZED,
            "maximized":window_placement[1] == win32con.SW_SHOWMAXIMIZED,
            "rectangle": rect,
            "topleft": (rect[0],rect[1]-30),
            "width": (rect[2]-rect[0]) - 16,
            "height":(rect[3]-rect[1])
        }
        results.append(obj)
        if obj["hwnd_above"] == 0:
            firstOne = obj
            
    enumerated_windows = []
    win32gui.EnumWindows(enum_handler, enumerated_windows)
    return cleanupList(sort_windows(enumerated_windows)) #windows.sort(key=lambda x: x['hwnd'])



tkarray = []
def makeMask(): #just to visualize the process hits
    for i in get_windows():
        root = Tk()
        root.title(i['process'])
        frame = Frame(root, background='red', height=i['height'], width=i['width'])
        frame.pack()
        coords = {'x': i['topleft'][0], 'y':i['topleft'][1]}
        root.geometry("+" + str(coords['x']) + "+" + str(coords['y']))
        tkarray.append(root)

    pool = ThreadPool(4)
    results = pool.map(loopem, tkarray)
        

def loopem(kint):
    kint.mainloop()

#windows = get_windows()
#for window in windows:
    #print(window["process"], window["hwnd"], window["hwnd_above"])
    
