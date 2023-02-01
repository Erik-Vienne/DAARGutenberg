import sys 

import re



def read (f):
	#f = open(file, "r")
	
	motFrequent = ['had', 'such', 'did', 'been', 'were','are', 'is','the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'was']




	for i in range(1) :
	
		with open(f, 'r', encoding="utf8") as file:
			data = file.read().replace('\n', ' ')
	
			f2 = re.sub(r'[^a-zA-Z0-9\s]+', '', data)
			f2 = f2.split()
			f2 = [x.lower() for x in f2]
			
			listeResultat = []
			
			for i in motFrequent :
				#print(i)
				f2 = list(filter(lambda a: a != i, f2))
				#f2.remove(str(i))
			
			print(f2[:100])


			while len(f2) > 0 :
				mot = f2[0]
				nbOccurence = f2.count(mot)
				
				listeResultat.append( (mot, nbOccurence))
				
				f2 = list(filter(lambda a: a != mot, f2))

			listeResultat.sort(reverse=True, key=lambda a: a[1])
			#listeResultat.reverse()
			
			#print( listeResultat[:100])
			file.close()

		# contenu = False	

		# for i in listeResultat :
		# 	if (i == sys.argv[2]) :
		# 		contenu

		
		print("contient " )	
			
		
		#print(f2[:500])
		
			
			
	

file = sys.argv[1]
read(file)	