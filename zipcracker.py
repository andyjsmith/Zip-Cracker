from multiprocessing import Process
import os
import zipfile
import zlib
import time

initial = 1504237855
now = int(time.time())
diff = now - initial
cpu = os.cpu_count()
increment = int(diff / cpu)
def calc(n):
	start = initial + increment * n
	print("[CPU", "%02d]" % n, "START:", start)
	cur = start
	with zipfile.ZipFile("flag.zip", 'r') as zip_ref:
		while True:
			if cur > start + increment:
				print("[CPU", "%02d]" % n, "COMPLETED")
				break
			
			cur += 1
			try:
				if cur % 100000 == 0: print("[CPU", "%02d]" % n, str("{0:.2f}".format(((cur - start) / increment) * 100)) + "%")
				zip_ref.extractall("test", pwd=bytes(str(cur), "ascii"))
				print("Found:", cur)
				zip_ref.extractall("found", pwd=bytes(str(cur), "ascii"))
				break
			except (RuntimeError, zlib.error, zipfile.BadZipFile):
				continue

processes = []
if __name__ == '__main__':
	for i in range(cpu):
		print("Registering process %02d" % i)
		processes.append(Process(target=calc, args=(i,)))

	for process in processes:
		process.start()

	for process in processes:
		process.join()