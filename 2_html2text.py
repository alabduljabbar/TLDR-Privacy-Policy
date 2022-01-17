from bs4 import BeautifulSoup
from bs4.element import Comment
import os
 
basepath = "./PolicyData/HTMLFiles/"


def pars(file_name):
	page=open(basepath+file_name, "r")
	soup = BeautifulSoup(page, 'html.parser')
	paragraphas= soup.find_all('p')

	#Divide File into paragraphs
	with open("./PolicyData/TextFiles/"+"/"+file_name[:-5]+".txt", 'w') as f:
		for i in range(0,len(paragraphas)):
			f.write(soup.find_all('p')[i].get_text()+"\n")

i=1
# List all subdirectories using scandir()
for file in sorted(os.listdir(basepath)):
	if file==".DS_Store":
		continue
	else:
		print(i)
		i=i+1
		print(file)
		try:
			pars(file)
		except:
			print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"+file+"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
