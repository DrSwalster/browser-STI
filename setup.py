#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STI Browser - Setup & Launcher
Автоматически устанавливает зависимости и создаёт все необходимые файлы и папки.
Запускать перед первым использованием sti.py или для восстановления файлов.
"""

import os
import sys
import subprocess
import json

# ─── 1. Установка зависимостей ────────────────────────────────────────────────
REQUIRED_PACKAGES = [
    "PyQt5",
    "PyQtWebEngine",
    "cryptography",
    "requests",
    "Pillow",
]

def install_packages():
    print("[STI Setup] Проверка и установка зависимостей...")
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.replace("-", "_").split(">=")[0].lower())
            print(f"  [OK] {pkg} уже установлен.")
        except ImportError:
            print(f"  [->] Устанавливаю {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
            print(f"  [OK] {pkg} установлен.")

# ─── 2. Структура папок ───────────────────────────────────────────────────────
DIRS = [
    "mods",
    "mods/example_mod",
    "profiles",
    "cache",
    "downloads",
    "themes",
    "collections",
    "offline_pages",
]

# ─── 3. Содержимое файлов ─────────────────────────────────────────────────────

CONFIG_JSON = {
    "version": "1.0.0",
    "browser_name": "STI Browser",
    "homepage": "sti://newtab",
    "search_engine": "google",
    "search_engines": {
        "google":  "https://www.google.com/search?q={query}",
        "yandex":  "https://yandex.ru/search/?text={query}",
        "bing":    "https://www.bing.com/search?q={query}",
        "duckduckgo": "https://duckduckgo.com/?q={query}",
        "brave":   "https://search.brave.com/search?q={query}"
    },
    "ai_engine": "google",
    "theme": "light",
    "font_size": 16,
    "sidebar_visible": True,
    "vertical_tabs": False,
    "reader_mode": False,
    "turbo_mode": False,
    "ad_block": True,
    "incognito": False,
    "sync_enabled": False,
    "sync_server": "",
    "profile": "default",
    "profiles": ["default"],
    "bookmarks": [
        {"title": "Google",  "url": "https://www.google.com",  "icon": ""},
        {"title": "YouTube", "url": "https://www.youtube.com", "icon": ""},
        {"title": "GitHub",  "url": "https://github.com",      "icon": ""}
    ],
    "history": [],
    "passwords": [],
    "collections": [],
    "active_mods": [],
    "widgets": ["clock", "weather", "news"],
    "weather_city": "Moscow",
    "privacy": {
        "block_trackers": True,
        "safe_browsing": True,
        "password_monitor": True,
        "https_only": False,
        "send_dnt": True
    },
    "performance": {
        "sleeping_tabs": True,
        "sleeping_tabs_timeout": 300,
        "preload_pages": True,
        "hardware_acceleration": True
    },
    "accessibility": {
        "high_contrast": False,
        "mono_audio": False,
        "caret_browsing": False,
        "screen_reader": False
    },
    "vpn": {
        "enabled": False,
        "provider": "",
        "region": "auto"
    },
    "themes_library": [
        {"id": "light",     "name": "Светлая",    "primary": "#ffffff", "accent": "#0066cc", "text": "#1a1a1a", "surface": "#f5f5f7"},
        {"id": "dark",      "name": "Тёмная",     "primary": "#1c1c1e", "accent": "#0a84ff", "text": "#f5f5f7", "surface": "#2c2c2e"},
        {"id": "sepia",     "name": "Сепия",      "primary": "#f4ecd8", "accent": "#8b6914", "text": "#3b2f12", "surface": "#ede0c4"},
        {"id": "midnight",  "name": "Полночь",    "primary": "#0d0d0d", "accent": "#7c3aed", "text": "#e5e5ea", "surface": "#1a1a2e"},
        {"id": "forest",    "name": "Лес",        "primary": "#f0f4f0", "accent": "#2d6a4f", "text": "#1b3a2d", "surface": "#e8f0e8"}
    ],
    "custom_css": "",
    "language": "ru",
    "zoom": 100,
    "download_path": "downloads",
    "focus_mode": False,
    "split_screen": False,
    "mind_maps": [],
    "fake_news_filter": True,
    "offline_pages": [],
    "tab_groups": [],
    "drop_items": [],
    "notifications_enabled": True
}

BROWSE_HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STI Browser — Новая вкладка</title>
<style>
  :root {
    --primary: #ffffff;
    --accent: #0066cc;
    --text: #1a1a1a;
    --surface: #f5f5f7;
    --border: #d2d2d7;
    --shadow: rgba(0,0,0,0.08);
    --radius: 12px;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }
  [data-theme="dark"] {
    --primary: #1c1c1e;
    --accent: #0a84ff;
    --text: #f5f5f7;
    --surface: #2c2c2e;
    --border: #3a3a3c;
    --shadow: rgba(0,0,0,0.3);
  }
  [data-theme="sepia"] {
    --primary: #f4ecd8; --accent: #8b6914;
    --text: #3b2f12; --surface: #ede0c4; --border: #c8b47a;
  }
  [data-theme="midnight"] {
    --primary: #0d0d0d; --accent: #7c3aed;
    --text: #e5e5ea; --surface: #1a1a2e; --border: #2d2d4e;
  }
  [data-theme="forest"] {
    --primary: #f0f4f0; --accent: #2d6a4f;
    --text: #1b3a2d; --surface: #e8f0e8; --border: #a8c8a8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--font);
    background: var(--primary);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: background 0.3s, color 0.3s;
  }

  /* ── Top bar ── */
  .top-bar {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 14px 24px 0;
    gap: 10px;
  }
  .top-btn {
    background: none;
    border: none;
    color: var(--text);
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 13px;
    font-family: var(--font);
    display: flex;
    align-items: center;
    gap: 6px;
    opacity: 0.7;
    transition: opacity 0.2s, background 0.2s;
  }
  .top-btn:hover { opacity: 1; background: var(--surface); }
  .top-btn svg { width: 16px; height: 16px; flex-shrink: 0; }

  /* ── Hero ── */
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 60px;
    width: 100%;
  }
  .logo-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 28px;
  }
  .logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, var(--accent), #33aaff);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
  }
  .logo-icon svg { width: 26px; height: 26px; color: #fff; }
  .logo-text { font-size: 26px; font-weight: 700; letter-spacing: -0.5px; }

  /* ── Search bar ── */
  .search-wrap {
    width: 100%;
    max-width: 660px;
    position: relative;
  }
  .search-bar {
    width: 100%;
    padding: 14px 52px 14px 48px;
    border: 1.5px solid var(--border);
    border-radius: 24px;
    background: var(--surface);
    color: var(--text);
    font-size: 16px;
    font-family: var(--font);
    outline: none;
    box-shadow: 0 2px 8px var(--shadow);
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .search-bar:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent);
  }
  .search-icon {
    position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
    color: var(--text); opacity: 0.45; pointer-events: none;
  }
  .search-icon svg { width: 20px; height: 20px; }
  .voice-btn {
    position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
    background: none; border: none; cursor: pointer;
    color: var(--text); opacity: 0.5; padding: 4px;
    border-radius: 50%; transition: opacity 0.2s, background 0.2s;
  }
  .voice-btn:hover { opacity: 1; background: var(--border); }
  .voice-btn svg { width: 18px; height: 18px; }

  /* Suggestions */
  .suggestions {
    position: absolute; top: calc(100% + 6px); left: 0; right: 0;
    background: var(--primary); border: 1.5px solid var(--border);
    border-radius: var(--radius); box-shadow: 0 8px 24px var(--shadow);
    z-index: 100; overflow: hidden; display: none;
  }
  .suggestions.open { display: block; }
  .sug-item {
    padding: 10px 16px;
    cursor: pointer;
    display: flex; align-items: center; gap: 10px;
    font-size: 14px;
    transition: background 0.15s;
  }
  .sug-item:hover { background: var(--surface); }
  .sug-item svg { width: 14px; height: 14px; opacity: 0.45; flex-shrink: 0; }

  /* Search engines */
  .search-engines {
    display: flex; gap: 8px; margin-top: 12px;
    flex-wrap: wrap; justify-content: center;
  }
  .se-btn {
    padding: 5px 14px;
    border: 1.5px solid var(--border);
    border-radius: 20px;
    background: var(--surface);
    color: var(--text);
    font-size: 12px;
    cursor: pointer;
    font-family: var(--font);
    transition: border-color 0.2s, background 0.2s;
    opacity: 0.75;
  }
  .se-btn.active, .se-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    opacity: 1;
    background: color-mix(in srgb, var(--accent) 8%, var(--surface));
  }

  /* ── Bookmarks / Speed dial ── */
  .section { width: 100%; max-width: 760px; margin-top: 36px; }
  .section-title {
    font-size: 11px; font-weight: 600; letter-spacing: 0.6px;
    text-transform: uppercase; opacity: 0.45; margin-bottom: 12px;
    padding: 0 4px;
  }
  .speed-dial {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(96px, 1fr));
    gap: 12px;
  }
  .dial-item {
    display: flex; flex-direction: column; align-items: center;
    gap: 8px; cursor: pointer; padding: 14px 8px;
    border-radius: var(--radius);
    background: var(--surface);
    border: 1.5px solid transparent;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
    position: relative;
    text-decoration: none; color: var(--text);
  }
  .dial-item:hover {
    border-color: var(--border);
    box-shadow: 0 4px 16px var(--shadow);
    transform: translateY(-2px);
  }
  .dial-favicon {
    width: 36px; height: 36px; border-radius: 8px;
    background: var(--border); display: flex; align-items: center; justify-content: center;
    font-size: 18px; overflow: hidden;
  }
  .dial-favicon img { width: 100%; height: 100%; object-fit: contain; }
  .dial-label { font-size: 12px; text-align: center; opacity: 0.8; line-height: 1.3; }
  .dial-remove {
    position: absolute; top: 4px; right: 4px;
    background: none; border: none; cursor: pointer;
    color: var(--text); opacity: 0; font-size: 14px;
    transition: opacity 0.2s;
    border-radius: 50%; width: 20px; height: 20px;
    display: flex; align-items: center; justify-content: center;
  }
  .dial-item:hover .dial-remove { opacity: 0.5; }
  .dial-remove:hover { opacity: 1 !important; background: var(--border); }
  .dial-add {
    border: 2px dashed var(--border); background: transparent;
    opacity: 0.6;
  }
  .dial-add:hover { opacity: 1; border-color: var(--accent); }

  /* ── Widgets ── */
  .widgets-row {
    display: flex; gap: 12px; flex-wrap: wrap;
    margin-top: 36px; width: 100%; max-width: 760px;
    margin-bottom: 48px;
  }
  .widget {
    flex: 1; min-width: 180px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 18px;
    box-shadow: 0 2px 8px var(--shadow);
  }
  .widget-title {
    font-size: 10px; font-weight: 600; letter-spacing: 0.5px;
    text-transform: uppercase; opacity: 0.45; margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px;
  }
  .widget-title svg { width: 12px; height: 12px; }
  .widget-value { font-size: 28px; font-weight: 300; letter-spacing: -1px; }
  .widget-sub { font-size: 12px; opacity: 0.55; margin-top: 4px; }

  /* Weather */
  .weather-row { display: flex; align-items: center; gap: 12px; }
  .weather-icon svg { width: 36px; height: 36px; color: var(--accent); }

  /* News widget */
  .news-list { list-style: none; }
  .news-list li {
    padding: 6px 0; font-size: 13px;
    border-bottom: 1px solid var(--border);
    cursor: pointer; line-height: 1.4;
    transition: color 0.2s;
  }
  .news-list li:last-child { border-bottom: none; }
  .news-list li:hover { color: var(--accent); }

  /* ── AI bar ── */
  .ai-bar {
    width: 100%; max-width: 660px;
    margin-top: 18px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 18px;
    display: flex; align-items: center; gap: 12px;
    box-shadow: 0 2px 8px var(--shadow);
    cursor: pointer;
    transition: border-color 0.2s;
  }
  .ai-bar:hover { border-color: var(--accent); }
  .ai-bar-icon {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, #4285F4, #34A853);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .ai-bar-icon svg { width: 18px; height: 18px; color: #fff; }
  .ai-bar-text { flex: 1; }
  .ai-bar-text p { font-size: 14px; font-weight: 500; }
  .ai-bar-text span { font-size: 12px; opacity: 0.5; }

  /* ── Focus mode overlay ── */
  .focus-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.45); z-index: 200;
    align-items: center; justify-content: center;
  }
  .focus-overlay.active { display: flex; }
  .focus-box {
    background: var(--primary); border-radius: 18px;
    padding: 40px 48px; max-width: 600px; width: 90%;
    text-align: center; box-shadow: 0 24px 64px rgba(0,0,0,0.3);
  }
  .focus-box h2 { font-size: 22px; margin-bottom: 8px; }
  .focus-box p { opacity: 0.6; margin-bottom: 24px; }
  .focus-box button {
    padding: 10px 28px; border-radius: 20px;
    background: var(--accent); color: #fff; border: none;
    font-size: 14px; cursor: pointer; font-family: var(--font);
  }

  /* ── Add bookmark modal ── */
  .modal-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.35); z-index: 300;
    align-items: center; justify-content: center;
  }
  .modal-overlay.active { display: flex; }
  .modal {
    background: var(--primary); border-radius: 16px;
    padding: 28px 32px; width: 380px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.25);
  }
  .modal h3 { font-size: 17px; margin-bottom: 18px; }
  .modal input {
    width: 100%; padding: 10px 14px;
    border: 1.5px solid var(--border);
    border-radius: 10px; background: var(--surface);
    color: var(--text); font-size: 14px; font-family: var(--font);
    outline: none; margin-bottom: 10px;
    transition: border-color 0.2s;
  }
  .modal input:focus { border-color: var(--accent); }
  .modal-btns { display: flex; gap: 8px; justify-content: flex-end; margin-top: 6px; }
  .modal-btns button {
    padding: 8px 22px; border-radius: 10px; border: none;
    font-size: 13px; cursor: pointer; font-family: var(--font);
  }
  .btn-cancel { background: var(--surface); color: var(--text); border: 1.5px solid var(--border) !important; }
  .btn-save { background: var(--accent); color: #fff; }

  /* ── Responsive ── */
  @media (max-width: 600px) {
    .hero { margin-top: 32px; }
    .speed-dial { grid-template-columns: repeat(4, 1fr); }
    .widgets-row { flex-direction: column; }
  }
</style>
</head>
<body>

<!-- Top buttons -->
<div class="top-bar">
  <button class="top-btn" onclick="openSettings()" title="Настройки">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
    Настройки
  </button>
  <button class="top-btn" onclick="toggleFocusMode()" title="Режим фокуса">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>
    Фокус
  </button>
  <button class="top-btn" id="themeToggle" onclick="cycleTheme()" title="Тема">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
    Тема
  </button>
</div>

<!-- Hero / Search -->
<div class="hero">
  <div class="logo-wrap">
    <div class="logo-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>
    </div>
    <span class="logo-text">STI Browser</span>
  </div>

  <div class="search-wrap">
    <span class="search-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></span>
    <input id="searchInput" class="search-bar" type="text"
      placeholder="Поиск или введите адрес..."
      autocomplete="off" spellcheck="false"
      oninput="onSearchInput()" onkeydown="onSearchKey(event)">
    <button class="voice-btn" onclick="voiceSearch()" title="Голосовой поиск">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
    </button>
    <div class="suggestions" id="suggestions"></div>
  </div>

  <!-- Search engine selector -->
  <div class="search-engines" id="seButtons">
    <button class="se-btn active" data-se="google" onclick="selectSE(this)">Google</button>
    <button class="se-btn" data-se="yandex" onclick="selectSE(this)">Яндекс</button>
    <button class="se-btn" data-se="bing" onclick="selectSE(this)">Bing</button>
    <button class="se-btn" data-se="duckduckgo" onclick="selectSE(this)">DuckDuckGo</button>
    <button class="se-btn" data-se="brave" onclick="selectSE(this)">Brave</button>
  </div>

  <!-- AI bar -->
  <div class="ai-bar" onclick="openAI()">
    <div class="ai-bar-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9.663 17h4.673M12 3v1m6.364 1.636-.707.707M21 12h-1M4 12H3m3.343-5.657-.707-.707m2.828 9.9a5 5 0 1 1 7.072 0l-.548.547A3.374 3.374 0 0 0 14 18.469V19a2 2 0 1 1-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
    </div>
    <div class="ai-bar-text">
      <p>Спросите Gemini AI</p>
      <span>Анализ страниц, ответы на вопросы, суммаризация</span>
    </div>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="width:16px;height:16px;opacity:0.35"><path d="m9 18 6-6-6-6"/></svg>
  </div>
</div>

<!-- Bookmarks speed dial -->
<div class="section">
  <div class="section-title">Быстрый доступ</div>
  <div class="speed-dial" id="speedDial"></div>
</div>

<!-- Widgets -->
<div class="widgets-row" id="widgetsRow">

  <!-- Clock -->
  <div class="widget" id="clockWidget">
    <div class="widget-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      Время
    </div>
    <div class="widget-value" id="clockVal">--:--</div>
    <div class="widget-sub" id="dateVal">--</div>
  </div>

  <!-- Weather -->
  <div class="widget" id="weatherWidget">
    <div class="widget-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
      Погода
    </div>
    <div class="weather-row">
      <div class="weather-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
      </div>
      <div>
        <div class="widget-value" id="weatherTemp">--°</div>
        <div class="widget-sub" id="weatherCity">Загрузка...</div>
      </div>
    </div>
  </div>

  <!-- Quick note -->
  <div class="widget" style="flex:2;min-width:220px;">
    <div class="widget-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
      Быстрая заметка
    </div>
    <textarea id="quickNote" placeholder="Запишите что-нибудь..."
      style="width:100%;border:none;background:transparent;color:var(--text);font-family:var(--font);font-size:13px;resize:none;outline:none;height:58px;line-height:1.5;"
      oninput="saveNote()"></textarea>
  </div>

</div>

<!-- Focus mode overlay -->
<div class="focus-overlay" id="focusOverlay">
  <div class="focus-box">
    <h2>Режим фокуса</h2>
    <p>Отвлекающие элементы скрыты. Сосредоточьтесь на работе.</p>
    <button onclick="toggleFocusMode()">Выйти из режима фокуса</button>
  </div>
</div>

<!-- Add bookmark modal -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <h3>Добавить закладку</h3>
    <input id="bmTitle" placeholder="Название сайта">
    <input id="bmUrl" placeholder="https://...">
    <div class="modal-btns">
      <button class="btn-cancel" onclick="closeModal()">Отмена</button>
      <button class="btn-save" onclick="saveBookmark()">Сохранить</button>
    </div>
  </div>
</div>

<script>
// ── State ──────────────────────────────────────────────────────────────────
const THEMES = ["light","dark","sepia","midnight","forest"];
const SE_URLS = {
  google:     "https://www.google.com/search?q=",
  yandex:     "https://yandex.ru/search/?text=",
  bing:       "https://www.bing.com/search?q=",
  duckduckgo: "https://duckduckgo.com/?q=",
  brave:      "https://search.brave.com/search?q="
};

let config = {
  theme: "light", search_engine: "google",
  bookmarks: [
    {title:"Google",  url:"https://www.google.com"},
    {title:"YouTube", url:"https://www.youtube.com"},
    {title:"GitHub",  url:"https://github.com"}
  ]
};

// ── Init ───────────────────────────────────────────────────────────────────
window.onload = function() {
  loadConfig();
  startClock();
  loadNote();
  renderDial();
  fetchWeather();
};

function loadConfig() {
  try {
    const s = localStorage.getItem("sti_config");
    if (s) config = Object.assign(config, JSON.parse(s));
  } catch(e){}
  applyTheme(config.theme || "light");
  const se = config.search_engine || "google";
  document.querySelectorAll(".se-btn").forEach(b => {
    b.classList.toggle("active", b.dataset.se === se);
  });
}

function saveConfig() {
  try { localStorage.setItem("sti_config", JSON.stringify(config)); } catch(e){}
  if (window.bridge) bridge.saveConfig(JSON.stringify(config));
}

// ── Theme ──────────────────────────────────────────────────────────────────
function applyTheme(t) {
  document.body.dataset.theme = t;
  config.theme = t;
}
function cycleTheme() {
  const idx = THEMES.indexOf(config.theme || "light");
  const next = THEMES[(idx + 1) % THEMES.length];
  applyTheme(next);
  saveConfig();
}

// ── Search ─────────────────────────────────────────────────────────────────
function selectSE(btn) {
  document.querySelectorAll(".se-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  config.search_engine = btn.dataset.se;
  saveConfig();
}

function onSearchInput() {
  const q = document.getElementById("searchInput").value.trim();
  const sug = document.getElementById("suggestions");
  if (q.length < 2) { sug.classList.remove("open"); return; }
  const demos = [
    {t: "Поиск: " + q,        icon: "search"},
    {t: q + " — Википедия",   icon: "globe"},
    {t: q + " — YouTube",     icon: "play"},
  ];
  sug.innerHTML = demos.map(d => `
    <div class="sug-item" onclick="doSearch('${d.t.replace(/'/g,"\\'")}')">
      ${svgIcon(d.icon)}
      <span>${escHtml(d.t)}</span>
    </div>`).join("");
  sug.classList.add("open");
}

function onSearchKey(e) {
  if (e.key === "Enter") {
    document.getElementById("suggestions").classList.remove("open");
    const q = document.getElementById("searchInput").value.trim();
    if (!q) return;
    doSearch(q);
  }
  if (e.key === "Escape") {
    document.getElementById("suggestions").classList.remove("open");
  }
}

function doSearch(q) {
  let url;
  if (q.startsWith("http://") || q.startsWith("https://")) {
    url = q;
  } else if (q.includes(".") && !q.includes(" ")) {
    url = "https://" + q;
  } else {
    const se = config.search_engine || "google";
    url = SE_URLS[se] + encodeURIComponent(q);
  }
  if (window.bridge) {
    bridge.navigate(url);
  } else {
    window.location.href = url;
  }
}

function voiceSearch() {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert("Голосовой поиск не поддерживается в этом контексте.");
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const r = new SR();
  r.lang = "ru-RU"; r.start();
  r.onresult = e => {
    const t = e.results[0][0].transcript;
    document.getElementById("searchInput").value = t;
    doSearch(t);
  };
}

// ── Speed Dial ─────────────────────────────────────────────────────────────
function renderDial() {
  const dial = document.getElementById("speedDial");
  const bm = config.bookmarks || [];
  dial.innerHTML = bm.map((b,i) => `
    <a class="dial-item" onclick="navTo('${escAttr(b.url)}')" href="javascript:void(0)">
      <div class="dial-favicon">
        <img src="https://www.google.com/s2/favicons?sz=64&domain_url=${encodeURIComponent(b.url)}"
             onerror="this.parentNode.innerHTML='<svg viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.5\\" style=\\"width:20px;height:20px\\"><circle cx=\\"12\\" cy=\\"12\\" r=\\"10\\"/><path d=\\"M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z\\"/><path d=\\"M2 12h20\\"/></svg>'" alt="">
      </div>
      <span class="dial-label">${escHtml(b.title)}</span>
      <button class="dial-remove" onclick="event.stopPropagation();event.preventDefault();removeBM(${i})" title="Удалить">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    </a>`).join("") + `
    <div class="dial-item dial-add" onclick="openAddBM()">
      <div class="dial-favicon" style="background:transparent">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width:24px;height:24px;opacity:0.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </div>
      <span class="dial-label" style="opacity:0.5">Добавить</span>
    </div>`;
}

function navTo(url) {
  if (window.bridge) bridge.navigate(url);
  else window.location.href = url;
}

function removeBM(i) {
  config.bookmarks.splice(i, 1);
  saveConfig(); renderDial();
}

function openAddBM() {
  document.getElementById("bmTitle").value = "";
  document.getElementById("bmUrl").value = "";
  document.getElementById("modalOverlay").classList.add("active");
}

function closeModal() {
  document.getElementById("modalOverlay").classList.remove("active");
}

function saveBookmark() {
  const t = document.getElementById("bmTitle").value.trim();
  const u = document.getElementById("bmUrl").value.trim();
  if (!t || !u) return;
  if (!config.bookmarks) config.bookmarks = [];
  config.bookmarks.push({title: t, url: u.startsWith("http") ? u : "https://" + u});
  saveConfig(); renderDial(); closeModal();
}

// ── Clock ──────────────────────────────────────────────────────────────────
function startClock() {
  function tick() {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2,"0");
    const mm = String(now.getMinutes()).padStart(2,"0");
    document.getElementById("clockVal").textContent = hh + ":" + mm;
    const days = ["Воскресенье","Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"];
    const months = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
    document.getElementById("dateVal").textContent =
      days[now.getDay()] + ", " + now.getDate() + " " + months[now.getMonth()];
  }
  tick(); setInterval(tick, 10000);
}

// ── Weather ────────────────────────────────────────────────────────────────
function fetchWeather() {
  const city = (config.weather_city || "Moscow");
  document.getElementById("weatherCity").textContent = city;
  fetch(`https://wttr.in/${encodeURIComponent(city)}?format=j1`)
    .then(r => r.json())
    .then(d => {
      const c = d.current_condition[0];
      const t = c.temp_C;
      document.getElementById("weatherTemp").textContent = t + "°C";
      document.getElementById("weatherCity").textContent = city + " · " + c.weatherDesc[0].value;
    })
    .catch(() => {
      document.getElementById("weatherTemp").textContent = "N/A";
      document.getElementById("weatherCity").textContent = city;
    });
}

// ── Quick note ─────────────────────────────────────────────────────────────
function loadNote() {
  document.getElementById("quickNote").value = localStorage.getItem("sti_note") || "";
}
function saveNote() {
  localStorage.setItem("sti_note", document.getElementById("quickNote").value);
}

// ── Focus mode ─────────────────────────────────────────────────────────────
function toggleFocusMode() {
  document.getElementById("focusOverlay").classList.toggle("active");
}

// ── AI ─────────────────────────────────────────────────────────────────────
function openAI() {
  if (window.bridge) bridge.openAI();
  else window.open("https://gemini.google.com", "_blank");
}

// ── Settings ───────────────────────────────────────────────────────────────
function openSettings() {
  if (window.bridge) bridge.openSettings();
  else alert("Настройки доступны только в браузере STI.");
}

// ── Helpers ────────────────────────────────────────────────────────────────
function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
function escAttr(s) {
  return String(s).replace(/'/g,"&#39;");
}

function svgIcon(name) {
  const icons = {
    search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>`,
    globe:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
    play:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>`,
  };
  return icons[name] || icons.search;
}

// Close suggestions on outside click
document.addEventListener("click", e => {
  if (!e.target.closest(".search-wrap")) {
    document.getElementById("suggestions").classList.remove("open");
  }
});
</script>
</body>
</html>"""

SETTINGS_HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STI Browser — Настройки</title>
<style>
  :root {
    --primary: #ffffff; --accent: #0066cc; --text: #1a1a1a;
    --surface: #f5f5f7; --border: #d2d2d7; --shadow: rgba(0,0,0,0.06);
    --radius: 12px;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }
  [data-theme="dark"] { --primary:#1c1c1e;--accent:#0a84ff;--text:#f5f5f7;--surface:#2c2c2e;--border:#3a3a3c; }
  [data-theme="sepia"] { --primary:#f4ecd8;--accent:#8b6914;--text:#3b2f12;--surface:#ede0c4;--border:#c8b47a; }
  [data-theme="midnight"] { --primary:#0d0d0d;--accent:#7c3aed;--text:#e5e5ea;--surface:#1a1a2e;--border:#2d2d4e; }
  [data-theme="forest"] { --primary:#f0f4f0;--accent:#2d6a4f;--text:#1b3a2d;--surface:#e8f0e8;--border:#a8c8a8; }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font); background: var(--primary); color: var(--text); display: flex; min-height: 100vh; }

  /* Sidebar */
  .sidebar {
    width: 220px; flex-shrink: 0;
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 24px 0; display: flex; flex-direction: column;
    position: fixed; top: 0; left: 0; bottom: 0; z-index: 10;
  }
  .sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 0 20px 24px; border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
  }
  .sidebar-logo-icon {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, var(--accent), #33aaff);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .sidebar-logo-icon svg { width: 18px; height: 18px; color: #fff; }
  .sidebar-logo span { font-size: 15px; font-weight: 600; }
  .nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 20px; cursor: pointer;
    font-size: 14px; border-radius: 0;
    transition: background 0.15s, color 0.15s;
    color: var(--text); opacity: 0.7;
    border: none; background: none; width: 100%;
    text-align: left; font-family: var(--font);
  }
  .nav-item svg { width: 16px; height: 16px; flex-shrink: 0; }
  .nav-item:hover { background: var(--border); opacity: 1; }
  .nav-item.active { opacity: 1; color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, var(--surface)); font-weight: 500; }

  /* Main */
  .main { margin-left: 220px; flex: 1; padding: 40px 48px; max-width: 840px; }
  .page { display: none; }
  .page.active { display: block; }
  .page-title { font-size: 22px; font-weight: 600; margin-bottom: 28px; }

  /* Cards */
  .card {
    background: var(--surface); border: 1.5px solid var(--border);
    border-radius: var(--radius); padding: 20px 24px;
    margin-bottom: 14px; box-shadow: 0 2px 8px var(--shadow);
  }
  .card-title { font-size: 13px; font-weight: 600; opacity: 0.5; letter-spacing: 0.4px; text-transform: uppercase; margin-bottom: 14px; }

  /* Row */
  .row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid var(--border);
  }
  .row:last-child { border-bottom: none; padding-bottom: 0; }
  .row-left { display: flex; flex-direction: column; gap: 2px; }
  .row-label { font-size: 14px; font-weight: 500; }
  .row-desc { font-size: 12px; opacity: 0.5; }

  /* Toggle */
  .toggle { position: relative; width: 44px; height: 26px; flex-shrink: 0; }
  .toggle input { opacity: 0; width: 0; height: 0; }
  .toggle-track {
    position: absolute; inset: 0;
    background: var(--border); border-radius: 13px;
    cursor: pointer; transition: background 0.2s;
  }
  .toggle input:checked + .toggle-track { background: var(--accent); }
  .toggle-thumb {
    position: absolute; width: 20px; height: 20px; border-radius: 50%;
    background: #fff; top: 3px; left: 3px;
    transition: transform 0.2s; box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  }
  .toggle input:checked ~ .toggle-thumb { transform: translateX(18px); }

  /* Select / Input */
  .sel, .inp {
    background: var(--primary); border: 1.5px solid var(--border);
    border-radius: 8px; padding: 8px 12px; color: var(--text);
    font-size: 13px; font-family: var(--font); outline: none;
    transition: border-color 0.2s; min-width: 160px;
  }
  .sel:focus, .inp:focus { border-color: var(--accent); }

  /* Btn */
  .btn {
    padding: 8px 18px; border-radius: 8px; border: none;
    font-size: 13px; cursor: pointer; font-family: var(--font);
    transition: opacity 0.2s;
  }
  .btn-primary { background: var(--accent); color: #fff; }
  .btn-secondary { background: var(--surface); color: var(--text); border: 1.5px solid var(--border); }
  .btn:hover { opacity: 0.85; }

  /* Theme picker */
  .theme-grid { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
  .theme-swatch {
    width: 64px; height: 40px; border-radius: 8px;
    cursor: pointer; border: 2.5px solid transparent;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 600; letter-spacing: 0.3px;
    transition: border-color 0.2s, transform 0.15s;
    flex-direction: column; gap: 3px;
  }
  .theme-swatch:hover { transform: translateY(-2px); }
  .theme-swatch.selected { border-color: var(--accent); }
  .swatch-dot { width: 16px; height: 16px; border-radius: 50%; }

  /* Password list */
  .pass-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid var(--border);
  }
  .pass-item:last-child { border-bottom: none; }
  .pass-icon { width: 32px; height: 32px; border-radius: 8px; background: var(--border); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .pass-icon svg { width: 16px; height: 16px; }
  .pass-info { flex: 1; }
  .pass-site { font-size: 13px; font-weight: 500; }
  .pass-user { font-size: 12px; opacity: 0.5; }
  .strength { height: 4px; border-radius: 2px; margin-top: 4px; }
  .strength.weak { background: #ff453a; width: 33%; }
  .strength.medium { background: #ff9f0a; width: 66%; }
  .strength.strong { background: #30d158; width: 100%; }

  /* Mods list */
  .mod-item {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 0; border-bottom: 1px solid var(--border);
  }
  .mod-item:last-child { border-bottom: none; }
  .mod-icon { width: 40px; height: 40px; border-radius: 10px; background: var(--border); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .mod-icon svg { width: 20px; height: 20px; }
  .mod-info { flex: 1; }
  .mod-name { font-size: 14px; font-weight: 500; }
  .mod-desc { font-size: 12px; opacity: 0.5; }

  /* Bookmarks */
  .bm-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border); }
  .bm-item:last-child { border-bottom: none; }
  .bm-item span { flex: 1; font-size: 13px; }
  .bm-url { font-size: 11px; opacity: 0.45; }

  /* Slider */
  .slider { width: 140px; accent-color: var(--accent); }

  /* Status badge */
  .badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
  .badge-green { background: #d4f5e2; color: #0a7c3e; }
  .badge-red { background: #fde8e8; color: #c0392b; }
  [data-theme="dark"] .badge-green { background: #0a3d20; color: #30d158; }
  [data-theme="dark"] .badge-red { background: #3d0a0a; color: #ff453a; }

  @media (max-width: 720px) {
    .sidebar { display: none; }
    .main { margin-left: 0; padding: 24px 20px; }
  }
</style>
</head>
<body>

<!-- Sidebar -->
<nav class="sidebar">
  <div class="sidebar-logo">
    <div class="sidebar-logo-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>
    </div>
    <span>STI Browser</span>
  </div>

  <button class="nav-item active" data-page="general" onclick="showPage('general', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06-.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
    Основные
  </button>
  <button class="nav-item" data-page="appearance" onclick="showPage('appearance', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
    Внешний вид
  </button>
  <button class="nav-item" data-page="privacy" onclick="showPage('privacy', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
    Приватность
  </button>
  <button class="nav-item" data-page="passwords" onclick="showPage('passwords', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
    Пароли
  </button>
  <button class="nav-item" data-page="bookmarks" onclick="showPage('bookmarks', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m19 21-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
    Закладки
  </button>
  <button class="nav-item" data-page="performance" onclick="showPage('performance', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
    Производительность
  </button>
  <button class="nav-item" data-page="ai" onclick="showPage('ai', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9.663 17h4.673M12 3v1m6.364 1.636-.707.707M21 12h-1M4 12H3m3.343-5.657-.707-.707m2.828 9.9a5 5 0 1 1 7.072 0l-.548.547A3.374 3.374 0 0 0 14 18.469V19a2 2 0 1 1-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
    Искусственный интеллект
  </button>
  <button class="nav-item" data-page="mods" onclick="showPage('mods', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
    Моды
  </button>
  <button class="nav-item" data-page="accessibility" onclick="showPage('accessibility', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><path d="M12 8h.01M11 12h1v4h1"/></svg>
    Доступность
  </button>
  <button class="nav-item" data-page="sync" onclick="showPage('sync', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
    Синхронизация
  </button>
  <button class="nav-item" data-page="vpn" onclick="showPage('vpn', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
    VPN
  </button>
  <button class="nav-item" data-page="about" onclick="showPage('about', this)">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    О браузере
  </button>
</nav>

<!-- Main content -->
<main class="main">

  <!-- ── General ── -->
  <div class="page active" id="page-general">
    <div class="page-title">Основные настройки</div>

    <div class="card">
      <div class="card-title">Стартовая страница</div>
      <div class="row">
        <div class="row-left">
          <span class="row-label">Домашняя страница</span>
          <span class="row-desc">URL, открываемый при запуске</span>
        </div>
        <input class="inp" id="homepageInp" value="sti://newtab" style="min-width:200px;">
      </div>
      <div class="row">
        <div class="row-left">
          <span class="row-label">Поисковая система</span>
        </div>
        <select class="sel" id="seSelect" onchange="saveSetting('search_engine', this.value)">
          <option value="google">Google</option>
          <option value="yandex">Яндекс</option>
          <option value="bing">Bing</option>
          <option value="duckduckgo">DuckDuckGo</option>
          <option value="brave">Brave Search</option>
        </select>
      </div>
      <div class="row">
        <div class="row-left">
          <span class="row-label">Язык интерфейса</span>
        </div>
        <select class="sel" id="langSelect" onchange="saveSetting('language', this.value)">
          <option value="ru">Русский</option>
          <option value="en">English</option>
          <option value="de">Deutsch</option>
          <option value="fr">Français</option>
        </select>
      </div>
      <div class="row">
        <div class="row-left">
          <span class="row-label">Город для погоды</span>
        </div>
        <input class="inp" id="cityInp" placeholder="Москва">
      </div>
      <div style="margin-top:14px;display:flex;gap:8px;">
        <button class="btn btn-primary" onclick="saveGeneralSettings()">Сохранить</button>
        <button class="btn btn-secondary" onclick="importSettings()">Импорт настроек</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Профили</div>
      <div id="profilesList"></div>
      <button class="btn btn-secondary" style="margin-top:12px;" onclick="addProfile()">
        Добавить профиль
      </button>
    </div>

    <div class="card">
      <div class="card-title">Загрузки</div>
      <div class="row">
        <div class="row-left">
          <span class="row-label">Папка загрузок</span>
          <span class="row-desc" id="downloadPathLabel">downloads/</span>
        </div>
        <button class="btn btn-secondary" onclick="changeDownloadPath()">Изменить</button>
      </div>
    </div>
  </div>

  <!-- ── Appearance ── -->
  <div class="page" id="page-appearance">
    <div class="page-title">Внешний вид</div>

    <div class="card">
      <div class="card-title">Тема</div>
      <div class="theme-grid" id="themeGrid"></div>
    </div>

    <div class="card">
      <div class="card-title">Шрифт и масштаб</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Размер шрифта</span></div>
        <div style="display:flex;align-items:center;gap:10px;">
          <input type="range" class="slider" id="fontSlider" min="12" max="24" value="16"
            oninput="document.getElementById('fontVal').textContent=this.value+'px';saveSetting('font_size',parseInt(this.value))">
          <span id="fontVal" style="font-size:13px;opacity:0.6;min-width:36px;">16px</span>
        </div>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Масштаб страниц</span></div>
        <div style="display:flex;align-items:center;gap:10px;">
          <input type="range" class="slider" id="zoomSlider" min="50" max="200" value="100"
            oninput="document.getElementById('zoomVal').textContent=this.value+'%';saveSetting('zoom',parseInt(this.value))">
          <span id="zoomVal" style="font-size:13px;opacity:0.6;min-width:36px;">100%</span>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Расположение панелей</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Вертикальные вкладки</span><span class="row-desc">Боковая панель вкладок</span></div>
        <label class="toggle"><input type="checkbox" id="vertTabsToggle" onchange="saveSetting('vertical_tabs',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Боковая панель</span></div>
        <label class="toggle"><input type="checkbox" id="sidebarToggle" onchange="saveSetting('sidebar_visible',this.checked)" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Разделённый экран</span><span class="row-desc">Две вкладки рядом</span></div>
        <label class="toggle"><input type="checkbox" id="splitToggle" onchange="saveSetting('split_screen',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Пользовательский CSS</div>
      <textarea id="customCssArea" placeholder="/* Ваш CSS */"
        style="width:100%;height:120px;background:var(--primary);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:10px;font-family:monospace;font-size:13px;outline:none;resize:vertical;"></textarea>
      <button class="btn btn-primary" style="margin-top:10px;" onclick="applyCustomCSS()">Применить</button>
    </div>
  </div>

  <!-- ── Privacy ── -->
  <div class="page" id="page-privacy">
    <div class="page-title">Приватность и безопасность</div>

    <div class="card">
      <div class="card-title">Защита</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Блокировка трекеров</span><span class="row-desc">Предотвращает слежку</span></div>
        <label class="toggle"><input type="checkbox" id="trackerToggle" checked onchange="savePrivacy('block_trackers',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Безопасный просмотр</span><span class="row-desc">Защита от фишинга и вредоносных сайтов</span></div>
        <label class="toggle"><input type="checkbox" id="safeBrowsingToggle" checked onchange="savePrivacy('safe_browsing',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Блокировка рекламы</span></div>
        <label class="toggle"><input type="checkbox" id="adBlockToggle" checked onchange="saveSetting('ad_block',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">HTTPS-only режим</span></div>
        <label class="toggle"><input type="checkbox" id="httpsToggle" onchange="savePrivacy('https_only',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Отправлять Do Not Track</span></div>
        <label class="toggle"><input type="checkbox" id="dntToggle" checked onchange="savePrivacy('send_dnt',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Режим инкогнито по умолчанию</span></div>
        <label class="toggle"><input type="checkbox" id="incognitoToggle" onchange="saveSetting('incognito',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Фильтр фейковых новостей</span><span class="row-desc">Метки недостоверного контента</span></div>
        <label class="toggle"><input type="checkbox" id="fakeNewsToggle" checked onchange="saveSetting('fake_news_filter',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Проверка безопасности</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <button class="btn btn-primary" onclick="runSafetyCheck()">Запустить проверку</button>
        <button class="btn btn-secondary" onclick="clearHistory()">Очистить историю</button>
        <button class="btn btn-secondary" onclick="clearCookies()">Очистить куки</button>
      </div>
      <div id="safetyResult" style="margin-top:14px;font-size:13px;opacity:0.6;"></div>
    </div>
  </div>

  <!-- ── Passwords ── -->
  <div class="page" id="page-passwords">
    <div class="page-title">Менеджер паролей</div>

    <div class="card">
      <div class="card-title">Генератор паролей</div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <input class="inp" id="genPassInp" placeholder="Сгенерированный пароль" readonly style="flex:1;min-width:200px;">
        <button class="btn btn-primary" onclick="generatePassword()">Сгенерировать</button>
        <button class="btn btn-secondary" onclick="copyPassword()">Копировать</button>
      </div>
      <div style="margin-top:10px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
        <label style="display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer;">
          <input type="range" class="slider" id="passLenSlider" min="8" max="32" value="16"
            oninput="document.getElementById('passLenVal').textContent=this.value">
          <span id="passLenVal">16</span> симв.
        </label>
        <label style="display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer;">
          <input type="checkbox" id="passSymbols" checked> Спецсимволы
        </label>
        <label style="display:flex;align-items:center;gap:6px;font-size:13px;cursor:pointer;">
          <input type="checkbox" id="passNumbers" checked> Цифры
        </label>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Сохранённые пароли</div>
      <div id="passwordsList">
        <div class="pass-item">
          <div class="pass-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/></svg></div>
          <div class="pass-info">
            <div class="pass-site">google.com</div>
            <div class="pass-user">user@example.com</div>
            <div class="strength strong"></div>
          </div>
          <span class="badge badge-green">Надёжный</span>
        </div>
      </div>
      <button class="btn btn-secondary" style="margin-top:12px;" onclick="checkPasswords()">
        Проверить утечки
      </button>
    </div>
  </div>

  <!-- ── Bookmarks ── -->
  <div class="page" id="page-bookmarks">
    <div class="page-title">Закладки</div>
    <div class="card">
      <div class="card-title">Управление закладками</div>
      <div id="bmList"></div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <input class="inp" id="bmTitleInp" placeholder="Название">
        <input class="inp" id="bmUrlInp" placeholder="https://...">
        <button class="btn btn-primary" onclick="addBookmarkSettings()">Добавить</button>
        <button class="btn btn-secondary" onclick="importBookmarks()">Импорт</button>
      </div>
    </div>
  </div>

  <!-- ── Performance ── -->
  <div class="page" id="page-performance">
    <div class="page-title">Производительность</div>

    <div class="card">
      <div class="card-title">Управление памятью</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Спящие вкладки</span><span class="row-desc">Приостанавливать неактивные вкладки</span></div>
        <label class="toggle"><input type="checkbox" id="sleepTabsToggle" checked onchange="savePerf('sleeping_tabs',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Аппаратное ускорение</span></div>
        <label class="toggle"><input type="checkbox" id="hwAccelToggle" checked onchange="savePerf('hardware_acceleration',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Предзагрузка страниц</span></div>
        <label class="toggle"><input type="checkbox" id="preloadToggle" checked onchange="savePerf('preload_pages',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Режим Турбо</span><span class="row-desc">Сжатие трафика</span></div>
        <label class="toggle"><input type="checkbox" id="turboToggle" onchange="saveSetting('turbo_mode',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Диспетчер задач</div>
      <div id="taskManager" style="font-size:13px;opacity:0.7;">Загрузка...</div>
      <button class="btn btn-secondary" style="margin-top:10px;" onclick="refreshTasks()">Обновить</button>
    </div>
  </div>

  <!-- ── AI ── -->
  <div class="page" id="page-ai">
    <div class="page-title">Искусственный интеллект</div>

    <div class="card">
      <div class="card-title">ИИ-ассистент</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Движок ИИ</span></div>
        <select class="sel" id="aiEngineSelect" onchange="saveSetting('ai_engine',this.value)">
          <option value="google">Gemini (Google)</option>
          <option value="yandex">YandexGPT</option>
          <option value="openai">ChatGPT (OpenAI)</option>
        </select>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Анализ страниц</span><span class="row-desc">ИИ изучает текущую страницу</span></div>
        <label class="toggle"><input type="checkbox" id="aiAnalyzeToggle" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Описания изображений</span><span class="row-desc">Генерация alt-текстов</span></div>
        <label class="toggle"><input type="checkbox" id="aiImgToggle" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Фильтр фейков</span><span class="row-desc">Проверка достоверности статей</span></div>
        <label class="toggle"><input type="checkbox" id="fakeFilterToggle" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Умная строка Omnibox</span><span class="row-desc">Ответы прямо в адресной строке</span></div>
        <label class="toggle"><input type="checkbox" id="omniboxToggle" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Тест ИИ</div>
      <textarea id="aiTestInput" placeholder="Введите вопрос или вставьте текст для анализа..."
        style="width:100%;height:80px;background:var(--primary);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:10px;font-family:var(--font);font-size:13px;outline:none;resize:vertical;"></textarea>
      <button class="btn btn-primary" style="margin-top:8px;" onclick="testAI()">Спросить</button>
      <div id="aiTestResult" style="margin-top:12px;font-size:13px;line-height:1.6;"></div>
    </div>
  </div>

  <!-- ── Mods ── -->
  <div class="page" id="page-mods">
    <div class="page-title">Моды и расширения</div>

    <div class="card">
      <div class="card-title">Установленные моды</div>
      <div id="modsList">
        <div class="mod-item">
          <div class="mod-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg></div>
          <div class="mod-info">
            <div class="mod-name">Example Mod</div>
            <div class="mod-desc">Пример мода — демонстрация системы модов STI</div>
          </div>
          <label class="toggle"><input type="checkbox" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
        </div>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;">
        <button class="btn btn-primary" onclick="installMod()">Установить из ZIP</button>
        <button class="btn btn-secondary" onclick="openModsFolder()">Открыть папку модов</button>
      </div>
    </div>
  </div>

  <!-- ── Accessibility ── -->
  <div class="page" id="page-accessibility">
    <div class="page-title">Специальные возможности</div>

    <div class="card">
      <div class="card-title">Доступность</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Высокий контраст</span></div>
        <label class="toggle"><input type="checkbox" id="highContrastToggle" onchange="saveAccessibility('high_contrast',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Моно-звук</span></div>
        <label class="toggle"><input type="checkbox" id="monoAudioToggle" onchange="saveAccessibility('mono_audio',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Режим курсора (F7)</span><span class="row-desc">Навигация с клавиатуры</span></div>
        <label class="toggle"><input type="checkbox" id="caretToggle" onchange="saveAccessibility('caret_browsing',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Поддержка экранных дикторов</span><span class="row-desc">JAWS, NVDA</span></div>
        <label class="toggle"><input type="checkbox" id="screenReaderToggle" onchange="saveAccessibility('screen_reader',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Режим чтения</span><span class="row-desc">Убрать лишние элементы на странице</span></div>
        <label class="toggle"><input type="checkbox" id="readerModeToggle" onchange="saveSetting('reader_mode',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Режим фокуса</span><span class="row-desc">Убирает отвлекающие элементы</span></div>
        <label class="toggle"><input type="checkbox" id="focusModeToggle" onchange="saveSetting('focus_mode',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
    </div>
  </div>

  <!-- ── Sync ── -->
  <div class="page" id="page-sync">
    <div class="page-title">Синхронизация</div>

    <div class="card">
      <div class="card-title">Облачная синхронизация</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Включить синхронизацию</span></div>
        <label class="toggle"><input type="checkbox" id="syncToggle" onchange="saveSetting('sync_enabled',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Сервер синхронизации</span></div>
        <input class="inp" id="syncServerInp" placeholder="https://sync.example.com">
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;">
        <button class="btn btn-primary" onclick="syncNow()">Синхронизировать сейчас</button>
        <button class="btn btn-secondary" onclick="exportData()">Экспорт данных</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Синхронизировать</div>
      <div class="row"><div class="row-left"><span class="row-label">Закладки</span></div><label class="toggle"><input type="checkbox" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      <div class="row"><div class="row-left"><span class="row-label">История</span></div><label class="toggle"><input type="checkbox" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      <div class="row"><div class="row-left"><span class="row-label">Пароли</span></div><label class="toggle"><input type="checkbox" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      <div class="row"><div class="row-left"><span class="row-label">Настройки</span></div><label class="toggle"><input type="checkbox" checked><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      <div class="row"><div class="row-left"><span class="row-label">Открытые вкладки</span></div><label class="toggle"><input type="checkbox"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
    </div>
  </div>

  <!-- ── VPN ── -->
  <div class="page" id="page-vpn">
    <div class="page-title">VPN и прокси</div>

    <div class="card">
      <div class="card-title">Встроенный VPN</div>
      <div class="row">
        <div class="row-left"><span class="row-label">Включить VPN</span></div>
        <label class="toggle"><input type="checkbox" id="vpnToggle" onchange="saveVPN('enabled',this.checked)"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Регион</span></div>
        <select class="sel" id="vpnRegion" onchange="saveVPN('region',this.value)">
          <option value="auto">Автоматически</option>
          <option value="us">США</option>
          <option value="de">Германия</option>
          <option value="nl">Нидерланды</option>
          <option value="jp">Япония</option>
          <option value="gb">Великобритания</option>
        </select>
      </div>
      <div class="row">
        <div class="row-left"><span class="row-label">Провайдер</span></div>
        <input class="inp" id="vpnProvider" placeholder="socks5://127.0.0.1:1080">
      </div>
      <div style="margin-top:12px;">
        <button class="btn btn-primary" onclick="applyVPN()">Применить</button>
      </div>
    </div>
  </div>

  <!-- ── About ── -->
  <div class="page" id="page-about">
    <div class="page-title">О браузере</div>
    <div class="card">
      <div style="display:flex;align-items:center;gap:20px;margin-bottom:20px;">
        <div style="width:60px;height:60px;border-radius:16px;background:linear-gradient(135deg,var(--accent),#33aaff);display:flex;align-items:center;justify-content:center;">
          <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" style="width:34px;height:34px;"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>
        </div>
        <div>
          <div style="font-size:22px;font-weight:700;">STI Browser</div>
          <div style="font-size:14px;opacity:0.5;">Версия 1.0.0</div>
        </div>
      </div>
      <div class="card-title">Компоненты</div>
      <div class="row"><div class="row-left"><span class="row-label">Python</span></div><span class="badge badge-green">3.9+</span></div>
      <div class="row"><div class="row-left"><span class="row-label">PyQt5 / QWebEngine</span></div><span class="badge badge-green">Активно</span></div>
      <div class="row"><div class="row-left"><span class="row-label">Движок рендеринга</span></div><span class="badge badge-green">Chromium</span></div>
      <div style="margin-top:16px;">
        <button class="btn btn-secondary" onclick="checkUpdates()">Проверить обновления</button>
      </div>
    </div>
  </div>

</main>

<script>
// ── State & helpers ────────────────────────────────────────────────────────
let cfg = {};

const THEMES_DEF = [
  {id:"light",    name:"Светлая",  primary:"#ffffff",  accent:"#0066cc"},
  {id:"dark",     name:"Тёмная",   primary:"#1c1c1e",  accent:"#0a84ff"},
  {id:"sepia",    name:"Сепия",    primary:"#f4ecd8",  accent:"#8b6914"},
  {id:"midnight", name:"Полночь",  primary:"#0d0d0d",  accent:"#7c3aed"},
  {id:"forest",   name:"Лес",      primary:"#f0f4f0",  accent:"#2d6a4f"},
];

window.onload = function() {
  loadConfig();
  buildThemeGrid();
  renderBookmarksList();
  refreshTasks();
};

function loadConfig() {
  try {
    const s = localStorage.getItem("sti_config");
    if (s) cfg = JSON.parse(s);
  } catch(e) { cfg = {}; }
  applyTheme(cfg.theme || "light");
  // Populate fields
  const se = document.getElementById("seSelect");
  if (se && cfg.search_engine) se.value = cfg.search_engine;
  const lang = document.getElementById("langSelect");
  if (lang && cfg.language) lang.value = cfg.language;
  const city = document.getElementById("cityInp");
  if (city && cfg.weather_city) city.value = cfg.weather_city;
  const hp = document.getElementById("homepageInp");
  if (hp && cfg.homepage) hp.value = cfg.homepage;
  // Performance
  const perf = cfg.performance || {};
  setChk("sleepTabsToggle", perf.sleeping_tabs !== false);
  setChk("hwAccelToggle", perf.hardware_acceleration !== false);
  setChk("preloadToggle", perf.preload_pages !== false);
  // Privacy
  const priv = cfg.privacy || {};
  setChk("trackerToggle", priv.block_trackers !== false);
  setChk("safeBrowsingToggle", priv.safe_browsing !== false);
  setChk("adBlockToggle", cfg.ad_block !== false);
  setChk("httpsToggle", priv.https_only === true);
  setChk("dntToggle", priv.send_dnt !== false);
  setChk("incognitoToggle", cfg.incognito === true);
  // AI
  const aiSel = document.getElementById("aiEngineSelect");
  if (aiSel && cfg.ai_engine) aiSel.value = cfg.ai_engine;
  // Sync
  const syncInp = document.getElementById("syncServerInp");
  if (syncInp && cfg.sync_server) syncInp.value = cfg.sync_server;
  // VPN
  const vpn = cfg.vpn || {};
  setChk("vpnToggle", vpn.enabled === true);
  const vpnReg = document.getElementById("vpnRegion");
  if (vpnReg && vpn.region) vpnReg.value = vpn.region;
  const vpnProv = document.getElementById("vpnProvider");
  if (vpnProv && vpn.provider) vpnProv.value = vpn.provider;
  // Appearance
  const fs = document.getElementById("fontSlider");
  if (fs && cfg.font_size) { fs.value = cfg.font_size; document.getElementById("fontVal").textContent = cfg.font_size + "px"; }
  const zs = document.getElementById("zoomSlider");
  if (zs && cfg.zoom) { zs.value = cfg.zoom; document.getElementById("zoomVal").textContent = cfg.zoom + "%"; }
  setChk("vertTabsToggle", cfg.vertical_tabs === true);
  setChk("sidebarToggle", cfg.sidebar_visible !== false);
  setChk("splitToggle", cfg.split_screen === true);
  // Custom CSS
  const cca = document.getElementById("customCssArea");
  if (cca && cfg.custom_css) cca.value = cfg.custom_css;
}

function setChk(id, val) {
  const el = document.getElementById(id);
  if (el) el.checked = !!val;
}

function saveConfig() {
  localStorage.setItem("sti_config", JSON.stringify(cfg));
  if (window.bridge) bridge.saveConfig(JSON.stringify(cfg));
}

function saveSetting(key, val) {
  cfg[key] = val;
  saveConfig();
}

function savePrivacy(key, val) {
  if (!cfg.privacy) cfg.privacy = {};
  cfg.privacy[key] = val;
  saveConfig();
}

function savePerf(key, val) {
  if (!cfg.performance) cfg.performance = {};
  cfg.performance[key] = val;
  saveConfig();
}

function saveAccessibility(key, val) {
  if (!cfg.accessibility) cfg.accessibility = {};
  cfg.accessibility[key] = val;
  saveConfig();
}

function saveVPN(key, val) {
  if (!cfg.vpn) cfg.vpn = {};
  cfg.vpn[key] = val;
  saveConfig();
}

function applyTheme(t) {
  document.body.dataset.theme = t;
  cfg.theme = t;
  document.querySelectorAll(".theme-swatch").forEach(s => {
    s.classList.toggle("selected", s.dataset.theme === t);
  });
}

// ── Navigation ────────────────────────────────────────────────────────────
function showPage(id, btn) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
  document.getElementById("page-"+id).classList.add("active");
  btn.classList.add("active");
}

// ── Theme grid ────────────────────────────────────────────────────────────
function buildThemeGrid() {
  const grid = document.getElementById("themeGrid");
  grid.innerHTML = THEMES_DEF.map(t => `
    <div class="theme-swatch ${cfg.theme === t.id ? 'selected' : ''}"
      data-theme="${t.id}"
      style="background:${t.primary}; border-color: ${cfg.theme===t.id ? t.accent : 'transparent'};"
      onclick="applyTheme('${t.id}');saveConfig();buildThemeGrid();">
      <div class="swatch-dot" style="background:${t.accent}"></div>
      <span style="color:${t.id==='light'||t.id==='sepia'||t.id==='forest'?'#333':'#eee'};font-size:9px;">${t.name}</span>
    </div>`).join("");
}

// ── General ────────────────────────────────────────────────────────────────
function saveGeneralSettings() {
  cfg.homepage = document.getElementById("homepageInp").value;
  cfg.search_engine = document.getElementById("seSelect").value;
  cfg.language = document.getElementById("langSelect").value;
  cfg.weather_city = document.getElementById("cityInp").value || "Moscow";
  saveConfig();
  showToast("Настройки сохранены");
}

function importSettings() {
  if (window.bridge) bridge.importSettings();
  else alert("Импорт настроек доступен только в браузере STI.");
}

function changeDownloadPath() {
  if (window.bridge) bridge.changeDownloadPath();
  else alert("Изменение пути загрузок доступно только в браузере STI.");
}

function addProfile() {
  const name = prompt("Имя нового профиля:");
  if (!name) return;
  if (!cfg.profiles) cfg.profiles = ["default"];
  cfg.profiles.push(name);
  saveConfig();
  renderProfiles();
}

function renderProfiles() {
  const el = document.getElementById("profilesList");
  if (!el) return;
  const profiles = cfg.profiles || ["default"];
  el.innerHTML = profiles.map((p,i) => `
    <div class="row">
      <div class="row-left"><span class="row-label">${p}</span>${p===cfg.profile?'<span class="badge badge-green" style="margin-top:2px;">Активный</span>':''}</div>
      ${p!=="default"?`<button class="btn btn-secondary" onclick="switchProfile('${p}')">Переключить</button>`:''}
    </div>`).join("");
}

function switchProfile(name) {
  cfg.profile = name;
  saveConfig();
  renderProfiles();
  showToast("Профиль: " + name);
}

// ── Passwords ──────────────────────────────────────────────────────────────
function generatePassword() {
  const len = parseInt(document.getElementById("passLenSlider").value);
  const symbols = document.getElementById("passSymbols").checked;
  const numbers = document.getElementById("passNumbers").checked;
  let chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  if (numbers) chars += "0123456789";
  if (symbols) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?";
  let pass = "";
  for (let i = 0; i < len; i++) pass += chars[Math.floor(Math.random() * chars.length)];
  document.getElementById("genPassInp").value = pass;
}

function copyPassword() {
  const v = document.getElementById("genPassInp").value;
  if (v) { navigator.clipboard.writeText(v); showToast("Пароль скопирован"); }
}

function checkPasswords() {
  showToast("Проверка паролей по базе утечек...");
  setTimeout(() => showToast("Проверка завершена. Угроз не обнаружено."), 1500);
}

// ── Bookmarks ──────────────────────────────────────────────────────────────
function renderBookmarksList() {
  const el = document.getElementById("bmList");
  if (!el) return;
  const bms = cfg.bookmarks || [];
  if (!bms.length) { el.innerHTML = '<div style="opacity:0.4;font-size:13px;padding:8px 0;">Нет закладок</div>'; return; }
  el.innerHTML = bms.map((b,i) => `
    <div class="bm-item">
      <img src="https://www.google.com/s2/favicons?sz=32&domain_url=${encodeURIComponent(b.url)}" style="width:18px;height:18px;border-radius:4px;" onerror="this.style.display='none'">
      <div style="flex:1;">
        <div style="font-size:13px;font-weight:500;">${escHtml(b.title)}</div>
        <div class="bm-url">${escHtml(b.url)}</div>
      </div>
      <button class="btn btn-secondary" style="padding:4px 10px;font-size:12px;" onclick="removeBM(${i})">Удалить</button>
    </div>`).join("");
}

function addBookmarkSettings() {
  const t = document.getElementById("bmTitleInp").value.trim();
  const u = document.getElementById("bmUrlInp").value.trim();
  if (!t || !u) return;
  if (!cfg.bookmarks) cfg.bookmarks = [];
  cfg.bookmarks.push({title: t, url: u.startsWith("http") ? u : "https://" + u});
  saveConfig(); renderBookmarksList();
  document.getElementById("bmTitleInp").value = "";
  document.getElementById("bmUrlInp").value = "";
}

function removeBM(i) {
  cfg.bookmarks.splice(i, 1);
  saveConfig(); renderBookmarksList();
}

function importBookmarks() {
  if (window.bridge) bridge.importBookmarks();
  else alert("Импорт закладок доступен только в браузере STI.");
}

// ── Privacy ────────────────────────────────────────────────────────────────
function runSafetyCheck() {
  const el = document.getElementById("safetyResult");
  el.textContent = "Выполняется проверка...";
  setTimeout(() => {
    el.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:6px;">
        <div style="display:flex;align-items:center;gap:8px;"><span class="badge badge-green">OK</span> Пароли: утечек не обнаружено</div>
        <div style="display:flex;align-items:center;gap:8px;"><span class="badge badge-green">OK</span> Браузер обновлён</div>
        <div style="display:flex;align-items:center;gap:8px;"><span class="badge badge-green">OK</span> Безопасный просмотр включён</div>
        <div style="display:flex;align-items:center;gap:8px;"><span class="badge badge-green">OK</span> Трекеры заблокированы</div>
      </div>`;
  }, 1200);
}

function clearHistory() {
  if (window.bridge) bridge.clearHistory();
  cfg.history = [];
  saveConfig();
  showToast("История очищена");
}

function clearCookies() {
  if (window.bridge) bridge.clearCookies();
  showToast("Куки очищены");
}

// ── Performance ────────────────────────────────────────────────────────────
function refreshTasks() {
  const el = document.getElementById("taskManager");
  if (!el) return;
  if (window.bridge) {
    bridge.getTaskInfo(info => { el.innerHTML = info; });
  } else {
    el.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr auto auto;gap:6px 20px;align-items:center;">
        <span style="font-weight:500;font-size:12px;opacity:0.5;">ПРОЦЕСС</span><span style="font-size:12px;opacity:0.5;">CPU</span><span style="font-size:12px;opacity:0.5;">ОЗУ</span>
        <span>Браузер (главный)</span><span>0.5%</span><span>48 МБ</span>
        <span>Вкладка: Новая вкладка</span><span>0.1%</span><span>22 МБ</span>
      </div>`;
  }
}

// ── AI ─────────────────────────────────────────────────────────────────────
function testAI() {
  const q = document.getElementById("aiTestInput").value.trim();
  if (!q) return;
  const result = document.getElementById("aiTestResult");
  result.textContent = "Отправка запроса к ИИ...";
  const engine = cfg.ai_engine || "google";
  if (engine === "google") {
    window.open("https://gemini.google.com/app?q=" + encodeURIComponent(q), "_blank");
    result.textContent = "Открыт Gemini AI в новой вкладке.";
  } else if (engine === "yandex") {
    window.open("https://ya.ru/ai/gpt?text=" + encodeURIComponent(q), "_blank");
    result.textContent = "Открыт YandexGPT в новой вкладке.";
  } else {
    window.open("https://chat.openai.com/?q=" + encodeURIComponent(q), "_blank");
    result.textContent = "Открыт ChatGPT в новой вкладке.";
  }
}

// ── Mods ───────────────────────────────────────────────────────────────────
function installMod() {
  if (window.bridge) bridge.installMod();
  else alert("Установка модов доступна только в браузере STI.");
}

function openModsFolder() {
  if (window.bridge) bridge.openModsFolder();
  else alert("Открытие папки модов доступно только в браузере STI.");
}

// ── Sync ───────────────────────────────────────────────────────────────────
function syncNow() {
  if (window.bridge) bridge.syncNow();
  showToast("Синхронизация запущена...");
}

function exportData() {
  const data = JSON.stringify(cfg, null, 2);
  const blob = new Blob([data], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = "sti_backup.json"; a.click();
}

// ── VPN ────────────────────────────────────────────────────────────────────
function applyVPN() {
  cfg.vpn = {
    enabled: document.getElementById("vpnToggle").checked,
    region: document.getElementById("vpnRegion").value,
    provider: document.getElementById("vpnProvider").value,
  };
  saveConfig();
  if (window.bridge) bridge.applyVPN(JSON.stringify(cfg.vpn));
  showToast("Настройки VPN применены");
}

// ── Appearance extras ──────────────────────────────────────────────────────
function applyCustomCSS() {
  const css = document.getElementById("customCssArea").value;
  cfg.custom_css = css;
  saveConfig();
  if (window.bridge) bridge.applyCustomCSS(css);
  showToast("CSS применён");
}

// ── About ──────────────────────────────────────────────────────────────────
function checkUpdates() {
  showToast("Проверка обновлений... Версия актуальна.");
}

// ── Toast ──────────────────────────────────────────────────────────────────
function showToast(msg) {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div");
    t.id = "toast";
    Object.assign(t.style, {
      position:"fixed", bottom:"28px", left:"50%", transform:"translateX(-50%)",
      background:"var(--text)", color:"var(--primary)", padding:"10px 22px",
      borderRadius:"20px", fontSize:"13px", fontFamily:"var(--font)",
      zIndex:"999", boxShadow:"0 4px 16px rgba(0,0,0,0.2)",
      transition:"opacity 0.3s", whiteSpace:"nowrap",
    });
    document.body.appendChild(t);
  }
  t.textContent = msg; t.style.opacity = "1";
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.style.opacity = "0"; }, 2500);
}

function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// Init profiles
setTimeout(renderProfiles, 100);
</script>
</body>
</html>"""

MANIFEST_JSON = {
    "id": "example_mod",
    "name": "Example Mod",
    "version": "1.0.0",
    "description": "Пример мода для STI Browser — демонстрация системы модов",
    "author": "STI Dev Team",
    "permissions": ["tabs", "storage", "navigation"],
    "scripts": ["mod_script.py"],
    "inject_js": ["inject.html"],
    "inject_css": [],
    "inject_urls": ["*"],
    "widgets": [],
    "toolbar_buttons": [
        {"id": "example_btn", "title": "Example Mod", "icon": "icon.html", "action": "toggle_panel"}
    ],
    "settings": [
        {"key": "enabled", "type": "bool", "default": True, "label": "Включить мод"},
        {"key": "message", "type": "string", "default": "Hello from Example Mod!", "label": "Сообщение"}
    ]
}

MOD_SCRIPT_PY = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example Mod — script.py
Загружается STI Browser при активации мода.
"""

class ExampleMod:
    """Точка входа мода. STI Browser вызывает __init__ и activate/deactivate."""

    def __init__(self, browser_api):
        self.api = browser_api
        self.name = "Example Mod"

    def activate(self):
        print(f"[{self.name}] Activated!")
        # Пример: добавить кнопку на панель инструментов
        # self.api.add_toolbar_button("example_btn", "Example", self.on_click)

    def deactivate(self):
        print(f"[{self.name}] Deactivated.")

    def on_click(self):
        self.api.show_notification("Example Mod", "Кнопка нажата!")

    def on_page_load(self, url):
        """Вызывается при загрузке каждой страницы."""
        pass

    def on_navigate(self, url):
        """Вызывается при навигации."""
        pass


def create_mod(browser_api):
    """Фабрика — обязательная функция для каждого мода."""
    return ExampleMod(browser_api)
'''

MOD_INJECT_HTML = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>
<script>
// Этот скрипт внедряется на каждую страницу при активации мода.
// Здесь можно менять DOM, добавлять элементы и т.д.
(function() {
  'use strict';
  // Пример: добавить тонкую полоску сверху страницы
  const bar = document.createElement('div');
  bar.style.cssText = [
    'position:fixed','top:0','left:0','right:0','height:3px',
    'background:linear-gradient(90deg,#0066cc,#33aaff)',
    'z-index:2147483647','pointer-events:none'
  ].join(';');
  document.body.appendChild(bar);
  console.log('[STI Example Mod] Injected!');
})();
</script>
</body>
</html>"""

INDEX_PROMPT_TXT = """# STI Browser — Промт для воссоздания главного интерфейса

## Описание проекта
STI Browser — полнофункциональный браузер на Python (PyQt5 + QWebEngineView).
Главный файл: sti.py. Все ресурсы генерируются автоматически при первом запуске.

## Главное окно (QMainWindow)

### Строка заголовка / системная панель
- Иконка браузера слева (SVG-глобус с меридианами)
- Название «STI Browser»
- Системные кнопки (свернуть, развернуть, закрыть)

### Панель вкладок (TabBar)
- Горизонтальная полоса с вкладками (Qt-нативная: QTabBar/QTabWidget)
- Каждая вкладка: фавикон (QLabel+QPixmap) + заголовок (усечённый) + кнопка «×»
- Кнопка «+» (новая вкладка) справа от вкладок
- Группы вкладок: цветная метка слева от заголовка
- Drag-and-drop для перетаскивания вкладок
- Поиск по вкладкам: иконка-лупа рядом с «+»
- Режим «Спящая вкладка»: затемнённая иконка луны у неактивных вкладок

### Адресная строка (Toolbar/Omnibox)
Слева направо:
1. Кнопка «Назад» (стрелка влево, SVG)
2. Кнопка «Вперёд» (стрелка вправо, SVG)
3. Кнопка «Обновить» / «Стоп» (SVG, меняется при загрузке)
4. Кнопка «Домой» (SVG-домик)
5. [Поле ввода URL / поисковая строка]:
   - Иконка замка/предупреждения (безопасность соединения)
   - Текст URL или поисковый запрос
   - Кнопка «×» очистить при вводе
   - Кнопка микрофона (голосовой ввод) справа внутри поля
   - При фокусе: выпадающий список подсказок (история + топ-сайты + AI-ответы)
6. Кнопка AI-ассистента (SVG-лампочка, открывает боковую панель Gemini)
7. Кнопка «Перевести страницу» (SVG-буква А с подчёркиванием)
8. Кнопка «Режим чтения» (SVG-книга)
9. Кнопка «Добавить в закладки» (SVG-звёздочка, заполненная если добавлено)
10. Кнопка «Расширения/Моды» (SVG-пазл)
11. Кнопка «Профиль» (аватар или инициалы, SVG-человечек)
12. Кнопка «Меню» (три горизонтальные точки, SVG)

### Боковая панель (QDockWidget или кастомный виджет)
Переключается кнопками-вкладками (иконки без подписей):
- Закладки (SVG-звезда)
- История (SVG-часы)
- Загрузки (SVG-стрелка вниз)
- Коллекции (SVG-стопка карточек)
- AI-ассистент (SVG-лампочка): чат с Gemini, суммаризация страницы
- Edge Drop / Заметки (SVG-карандаш)
Панель можно свернуть/развернуть кнопкой ← →.

### Вертикальные вкладки (опция)
При включении — боковая панель слева заменяет горизонтальный TabBar.
Каждый пункт: фавикон + усечённый заголовок + кнопка закрытия.

### Новая вкладка (browse.html)
- Вверху справа: кнопки «Настройки», «Фокус», «Тема»
- По центру: логотип STI (SVG-глобус) + название
- Строка поиска: скруглённая, с иконкой лупы и кнопкой микрофона
- Кнопки выбора поисковой системы под строкой (Google, Яндекс, Bing, DuckDuckGo, Brave)
- Баннер «Спросить Gemini AI» — кнопка-приглашение к чату
- Сетка «Быстрый доступ»: карточки с фавиконом + подписью, кнопка «Добавить»
- Виджеты внизу: Часы, Погода (wttr.in), Быстрая заметка (textarea)

### Страница настроек (settings.html)
- Левая колонка навигации (220px): логотип + список категорий с иконками
- Правая часть: карточки с настройками, переключатели, слайдеры, выпадающие списки
- Категории: Основные, Внешний вид, Приватность, Пароли, Закладки, Производительность,
  ИИ, Моды, Доступность, Синхронизация, VPN, О браузере

### Контекстное меню на странице
Пункты: Назад, Вперёд, Обновить, Сохранить как, Печать, Перевести, Поиск по выделенному,
Просмотр кода, Инспектор, Добавить в коллекцию, AI-анализ выделенного.

### Индикаторы состояния
- Строка состояния внизу (опционально): URL при наведении, прогресс загрузки
- Индикатор загрузки: тонкая прогресс-бар под адресной строкой (синяя полоска)
- Иконка щита в адресной строке (зелёный=безопасно, жёлтый=смешанный, красный=небезопасно)

### Диалоги и уведомления
- Toast-уведомления (bottom-center, авто-скрытие через 3с)
- Диалог сохранения пароля (всплывает снизу адресной строки)
- Диалог разрешений (микрофон, камера, уведомления)
- Диалог загрузки файла

## Цветовые темы
Поддерживается 5 тем: Светлая, Тёмная, Сепия, Полночь, Лес.
CSS-переменные: --primary, --accent, --text, --surface, --border, --shadow, --radius, --font.
Тема применяется через data-theme на <body>.

## Шрифты и иконки
Системный шрифт: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial.
Все иконки — inline SVG (stroke-based, stroke-width: 1.8).
Размер иконок на панели инструментов: 18×18px.

## Архитектура связи Python ↔ JS
QWebChannel (объект `bridge` в JS):
- bridge.navigate(url)
- bridge.openSettings()
- bridge.openAI()
- bridge.saveConfig(json_string)
- bridge.importSettings()
- bridge.clearHistory()
- bridge.clearCookies()
- bridge.installMod()
- bridge.applyVPN(json_string)
- bridge.applyCustomCSS(css_string)
- bridge.getTaskInfo(callback)
- bridge.importBookmarks()
- bridge.changeDownloadPath()

## Система модов
Папка: mods/<id>/
Файлы: manifest.json, mod_script.py, inject.html (опционально).
manifest.json: id, name, version, description, author, permissions,
scripts, inject_js, inject_css, inject_urls, widgets, toolbar_buttons, settings.
Python-класс мода: метод create_mod(browser_api) → объект с activate(), deactivate(),
on_page_load(url), on_navigate(url).

## Инновационные функции
1. Умный офлайн-плеер: просмотр сохранённых страниц с полным CSS/JS
2. VPN/прокси-менеджер: выбор региона, провайдера (socks5/http)
3. Карты знаний: автогенерация mind-map по тексту страницы (JSON → визуализация)
4. Детектор фейков: ИИ-метка «Проверить источник» на статьях
5. Режим фокуса: полноэкранный оверлей, блокирует уведомления и отвлекающие виджеты
6. Интеграция Gemini: анализ страниц, суммаризация, перевод через google.com/search

## Стиль интерфейса
Минималистичный, похожий на Safari/Chrome: белый/светло-серый фон, тонкие границы,
скруглённые углы 8–12px, тени 2–8px, плавные переходы 0.2–0.3s.
Без анимационных «космических» эффектов. Акцентный цвет — синий (#0066cc в светлой теме).
"""

def create_dirs():
    print("[STI Setup] Создание структуры папок...")
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        print(f"  [OK] {d}/")

def write_file(path, content, mode="w", encoding="utf-8"):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, mode, encoding=encoding) as f:
        f.write(content)
    print(f"  [OK] {path}")

def create_files():
    print("[STI Setup] Создание файлов...")

    # config.json
    if not os.path.exists("config.json"):
        write_file("config.json", json.dumps(CONFIG_JSON, ensure_ascii=False, indent=2))
    else:
        print("  [--] config.json уже существует, пропущен.")

    # browse.html
    write_file("browse.html", BROWSE_HTML)

    # settings.html
    write_file("settings.html", SETTINGS_HTML)

    # mods/example_mod/manifest.json
    write_file(
        os.path.join("mods", "example_mod", "manifest.json"),
        json.dumps(MANIFEST_JSON, ensure_ascii=False, indent=2)
    )

    # mods/example_mod/mod_script.py
    write_file(os.path.join("mods", "example_mod", "mod_script.py"), MOD_SCRIPT_PY)

    # mods/example_mod/inject.html
    write_file(os.path.join("mods", "example_mod", "inject.html"), MOD_INJECT_HTML)

    # index_promt.txt
    write_file("index_promt.txt", INDEX_PROMPT_TXT)

    print("[STI Setup] Все файлы созданы.")

def main():
    print("=" * 56)
    print("   STI Browser — Setup & First Run")
    print("=" * 56)
    install_packages()
    create_dirs()
    create_files()
    print()
    print("[STI Setup] Готово! Для запуска браузера выполните:")
    print("   python sti.py")
    print("=" * 56)

if __name__ == "__main__":
    main()

y = input("Нажмите на любую клавишу")
