#bias calculations
import random, datetime
data = [[] for i in range(100)]
f = open("Documents/Programs/Python Programs/Bang_store_data.txt", 'a')
f.write("-----------------------------------------\n%s\n"%datetime.datetime.now())
# deck_date = [card name, ranking, occurances]
deck_data = [['Bang!',0,0],
			['Missed!',0,0],
			["Beer",0,0],
			["Duel",0,0],
			["Cat Balou",0,0],
			["Panic!",0,0],
			["Indians!",0,0],
			["Gatling",0,0],
			["Saloon",0,0],
			["General Store",0,0],
			#["Stagecoach"],
			#["Wells Fargo"],
			["Volcanic",0,0],
			["Mustang",0,0],
			["Jail",0,0],
			["Barrel",0,0],
			["Scope",0,0],
			["Dynamite",0,0]     
			]
leng = len(deck_data)
for a in range(100):
	deck = [('Bang!'),
			('Missed!'),
			("Beer"),
			("Duel"),
			("Cat Balou"),
			("Panic!"),
			("Indians!"),
			("Gatling"),
			("Saloon"),
			("General Store"),
			#("Stagecoach"),
			#("Wells Fargo"),
			("Volcanic"),
			("Mustang"),
			("Jail"),
			("Barrel"),
			("Scope"),
			("Dynamite")     
			]

	random.shuffle(deck)

	#for a 3 person game, which cards I would pick in order
	"""
	I have to be able to 1. select what cards I would pick first and 2. compare one card to another as to why I picked
	one card rather than another.
	[higher card, your card, lower card]
	"""
	cards = deck[:3]
	data[a] = list(range(3))
	print(cards)
	for i in range(3):
		inp = int(input("%i card: "%(i+1)))
		if inp == 4:
			break
		choice = cards[inp-1]
		data[a][i] = (choice)
		f.write(data[a][i]+" ")
		for j in range(leng):
			if deck_data[j][0] == choice:
				deck_data[j][1] += i
				deck_data[j][2] += 1

	f.write("\n")
	if inp == 4:
		break
	
#sorting the cards from lowest ranking to highest
rankings = [deck_data[i][1] for i in range(leng)]
rankings.sort()
#for loops that represents the generator
"""
data_sorted = [None for i in range(leng)]
for l in range(leng):
	for m in range(leng):
		if ranings[l] == deck_data[m][1]:
			data_sorted.append(deck_data[m][1])
			continue """
data_sorted = [deck_data[m][1] for l in range(leng) for m in range(leng) if rankings[l] == deck_data[m][1]]
for k in range(leng):
	f.write(str(data_sorted[k])+"\n")

f.close()
