import simplejson as json
import sys
import os

class FileWorker(object):

	json_dir_output = "../Outputs/"
	txt_dir_output = "./outputs/"

	def read(self,filename):#read a text file
		array = []
		with open(filename) as file:
			for line in file:
				line = line.rstrip('\r')
				line = line.rstrip('\n')
				array.append(line)
		return array

	def readJSON(self,filename):#read a json file
		with open(filename) as file:
			data = json.load(file)
			return data

	def writeJSON(self,filename,data):#write data like json file
		try:
			jsondata = json.dumps(data, indent=4, skipkeys=True, sort_keys=True)
			fd = open(filename, 'w')
			fd.write(jsondata)
			fd.close()
			print filename + " ha sido escrito exitosamente"
		except:
			print 'ERROR writing', filename
			pass

	def write(self,filename,dataList):# write data like .txt file
		filename = os.path.join(self.txt_dir_output,filename)
		fd = open(filename,mode='w+')
		for item in dataList:
			try:
				line = "%s\n"%(item)
				fd.write(line)
			except:
				print item
				pass
		fd.close()
		print filename + " ha sido escrito exitosamente"