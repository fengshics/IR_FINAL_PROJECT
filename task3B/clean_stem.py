name = ["CACM-000","CACM-00","CACM-0","CACM-"]

def createfile():
	file_object = open("cacm_stem.txt")
	all_the_text = file_object.read( ).split("# ")
	i = 1
	while i < len(all_the_text):
		prefix = all_the_text[i].split("\n")[0]
		filename = name[len(prefix)-1] + prefix+".html"
		content = all_the_text[i][len(prefix):].strip()
		file = open("cacm_stem/"+filename,'w')
		file.write(content)
		file.close()
		i += 1
	
createfile()
