from os import listdir, mkdir
from pyrogram import Client
from MusicPlayer import config
from MusicPlayer.tgcalls.queues import clear, get, is_empty, put, task_done
from MusicPlayer.tgcalls import queues
from MusicPlayer.tgcalls.youtube import download
from MusicPlayer.tgcalls.calls import run, pytgcalls
from MusicPlayer.tgcalls.calls import client

if "raw_files" not in listdir():
    mkdir("raw_files")

from MusicPlayer.tgcalls.convert import convert
