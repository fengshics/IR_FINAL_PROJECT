import unirest
import json

word_dic = {}
querys = []


def thesauri(word):
	global word_dic
	response = unirest.post("http://words.bighugelabs.com/api/2/cacbd5c7037f0cc536df9fcd22682b95/"+word+"/json")
	a = response.body
	i = 0
	if a !="":
		for key in a:
			if "syn" in a[key]:
				while i < len(a[key]["syn"]):
					word_dic[word].append(a[key]["syn"][i])
					i += 1
	#print word_dic[word]

def readfile():
	global word_dic
	file_object = open("cacm_query_token.txt")
	all_the_text = file_object.read( ).split()
	for word in all_the_text:
		if word not in word_dic :
			word_dic[word] = []
	for key in word_dic:
		thesauri(key)
	file_object.close()

def get_querys():
	global querys
	file_object = open("cacm_query_token.txt")
	querys = file_object.read().split('\n')
	i = 0
	for query in querys:
		query_process(query,i)
		i += 1
	file_object.close()
	saveExpandedQueries()

def query_process(query,index):
	global word_dic
	global querys
	for word in query.split(" "):
		if word != "":
			count = len(word_dic[word])/10
			j = 0
			while j < count:
				querys[index] =querys[index] + word_dic[word][j]+" "
				j += 1
	print querys[index]

def saveExpandedQueries():
	global querys
	with open("expanded_queries_Thesaurus.txt", "w") as f:
		for i in range(0, 64):
			f.write(querys[i] + '\n')

		

if __name__ == '__main__':
	readfile()
	get_querys()