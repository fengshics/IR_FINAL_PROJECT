name = ["CACM-000","CACM-00","CACM-0","CACM-"]

def createfile():
	file_object = open("cacm_stem.txt")
	all_the_text = file_object.read( ).split("# ")
	prefix = all_the_text[1].split("\n")[0]
	filename = name[len(prefix)-1] + prefix+".html"
	content = all_the_text[1][len(prefix):].strip()
	file = open(filename,'w')
	file.write(content)
	file.close()
	
createfile()
