import sys
import os
import json
import subprocess
import importlib.util
import zipfile
import shutil
import tempfile
import hashlib
import webbrowser
from datetime import datetime

# ------------------------------------------------------------------------------
# Auto-generate files on startup
# ------------------------------------------------------------------------------
def bootstrap():
    needs_setup = not os.path.exists("browse.html") or not os.path.exists("settings.html")
    if needs_setup:
        print("[STI] First launch - generating files...")
        spec = importlib.util.spec_from_file_location("setup", "setup.py")
        if spec:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.create_dirs()
            mod.create_files()
        else:
            print("[STI] setup.py not found. Please run setup.py manually.")
            sys.exit(1)

bootstrap()

# ------------------------------------------------------------------------------
# PyQt5 imports
# ------------------------------------------------------------------------------
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QToolBar, QLineEdit, QPushButton, QLabel,
        QMenu, QAction, QFileDialog, QSizePolicy, QStatusBar,
        QDockWidget, QListWidget, QListWidgetItem, QMessageBox,
        QProgressBar, QShortcut, QSplitter, QFrame, QScrollArea,
        QSystemTrayIcon, QToolButton, QInputDialog,
        QTextEdit, QStackedWidget, QGraphicsOpacityEffect
    )
    from PyQt5.QtWebEngineWidgets import (
        QWebEngineView, QWebEnginePage, QWebEngineProfile,
        QWebEngineSettings, QWebEngineDownloadItem
    )
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtCore import (
        Qt, QUrl, QSize, QTimer, pyqtSignal, pyqtSlot,
        QObject, QPoint, QRect, QStandardPaths, QSettings, QByteArray,
        QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
        QSequentialAnimationGroup, QPauseAnimation
    )
    from PyQt5.QtGui import (
        QIcon, QFont, QColor, QPalette, QPixmap, QKeySequence,
        QFontDatabase, QCursor, QPainter, QBrush, QLinearGradient,
        QPen, QPainterPath, QImage, QRadialGradient, QConicalGradient
    )
    from PyQt5.QtNetwork import QNetworkProxy
    from PyQt5.QtSvg import QSvgRenderer
except ImportError as e:
    print(f"[STI] PyQt5 import error: {e}")
    print("[STI] Run: python setup.py")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
CONFIG_PATH   = "config.json"
BROWSE_HTML   = os.path.abspath("browse.html")
SETTINGS_HTML = os.path.abspath("settings.html")
MODS_DIR      = os.path.abspath("mods")
DOWNLOADS_DIR = os.path.abspath("downloads")
THEMES_DIR    = os.path.abspath("themes")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(THEMES_DIR, exist_ok=True)

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(cfg: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[STI] Config save error: {e}")

# ------------------------------------------------------------------------------
# SVG Icons (Microsoft Fluent Design style)
# ------------------------------------------------------------------------------
def create_svg_icon(path_data, size=20, color="#ffffff"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="{path_data}"/>
</svg>'''
    return svg

# Enhanced icon set with Microsoft Fluent Design
ICON_PATHS = {
    "back": "M15 18l-6-6 6-6",
    "forward": "M9 18l6-6-6-6",
    "reload": "M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15",
    "home": "M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z M9 22V12h6v10",
    "search": "M21 21l-4.35-4.35M11 17a6 6 0 100-12 6 6 0 000 12z",
    "mic": "M12 2a3 3 0 00-3 3v7a3 3 0 006 0V5a3 3 0 00-3-3z M19 10v2a7 7 0 01-14 0v-2 M12 19v3 M8 22h8",
    "translate": "M5 8h10M9 4v4M2 8h2M18 8h5M2 12h5M14 12h8M2 16h3M10 16h4M2 20h1M6 20h2M16 20h6M3 20l4-6 4 6",
    "reader": "M4 6h16v1H4z M4 10h16v1H4z M4 14h10v1H4z M4 18h16v1H4z",
    "bookmark": "M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z",
    "bookmark_filled": "M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z",
    "sidebar": "M4 4h16v16H4z M9 4v16",
    "ai": "M12 2a10 10 0 0110 10c0 2.5-1 4.8-2.5 6.5 M12 2a10 10 0 00-10 10c0 2.5 1 4.8 2.5 6.5 M12 2v20 M8 8l4 4-4 4 M16 8l-4 4 4 4",
    "incognito": "M12 2a10 10 0 0110 10c0 2.5-1 4.8-2.5 6.5 M12 2a10 10 0 00-10 10c0 2.5 1 4.8 2.5 6.5 M2 22l20-20",
    "menu": "M4 6h16M4 12h16M4 18h16",
    "settings": "M12 15a3 3 0 100-6 3 3 0 000 6z M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z",
    "plus": "M12 5v14M5 12h14",
    "close": "M18 6L6 18M6 6l12 12",
    "download": "M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4 M7 10l5 5 5-5 M12 15V3",
    "history": "M12 8v4l3 3M12 22a10 10 0 110-20 10 10 0 010 20z",
    "collections": "M4 4h6v6H4z M14 4h6v6h-6z M4 14h6v6H4z M14 14h6v6h-6z",
    "notes": "M16 3h5v5M14 10l6-6M10 21H5a2 2 0 01-2-2V5a2 2 0 012-2h7M15 21h4a2 2 0 002-2v-5",
    "zoom_in": "M21 21l-4.35-4.35M11 17a6 6 0 100-12 6 6 0 000 12z M11 8v6 M8 11h6",
    "zoom_out": "M21 21l-4.35-4.35M11 17a6 6 0 100-12 6 6 0 000 12z M8 11h6",
    "fullscreen": "M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3",
    "copy": "M8 4v12a2 2 0 002 2h8M16 4v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2z",
    "paste": "M20 12v6a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2m8 0h2a2 2 0 012 2v2M12 8V4M10 2h4v4h-4z",
    "star": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
    "lock": "M12 2a5 5 0 00-5 5v4H5v8h14v-8h-2V7a5 5 0 00-5-5z M12 13v3",
    "globe": "M12 2a10 10 0 0110 10 10 10 0 01-10 10 10 10 0 01-10-10 10 10 0 0110-10z M2 12h20 M12 2a15 15 0 014 10 15 15 0 01-4 10 15 15 0 01-4-10 15 15 0 014-10z",
    "cpu": "M12 4v2M12 18v2M4 12h2M18 12h2M12 8v8M8 12h8",
    "memory": "M4 4h16v16H4zM9 9h6v6H9z",
    "currency": "M3 10h18M6 6h12M6 18h12M3 14h18",
    "quote": "M10 11h-4a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2z M18 11h-4a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2z",
    "theme": "M12 2a10 10 0 0110 10 10 10 0 01-10 10 10 10 0 01-10-10 10 10 0 0110-10z M12 2a15 15 0 014 10 15 15 0 01-4 10 15 15 0 01-4-10 15 15 0 014-10z",
    "focus": "M15 3h6v6M9 3H3v6M15 21h6v-6M9 21H3v-6",
    "vpn": "M12 2a10 10 0 0110 10c0 2.5-1 4.8-2.5 6.5 M12 2a10 10 0 00-10 10c0 2.5 1 4.8 2.5 6.5 M12 22v0 M8 8l8 8 M16 8l-8 8",
    "sync": "M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15",
    "accessibility": "M12 2a10 10 0 0110 10 10 10 0 01-10 10 10 10 0 01-10-10 10 10 0 0110-10z M12 8h.01M11 12h1v4h1",
    "mods": "M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z",
    "password": "M3 11h18M9 7v4M15 7v4M5 3h14v18H5z",
    "security": "M12 2a10 10 0 0110 10 10 10 0 01-10 10 10 10 0 01-10-10 10 10 0 0110-10z M12 6v6 M12 15h.01",
    "help": "M12 22a10 10 0 110-20 10 10 0 010 20z M12 16v.01M12 12a2 2 0 100-4 2 2 0 000 4z",
    "warning": "M12 9v4M12 17h.01 M12 2L2 19h20L12 2z",
    "info": "M12 22a10 10 0 110-20 10 10 0 010 20z M12 16v-4M12 8h.01",
    "check": "M20 6L9 17l-5-5",
    "chevron_down": "M6 9l6 6 6-6",
    "chevron_left": "M15 18l-6-6 6-6",
    "chevron_right": "M9 18l6-6-6-6",
    "chevron_up": "M18 15l-6-6-6 6",
    "x": "M18 6L6 18M6 6l12 12",
    "profile": "M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2 M12 3a4 4 0 100 8 4 4 0 000-8z",
    "extensions": "M20 7l-7-4-7 4v10l7 4 7-4V7z M12 12v8",
    "share": "M18 8a3 3 0 100-6 3 3 0 000 6z M6 15a3 3 0 100-6 3 3 0 000 6z M18 22a3 3 0 100-6 3 3 0 000 6z M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98",
    "print": "M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2M6 14h12v8H6z",
    "shield": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
    "cloud": "M17.5 19H9a7 7 0 116.71-9h1.79a4.5 4.5 0 110 9z",
    "wifi": "M5 12.55a11 11 0 0114.08 0M8.53 16.11a6 6 0 016.95 0M12 20h.01",
    "bluetooth": "M6.5 6.5l11 11L12 23V1l5.5 5.5-11 11",
    "battery": "M17 6H3a2 2 0 00-2 2v8a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2z M23 10v4",
    "cast": "M2 16.1A5 5 0 015.9 20M2 12.05A9 9 0 019.95 20M2 8V6a2 2 0 012-2h16a2 2 0 012 2v12a2 2 0 01-2 2h-6 M2 20h.01",
}

def pixmap_from_svg(path_data, size=20, color="#ffffff"):
    svg = create_svg_icon(path_data, size, color)
    renderer = QSvgRenderer(QByteArray(svg.encode()))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap

# ------------------------------------------------------------------------------
# Animated Button Widget
# ------------------------------------------------------------------------------
class AnimatedButton(QPushButton):
    def __init__(self, icon_path, tooltip="", parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.setToolTip(tooltip)
        self.setFixedSize(36, 36)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._animation = None
        self._setup_animation()
        
    def _setup_animation(self):
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        
    def mousePressEvent(self, event):
        self._animate_click()
        super().mousePressEvent(event)
        
    def _animate_click(self):
        self._animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._animation.setDuration(150)
        self._animation.setStartValue(0.5)
        self._animation.setEndValue(1.0)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.start()

# ------------------------------------------------------------------------------
# QWebChannel bridge
# ------------------------------------------------------------------------------
class STIBridge(QObject):
    navigate_signal = pyqtSignal(str)
    open_settings_signal = pyqtSignal()
    open_ai_signal = pyqtSignal()
    notification_signal = pyqtSignal(str, str)
    download_offline_signal = pyqtSignal(str)

    def __init__(self, browser):
        super().__init__()
        self.browser = browser

    @pyqtSlot(str)
    def navigate(self, url: str):
        self.navigate_signal.emit(url)

    @pyqtSlot()
    def openSettings(self):
        self.open_settings_signal.emit()

    @pyqtSlot()
    def openAI(self):
        self.open_ai_signal.emit()

    @pyqtSlot(str)
    def saveConfig(self, json_str: str):
        try:
            cfg = json.loads(json_str)
            save_config(cfg)
        except Exception as e:
            print(f"[Bridge] saveConfig error: {e}")

    @pyqtSlot()
    def clearHistory(self):
        cfg = load_config()
        cfg["history"] = []
        save_config(cfg)

    @pyqtSlot()
    def clearCookies(self):
        if self.browser and self.browser.webprofile:
            self.browser.webprofile.cookieStore().deleteAllCookies()

    @pyqtSlot(str)
    def applyVPN(self, json_str: str):
        try:
            vpn = json.loads(json_str)
            if vpn.get("enabled"):
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.Socks5Proxy, "127.0.0.1", 1080))
            else:
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.NoProxy))
        except Exception as e:
            print(f"[Bridge] applyVPN error: {e}")

    @pyqtSlot(str)
    def applyCustomCSS(self, css: str):
        if self.browser and self.browser.current_view():
            script = f"""
            (function(){{
              let s = document.getElementById('sti-custom-css');
              if (!s) {{ s = document.createElement('style'); s.id = 'sti-custom-css'; document.head.appendChild(s); }}
              s.textContent = `{css.replace('`','\\`')}`;
            }})();
            """
            self.browser.current_view().page().runJavaScript(script)

    @pyqtSlot()
    def importSettings(self):
        path, _ = QFileDialog.getOpenFileName(None, "Import Settings", "", "JSON (*.json)")
        if path:
            try:
                with open(path, "r") as f:
                    imported = json.load(f)
                cfg = load_config()
                cfg.update(imported)
                save_config(cfg)
                QMessageBox.information(None, "Import", "Settings imported successfully.")
            except Exception as e:
                QMessageBox.critical(None, "Error", str(e))

    @pyqtSlot()
    def importBookmarks(self):
        path, _ = QFileDialog.getOpenFileName(None, "Import Bookmarks", "", "HTML (*.html);;JSON (*.json)")
        if path:
            QMessageBox.information(None, "Import", f"File selected: {path}")

    @pyqtSlot()
    def changeDownloadPath(self):
        cfg = load_config()
        dl_path = cfg.get("download_path", DOWNLOADS_DIR)
        path = QFileDialog.getExistingDirectory(None, "Download Folder", dl_path)
        if path:
            cfg["download_path"] = path
            save_config(cfg)
            if self.browser:
                self.browser.webprofile.setDownloadPath(path)

    @pyqtSlot()
    def installMod(self):
        path, _ = QFileDialog.getOpenFileName(None, "Install Mod", "", "ZIP (*.zip)")
        if path:
            try:
                with zipfile.ZipFile(path, "r") as z:
                    names = z.namelist()
                    manifest_path = next((n for n in names if n.endswith("manifest.json")), None)
                    if not manifest_path:
                        QMessageBox.critical(None, "Error", "manifest.json not found.")
                        return
                    with z.open(manifest_path) as mf:
                        manifest = json.load(mf)
                    mod_id = manifest.get("id", "unknown_mod")
                    dest = os.path.join(MODS_DIR, mod_id)
                    z.extractall(dest)
                    cfg = load_config()
                    if "active_mods" not in cfg:
                        cfg["active_mods"] = []
                    if mod_id not in cfg["active_mods"]:
                        cfg["active_mods"].append(mod_id)
                    save_config(cfg)
                    QMessageBox.information(None, "Mod Installed", f"Mod installed.")
            except Exception as e:
                QMessageBox.critical(None, "Error", str(e))

    @pyqtSlot()
    def openModsFolder(self):
        if sys.platform == "win32":
            os.startfile(MODS_DIR)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", MODS_DIR])
        else:
            subprocess.Popen(["xdg-open", MODS_DIR])

    @pyqtSlot()
    def syncNow(self):
        self.notification_signal.emit("Sync", "Synchronization started...")

    @pyqtSlot(str)
    def showNotification(self, title: str, message: str):
        self.notification_signal.emit(title, message)

    @pyqtSlot(str)
    def downloadOfflinePage(self, url: str):
        self.download_offline_signal.emit(url)

    @pyqtSlot(str)
    def setWeatherCity(self, city: str):
        cfg = load_config()
        cfg["weather_city"] = city
        save_config(cfg)

    @pyqtSlot(str)
    def installTheme(self, theme_data: str):
        try:
            theme = json.loads(theme_data)
            theme_id = theme.get("id", f"custom_{hashlib.md5(theme_data.encode()).hexdigest()[:8]}")
            theme_path = os.path.join(THEMES_DIR, f"{theme_id}.json")
            with open(theme_path, "w") as f:
                json.dump(theme, f)
            cfg = load_config()
            cfg["themes"] = cfg.get("themes", {})
            cfg["themes"][theme_id] = theme
            save_config(cfg)
            self.notification_signal.emit("Theme", f"Theme '{theme.get('name', theme_id)}' installed")
        except Exception as e:
            print(f"[Bridge] installTheme error: {e}")

# ------------------------------------------------------------------------------
# Custom Web Page
# ------------------------------------------------------------------------------
class STIWebPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        pass

    def createWindow(self, _type):
        if hasattr(self.parent(), "browser"):
            return self.parent().browser.add_tab().page()
        return super().createWindow(_type)

# ------------------------------------------------------------------------------
# Loading Animation Widget (Enhanced)
# ------------------------------------------------------------------------------
class LoadingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.setInterval(16)
        self.is_loading = False
        self._opacity = 0.0
        self._fade_anim = None
        
    def rotate(self):
        self.angle = (self.angle + 8) % 360
        self.update()
        
    def start(self):
        self.is_loading = True
        self.timer.start()
        self._fade_in()
        self.show()
        
    def stop(self):
        self._fade_out()
        self.timer.stop()
        
    def _fade_in(self):
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(200)
        self._fade_anim.setStartValue(self._opacity)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()
        self._opacity = 1.0
        
    def _fade_out(self):
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(200)
        self._fade_anim.setStartValue(self._opacity)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.finished.connect(lambda: self.is_loading and self.hide())
        self._fade_anim.start()
        self._opacity = 0.0
        
    def paintEvent(self, event):
        if not self.is_loading:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw gradient circle
        gradient = QConicalGradient(12, 12, -self.angle)
        gradient.setColorAt(0, QColor("#0078D4"))
        gradient.setColorAt(0.3, QColor("#00B7C3"))
        gradient.setColorAt(0.7, QColor("#0078D4"))
        gradient.setColorAt(1, QColor("#0078D4"))
        
        pen = QPen(QBrush(gradient), 2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        rect = QRect(3, 3, 18, 18)
        painter.drawArc(rect, 0, 360 * 16)

# ------------------------------------------------------------------------------
# Splash Screen (Startup Animation)
# ------------------------------------------------------------------------------
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
        
        self._opacity = 0.0
        self.setWindowOpacity(0.0)
        
        # Animation timers
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_anim.setDuration(600)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_anim.setDuration(400)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.InCubic)
        self.fade_out_anim.finished.connect(self.close)
        
        self.loading_progress = 0
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._update_progress)
        
    def show_splash(self):
        self.show()
        self.fade_in_anim.start()
        self.progress_timer.start(30)
        
    def _update_progress(self):
        self.loading_progress += 1
        if self.loading_progress >= 100:
            self.progress_timer.stop()
            QTimer.singleShot(300, self._start_fade_out)
        self.update()
        
    def _start_fade_out(self):
        self.fade_out_anim.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        bg_rect = QRect(50, 50, 300, 200)
        painter.setBrush(QColor(30, 30, 30, 240))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bg_rect, 20, 20)
        
        # Logo text
        painter.setPen(QColor("#0078D4"))
        font = QFont("Segoe UI", 32, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(50, 80, 300, 60), Qt.AlignCenter, "STI")
        
        # Subtitle
        painter.setPen(QColor("#e0e0e0"))
        font = QFont("Segoe UI", 12)
        painter.setFont(font)
        painter.drawText(QRect(50, 140, 300, 30), Qt.AlignCenter, "Browser")
        
        # Progress bar
        progress_y = 200
        progress_width = 200
        progress_x = (self.width() - progress_width) // 2
        
        # Background
        painter.setBrush(QColor(60, 60, 60))
        painter.drawRoundedRect(QRect(progress_x, progress_y, progress_width, 4), 2, 2)
        
        # Progress
        if self.loading_progress > 0:
            gradient = QLinearGradient(progress_x, 0, progress_x + progress_width, 0)
            gradient.setColorAt(0, QColor("#0078D4"))
            gradient.setColorAt(1, QColor("#00B7C3"))
            painter.setBrush(QBrush(gradient))
            current_width = int(progress_width * self.loading_progress / 100)
            painter.drawRoundedRect(QRect(progress_x, progress_y, current_width, 4), 2, 2)

# ------------------------------------------------------------------------------
# Custom Tab Bar (Microsoft Edge style with animations)
# ------------------------------------------------------------------------------
class TabWidget(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, view, index, title, parent=None):
        super().__init__(parent)
        self.view = view
        self.index = index
        self._active = False
        self._hover = False
        self._opacity = 1.0
        
        self.setFixedHeight(34)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 4, 4)
        layout.setSpacing(6)
        
        self.favicon = QLabel()
        self.favicon.setFixedSize(16, 16)
        layout.addWidget(self.favicon)
        
        self.title_lbl = QLabel(title[:30])
        self.title_lbl.setStyleSheet("color: #e8eaed; font-size: 12px;")
        layout.addWidget(self.title_lbl, 1)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.setObjectName("TabClose")
        self.close_btn.setStyleSheet("""
            QPushButton#TabClose {
                background: transparent;
                border: none;
                color: #9aa0a6;
                font-size: 14px;
                border-radius: 11px;
            }
            QPushButton#TabClose:hover {
                background: #3c3f41;
                color: #e8eaed;
            }
        """)
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.close_btn)
        
        self._setup_animation()
        
    def _setup_animation(self):
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        
    def setActive(self, active):
        self._active = active
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
        
    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self._active:
            bg_color = QColor("#3c3f41")
            self.title_lbl.setStyleSheet("color: #ffffff; font-size: 12px;")
        elif self._hover:
            bg_color = QColor("#35363a")
            self.title_lbl.setStyleSheet("color: #e8eaed; font-size: 12px;")
        else:
            bg_color = QColor(0, 0, 0, 0)
            self.title_lbl.setStyleSheet("color: #9aa0a6; font-size: 12px;")
            
        if bg_color.alpha() > 0:
            painter.setBrush(bg_color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 6, 6)

class CustomTabBar(QWidget):
    tab_clicked = pyqtSignal(int)

    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setObjectName("CustomTabBar")
        self.setFixedHeight(38)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(1)
        
        self.tabs_container = QWidget()
        self.tabs_layout = QHBoxLayout(self.tabs_container)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(1)
        
        layout.addWidget(self.tabs_container, 1)
        
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setToolTip("New Tab (Ctrl+T)")
        self.new_tab_btn.setFixedSize(28, 28)
        self.new_tab_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #9aa0a6;
                font-size: 16px;
                border-radius: 14px;
            }
            QPushButton:hover {
                background: #3c3f41;
                color: #e8eaed;
            }
        """)
        self.new_tab_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.new_tab_btn.clicked.connect(lambda: self.browser.add_tab())
        layout.addWidget(self.new_tab_btn)
        
        self.tab_widgets = []
        
    def add_tab_button(self, view, index, title):
        tab_widget = TabWidget(view, index, title)
        tab_widget.clicked.connect(lambda: self._on_tab_clicked(index))
        tab_widget.close_btn.clicked.connect(lambda: self.browser.close_tab(index))
        
        self.tabs_layout.addWidget(tab_widget)
        self.tab_widgets.append(tab_widget)
        
        return tab_widget
        
    def remove_tab_button(self, view):
        for i, widget in enumerate(self.tab_widgets):
            if widget.view == view:
                widget.deleteLater()
                self.tab_widgets.pop(i)
                break
        
        # Update indices
        for i, widget in enumerate(self.tab_widgets):
            widget.index = i
                
    def update_tab_title(self, view, title):
        for widget in self.tab_widgets:
            if widget.view == view:
                widget.title_lbl.setText(title[:30])
                break
                
    def update_tab_icon(self, view, icon):
        for widget in self.tab_widgets:
            if widget.view == view and not icon.isNull():
                pixmap = icon.pixmap(16, 16)
                widget.favicon.setPixmap(pixmap)
                break
                
    def set_current_tab(self, index):
        for i, widget in enumerate(self.tab_widgets):
            widget.setActive(i == index)
            
    def _on_tab_clicked(self, index):
        self.tab_clicked.emit(index)
        self.browser._tabs.setCurrentIndex(index)

# ------------------------------------------------------------------------------
# WebView
# ------------------------------------------------------------------------------
class STIWebView(QWebEngineView):
    def __init__(self, browser, incognito=False):
        super().__init__()
        self.browser = browser

        if incognito:
            profile = QWebEngineProfile(self)
            profile.setHttpCacheType(QWebEngineProfile.NoCache)
        else:
            profile = browser.webprofile

        page = STIWebPage(profile, self)
        self.setPage(page)

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

        self.channel = QWebChannel(self.page())
        self.bridge = browser.bridge
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)

        self.page().action(QWebEnginePage.Back).changed.connect(lambda: browser._update_nav_buttons(self))
        self.page().action(QWebEnginePage.Forward).changed.connect(lambda: browser._update_nav_buttons(self))

        self.loadFinished.connect(self._on_load_finished)
        self.loadProgress.connect(self._on_load_progress)
        self.titleChanged.connect(self._on_title_changed)
        self.iconChanged.connect(self._on_icon_changed)
        self.urlChanged.connect(lambda u: self._on_url_changed_internal(u))

    def _on_url_changed_internal(self, url):
        if hasattr(self.browser, '_on_url_changed_handler'):
            self.browser._on_url_changed_handler(url, self)

    def _on_load_finished(self, ok):
        self.page().runJavaScript("""
        if (typeof QWebChannel === 'undefined') {
          var s = document.createElement('script');
          s.src = 'qrc:///qtwebchannel/qwebchannel.js';
          s.onload = function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
              window.bridge = channel.objects.bridge;
            });
          };
          document.head.appendChild(s);
        }
        """)
        cfg = load_config()
        custom_css = cfg.get("custom_css", "")
        if custom_css:
            script = f"""
            (function(){{
              let s = document.getElementById('sti-custom-css');
              if (!s) {{ s = document.createElement('style'); s.id='sti-custom-css'; document.head.appendChild(s); }}
              s.textContent = `{custom_css.replace('`','\\`')}`;
            }})();
            """
            self.page().runJavaScript(script)
        theme = cfg.get("theme", "dark")
        self.page().runJavaScript(f"""
        if (document.body) {{
            document.body.dataset.theme = '{theme}';
        }}
        """)
        self.browser.inject_mods(self)
        self.browser._update_nav_buttons(self)

    def _on_load_progress(self, pct):
        self.browser.update_progress(pct, self)

    def _on_title_changed(self, title):
        self.browser.update_tab_title(self, title)

    def _on_icon_changed(self, icon):
        self.browser.update_tab_icon(self, icon)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet(self.browser.menu_stylesheet())

        hit = self.page().contextMenuData()

        back_act = QAction("Back", self)
        back_act.triggered.connect(self.back)
        menu.addAction(back_act)

        fwd_act = QAction("Forward", self)
        fwd_act.triggered.connect(self.forward)
        menu.addAction(fwd_act)

        reload_act = QAction("Reload", self)
        reload_act.triggered.connect(self.reload)
        menu.addAction(reload_act)

        menu.addSeparator()

        save_act = QAction("Save Page", self)
        save_act.triggered.connect(lambda: self.page().save(
            os.path.join(DOWNLOADS_DIR, "page.html"),
            QWebEnginePage.CompleteHtmlSaveFormat
        ))
        menu.addAction(save_act)

        menu.addSeparator()

        if hit.selectedText():
            search_act = QAction(f"Search '{hit.selectedText()[:30]}'", self)
            search_act.triggered.connect(lambda: self.browser.search_text(hit.selectedText()))
            menu.addAction(search_act)

        reader_act = QAction("Reader Mode", self)
        reader_act.triggered.connect(lambda: self.browser.toggle_reader_mode(self))
        menu.addAction(reader_act)

        menu.addSeparator()

        devtools_act = QAction("Developer Tools", self)
        devtools_act.triggered.connect(lambda: self.browser.open_devtools(self))
        menu.addAction(devtools_act)

        menu.exec_(event.globalPos())

# ------------------------------------------------------------------------------
# Side Panel (Enhanced with smooth animations)
# ------------------------------------------------------------------------------
class SidePanel(QWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setFixedWidth(340)
        self.setObjectName("SidePanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        btn_bar = QWidget()
        btn_bar.setObjectName("SidePanelBar")
        btn_bar.setFixedHeight(48)
        btn_lay = QHBoxLayout(btn_bar)
        btn_lay.setContentsMargins(10, 8, 10, 8)
        btn_lay.setSpacing(2)

        self.tabs_stack = QStackedWidget()

        panels = [
            ("Bookmarks", self._make_bookmarks_panel(), "bookmark"),
            ("History", self._make_history_panel(), "history"),
            ("Downloads", self._make_downloads_panel(), "download"),
            ("Collections", self._make_collections_panel(), "collections"),
            ("AI Assistant", self._make_ai_panel(), "ai"),
            ("Notes", self._make_notes_panel(), "notes"),
            ("Themes", self._make_themes_panel(), "theme"),
        ]
        
        self.side_buttons = []

        for idx, (name, widget, icon_key) in enumerate(panels):
            btn = QPushButton()
            btn.setToolTip(name)
            btn.setCheckable(True)
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 8px;
                    padding: 4px;
                }
                QPushButton:checked {
                    background: #0078D4;
                }
                QPushButton:hover {
                    background: #3c3f41;
                }
            """)
            btn.setIcon(QIcon(pixmap_from_svg(ICON_PATHS.get(icon_key, "star"), 16, "#e8eaed")))
            btn.clicked.connect(lambda checked, i=idx: self._switch_panel(i))
            btn_lay.addWidget(btn)
            self.side_buttons.append(btn)
            self.tabs_stack.addWidget(widget)

        btn_lay.addStretch()

        close_btn = QPushButton()
        close_btn.setFixedSize(28, 28)
        close_btn.setToolTip("Close Sidebar")
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #3c3f41;
            }
        """)
        close_btn.setIcon(QIcon(pixmap_from_svg(ICON_PATHS["x"], 14, "#9aa0a6")))
        close_btn.clicked.connect(browser.toggle_sidebar)
        btn_lay.addWidget(close_btn)

        layout.addWidget(btn_bar)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: #3c3f41; max-height: 1px;")
        layout.addWidget(line)

        layout.addWidget(self.tabs_stack, 1)

        if self.tabs_stack.count() > 0:
            self._switch_panel(0)
            
        # Setup opacity animation for panel
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        
    def _animate_show(self):
        self._anim = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._anim.setDuration(200)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.start()

    def _switch_panel(self, idx):
        self.tabs_stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.side_buttons):
            btn.setChecked(i == idx)

    def _make_bookmarks_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        header = QHBoxLayout()
        lbl = QLabel("Bookmarks")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        header.addWidget(lbl)
        
        add_btn = QPushButton("+ Add")
        add_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #3c3f41;
                color: #0078D4;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #3c3f41;
            }
        """)
        add_btn.clicked.connect(self._bookmark_current)
        header.addWidget(add_btn)
        v.addLayout(header)
        
        self.bm_list = QListWidget()
        self.bm_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                background: #2d2e30;
                border-radius: 8px;
                margin: 2px 0;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #3c3f41;
            }
        """)
        self.bm_list.itemDoubleClicked.connect(self._on_bm_click)
        v.addWidget(self.bm_list)
        self.refresh_bookmarks()
        return w

    def refresh_bookmarks(self):
        self.bm_list.clear()
        cfg = load_config()
        for bm in cfg.get("bookmarks", []):
            item = QListWidgetItem(bm.get("title", ""))
            item.setData(Qt.UserRole, bm.get("url", ""))
            self.bm_list.addItem(item)

    def _on_bm_click(self, item):
        url = item.data(Qt.UserRole)
        if url:
            self.browser.current_view().load(QUrl(url))

    def _bookmark_current(self):
        self.browser._bookmark_current()

    def _make_history_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        header = QHBoxLayout()
        lbl = QLabel("History")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        header.addWidget(lbl)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #3c3f41;
                color: #9aa0a6;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #3c3f41;
            }
        """)
        clear_btn.clicked.connect(self._clear_history)
        header.addWidget(clear_btn)
        v.addLayout(header)
        
        self.hist_list = QListWidget()
        self.hist_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                background: #2d2e30;
                border-radius: 8px;
                margin: 2px 0;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #3c3f41;
            }
        """)
        self.hist_list.itemDoubleClicked.connect(lambda item: self.browser.current_view().load(QUrl(item.data(Qt.UserRole))))
        v.addWidget(self.hist_list)
        return w

    def _clear_history(self):
        cfg = load_config()
        cfg["history"] = []
        save_config(cfg)
        self.refresh_history()

    def refresh_history(self):
        self.hist_list.clear()
        cfg = load_config()
        for h in reversed(cfg.get("history", [])[-200:]):
            item = QListWidgetItem(h.get("title", h.get("url", "")))
            item.setData(Qt.UserRole, h.get("url", ""))
            self.hist_list.addItem(item)

    def _make_downloads_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        lbl = QLabel("Downloads")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        v.addWidget(lbl)
        
        self.dl_list = QListWidget()
        self.dl_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                background: #2d2e30;
                border-radius: 8px;
                margin: 2px 0;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #3c3f41;
            }
        """)
        v.addWidget(self.dl_list)
        
        open_btn = QPushButton("Open Downloads Folder")
        open_btn.setStyleSheet("""
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066B3;
            }
        """)
        open_btn.clicked.connect(lambda: self._open_folder(DOWNLOADS_DIR))
        v.addWidget(open_btn)
        return w

    def _open_folder(self, path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def add_download(self, filename, status="Completed"):
        item = QListWidgetItem(f"{filename} - {status}")
        self.dl_list.insertItem(0, item)

    def _make_collections_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        lbl = QLabel("Collections")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        v.addWidget(lbl)
        
        self.col_list = QListWidget()
        self.col_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                background: #2d2e30;
                border-radius: 8px;
                margin: 2px 0;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #3c3f41;
            }
        """)
        v.addWidget(self.col_list)
        self._refresh_collections()
        return w

    def _refresh_collections(self):
        self.col_list.clear()
        cfg = load_config()
        for c in cfg.get("collections", []):
            item = QListWidgetItem(c.get("title", c.get("url", "")))
            item.setData(Qt.UserRole, c.get("url", ""))
            self.col_list.addItem(item)

    def _make_ai_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        lbl = QLabel("AI Assistant")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        v.addWidget(lbl)

        self.ai_input = QTextEdit()
        self.ai_input.setPlaceholderText("Ask anything or click 'Analyze Page'...")
        self.ai_input.setMaximumHeight(100)
        self.ai_input.setStyleSheet("""
            QTextEdit {
                background: #2d2e30;
                border: 1px solid #3c3f41;
                border-radius: 10px;
                padding: 12px;
                color: #e8eaed;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        v.addWidget(self.ai_input)

        btn_row = QHBoxLayout()
        ask_btn = QPushButton("Ask Gemini")
        ask_btn.setStyleSheet("""
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066B3;
            }
        """)
        ask_btn.clicked.connect(self._ask_ai)
        analyze_btn = QPushButton("Analyze Page")
        analyze_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #3c3f41;
                color: #e8eaed;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #3c3f41;
            }
        """)
        analyze_btn.clicked.connect(self._analyze_page)
        btn_row.addWidget(ask_btn)
        btn_row.addWidget(analyze_btn)
        v.addLayout(btn_row)

        self.ai_result = QTextEdit()
        self.ai_result.setReadOnly(True)
        self.ai_result.setPlaceholderText("AI response will appear here...")
        self.ai_result.setStyleSheet("""
            QTextEdit {
                background: #2d2e30;
                border: 1px solid #3c3f41;
                border-radius: 10px;
                padding: 12px;
                color: #e8eaed;
                font-size: 13px;
            }
        """)
        v.addWidget(self.ai_result)
        return w

    def _ask_ai(self):
        q = self.ai_input.toPlainText().strip()
        if not q:
            return
        url = "https://gemini.google.com/app?q=" + q.replace(" ", "+")
        self.browser.navigate_url(url)
        self.ai_result.setPlainText("AI assistant opened in browser.")

    def _analyze_page(self):
        view = self.browser.current_view()
        if not view:
            return
        url = view.url().toString()
        ai_url = f"https://gemini.google.com/app?q=analyze+this+page:+{url}"
        self.browser.add_tab(ai_url)

    def _make_themes_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        lbl = QLabel("Themes")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        v.addWidget(lbl)
        
        self.themes_list = QListWidget()
        self.themes_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                background: #2d2e30;
                border-radius: 8px;
                margin: 2px 0;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #3c3f41;
            }
        """)
        v.addWidget(self.themes_list)
        
        self.refresh_themes_list()
        
        import_btn = QPushButton("Import Theme from AI Prompt")
        import_btn.setStyleSheet("""
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066B3;
            }
        """)
        import_btn.clicked.connect(self._import_theme_from_prompt)
        v.addWidget(import_btn)
        
        return w
        
    def refresh_themes_list(self):
        self.themes_list.clear()
        cfg = load_config()
        themes = cfg.get("themes", {})
        for theme_id, theme in themes.items():
            item = QListWidgetItem(theme.get("name", theme_id))
            item.setData(Qt.UserRole, theme)
            self.themes_list.addItem(item)
            
        self.themes_list.itemDoubleClicked.connect(self._apply_theme)
        
    def _apply_theme(self, item):
        theme = item.data(Qt.UserRole)
        if theme:
            self.browser._apply_custom_theme(theme)
            
    def _import_theme_from_prompt(self):
        prompt, ok = QInputDialog.getText(self, "AI Theme Generator", 
                                          "Describe your theme (colors, style, mood):")
        if ok and prompt:
            url = f"https://gemini.google.com/app?q=generate+a+browser+theme+JSON+with+these+colors:+background,+surface,+border,+text,+accent.+Theme+description:+{prompt.replace(' ', '+')}"
            self.browser.add_tab(url)

    def _make_notes_panel(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(16, 16, 16, 16)
        v.setSpacing(8)
        
        lbl = QLabel("Notes")
        lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #e8eaed;")
        v.addWidget(lbl)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Write your notes here...")
        self.notes_edit.setStyleSheet("""
            QTextEdit {
                background: #2d2e30;
                border: 1px solid #3c3f41;
                border-radius: 10px;
                padding: 12px;
                color: #e8eaed;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        v.addWidget(self.notes_edit)
        
        save_btn = QPushButton("Save Notes")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #0066B3;
            }
        """)
        save_btn.clicked.connect(self._save_notes)
        v.addWidget(save_btn)
        self._load_notes()
        return w

    def _load_notes(self):
        cfg = load_config()
        self.notes_edit.setPlainText(cfg.get("drop_notes", ""))

    def _save_notes(self):
        cfg = load_config()
        cfg["drop_notes"] = self.notes_edit.toPlainText()
        save_config(cfg)
        self.browser._show_status("Notes saved!")

# ------------------------------------------------------------------------------
# Omnibox (Microsoft Edge style)
# ------------------------------------------------------------------------------
class OmniBox(QLineEdit):
    navigate_requested = pyqtSignal(str)

    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setPlaceholderText("Search or enter web address")
        self.setObjectName("OmniBox")
        self.returnPressed.connect(self._on_enter)
        self._animation = None

    def _on_enter(self):
        q = self.text().strip()
        if not q:
            return
        url = self._resolve(q)
        self._animate_search()
        self.navigate_requested.emit(url)

    def _animate_search(self):
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(300)
        self._animation.setStartValue(self.geometry().adjusted(0, 0, 0, 0))
        self._animation.setEndValue(self.geometry())
        self._animation.setEasingCurve(QEasingCurve.OutElastic)
        self._animation.start()

    def _resolve(self, q: str) -> str:
        if q.startswith(("http://", "https://", "ftp://", "file://", "sti://")):
            return q
        if "." in q and " " not in q and not q.startswith("sti://"):
            return "https://" + q
        cfg = load_config()
        se = cfg.get("search_engine", "bing")
        engines = {
            "google": "https://www.google.com/search?q={query}",
            "yandex": "https://yandex.ru/search/?text={query}",
            "bing": "https://www.bing.com/search?q={query}",
            "duckduckgo": "https://duckduckgo.com/?q={query}",
            "brave": "https://search.brave.com/search?q={query}"
        }
        tpl = engines.get(se, engines["bing"])
        return tpl.replace("{query}", q.replace(" ", "+"))

    def set_url(self, url: str):
        if not self.hasFocus():
            self.setText(url)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.selectAll()

# ------------------------------------------------------------------------------
# Main Browser Window (Microsoft Edge style)
# ------------------------------------------------------------------------------
class DraggableTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.drag_pos = None
        self.maximized = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos is not None:
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.maximized = False
            self.parent.move(event.globalPos() - self.drag_pos)
            event.accept()
            
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent._toggle_maximize()

class STIBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.loaded_mods = {}
        self._animations_enabled = True

        self.webprofile = QWebEngineProfile("STIProfile", self)
        self.webprofile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0 STIBrowser/2.0"
        )
        dl_path = self.config.get("download_path", DOWNLOADS_DIR)
        self.webprofile.setDownloadPath(dl_path)
        self.webprofile.downloadRequested.connect(self._on_download)

        self.bridge = STIBridge(self)
        self.bridge.navigate_signal.connect(self.navigate_url)
        self.bridge.open_settings_signal.connect(self.open_settings)
        self.bridge.open_ai_signal.connect(self.open_ai)
        self.bridge.notification_signal.connect(self._show_notification)
        self.bridge.download_offline_signal.connect(self._download_offline)

        self.loading_indicator = LoadingIndicator(self)

        self._setup_ui()
        self._apply_stylesheet()
        self._load_mods()

        self.add_tab()
        self._setup_shortcuts()

        # Исправляем проблему с отображением
        # Убираем FramelessWindowHint для отладки, или настраиваем правильно
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Вместо этого используем обычное окно с рамкой
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        
        # Устанавливаем непрозрачный фон
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        
    def _download_offline(self, url):
        self.add_tab(url)

    def _setup_ui(self):
        self.setWindowTitle("STI Browser")
        self.setMinimumSize(1024, 680)
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)
        self._main_layout = QVBoxLayout(central)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)
        
        # Custom title bar
        self.title_bar = DraggableTitleBar(self)
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(36)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(14, 0, 10, 0)
        title_layout.setSpacing(10)
        
        # macOS-style window control buttons
        btn_container = QWidget()
        btn_container.setFixedWidth(52)
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)
        
        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(12, 12)
        self.close_btn.setToolTip("Close")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5F57;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF3B30;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.close_btn)

        self.min_btn = QPushButton()
        self.min_btn.setFixedSize(12, 12)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFBD2E;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF9F0A;
            }
        """)
        self.min_btn.clicked.connect(self.showMinimized)
        btn_layout.addWidget(self.min_btn)

        self.max_btn = QPushButton()
        self.max_btn.setFixedSize(12, 12)
        self.max_btn.setToolTip("Maximize")
        self.max_btn.setStyleSheet("""
            QPushButton {
                background-color: #28CA41;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #34C759;
            }
        """)
        self.max_btn.clicked.connect(self._toggle_maximize)
        btn_layout.addWidget(self.max_btn)
        
        title_layout.addWidget(btn_container)

        title_layout.addStretch()
        
        self._main_layout.addWidget(self.title_bar)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        self._main_layout.addWidget(content, 1)

        # Main content area
        main_content = QWidget()
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab bar (Microsoft Edge style)
        self._tab_bar_widget = self._build_tab_bar()
        main_layout.addWidget(self._tab_bar_widget)

        # Toolbar
        self._toolbar = self._build_toolbar()
        main_layout.addWidget(self._toolbar)

        # Progress bar
        self._progress = QProgressBar()
        self._progress.setMaximumHeight(3)
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setObjectName("LoadProgress")
        self._progress.setVisible(False)
        main_layout.addWidget(self._progress)

        # Tabs container
        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.setMovable(True)
        self._tabs.setDocumentMode(True)
        self._tabs.setObjectName("MainTabs")
        self._tabs.tabCloseRequested.connect(self.close_tab)
        self._tabs.currentChanged.connect(self._on_tab_changed)
        self._tabs.tabBar().setVisible(False)
        main_layout.addWidget(self._tabs, 1)

        content_layout.addWidget(main_content, 1)

        # Side panel
        self.side_panel = SidePanel(self)
        self.side_panel.setVisible(self.config.get("sidebar_visible", False))
        content_layout.addWidget(self.side_panel)

        self._status = QStatusBar()
        self._status.setObjectName("StatusBar")
        self._status.setMaximumHeight(24)
        self.setStatusBar(self._status)
        
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _build_tab_bar(self):
        w = QWidget()
        w.setObjectName("TabBarWidget")
        w.setFixedHeight(40)
        layout = QHBoxLayout(w)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(0)

        self._custom_tab_bar = CustomTabBar(self)
        self._custom_tab_bar.tab_clicked.connect(self._on_tab_changed)
        layout.addWidget(self._custom_tab_bar, 1)

        return w

    def _build_toolbar(self):
        w = QWidget()
        w.setObjectName("Toolbar")
        w.setFixedHeight(46)
        layout = QHBoxLayout(w)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(4)

        # Left group: navigation buttons
        self._btn_back = self._create_tool_button("back", "Back (Alt+Left)")
        self._btn_back.clicked.connect(lambda: self.current_view() and self.current_view().back())
        layout.addWidget(self._btn_back)

        self._btn_fwd = self._create_tool_button("forward", "Forward (Alt+Right)")
        self._btn_fwd.clicked.connect(lambda: self.current_view() and self.current_view().forward())
        layout.addWidget(self._btn_fwd)

        self._btn_reload = self._create_tool_button("reload", "Reload (F5)")
        self._btn_reload.clicked.connect(self._toggle_reload)
        layout.addWidget(self._btn_reload)

        self._btn_home = self._create_tool_button("home", "Home")
        self._btn_home.clicked.connect(self._go_home)
        layout.addWidget(self._btn_home)

        # Omnibox
        omnibox_container = QWidget()
        omnibox_container.setObjectName("OmniboxContainer")
        omnibox_layout = QHBoxLayout(omnibox_container)
        omnibox_layout.setContentsMargins(4, 0, 4, 0)
        omnibox_layout.setSpacing(8)
        
        self._security_lbl = QLabel()
        self._security_lbl.setFixedSize(20, 20)
        lock_pix = pixmap_from_svg(ICON_PATHS["lock"], 16, "#8e8e93")
        self._security_lbl.setPixmap(lock_pix)
        omnibox_layout.addWidget(self._security_lbl)
        
        self._omnibox = OmniBox(self)
        self._omnibox.navigate_requested.connect(self.navigate_url)
        omnibox_layout.addWidget(self._omnibox, 1)
        
        layout.addWidget(omnibox_container, 1)

        # Right group: action buttons
        self._btn_bookmark = self._create_tool_button("bookmark", "Add Bookmark")
        self._btn_bookmark.clicked.connect(self._bookmark_current)
        layout.addWidget(self._btn_bookmark)

        self._btn_sidebar = self._create_tool_button("sidebar", "Sidebar")
        self._btn_sidebar.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self._btn_sidebar)

        self._btn_ai = self._create_tool_button("ai", "AI Assistant")
        self._btn_ai.clicked.connect(self.open_ai)
        layout.addWidget(self._btn_ai)
        
        self._btn_menu = self._create_tool_button("menu", "Menu")
        self._btn_menu.clicked.connect(self._show_main_menu)
        layout.addWidget(self._btn_menu)
        
        layout.addWidget(self.loading_indicator)
        self.loading_indicator.hide()

        return w

    def _create_tool_button(self, icon_name, tooltip):
        btn = QPushButton()
        btn.setToolTip(tooltip)
        btn.setFixedSize(34, 34)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 17px;
            }
            QPushButton:hover {
                background: #3c3f41;
            }
            QPushButton:disabled {
                opacity: 0.3;
            }
        """)
        pix = pixmap_from_svg(ICON_PATHS[icon_name], 18, "#e8eaed")
        btn.setIcon(QIcon(pix))
        btn.setIconSize(QSize(18, 18))
        return btn

    def add_tab(self, url: str = None, incognito: bool = False) -> STIWebView:
        if url is None:
            url = "sti://newtab"

        view = STIWebView(self, incognito=incognito)
        view.browser = self

        idx = self._tabs.addTab(view, "New Tab")
        self._tabs.setCurrentIndex(idx)

        # Add tab button to custom tab bar
        self._custom_tab_bar.add_tab_button(view, idx, "New Tab")
        
        # Set the initial active state
        self._custom_tab_bar.set_current_tab(idx)

        if url == "sti://newtab":
            view.load(QUrl.fromLocalFile(BROWSE_HTML))
        else:
            view.load(QUrl(url))

        view.loadStarted.connect(lambda v=view: self._on_load_started(v))
        view.loadFinished.connect(lambda v=view: self._on_load_finished(v))

        return view

    def close_tab(self, idx: int):
        if self._tabs.count() <= 1:
            self.add_tab()
        w = self._tabs.widget(idx)
        if w:
            self._custom_tab_bar.remove_tab_button(w)
        self._tabs.removeTab(idx)
        
        # Update active tab after closing
        current_idx = self._tabs.currentIndex()
        if current_idx >= 0:
            self._custom_tab_bar.set_current_tab(current_idx)

    def current_view(self) -> STIWebView:
        return self._tabs.currentWidget()

    def _on_tab_changed(self, idx):
        if idx < 0:
            return
        view = self._tabs.widget(idx)
        if view:
            url = view.url().toString()
            self._omnibox.set_url(url)
            self._update_nav_buttons(view)
            self._custom_tab_bar.set_current_tab(idx)

    def _on_url_changed_handler(self, url: QUrl, view: STIWebView):
        url_str = url.toString()
        if view == self.current_view():
            self._omnibox.set_url(url_str)
            self._update_security_icon(url)
        if url_str and not url_str.startswith("file://") and url_str != "about:blank":
            self._add_to_history(url_str, view.title())

    def _on_load_started(self, view: STIWebView):
        if view == self.current_view():
            self._btn_reload.setIcon(QIcon(pixmap_from_svg(ICON_PATHS["x"], 16, "#e8eaed")))
            self._progress.setVisible(True)
            self._progress.setValue(0)
            self.loading_indicator.start()
            self.loading_indicator.show()
            self._update_nav_buttons(view)

    def _on_load_finished(self, view: STIWebView):
        if view == self.current_view():
            self._btn_reload.setIcon(QIcon(pixmap_from_svg(ICON_PATHS["reload"], 16, "#e8eaed")))
            self.loading_indicator.stop()
            self.loading_indicator.hide()
            QTimer.singleShot(300, lambda: self._progress.setVisible(False))
            self._update_nav_buttons(view)

    def _add_to_history(self, url: str, title: str = ""):
        cfg = load_config()
        if "history" not in cfg:
            cfg["history"] = []
        if cfg["history"] and cfg["history"][-1].get("url") == url:
            return
        cfg["history"].append({"url": url, "title": title, "timestamp": datetime.now().isoformat()})
        if len(cfg["history"]) > 1000:
            cfg["history"] = cfg["history"][-1000:]
        save_config(cfg)
        if hasattr(self, "side_panel"):
            self.side_panel.refresh_history()

    def update_tab_title(self, view: STIWebView, title: str):
        idx = self._tabs.indexOf(view)
        if idx >= 0:
            short = title[:40] if title else "New Tab"
            self._tabs.setTabText(idx, short)
        self._custom_tab_bar.update_tab_title(view, title)

    def update_tab_icon(self, view: STIWebView, icon: QIcon):
        idx = self._tabs.indexOf(view)
        if idx >= 0:
            self._tabs.setTabIcon(idx, icon)
        self._custom_tab_bar.update_tab_icon(view, icon)

    def update_progress(self, pct: int, view: STIWebView):
        if view == self.current_view():
            if pct == 100:
                self._progress.setValue(100)
            else:
                self._progress.setValue(pct)
                self._progress.setVisible(True)

    def _update_nav_buttons(self, view: STIWebView):
        if view:
            self._btn_back.setEnabled(view.history().canGoBack())
            self._btn_fwd.setEnabled(view.history().canGoForward())

    def _update_security_icon(self, url: QUrl):
        scheme = url.scheme().lower()
        if scheme == "https":
            pix = pixmap_from_svg(ICON_PATHS["lock"], 16, "#8bc34a")
        elif scheme in ("http",):
            pix = pixmap_from_svg(ICON_PATHS["warning"], 16, "#ffb74d")
        else:
            pix = pixmap_from_svg(ICON_PATHS["info"], 16, "#8e8e93")
        self._security_lbl.setPixmap(pix)

    def navigate_url(self, url: str):
        view = self.current_view()
        if not view:
            view = self.add_tab(url)
            return
        if url == "sti://newtab":
            view.load(QUrl.fromLocalFile(BROWSE_HTML))
        elif url == "sti://settings":
            self.open_settings()
        else:
            view.load(QUrl(url))
        self._omnibox.set_url(url)

    def _go_home(self):
        cfg = load_config()
        home = cfg.get("homepage", "sti://newtab")
        self.navigate_url(home)

    def _toggle_reload(self):
        view = self.current_view()
        if not view:
            return
        if self._btn_reload.icon().cacheKey() == QIcon(pixmap_from_svg(ICON_PATHS["x"], 16, "#e8eaed")).cacheKey():
            view.stop()
        else:
            view.reload()

    def open_settings(self):
        view = self.current_view()
        if view:
            view.load(QUrl.fromLocalFile(SETTINGS_HTML))

    def open_ai(self):
        url = "https://gemini.google.com/"
        self.add_tab(url)

    def toggle_sidebar(self):
        visible = not self.side_panel.isVisible()
        self.side_panel.setVisible(visible)
        if visible:
            self.side_panel._animate_show()
        cfg = load_config()
        cfg["sidebar_visible"] = visible
        save_config(cfg)

    def toggle_reader_mode(self, view: STIWebView):
        if not view:
            return
        script = """
        (function() {
          if (document.getElementById('sti-reader-mode')) {
            document.getElementById('sti-reader-mode').remove();
            document.body.style.maxWidth = '';
            document.body.style.margin = '';
            return;
          }
          var style = document.createElement('style');
          style.id = 'sti-reader-mode';
          style.textContent = `
            body { max-width: 720px !important; margin: 40px auto !important;
              font-family: -apple-system, Georgia, serif !important; font-size: 18px !important;
              line-height: 1.8 !important; background: #202124 !important;
              color: #e8eaed !important; padding: 0 24px !important; }
            header, footer, nav, aside, .ad, .sidebar, [class*="banner"],
            [class*="popup"], [class*="modal"] { display: none !important; }
          `;
          document.head.appendChild(style);
        })();
        """
        view.page().runJavaScript(script)

    def search_text(self, text: str):
        cfg = load_config()
        se = cfg.get("search_engine", "bing")
        engines = {
            "google": "https://www.google.com/search?q={query}",
            "bing": "https://www.bing.com/search?q={query}",
            "duckduckgo": "https://duckduckgo.com/?q={query}",
        }
        tpl = engines.get(se, engines["bing"])
        url = tpl.replace("{query}", text.replace(" ", "+"))
        self.add_tab(url)

    def _bookmark_current(self):
        view = self.current_view()
        if not view:
            return
        url = view.url().toString()
        title = view.title() or url
        if not url or url.startswith("file://"):
            return
        cfg = load_config()
        if "bookmarks" not in cfg:
            cfg["bookmarks"] = []
        for bm in cfg["bookmarks"]:
            if bm.get("url") == url:
                self._show_status("Already bookmarked")
                return
        cfg["bookmarks"].append({"title": title, "url": url})
        save_config(cfg)
        self._btn_bookmark.setIcon(QIcon(pixmap_from_svg(ICON_PATHS["bookmark_filled"], 18, "#0078D4")))
        QTimer.singleShot(2000, lambda: self._btn_bookmark.setIcon(QIcon(pixmap_from_svg(ICON_PATHS["bookmark"], 18, "#e8eaed"))))
        self._show_status("Bookmark added")
        if hasattr(self, "side_panel"):
            self.side_panel.refresh_bookmarks()

    def open_devtools(self, view: STIWebView):
        if not view:
            return
        dev_view = QWebEngineView()
        dev_view.setWindowTitle("Developer Tools - STI")
        view.page().setDevToolsPage(dev_view.page())
        dev_view.resize(900, 600)
        dev_view.show()

    def _show_main_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(self.menu_stylesheet())

        menu.addAction("New Tab\tCtrl+T", lambda: self.add_tab())
        menu.addAction("New Incognito Tab\tCtrl+Shift+N", lambda: self.add_tab(incognito=True))
        menu.addSeparator()
        menu.addAction("Bookmarks", lambda: self.side_panel.setVisible(True))
        menu.addAction("History", lambda: self.side_panel.setVisible(True))
        menu.addAction("Downloads\tCtrl+J", lambda: self.side_panel.setVisible(True))
        menu.addSeparator()
        menu.addAction("Zoom In\tCtrl++", lambda: self._zoom(1.1))
        menu.addAction("Zoom Out\tCtrl+-", lambda: self._zoom(0.9))
        menu.addAction("Reset Zoom\tCtrl+0", self._zoom_reset)
        menu.addSeparator()
        
        theme_menu = menu.addMenu("Theme")
        themes = [("Dark", "dark"), ("Light", "light"), ("System", "system")]
        for tname, tid in themes:
            act = QAction(tname, self)
            act.triggered.connect(lambda checked, t=tid: self._set_theme(t))
            theme_menu.addAction(act)

        engine_menu = menu.addMenu("Search Engine")
        for se_id, se_name in [("bing","Bing"), ("google","Google"), ("duckduckgo","DuckDuckGo")]:
            act = QAction(se_name, self)
            act.triggered.connect(lambda checked, s=se_id: self._set_search_engine(s))
            engine_menu.addAction(act)

        menu.addSeparator()
        menu.addAction("Settings\tCtrl+,", self.open_settings)
        menu.addSeparator()
        menu.addAction("Exit\tCtrl+Q", self.close)

        btn = self._btn_menu
        menu.exec_(btn.mapToGlobal(QPoint(0, btn.height())))

    def _set_theme(self, theme_id: str):
        cfg = load_config()
        cfg["theme"] = theme_id
        save_config(cfg)
        self._apply_stylesheet()
        for i in range(self._tabs.count()):
            v = self._tabs.widget(i)
            if v:
                v.page().runJavaScript(f"if(document.body)document.body.dataset.theme='{theme_id}';")
        self._show_status(f"Theme: {theme_id}")

    def _apply_custom_theme(self, theme: dict):
        cfg = load_config()
        cfg["custom_theme"] = theme
        save_config(cfg)
        self._apply_stylesheet()
        self._show_status(f"Theme: {theme.get('name', 'Custom')}")

    def _set_search_engine(self, se: str):
        cfg = load_config()
        cfg["search_engine"] = se
        save_config(cfg)
        self._show_status(f"Search engine: {se}")

    def _zoom(self, factor: float):
        view = self.current_view()
        if view:
            current = view.zoomFactor()
            view.setZoomFactor(min(max(current * factor, 0.25), 5.0))

    def _zoom_reset(self):
        view = self.current_view()
        if view:
            view.setZoomFactor(1.0)

    def _setup_shortcuts(self):
        shortcuts = [
            ("Ctrl+T",       lambda: self.add_tab()),
            ("Ctrl+W",       lambda: self.close_tab(self._tabs.currentIndex())),
            ("Ctrl+Tab",     self._next_tab),
            ("Ctrl+Shift+Tab", self._prev_tab),
            ("Ctrl+L",       lambda: self._omnibox.setFocus()),
            ("Ctrl+R",       lambda: self.current_view() and self.current_view().reload()),
            ("F5",           lambda: self.current_view() and self.current_view().reload()),
            ("Ctrl+Shift+R", lambda: self.current_view() and self.current_view().page().triggerAction(QWebEnginePage.ReloadAndBypassCache)),
            ("Ctrl+,",       self.open_settings),
            ("Ctrl+Q",       self.close),
            ("Ctrl+Shift+N", lambda: self.add_tab(incognito=True)),
            ("Ctrl+J",       self._show_downloads),
            ("Ctrl+B",       self._bookmark_current),
            ("Ctrl+H",       lambda: self.side_panel.setVisible(True)),
            ("Alt+Left",     lambda: self.current_view() and self.current_view().back()),
            ("Alt+Right",    lambda: self.current_view() and self.current_view().forward()),
            ("F11",          self._toggle_fullscreen),
            ("Ctrl+Plus",    lambda: self._zoom(1.1)),
            ("Ctrl+Minus",   lambda: self._zoom(0.9)),
            ("Ctrl+0",       self._zoom_reset),
            ("Ctrl+F",       self._find_in_page),
            ("Ctrl+S",       lambda: self.current_view() and self.save_offline(self.current_view())),
            ("Ctrl+Shift+I", lambda: self.open_devtools(self.current_view())),
        ]
        for keys, func in shortcuts:
            QShortcut(QKeySequence(keys), self, func)

    def _show_downloads(self):
        self.side_panel.setVisible(True)
        if hasattr(self.side_panel, "_switch_panel"):
            self.side_panel._switch_panel(2)

    def _next_tab(self):
        idx = (self._tabs.currentIndex() + 1) % self._tabs.count()
        self._tabs.setCurrentIndex(idx)

    def _prev_tab(self):
        idx = (self._tabs.currentIndex() - 1) % self._tabs.count()
        self._tabs.setCurrentIndex(idx)

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _find_in_page(self):
        text, ok = QInputDialog.getText(self, "Find in Page", "Find:")
        if ok and text:
            self.current_view().findText(text)

    def save_offline(self, view: STIWebView):
        url = view.url().toString()
        title = view.title() or "page"
        safe_name = "".join(c if c.isalnum() else "_" for c in title[:40])
        dest_dir = os.path.join("offline_pages")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, safe_name + ".html")
        view.page().save(dest, QWebEnginePage.CompleteHtmlSaveFormat)
        self._show_status(f"Page saved: {dest}")

    def _on_download(self, download: QWebEngineDownloadItem):
        cfg = load_config()
        dl_path = cfg.get("download_path", DOWNLOADS_DIR)
        filename = os.path.basename(download.path())
        dest = os.path.join(dl_path, filename)
        download.setPath(dest)
        download.accept()
        download.finished.connect(lambda: self._download_finished(filename))
        self._show_status(f"Downloading: {filename}")

    def _download_finished(self, filename: str):
        self._show_status(f"Downloaded: {filename}")
        if hasattr(self, "side_panel"):
            self.side_panel.add_download(filename)

    def _load_mods(self):
        cfg = load_config()
        active = cfg.get("active_mods", [])
        if not os.path.exists(MODS_DIR):
            return
        for mod_id in os.listdir(MODS_DIR):
            if mod_id not in active:
                continue
            mod_dir = os.path.join(MODS_DIR, mod_id)
            manifest_path = os.path.join(mod_dir, "manifest.json")
            script_path = os.path.join(mod_dir, "mod_script.py")
            if not os.path.exists(manifest_path):
                continue
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                if os.path.exists(script_path):
                    spec = importlib.util.spec_from_file_location(mod_id, script_path)
                    mod_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod_module)
                    if hasattr(mod_module, "create_mod"):
                        mod_obj = mod_module.create_mod(self)
                        mod_obj.activate()
                        self.loaded_mods[mod_id] = {"manifest": manifest, "instance": mod_obj}
                        print(f"[Mods] Loaded: {manifest.get('name', mod_id)}")
            except Exception as e:
                print(f"[Mods] Error loading {mod_id}: {e}")

    def inject_mods(self, view: STIWebView):
        for mod_id, mod_data in self.loaded_mods.items():
            inst = mod_data.get("instance")
            if inst and hasattr(inst, "on_page_load"):
                inst.on_page_load(view.url().toString())

    def _show_notification(self, title: str, message: str):
        self._status.showMessage(f"{title}: {message}", 4000)

    def _show_status(self, msg: str, duration: int = 3000):
        self._status.showMessage(msg, duration)

    def _apply_stylesheet(self):
        cfg = load_config()
        theme = cfg.get("theme", "dark")
        custom_theme = cfg.get("custom_theme", None)
        
        if custom_theme:
            bg = custom_theme.get("background", "#1e1e1e")
            surface = custom_theme.get("surface", "#2d2d30")
            border = custom_theme.get("border", "#3e3e42")
            text = custom_theme.get("text", "#e0e0e0")
            accent = custom_theme.get("accent", "#0078d4")
        else:
            if theme == "light":
                bg = "#ffffff"
                surface = "#f3f3f3"
                border = "#e0e0e0"
                text = "#1e1e1e"
                accent = "#0078d4"
            else:
                bg = "#1e1e1e"
                surface = "#2d2d30"
                border = "#3e3e42"
                text = "#e0e0e0"
                accent = "#0078d4"

        self.setStyleSheet(f"""
        QMainWindow {{
            background: {bg};
        }}
        
        QWidget {{
            background: {bg};
            color: {text};
            font-family: 'Segoe UI', -apple-system, system-ui, sans-serif;
            font-size: 13px;
        }}
        
        QWidget#TitleBar {{
            background: {surface};
            border-bottom: 1px solid {border};
        }}
        
        QWidget#Toolbar {{
            background: {surface};
            border-bottom: 1px solid {border};
        }}
        
        QWidget#TabBarWidget {{
            background: {surface};
            border-bottom: 1px solid {border};
        }}
        
        QLineEdit#OmniBox {{
            background: {bg};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 6px 16px;
            color: {text};
            font-size: 13px;
            selection-background-color: {accent};
        }}
        QLineEdit#OmniBox:focus {{
            border: 1px solid {accent};
        }}
        
        QWidget#OmniboxContainer {{
            background: transparent;
        }}
        
        QWidget#SidePanel {{
            background: {surface};
            border-left: 1px solid {border};
        }}
        
        QWidget#SidePanelBar {{
            background: {surface};
            border-bottom: 1px solid {border};
        }}
        
        QListWidget {{
            background: transparent;
            border: none;
            outline: none;
        }}
        QListWidget::item {{
            background: {bg};
            border-radius: 6px;
            margin: 2px 0;
            padding: 8px;
            color: {text};
        }}
        QListWidget::item:hover {{
            background: {border};
        }}
        QListWidget::item:selected {{
            background: {accent};
            color: white;
        }}
        
        QProgressBar#LoadProgress {{
            background: transparent;
            border: none;
            max-height: 3px;
        }}
        QProgressBar#LoadProgress::chunk {{
            background: {accent};
            border-radius: 1px;
        }}
        
        QStatusBar#StatusBar {{
            background: {surface};
            color: {text};
            border-top: 1px solid {border};
            font-size: 11px;
            padding: 2px 8px;
        }}
        
        QTabWidget::pane {{
            border: none;
            background: {bg};
        }}
        
        QMenu {{
            background: {surface};
            color: {text};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 6px;
            margin: 2px 4px;
        }}
        QMenu::item:selected {{
            background: {border};
        }}
        QMenu::separator {{
            background: {border};
            height: 1px;
            margin: 6px 8px;
        }}
        
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {border};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {accent};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 8px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {border};
            border-radius: 4px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {accent};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """)

    def menu_stylesheet(self) -> str:
        return """
        QMenu {
            background: #2d2d30;
            color: #e0e0e0;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            padding: 4px;
        }
        QMenu::item {
            padding: 8px 24px;
            border-radius: 6px;
            margin: 2px 4px;
        }
        QMenu::item:selected {
            background: #3e3e42;
        }
        QMenu::separator {
            background: #3e3e42;
            height: 1px;
            margin: 6px 8px;
        }
        """

    def closeEvent(self, event):
        for mod_id, mod_data in self.loaded_mods.items():
            try:
                mod_data["instance"].deactivate()
            except Exception:
                pass
        event.accept()

def main():
    # Включаем аппаратное ускорение
    os.environ["QT_QUICK_BACKEND"] = "software"  # Убираем если есть
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --enable-zero-copy --ignore-gpu-blocklist"
    os.environ["QMLSCENE_DEVICE"] = "softwarecontext"  # Убираем эту строку
    
    # ВАЖНО: Убираем software рендеринг
    if "QT_QUICK_BACKEND" in os.environ:
        del os.environ["QT_QUICK_BACKEND"]
    
    # Включаем аппаратное ускорение WebEngine
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join([
        "--enable-gpu-rasterization",
        "--enable-zero-copy",
        "--ignore-gpu-blocklist",
        "--enable-features=VaapiVideoDecoder",
        "--disable-features=UseChromeOSDirectVideoDecoder",
        "--enable-accelerated-2d-canvas",
        "--enable-accelerated-video-decode",
        "--num-raster-threads=4"
    ])
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setAttribute(Qt.AA_UseDesktopOpenGL, True)  # Используем настольный OpenGL
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)  # Шарим контексты OpenGL

    app = QApplication(sys.argv)
    app.setApplicationName("STI Browser")
    app.setOrganizationName("STI")
    app.setApplicationVersion("2.0.0")

    window = STIBrowser()
    window.show()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec_())

def show_main_window(window, splash):
    """Показывает главное окно с анимацией появления"""
    window.setWindowOpacity(0.0)
    window.show()
    
    # Анимация появления главного окна
    anim = QPropertyAnimation(window, b"windowOpacity")
    anim.setDuration(500)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
    
    # Закрываем сплэш-скрин
    QTimer.singleShot(200, splash.close)

if __name__ == "__main__":
    main()
