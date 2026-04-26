import sys
import os
import json
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

# ------------------------------------------------------------------------------
# Auto-update system
# ------------------------------------------------------------------------------
class BrowserUpdater:
    def __init__(self):
        self.version_file = "browser-ver.json"
        self.github_base = "https://raw.githubusercontent.com/DrSwalster/browser-STI/main"
        self.update_available = False
        self.current_version = "2.0.0"
        
    def check_for_updates(self):
        """Проверяет наличие обновлений на GitHub"""
        try:
            url = f"{self.github_base}/browser-ver.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'STI-Browser-Updater/2.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                remote_data = json.loads(response.read().decode('utf-8'))
            
            local_data = {}
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    local_data = json.load(f)
            
            remote_version = remote_data.get('version', '0.0.0')
            local_version = local_data.get('version', '0.0.0')
            
            if remote_version > local_version:
                self.update_available = True
                return remote_data
            return None
            
        except Exception as e:
            print(f"[Updater] Check failed: {e}")
            return None
    
    def download_update(self, filename, url):
        """Скачивает обновленный файл"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'STI-Browser-Updater/2.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"[Updater] Download failed for {filename}: {e}")
            return None
    
    def apply_update(self, update_data):
        """Применяет обновления"""
        if not update_data:
            return False
        
        try:
            files = update_data.get('files', {})
            updated = []
            
            for filename, info in files.items():
                remote_version = info.get('version', '0')
                
                local_version = '0'
                if os.path.exists(self.version_file):
                    with open(self.version_file, 'r', encoding='utf-8') as f:
                        local_data = json.load(f)
                    local_files = local_data.get('files', {})
                    local_version = local_files.get(filename, {}).get('version', '0')
                
                if remote_version > local_version:
                    content = self.download_update(filename, info.get('url', ''))
                    if content:
                        # Создаем бэкап
                        if os.path.exists(filename):
                            backup = f"{filename}.bak"
                            shutil.copy2(filename, backup)
                        
                        # Сохраняем новый файл
                        temp_file = f"{filename}.tmp"
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        if os.path.exists(filename):
                            os.remove(filename)
                        os.rename(temp_file, filename)
                        updated.append(filename)
                        print(f"[Updater] Updated: {filename} -> v{remote_version}")
            
            if updated:
                with open(self.version_file, 'w', encoding='utf-8') as f:
                    json.dump(update_data, f, ensure_ascii=False, indent=2)
                print(f"[Updater] Updated {len(updated)} files to version {update_data['version']}")
                return True
            
            return False
            
        except Exception as e:
            print(f"[Updater] Apply failed: {e}")
            return False

# ------------------------------------------------------------------------------
# Bootstrap - загрузка файлов при первом запуске
# ------------------------------------------------------------------------------
def bootstrap():
    """Создает необходимые файлы при первом запуске"""
    required_files = {
        "browse-interface.html": "browse-interface.html",
        "browse.html": "browse.html",
        "settings.html": "settings.html",
        "browser-ver.json": "browser-ver.json"
    }
    
    updater = BrowserUpdater()
    
    for local_name, remote_name in required_files.items():
        if not os.path.exists(local_name):
            print(f"[STI] Missing: {local_name}, downloading from GitHub...")
            url = f"{updater.github_base}/{remote_name}"
            content = updater.download_update(local_name, url)
            if content:
                with open(local_name, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[STI] Downloaded: {local_name}")
            else:
                print(f"[STI] Failed to download: {local_name}")
                # Создаем минимальные версии если не удалось скачать
                if local_name == "browser-ver.json":
                    create_default_version_file()
                elif local_name == "browse.html":
                    create_default_browse_html()
                elif local_name == "browse-interface.html":
                    print("[STI] ERROR: browse-interface.html is required!")
                    sys.exit(1)
                elif local_name == "settings.html":
                    create_default_settings_html()

def create_default_version_file():
    """Создает файл версии по умолчанию"""
    data = {
        "version": "2.0.0",
        "build_date": "2025-01-15",
        "files": {
            "sti.py": {
                "version": "2.0.0",
                "url": "https://raw.githubusercontent.com/DrSwalster/browser-STI/main/sti.py"
            },
            "browse-interface.html": {
                "version": "2.0.0",
                "url": "https://raw.githubusercontent.com/DrSwalster/browser-STI/main/browse-interface.html"
            },
            "browse.html": {
                "version": "2.0.0",
                "url": "https://raw.githubusercontent.com/DrSwalster/browser-STI/main/browse.html"
            },
            "settings.html": {
                "version": "2.0.0",
                "url": "https://raw.githubusercontent.com/DrSwalster/browser-STI/main/settings.html"
            }
        },
        "auto_update": True
    }
    with open("browser-ver.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_default_browse_html():
    """Создает browse.html со speed dial"""
    content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STI Browser - New Tab</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #1e1e1e;
    color: #e0e0e0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .logo { font-size: 32px; font-weight: 700; margin-bottom: 24px; color: #4da3e0; }
  .search-box {
    width: 600px; max-width: 90%; padding: 14px 24px;
    border-radius: 28px; border: 1.5px solid #505055;
    background: #2a2a2c; color: #e0e0e0; font-size: 15px;
    outline: none; margin-bottom: 32px; transition: all 0.2s;
  }
  .search-box:focus { border-color: #4da3e0; box-shadow: 0 0 0 3px #1e3a4d; }
  .speed-dial {
    display: flex; flex-wrap: wrap; gap: 16px;
    justify-content: center; max-width: 640px;
  }
  .dial-item {
    display: flex; flex-direction: column; align-items: center;
    gap: 8px; cursor: pointer; padding: 16px 12px;
    border-radius: 12px; transition: all 0.2s; width: 88px;
    text-decoration: none; color: #e0e0e0;
  }
  .dial-item:hover { background: #333336; transform: translateY(-2px); }
  .dial-icon {
    width: 48px; height: 48px; border-radius: 12px;
    background: #3e3e42; display: flex; align-items: center;
    justify-content: center; overflow: hidden;
  }
  .dial-icon img { width: 28px; height: 28px; }
  .dial-label { font-size: 12px; text-align: center; max-width: 80px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
</head>
<body>
  <div class="logo">STI Browser</div>
  <input class="search-box" type="text" placeholder="Search or enter web address" id="searchInput" 
         onkeydown="if(event.key==='Enter'){let q=this.value.trim();if(q){if(q.includes('.')&&!q.includes(' ')){q='https://'+q}else{q='https://www.google.com/search?q='+encodeURIComponent(q)}if(window.bridge)bridge.navigate(q);else window.location.href=q}}">
  <div class="speed-dial" id="speedDial"></div>
  <script>
    try{
      let cfg=JSON.parse(localStorage.getItem('sti_config_v3')||'{}');
      let bm=cfg.bookmarks||[
        {title:'Google',url:'https://google.com'},
        {title:'YouTube',url:'https://youtube.com'},
        {title:'GitHub',url:'https://github.com'}
      ];
      document.getElementById('speedDial').innerHTML=bm.map(b=>`
        <div class="dial-item" onclick="let u='${b.url}';if(window.bridge)bridge.navigate(u);else window.location.href=u;">
          <div class="dial-icon"><img src="https://www.google.com/s2/favicons?sz=64&domain_url=${encodeURIComponent(b.url)}" onerror="this.style.display='none'"></div>
          <span class="dial-label">${b.title}</span>
        </div>`).join('');
    }catch(e){}
  </script>
</body>
</html>"""
    with open("browse.html", 'w', encoding='utf-8') as f:
        f.write(content)

def create_default_settings_html():
    """Создает settings.html"""
    content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>STI Settings</title>
<style>
  body { 
    font-family: 'Segoe UI', sans-serif; 
    background: #1e1e1e; 
    color: #e0e0e0; 
    padding: 40px; 
  }
  h1 { font-size: 24px; margin-bottom: 20px; }
  .setting { margin-bottom: 16px; }
  label { display: block; margin-bottom: 6px; font-size: 14px; }
  select, input { 
    background: #2d2d30; 
    color: #e0e0e0; 
    border: 1px solid #3e3e42; 
    padding: 8px 12px; 
    border-radius: 6px; 
    font-size: 13px; 
    width: 300px; 
  }
  button { 
    background: #0078D4; 
    color: white; 
    border: none; 
    padding: 10px 20px; 
    border-radius: 6px; 
    cursor: pointer; 
    font-size: 13px; 
    margin-top: 20px; 
  }
  button:hover { background: #0066B3; }
</style>
</head>
<body>
  <h1>Settings</h1>
  <div class="setting">
    <label>Search Engine</label>
    <select id="seSelect" onchange="saveSetting('search_engine',this.value)">
      <option value="google">Google</option>
      <option value="yandex">Yandex</option>
      <option value="bing">Bing</option>
      <option value="duckduckgo">DuckDuckGo</option>
      <option value="brave">Brave</option>
    </select>
  </div>
  <div class="setting">
    <label>Homepage</label>
    <input id="homepageInp" value="sti://newtab" placeholder="https://example.com">
  </div>
  <div class="setting">
    <label>Weather City</label>
    <input id="cityInp" value="Moscow" placeholder="City name">
  </div>
  <button onclick="saveAll()">Save Settings</button>
  <script>
    try{
      let cfg=JSON.parse(localStorage.getItem('sti_config_v3')||'{}');
      document.getElementById('seSelect').value=cfg.search_engine||'google';
      document.getElementById('homepageInp').value=cfg.homepage||'sti://newtab';
      document.getElementById('cityInp').value=cfg.weather_city||'Moscow';
    }catch(e){}
    function saveSetting(key,val){
      try{
        let cfg=JSON.parse(localStorage.getItem('sti_config_v3')||'{}');
        cfg[key]=val;
        localStorage.setItem('sti_config_v3',JSON.stringify(cfg));
        if(window.bridge)bridge.saveConfig(JSON.stringify(cfg));
      }catch(e){}
    }
    function saveAll(){
      saveSetting('search_engine',document.getElementById('seSelect').value);
      saveSetting('homepage',document.getElementById('homepageInp').value);
      saveSetting('weather_city',document.getElementById('cityInp').value);
      alert('Settings saved!');
    }
  </script>
</body>
</html>"""
    with open("settings.html", 'w', encoding='utf-8') as f:
        f.write(content)

# Запускаем бутстрап
bootstrap()

# ------------------------------------------------------------------------------
# PyQt5 imports
# ------------------------------------------------------------------------------
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QPushButton, QLabel, QMenu, QAction, QFileDialog,
        QMessageBox, QProgressBar, QShortcut, QStatusBar
    )
    from PyQt5.QtWebEngineWidgets import (
        QWebEngineView, QWebEnginePage, QWebEngineProfile,
        QWebEngineSettings, QWebEngineDownloadItem
    )
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtCore import (
        Qt, QUrl, QSize, QTimer, pyqtSignal, pyqtSlot,
        QObject, QPoint, QByteArray
    )
    from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QCursor, QPainter
    from PyQt5.QtSvg import QSvgRenderer
except ImportError as e:
    print(f"[STI] PyQt5 import error: {e}")
    print("[STI] Run: pip install PyQt5 PyQtWebEngine")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
CONFIG_PATH = "config.json"
BROWSE_INTERFACE_HTML = os.path.abspath("browse-interface.html")
BROWSE_HTML = os.path.abspath("browse.html")
SETTINGS_HTML = os.path.abspath("settings.html")
DOWNLOADS_DIR = os.path.abspath("downloads")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def load_config():
    """Загружает конфигурацию из файла"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(cfg: dict):
    """Сохраняет конфигурацию в файл"""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[STI] Config save error: {e}")

# ------------------------------------------------------------------------------
# QWebChannel bridge для связи Python ↔ JavaScript
# ------------------------------------------------------------------------------
class STIBridge(QObject):
    """Мост между Python и JavaScript в WebView"""
    navigate_signal = pyqtSignal(str)
    open_settings_signal = pyqtSignal()
    open_ai_signal = pyqtSignal()

    def __init__(self, browser):
        super().__init__()
        self.browser = browser

    @pyqtSlot(str)
    def navigate(self, url: str):
        """Навигация по URL из JavaScript"""
        self.navigate_signal.emit(url)

    @pyqtSlot()
    def openSettings(self):
        """Открыть настройки из JavaScript"""
        self.open_settings_signal.emit()

    @pyqtSlot()
    def openAI(self):
        """Открыть AI ассистент из JavaScript"""
        self.open_ai_signal.emit()

    @pyqtSlot(str)
    def saveConfig(self, json_str: str):
        """Сохранить конфигурацию из JavaScript"""
        try:
            cfg = json.loads(json_str)
            save_config(cfg)
        except Exception as e:
            print(f"[Bridge] saveConfig error: {e}")

    @pyqtSlot()
    def clearHistory(self):
        """Очистить историю"""
        cfg = load_config()
        cfg["history"] = []
        save_config(cfg)

    @pyqtSlot()
    def clearCookies(self):
        """Очистить cookies"""
        if self.browser and self.browser.webprofile:
            self.browser.webprofile.cookieStore().deleteAllCookies()

# ------------------------------------------------------------------------------
# Кастомная WebPage для обработки новых вкладок
# ------------------------------------------------------------------------------
class STIWebPage(QWebEnginePage):
    """Кастомная страница с поддержкой открытия новых вкладок"""
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

    def createWindow(self, _type):
        """Создает новую вкладку при window.open()"""
        if hasattr(self.parent(), "browser"):
            return self.parent().browser.add_tab().page()
        return super().createWindow(_type)

# ------------------------------------------------------------------------------
# WebView с поддержкой QWebChannel
# ------------------------------------------------------------------------------
class STIWebView(QWebEngineView):
    """Основной WebView с мостом JavaScript"""
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self._current_url = "sti://newtab"

        # Используем общий профиль
        page = STIWebPage(browser.webprofile, self)
        self.setPage(page)

        # Настройки WebEngine
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)

        # QWebChannel
        self.channel = QWebChannel(self.page())
        self.bridge = browser.bridge
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)

        # Сигналы
        self.loadFinished.connect(self._on_load_finished)
        self.titleChanged.connect(self._on_title_changed)
        self.urlChanged.connect(self._on_url_changed)

    def _on_url_changed(self, url):
        """Отслеживает изменение URL"""
        self._current_url = url.toString()

    def _on_load_finished(self, ok):
        """Инициализирует QWebChannel после загрузки"""
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

    def _on_title_changed(self, title):
        """Обновляет заголовок вкладки"""
        self.browser.update_tab_title(self, title)

# ------------------------------------------------------------------------------
# Главное окно браузера
# ------------------------------------------------------------------------------
class STIBrowser(QMainWindow):
    """Главный класс браузера STI"""
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.updater = BrowserUpdater()

        # Профиль
        self.webprofile = QWebEngineProfile("STIProfile", self)
        self.webprofile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0 STIBrowser/2.0"
        )
        dl_path = self.config.get("download_path", DOWNLOADS_DIR)
        self.webprofile.setDownloadPath(dl_path)
        self.webprofile.downloadRequested.connect(self._on_download)

        # Bridge
        self.bridge = STIBridge(self)
        self.bridge.navigate_signal.connect(self.navigate_url)
        self.bridge.open_settings_signal.connect(self.open_settings)

        # UI
        self._setup_ui()
        self._apply_dark_stylesheet()
        self._setup_shortcuts()

        # Запускаем с интерфейсом
        self.add_tab("sti://newtab")
        
        # Проверка обновлений
        QTimer.singleShot(2000, self._check_updates)

    def _setup_ui(self):
        """Создает UI браузера"""
        self.setWindowTitle("STI Browser")
        self.setMinimumSize(1024, 680)
        self.resize(1280, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Прогресс-бар
        self._progress = QProgressBar()
        self._progress.setMaximumHeight(3)
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        self._progress.setVisible(False)
        layout.addWidget(self._progress)

        # Вкладки
        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.setMovable(True)
        self._tabs.setDocumentMode(True)
        self._tabs.tabCloseRequested.connect(self.close_tab)
        self._tabs.currentChanged.connect(self._on_tab_changed)
        layout.addWidget(self._tabs, 1)

        # Статус-бар
        self._status = QStatusBar()
        self._status.setMaximumHeight(24)
        self.setStatusBar(self._status)

    def add_tab(self, url: str = None) -> STIWebView:
        """Добавляет новую вкладку"""
        if url is None:
            url = "sti://newtab"

        view = STIWebView(self)
        
        idx = self._tabs.addTab(view, "New Tab")
        self._tabs.setCurrentIndex(idx)

        # Загружаем browse-interface.html для новых вкладок
        if url == "sti://newtab":
            view.load(QUrl.fromLocalFile(BROWSE_INTERFACE_HTML))
        elif url == "sti://settings":
            view.load(QUrl.fromLocalFile(SETTINGS_HTML))
        else:
            view.load(QUrl(url))

        # Прогресс-бар
        view.loadStarted.connect(lambda v=view: self._on_load_started(v))
        view.loadFinished.connect(lambda v=view: self._on_load_finished(v))

        return view

    def _on_load_started(self, view: STIWebView):
        """Показывает прогресс-бар при загрузке"""
        if view == self.current_view():
            self._progress.setVisible(True)
            self._progress.setValue(0)
            # Анимация прогресса
            for i in range(1, 91, 10):
                QTimer.singleShot(i * 10, lambda v=i: self._progress.setValue(v) if self._progress.isVisible() else None)

    def _on_load_finished(self, view: STIWebView):
        """Скрывает прогресс-бар после загрузки"""
        if view == self.current_view():
            self._progress.setValue(100)
            QTimer.singleShot(300, lambda: self._progress.setVisible(False))

    def close_tab(self, idx: int):
        """Закрывает вкладку"""
        if self._tabs.count() <= 1:
            # Открываем новую если закрываем последнюю
            self.add_tab("sti://newtab")
        self._tabs.removeTab(idx)

    def current_view(self) -> STIWebView:
        """Возвращает текущий WebView"""
        return self._tabs.currentWidget()

    def _on_tab_changed(self, idx):
        """Обработчик смены вкладки"""
        if idx < 0:
            return
        view = self._tabs.widget(idx)
        if view:
            self._status.showMessage(view._current_url, 3000)

    def update_tab_title(self, view: STIWebView, title: str):
        """Обновляет заголовок вкладки"""
        idx = self._tabs.indexOf(view)
        if idx >= 0:
            short = title[:40] if title else "New Tab"
            self._tabs.setTabText(idx, short)

    def navigate_url(self, url: str):
        """Навигация по URL"""
        view = self.current_view()
        if not view:
            view = self.add_tab(url)
            return
        
        if url == "sti://newtab":
            view.load(QUrl.fromLocalFile(BROWSE_INTERFACE_HTML))
        elif url == "sti://settings":
            self.open_settings()
        else:
            if not url.startswith(("http://", "https://", "file://")):
                if "." in url and " " not in url:
                    url = "https://" + url
                else:
                    se = self.config.get("search_engine", "google")
                    engines = {
                        "google": "https://www.google.com/search?q=",
                        "yandex": "https://yandex.ru/search/?text=",
                        "bing": "https://www.bing.com/search?q=",
                        "duckduckgo": "https://duckduckgo.com/?q=",
                        "brave": "https://search.brave.com/search?q="
                    }
                    url = engines.get(se, engines["google"]) + url.replace(" ", "+")
            view.load(QUrl(url))

    def open_settings(self):
        """Открывает страницу настроек"""
        view = self.current_view()
        if view:
            view.load(QUrl.fromLocalFile(SETTINGS_HTML))

    def _on_download(self, download: QWebEngineDownloadItem):
        """Обработчик загрузок"""
        dl_path = self.config.get("download_path", DOWNLOADS_DIR)
        filename = os.path.basename(download.path())
        dest = os.path.join(dl_path, filename)
        download.setPath(dest)
        download.accept()
        download.finished.connect(lambda: self._status.showMessage(f"Downloaded: {filename}", 5000))

    def _check_updates(self):
        """Проверяет обновления"""
        update_data = self.updater.check_for_updates()
        if update_data and self.updater.update_available:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"New version {update_data.get('version')} is available!\n\nUpdate now?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                success = self.updater.apply_update(update_data)
                if success:
                    QMessageBox.information(self, "Update Complete", 
                        "Browser updated! Please restart.")
                else:
                    QMessageBox.warning(self, "Update Failed", 
                        "Could not complete the update.")

    def _setup_shortcuts(self):
        """Горячие клавиши"""
        shortcuts = [
            ("Ctrl+T", lambda: self.add_tab("sti://newtab")),
            ("Ctrl+W", lambda: self.close_tab(self._tabs.currentIndex())),
            ("Ctrl+R", lambda: self.current_view() and self.current_view().reload()),
            ("F5", lambda: self.current_view() and self.current_view().reload()),
            ("Ctrl+,", self.open_settings),
            ("Ctrl+Q", self.close),
        ]
        for keys, func in shortcuts:
            QShortcut(QKeySequence(keys), self, func)

    def _apply_dark_stylesheet(self):
        """Применяет темную тему к окну"""
        self.setStyleSheet("""
        QMainWindow {
            background: #1e1e1e;
        }
        QWidget {
            background: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Segoe UI', -apple-system, system-ui, sans-serif;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: none;
            background: #1e1e1e;
        }
        QTabBar::tab {
            background: #252526;
            color: #9d9d9d;
            padding: 6px 16px;
            border: none;
            border-bottom: 2px solid transparent;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #2a2a2c;
            color: #e0e0e0;
            border-bottom: 2px solid #4da3e0;
        }
        QTabBar::tab:hover {
            background: #38383a;
        }
        QTabBar::close-button {
            image: none;
        }
        QProgressBar {
            background: transparent;
            border: none;
            max-height: 3px;
        }
        QProgressBar::chunk {
            background: #4da3e0;
        }
        QStatusBar {
            background: #252526;
            color: #9d9d9d;
            border-top: 1px solid #3e3e42;
            font-size: 11px;
            padding: 2px 8px;
        }
        QMenu {
            background: #2a2a2c;
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
        """)

    def closeEvent(self, event):
        """Закрытие приложения"""
        event.accept()


def main():
    """Точка входа"""
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("STI Browser")
    app.setOrganizationName("STI")
    app.setApplicationVersion("2.0.0")

    window = STIBrowser()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
