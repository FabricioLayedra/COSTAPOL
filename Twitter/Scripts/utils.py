import json
import simplejson
from FileWorker import FileWorker

def write_tokens(raw_tokens, output):
	fw = FileWorker()
	f = open(raw_tokens, 'r')
	i = 1
	credentials = []
	credential = dict()
	tokens =0
	for line in f:
		if i == 1:
			credential["consumer_key"] = line.strip().split()[4]
			i+=1
		elif i==2:
			credential["consumer_secret"] = line.strip().split()[4]
			i+=1
		elif i==3:
			credential["access_token"] = line.strip().split()[2]
			i+=1
		elif i==4:
			credential["access_token_secret"] = line.strip().split()[3]
			i+=1
			tokens +=1
			credentials.append(credential)
		else:
			i=1
			credential=dict()
			pass
	f.close()
	print("Se han registrado %d tokens en el archivo %s" %(tokens,output))
	data = {'configs':credentials}
	fw.writeJSON(output,data)

write_tokens("../Data/raw_tokens.txt","../Data/timelines_tokens.json")

