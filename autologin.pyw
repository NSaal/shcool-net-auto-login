# Creates a task-bar icon.  Run from Python.exe to see the messages printed.
# Author : Guo
# Contact : guoqr1997@163.com
import multiprocessing
import os
import subprocess
import sys
import time
from multiprocessing import Process

import requests
import win32api
import win32con
import win32gui
import winerror

url = 'http://202.204.48.66/'
pingdress = 'www.4399.com'  # The web to test net connection


def login():
    my_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Connection': 'keep-alive',
    }
    my_data = {
        'DDDDD': 'your id here',
        'upass': 'your password here',
        # 'v6ip': '', # useless
        '0MKKey': '123456789',
    }
    a = requests.post(url, data=my_data, headers=my_headers)


def scan():
    while 1:
        state = subprocess.getstatusoutput('ping -w 500 -n 2 %s' % pingdress)
        if state[0]:
            login()
            print('login sucess')
        print('already login')
        time.sleep(5)


class MainWindow:
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated")
        message_map = {
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER+20: self.OnTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        # Don't blow up if class already registered to make testing easier
        try:
            classAtom = win32gui.RegisterClass(wc)
        except win32gui.error:  # , err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()
        self.p = Process(target=scan)
        self.p.start()

    def _DoCreateIcons(self):
        hinst = win32api.GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join(
            os.path.split(sys.executable)[0], "pyc.ico"))
        if not os.path.isfile(iconPathName):
            iconPathName = os.path.abspath(os.path.join(
                os.path.split(sys.executable)[0], "DLLs", "pyc.ico"))
        if not os.path.isfile(iconPathName):
            iconPathName = os.path.abspath(os.path.join(
                os.path.split(sys.executable)[0], "..\\PC\\pyc.ico"))
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(
                hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            print("Can't find a Python icon file - using default")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "Python Demo")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            print("Failed to add the taskbar icon - is explorer running?")
    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_RBUTTONUP:
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "退出")
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(
                menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1025:
            self.p.terminate()
            win32gui.DestroyWindow(self.hwnd)
        else:
            print("Unknown command -", id)


def main():
    w = MainWindow()
    win32gui.PumpMessages()


if __name__ == '__main__':
    main()
