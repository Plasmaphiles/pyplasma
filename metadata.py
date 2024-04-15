import struct

class Metadata:
	def __init__(self, filename: str):
		self.index = 0
		self.filename = filename

		with open(filename, 'rb') as fp:
			self.data = fp.read()

		self.i8()
		self.i16(5) #Header info?
		self.str() #Serialization text
		self.i16(4) #what is this?


		self.info = {i[0]: i[1] for i in [
			self.key_value(),
			self.key_value(),
		]}

		self.name = self.info.get('name')
		self.description = self.info.get('description')

	def get(self, format: str) -> list:
		length = struct.calcsize(format)
		result = struct.unpack(format, self.data[self.index : (self.index + length)])
		self.index += length
		return result

	def i32(self, count: int = 1) -> list:
		return self.get(f'@{count}\i')

	def i16(self, count: int = 1) -> list[int]:
		return self.get(f'@{count}h')

	def i8(self, count: int = 1) -> list[int]:
		return self.get(f'@{count}b')

	def str(self, character_ct: int | None = None) -> str:
		if character_ct is not None:
			ix_offset = 0
			end_ix = self.index + character_ct * 2
		else:
			ix_offset = 2
			end_ix = self.index
			while self.data[end_ix] or self.data[end_ix + 1]:
				if self.data[end_ix] == 1:
					ix_offset += 2
					break
				end_ix += 2

		result = self.data[self.index:end_ix]#.replace(b'\x03', b'').replace(b'\x01', b'').replace(b'\x27', b'')

		self.index = end_ix + ix_offset
		result = result.decode('utf-16le', errors = 'ignore').encode().replace(b'\xc4\xa7', b'').replace(b'\xc4\x83', b'').replace(b'\xc4\xad', b'').decode()
		return result.replace('\x0b', '\n').replace('\x0c', '\n').replace('\r', '')

	def key_value(self) -> tuple[str, str]:
		key = self.str().strip()
		self.i8()
		value = self.str().strip()

		return key, value
