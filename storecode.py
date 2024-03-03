import csv
import sys
from time import sleep as wait
sys.setrecursionlimit(5000)
INSIDE = []
FLOWERS = 0
OUTSIDE = []
ALLHANDS = []
WILDCARD = None
WILDCARD_COUNTER = 0
LAST_PICKED = None
LAST_INSIDE = None
INSIDE_WINDOW_COUNTER = 0
def readwriteCSV(file, option, data=""):
	if option == "r":
		with open(file) as csv_file:
			lines = []
			read = csv.reader(csv_file, delimiter = ",")
			for line in read:
				lines.append(line)
		return lines
	elif option == "a":
		with open(file, "a") as csv_file:
			writer = csv.writer(csv_file, lineterminator="\n")
			writer.writerow(data)

def isPong(tiles, tile):
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) == 3:
		return True
	return False

def isSequence(tiles, tile):
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+1)}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+2)}) >= 1:
		return True
	return False

def removePong(tiles, tile):
	# if tile['number'] == 3:
	# 	print(tiles)
	tempTiles = tiles[:]
	try:
		for i in range(3):
			tempTiles.remove({'suit':tile['suit'],'number':tile['number']})
			# print(tempTiles, "\t\t\t", tile)
		return tempTiles
	except:
		return False

def removeSequence(tiles, tile):
	tempTiles = tiles[:]
	try:
		for i in range(3):
			tempTiles.remove({'suit':tile['suit'],'number':(tile['number']+i)})
		return tempTiles
	except:
		return False

def makeTile(suit, number):
	return {'suit':suit, 'number':number}

def readOutside(lstMarker, data, index1, currentIndex):
	marker = lstMarker
	current = currentIndex
	tempDict = {}
	tileCounter = 0
	cardName = None
	while marker <= current:
		if (marker%2) == 0:
			tileCounter += 1
			cardName = "card"+str(tileCounter)
			if tileCounter == 1:
				tempDict[cardName] = makeTile(data[index1][marker-1][2], data[index1][marker][0])
			else:
				tempDict[cardName] = makeTile(data[index1][marker-1][1], data[index1][marker][0])
		marker += 1
	return tempDict

def readData(data):
	outsideCounter = 0
	stopProgram = False
	for i in range(len(data)):
		if data[i][0].lower() == "inside":
			for j in range(len(data[i])):
				if (j%2) == 0 and j != 0:
					INSIDE.append(makeTile(int(data[i][j-1][1]),int(data[i][j][0])))
		elif data[i][0].lower() == "flower":
			FLOWERS = int(data[i][1])
		elif data[i][0].lower() == "outside":
			progress = 0
			marker = None
			for j in range(len(data[i])):
				try:
					if data[i][j][0] == "(":
						progress += 1
						if data[i][j][1] == "(":
							progress += 1
							marker = j
						if progress > 2:
							stopProgram = True
					elif data[i][j][1] == ")":
						progress -= 1
						if data[i][j][2] == ")":
							progress -= 1
							OUTSIDE.append(readOutside(marker, data, i, j))
				except:
					pass
	return stopProgram

def insideKeySuit(dict):
	return dict['suit']

def insideKeyNumber(dict):
	return dict['number']

def allPongs():
	eyes = 0
	for i in range(len(INSIDE)):
		if i == 0:
			marker = i
		elif i == len(INSIDE)-1:
			if eyes == 0:
				if INSIDE[i] != INSIDE[i-1]:
					return False
				eyes += 1
			elif eyes == 1:
				if INSIDE[i] != INSIDE[i-1] or INSIDE[i-1] != INSIDE[i-2]:
					return False
		else:
			if INSIDE[i] != INSIDE[i-1]:
				if i - marker == 2:
					eyes += 1
				while marker < i-1:
					if INSIDE[marker] != INSIDE[marker+1]:
						return False
					marker += 1
				marker = i
	if eyes > 1:
		return False
	for i in range(len(OUTSIDE)):
		if OUTSIDE[i]['card1'] != OUTSIDE[i]['card2'] or OUTSIDE[i]['card2'] != OUTSIDE[i]['card3']:
			return False
		if len(OUTSIDE[i]) == 4:
			if OUTSIDE[i]['card3'] != OUTSIDE[i]['card4']:
				return False
	return True

def findEyes():
	possibleHands = []
	possibleEyes = []
	seen = []
	c = []
	d = []
	s = []
	w = []

	for a in range(2):
		if a == 0:
			for i in range(len(INSIDE)):
				if INSIDE[i]['suit'] == 1:
					c.append(INSIDE[i])
				elif INSIDE[i]['suit'] == 2:
					d.append(INSIDE[i])
				elif INSIDE[i]['suit'] == 3:
					s.append(INSIDE[i])
				elif INSIDE[i]['suit'] == 4:
					w.append(INSIDE[i])
		else:
			if len(c) % 3 == 2:
				lstSuit = c
			elif len(d) % 3 == 2:
				lstSuit = d
			elif len(s) % 3 == 2:
				lstSuit = s
			elif len(w) % 3 == 2:
				lstSuit = w
			for i in range(len(lstSuit)):
				if lstSuit[i] in possibleEyes:
					pass
				elif lstSuit[i] in seen:
					possibleEyes.append(lstSuit[i])
				else:
					seen.append(lstSuit[i])
	for i in range(len(possibleEyes)):
		# print(possibleEyes[i], "helllooooo\n\n\n\n")
		makeHand(possibleEyes[i])

def helper(accumHand, remaining, eyes):
	newAccumHand1 = accumHand[:]
	newAccumHand2 = accumHand[:]
	if len(remaining) == 0:
		newHand = accumHand[:]
		newHand.append({'eyes1':eyes,'eyes2':eyes})
		ALLHANDS.append(newHand)
		for i in range(len(newHand)):
			print(newHand[i])
		print("\n")
		pass
	else:
		if isPong(remaining, remaining[0]):
			newAccumHand1.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])},
								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])}})
			tempTiles = removePong(remaining, remaining[0])
			if tempTiles != False:
				helper(newAccumHand1, tempTiles, eyes)
			else:
				pass
		if isSequence(remaining, remaining[0]):
			newAccumHand2.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+1)},
								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+2)}})
			# print(newAccumHand)
			tempTiles = removeSequence(remaining, remaining[0])
			if tempTiles != False:
				helper(newAccumHand2, tempTiles, eyes)
			else:
				pass

def makeHand(eyes):
	tempInside = list(INSIDE)
	for i in range(2):
		tempInside.remove(eyes)
	helper([], tempInside, eyes)

def findSequences(possibleEyes):
	possEyes = list(possibleEyes)
	pass

def main():
	testName = "testcaseKenny1.csv"
	data = readwriteCSV(testName, "r")
	stopProgram = readData(data)
	if not stopProgram:
		INSIDE.sort(key=insideKeyNumber)
		INSIDE.sort(key=insideKeySuit)
		# print("inside:")
		# print(INSIDE)
		# print("flowers:", FLOWERS)
		# print("outside:")
		# for i in range(len(OUTSIDE)):
		# 	print(OUTSIDE[i], "\n")
		findEyes()
		# for i in range(len(ALLHANDS)):
		# 	for j in range(len(ALLHANDS[i])):
		# 		print(ALLHANDS[i][j])
		# print(allPongs())
main()