import platform
import subprocess
import threading

def send_notification(title: str, message: str):
    threading.Thread(target=_send_notification_sync, args=(title, message), daemon=True).start()

def _send_notification_sync(title: str, message: str):
    system = platform.system()
    
    try:
        if system == "Windows":
            _notify_windows(title, message)
        elif system == "Darwin":
            _notify_macos(title, message)
        else:
            _notify_linux(title, message)
    except:
        pass

def _notify_windows(title: str, message: str):
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5, threaded=True)
        return
    except ImportError:
        pass
    
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
    except:
        pass

def _notify_macos(title: str, message: str):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)

def _notify_linux(title: str, message: str):
    subprocess.run(["notify-send", title, message], capture_output=True)
