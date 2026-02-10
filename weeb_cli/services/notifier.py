import platform
import subprocess
import threading
from typing import Optional


def send_notification(title: str, message: str) -> None:
    threading.Thread(
        target=_send_notification_sync, 
        args=(title, message), 
        daemon=True
    ).start()


def _send_notification_sync(title: str, message: str) -> None:
    system = platform.system()
    
    try:
        if system == "Windows":
            _notify_windows(title, message)
        elif system == "Darwin":
            _notify_macos(title, message)
        else:
            _notify_linux(title, message)
    except Exception:
        pass


def _notify_windows(title: str, message: str) -> None:
    if _try_winotify(title, message):
        return
    
    if _try_win10toast(title, message):
        return
    
    _try_powershell(title, message)


def _try_winotify(title: str, message: str) -> bool:
    try:
        from winotify import Notification, audio
        toast = Notification(
            app_id="Weeb CLI",
            title=title,
            msg=message,
            duration="short"
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
        return True
    except ImportError:
        return False


def _try_win10toast(title: str, message: str) -> bool:
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=3, threaded=True)
        return True
    except ImportError:
        return False


def _try_powershell(title: str, message: str) -> None:
    try:
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $textNodes = $template.GetElementsByTagName("text")
        $textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) | Out-Null
        $textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) | Out-Null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Weeb CLI").Show($toast)
        '''
        subprocess.run(
            ["powershell", "-Command", ps_script], 
            capture_output=True, 
            timeout=5
        )
    except Exception:
        pass


def _notify_macos(title: str, message: str) -> None:
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def _notify_linux(title: str, message: str) -> None:
    subprocess.run(["notify-send", title, message], capture_output=True)

