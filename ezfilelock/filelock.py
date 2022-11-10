import asyncio
import builtins
import contextlib
import os
import threading
from typing import Dict


class FileLock:
    sharelock = threading.Lock()
    filelock_dict: Dict[str, threading.Lock] = {}

    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        with self.sharelock:
            if self.filepath not in self.filelock_dict:
                self.filelock_dict[self.filepath] = threading.Lock()

    def release(self):
        self.filelock_dict[self.filepath].release()

    def acquire(self):
        self.filelock_dict[self.filepath].acquire()
        return self

    __enter__ = acquire

    def __exit__(self, type, value, traceback):
        self.release()


class AsyncFileLock:
    """
    not thread safe, use with pure coroutine
    """

    sharelock = asyncio.Lock()
    filelock_dict: Dict[str, asyncio.Lock] = {}

    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)

    def release(self):
        self.filelock_dict[self.filepath].release()

    def release(self):
        self.filelock_dict[self.filepath].release()

    async def acquire(self):
        async with self.sharelock:
            if self.filepath not in self.filelock_dict:
                self.filelock_dict[self.filepath] = asyncio.Lock()
        await self.filelock_dict[self.filepath].acquire()

    __aenter__ = acquire

    def __await__(self):
        yield

    def __aexit__(self, type, value, traceback):
        self.release()
        return self


@contextlib.contextmanager
def open(filepath, *args, **kwargs):
    with FileLock(filepath):
        with builtins.open(filepath, *args, **kwargs) as fp:
            yield fp


@contextlib.asynccontextmanager
async def aopen(filepath, *args, **kwargs):
    async with AsyncFileLock(filepath):
        with builtins.open(filepath, *args, **kwargs) as fp:
            yield fp
