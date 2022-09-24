"""https://stackoverflow.com/a/52959617"""

import win32gui
from win32con import WM_GETTEXTLENGTH, WM_GETTEXT
import ctypes
import win32com.client as win32
import urllib.parse

clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'  # Valid for IE as well!

def getEditText(hwnd):
    # api returns 16 bit characters so buffer needs 1 more char for null and twice the num of chars
    buf_size = (win32gui.SendMessage(hwnd, WM_GETTEXTLENGTH, 0, 0) + 1) * 2
    target_buff = ctypes.create_string_buffer(buf_size)
    win32gui.SendMessage(hwnd, WM_GETTEXT, buf_size,
                         ctypes.addressof(target_buff))
    # remove the null char on the end
    return target_buff.raw.decode('utf16')[:-1]


def _normaliseText(controlText):
    '''Remove '&' characters, and lower case.
    Useful for matching control text.'''
    return controlText.lower().replace('&', '')


def _windowEnumerationHandler(hwnd, resultList):
    '''Pass to win32gui.EnumWindows() to generate list of window handle,
    window text, window class tuples.'''
    resultList.append((hwnd, win32gui.GetWindowText(hwnd),
                      win32gui.GetClassName(hwnd)))


def searchChildWindows(currentHwnd,
                       wantedText=None,
                       wantedClass=None,
                       selectionFunction=None):
    results = []
    childWindows = []
    try:
        win32gui.EnumChildWindows(currentHwnd,
                                  _windowEnumerationHandler,
                                  childWindows)
    except win32gui.error:
        # This seems to mean that the control *cannot* have child windows,
        # i.e. not a container.
        return
    for childHwnd, windowText, windowClass in childWindows:
        descendentMatchingHwnds = searchChildWindows(childHwnd)
        if descendentMatchingHwnds:
            results += descendentMatchingHwnds

        if wantedText and \
                not _normaliseText(wantedText) in _normaliseText(windowText):
            continue
        if wantedClass and \
                not windowClass == wantedClass:
            continue
        if selectionFunction and \
                not selectionFunction(childHwnd):
            continue
        results.append(childHwnd)
    return results


def get_current_explorer_path() -> str:
    global clsid
    address_1 = ""
    files = []
    shellwindows = win32.Dispatch(clsid)
    w = win32gui
    window = w.GetForegroundWindow()
    #print("window: %s" % window)
    if (window != 0):
        if (w.GetClassName(window) == 'CabinetWClass'):  # the main explorer window
            #print("class: %s" % w.GetClassName(window))
            #print("text: %s " %w.GetWindowText(window))
            children = list(set(searchChildWindows(window)))
            addr_edit = None
            file_view = None
            for child in children:
                if (w.GetClassName(child) == 'WorkerW'):  # the address bar
                    addr_children = list(set(searchChildWindows(child)))
                    for addr_child in addr_children:
                        if (w.GetClassName(addr_child) == 'ReBarWindow32'):
                            addr_edit = addr_child
                            addr_children = list(
                                set(searchChildWindows(child)))
                            for addr_child in addr_children:
                                if (w.GetClassName(addr_child) == 'Address Band Root'):
                                    addr_edit = addr_child
                                    addr_children = list(
                                        set(searchChildWindows(child)))
                                    for addr_child in addr_children:
                                        if (w.GetClassName(addr_child) == 'msctls_progress32'):
                                            addr_edit = addr_child
                                            addr_children = list(
                                                set(searchChildWindows(child)))
                                            for addr_child in addr_children:
                                                if (w.GetClassName(addr_child) == 'Breadcrumb Parent'):
                                                    addr_edit = addr_child
                                                    addr_children = list(
                                                        set(searchChildWindows(child)))
                                                    for addr_child in addr_children:
                                                        if (w.GetClassName(addr_child) == 'ToolbarWindow32'):
                                                            text = getEditText(
                                                                addr_child)
                                                            if "\\" in text:
                                                                address_1 = getEditText(addr_child)[
                                                                    text.index(" ")+1:]
                                                                print(
                                                                    "Address --> "+address_1)

    window_URL = urllib.parse.unquote(
        shellwindows[0].LocationURL, encoding='ISO 8859-1')
    window_dir = window_URL.split("///")[1].replace("/", "\\")
    return window_dir
