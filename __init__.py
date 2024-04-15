__all__ = ['devices', 'worlds', 'Blueprint']

from typing import Generator
from .metadata import Metadata
from pathlib import Path
import os
import hashlib

class Blueprint:
	def __init__(self, filename: Path):
		meta = Metadata(str(filename))

		self.filename: Path = filename
		self.id: str = filename.stem
		self.name: str = meta.name
		self.description: str = meta.description

	def md5sum(self) -> str:
		md5 = hashlib.md5()
		with open(str(self.filename), 'rb') as f:
			for chunk in iter(lambda: f.read(4096), b''):
				md5.update(chunk)

		return md5.hexdigest()

def devices() -> Generator[Blueprint, None, None]:
	for file in Path(os.getenv('APPDATA') + '\\..\\LocalLow\\DryLicorice\\Plasma\\User Data\\Devices').iterdir():
		if file.suffix == '.metadata':
			device = Blueprint(file)
			if device.name:
				yield device

def worlds() -> Generator[Blueprint, None, None]:
	for file in Path(os.getenv('APPDATA') + '\\..\\LocalLow\\DryLicorice\\Plasma\\User Data\\Worlds').iterdir():
		if file.suffix == '.metadata':
			device = Blueprint(file)
			if device.name:
				yield device
