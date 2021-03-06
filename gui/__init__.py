import asyncio
from threading import Thread

from mttkinter import mtTkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import Menu
from tkinter.ttk import Notebook

from audiobot.AudioBot import Global_Audio_Bot
from config import Config
from gui.BlacklistGUI import BlacklistGUI
from gui.ConfigGUI import ConfigGUI
from gui.HistoryPlaylistGUI import HistoryPlaylistGUI
from gui.InfoGUI import InfoGUI
from gui.PlaylistGUI import PlaylistGUI
from gui.MPVGUI import MPVGUI
from gui.RoomGUI import RoomGUI
from gui.SearchGUI import SearchGUI
from utils import vasyncio, vfile
import sys

class MainWindow():
    def __init__(self, loop=None, interval=1 / 20):
        self.window = tk.Tk()
        self.interval = interval
        self.window.title(Config.gui_title)
        self.tab_controller: Notebook = ttk.Notebook(self.window)
        self.menu_controller = Menu(self.window)
        self._loop = asyncio.get_event_loop() if loop == None else loop
        self._running = True
        self._initialize()

    def _initialize(self):
        self.window.iconphoto(True, PhotoImage(file=vfile.getResourcePath('resource/favicon.png')))
        self.window.resizable(False, False)
        self.window.geometry("720x480")
        self.tab_controller.pack(expand=1, fill="both")

    def getTabController(self) -> Notebook:
        return self.tab_controller

    def async_update(self, func, *args, **kwargs):
        asyncio.ensure_future(vasyncio.asyncwrapper(func)(*args, **kwargs), loop=self._loop)

    def threading_update(self, func, *args, **kwargs):
        thread = Thread(target=func,args=args,kwargs=kwargs)
        thread.start()

    async def _async_update(self):
        while self._running:
            try:
                self.window.update()
                await asyncio.sleep(self.interval)
            except:
                break

    def start(self):
        self.createWidgets()
        self.window.quit()
        return self._async_update()

    def createWidgets(self):
        mpv = MPVGUI(self)
        room = RoomGUI(self)
        playlist = PlaylistGUI(self)
        search = SearchGUI(self)
        configgui = ConfigGUI(self)
        infogui = InfoGUI(self)
        blacklistgui = BlacklistGUI(self)
        hitorylistgui = HistoryPlaylistGUI(self)

        mpv.createWidgets()
        room.createWidgets()
        playlist.createWidgets()
        configgui.createWidgets()
        search.createWidgets()
        infogui.createWidgets()
        blacklistgui.createWidgets()
        hitorylistgui.createWidgets()

        room.initialize()
        playlist.initialize()
        search.initialize()
        hitorylistgui.initialize()
        configgui.initialize()
        blacklistgui.initialize()
        infogui.initialize()
        mpv.initialize()

        Global_Audio_Bot.start()
