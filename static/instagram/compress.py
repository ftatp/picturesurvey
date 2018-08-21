import zipfile
import os

files = os.listdir()
files.sort()
print(files)

for i in range(60):
	zipfp = zipfile.ZipFile(os.getcwd() + str(i*100).zfill(4) + '.zip', 'w')
	for file in files[i * 100:(i + 1)*100]:
		zipfp.write(file)
	zipfp.close()
