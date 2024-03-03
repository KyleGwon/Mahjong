import csv
import sys
from time import sleep as wait
import scoring as score
from graphics import *
INSIDE = []
FLOWERS = 0
OUTSIDE = []
ALLHANDS = []
WILDCARD = None
WILDCARD_COUNT = 0
LAST_PICKED = None
LAST_INSIDE = None
SELF_PICK = None
FLOWER_PICK = None
DEALER_COUNT = 0
CALLING_FROM_START = None
NICKLE_HANDS = []
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

def isMiddle(tiles, tile):
	for i in range(len(tiles)):
		if tile == tiles[i]['card2'] and isSequence(tiles, tile):
			return True
	return False

def isSpecialMiddle(tiles, tile):
	for i in range(len(tiles)-1):
		if tile == tiles[i]['card2'] and specialSequence(tiles, tile):
			return True
	return False

def isPong(tiles, tile):
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) == 3:
		return True
	elif tiles.count(tile) == 2 and WILDCARD in tiles:
		return True
	elif tile in tiles and tiles.count(WILDCARD) == 2:
		return True
	elif tile == WILDCARD and tiles.count({'suit':4,'number':8}) == 2:
		return True
	return False

def isPair(tiles, tile):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) == 2:
		return True
	elif tile in tiles and WILDCARD in tiles:
		return True
	return False

def isKong(tiles, tile):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) == 4:
		return True
	elif tiles.count(tile) == 3 and WILDCARD in tiles:
		return True
	elif tiles.count(tile) == 2 and tiles.count(WILDCARD) == 2:
		return True
	elif tiles.count(tile) == 1 and tiles.count(WILDCARD) == 3:
		return True
	return False


def isSequence(tiles, tile):
	if tiles.count({'suit':tile['suit'],'number':tile['number']}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+1)}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+2)}) >= 1:
		if tile['suit'] != 4:
			return True
	return False

def specialSequence(tiles, tile, returnPlacement=False, remove=False):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	valid = True
	if tiles.count({'suit':4,'number':8}) >= 1 and WILDCARD['suit'] != 4:
		if tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-2)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)}) >= 1:
			placement = "card1"
			if remove:
				tempTiles = tiles[:]
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-2)})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)})
				tempTiles.remove({'suit':4,'number':8})
		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1:
			placement = "card2"
			if remove:
				tempTiles = tiles[:]
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)})
				tempTiles.remove({'suit':4,'number':8})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
		elif tile == {'suit':4,'number':8} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1 and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)}) >= 1:
			placement = "card3"
			if remove:
				tempTiles = tiles[:]
				tempTiles.remove({'suit':4,'number':8})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)}) >= 1:
			placement = "card4"
			if remove:
				tempTiles = tiles[:]
				tempTiles.remove({'suit':4,'number':8})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1:
			placement = "card5"
			if remove:
				tempTiles = tiles[:]
				tempTiles.remove({'suit':4,'number':8})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
		else:
			valid = False
		if not valid:
			return False
		if remove:
			if returnPlacement:
				return placement, tempTiles
			elif not returnPlacement:
				return tempTiles
		if not returnPlacement:
			return True
		return placement
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
	return {'suit':int(suit), 'number':int(number)}

def readOutside(lstMarker, data, index1, currentIndex):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
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
				tempDict[cardName] = makeTile(int(data[index1][marker-1][2]), int(data[index1][marker][0]))
			else:
				tempDict[cardName] = makeTile(int(data[index1][marker-1][1]), int(data[index1][marker][0]))
		marker += 1
	return tempDict

def readData(data):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	outsideCounter = 0
	stopProgram = False
	for i in range(len(data)):
		if data[i][0].lower() == "inside":
			for j in range(len(data[i])):
				if (j%2) == 0 and j != 0:
					INSIDE.append(makeTile(int(data[i][j-1][1]),int(data[i][j][0])))
		elif data[i][0].lower() == "flowers":
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
		elif data[i][0].lower() == "wildcard":
			WILDCARD = makeTile(int(data[i][1][1]),int(data[i][2][0]))
		elif data[i][0].lower() == "wildcard_counter":
			WILDCARD_COUNT = int(data[i][1])
		elif data[i][0].lower() == "last_picked":
			LAST_PICKED = makeTile(int(data[i][1][1]),int(data[i][2][0]))
		elif data[i][0].lower() == "LAST_INSIDE":
			if data[i][1].lower() == "true":
				LAST_INSIDE = True
			elif data[i][1].lower() == "false":
				LAST_INSIDE = False
		elif data[i][0].lower() == "self_pick":
			if data[i][1].lower() == "true":
				SELF_PICK = True
			elif data[i][1].lower() == "false":
				SELF_PICK = False
		elif data[i][0].lower() == "flower_pick":
			if data[i][1].lower() == "true":
				FLOWER_PICK = True
			elif data[i][1].lower() == "false":
				FLOWER_PICK = False
		elif data[i][0].lower() == "dealer_count":
			DEALER_COUNT = int(data[i][1])
		elif data[i][0].lower() == "calling_from_start":
			if data[i][1].lower() == "true":
				CALLING_FROM_START = True
			elif data[i][1].lower() == "false":
				CALLING_FROM_START = False
	return stopProgram

def insideKeySuit(dict):
	return dict['suit']

def insideKeyNumber(dict):
	return dict['number']

# def allPongs():
# 	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
# 	eyes = 0
# 	for i in range(len(INSIDE)):
# 		if i == 0:
# 			marker = i
# 		elif i == len(INSIDE)-1:
# 			if eyes == 0:
# 				if INSIDE[i] != INSIDE[i-1]:
# 					return False
# 				eyes += 1
# 			elif eyes == 1:
# 				if INSIDE[i] != INSIDE[i-1] or INSIDE[i-1] != INSIDE[i-2]:
# 					return False
# 		else:
# 			if INSIDE[i] != INSIDE[i-1]:
# 				if i - marker == 2:
# 					eyes += 1
# 				while marker < i-1:
# 					if INSIDE[marker] != INSIDE[marker+1]:
# 						return False
# 					marker += 1
# 				marker = i
# 	if eyes > 1:
# 		return False
# 	for i in range(len(OUTSIDE)):
# 		if OUTSIDE[i]['card1'] != OUTSIDE[i]['card2'] or OUTSIDE[i]['card2'] != OUTSIDE[i]['card3']:
# 			return False
# 		if len(OUTSIDE[i]) == 4:
# 			if OUTSIDE[i]['card3'] != OUTSIDE[i]['card4']:
# 				return False
# 	return True

def findEyes(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	possibleHands = []
	possibleEyes = []
	seen = []
	c = []
	d = []
	s = []
	w = []
	c2 = []
	d2 = []
	s2 = []
	w2 = []
	lstSuit = []
	lstSuit2 = []
	for a in range(2):
		if a == 0:
			# for i in range(len(tiles)):
			# 	if tiles[i]['suit'] == 1:
			# 		c.append(tiles[i])
			# 	elif tiles[i]['suit'] == 2:
			# 		d.append(tiles[i])
			# 	elif tiles[i]['suit'] == 3:
			# 		s.append(tiles[i])
			# 	elif tiles[i]['suit'] == 4:
			# 		w.append(tiles[i])

			for i in range(len(tiles)):
				if tiles[i]['suit'] == 1:
					c2.append(tiles[i])
				if tiles[i]['suit'] == 2:
					d2.append(tiles[i])
				if tiles[i]['suit'] == 3:
					s2.append(tiles[i])
				if tiles[i] == {'suit':4,'number':7}:
					if WILDCARD['suit'] == 1:
						c2.append(WILDCARD)
					if WILDCARD['suit'] == 2:
						d2.append(WILDCARD)
					if WILDCARD['suit'] == 3:
						s2.append(WILDCARD)
					if WILDCARD['suit'] == 4:
						w2.append(WILDCARD)
				elif tiles[i]['suit'] == 4:
					w2.append(tiles[i])


		else:
			# if len(c) % 3 == 2:
			# 	lstSuit = c
			# elif len(d) % 3 == 2:
			# 	lstSuit = d
			# elif len(s) % 3 == 2:
			# 	lstSuit = s
			# elif len(w) % 3 == 2:
			# 	lstSuit = w
			if len(c2) % 3 == 2:
				lstSuit2 = c2
			elif len(d2) % 3 == 2:
				lstSuit2 = d2
			elif len(s2) % 3 == 2:
				lstSuit2 = s2
			elif len(w2) % 3 == 2:
				lstSuit2 = w2
			# for i in range(len(lstSuit)):
			# 	if lstSuit[i] in possibleEyes:
			# 		pass
			# 	elif lstSuit[i] in seen:
			# 		possibleEyes.append(lstSuit[i])
			# 	else:
			# 		seen.append(lstSuit[i])
			for i in range(len(lstSuit2)):
				if lstSuit2[i] in possibleEyes:
					pass
				elif lstSuit2[i] in seen:
					lstSuit2[i] == WILDCARD
					# print(lstSuit2)
					possibleEyes.append(lstSuit2[i])
				else:
					seen.append(lstSuit2[i])
	for i in range(len(possibleEyes)):
		if {'suit':4, 'number':7} in tiles:
			tempTiles = tiles[:]
			tempPossibleEye = possibleEyes[i]
			while {'suit':4, 'number':7} in tempTiles:
				tempTiles.remove({'suit':4, 'number':7})
				tempTiles.append({'suit':4, 'number':8})
			if {'suit':4, 'number':7} == tempPossibleEye:
				tempPossibleEye = {'suit':4, 'number':8}
			# if {'suit':2,'number':7} in tiles:
			# 	print()
			makeHand(tempTiles, tempPossibleEye)
		if tiles.count(possibleEyes[i]) > 1:
			makeHand(tiles, possibleEyes[i])

def helper(accumHand, remaining, eyes, different=False):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	newAccumHand1 = accumHand[:]
	newAccumHand2 = accumHand[:]
	if len(remaining) == 0:
		newHand = accumHand[:]
		if different:
			newHand.append({'eyes1':{'suit':4,'number':8},'eyes2':eyes})
		else:
			newHand.append({'eyes1':eyes,'eyes2':eyes})
		ALLHANDS.append(newHand)
		# print(ALLHANDS)
		pass
	else:
		if isPong(remaining, remaining[0]):
			newAccumHand1.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])},
								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])}})
			tempTiles = removePong(remaining, remaining[0])
			if tempTiles != False:
				if different:
					helper(newAccumHand1, tempTiles, eyes, True)
				else:
					helper(newAccumHand1, tempTiles, eyes)
			else:
				pass
		if remaining[0]['suit'] != 4:
			if isSequence(remaining, remaining[0]):
				newAccumHand2.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
									'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+1)},
									'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+2)}})
				tempTiles = removeSequence(remaining, remaining[0])
				if tempTiles != False:
					if different:
						helper(newAccumHand2, tempTiles, eyes, True)
					else:
						helper(newAccumHand2, tempTiles, eyes)
				else:
					pass
		if specialSequence(remaining, remaining[0], True) == "card1":
			newAccumHand2.append({	'card1':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']-2)},
								'card2':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)},
								'card3':{'suit':4,'number':8}})
			tempTiles = specialSequence(remaining, remaining[0], False, True)
			if different:
				helper(newAccumHand2, tempTiles, eyes, True)
			else:
				helper(newAccumHand2, tempTiles, eyes)

		elif specialSequence(remaining, remaining[0], True) == "card2":
			newAccumHand2.append({	'card1':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)},
								'card2':{'suit':4,'number':8},
								'card3':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}})
			tempTiles = specialSequence(remaining, remaining[0], False, True)
			if different:
				helper(newAccumHand2, tempTiles, eyes, True)
			else:
				helper(newAccumHand2, tempTiles, eyes)

		elif specialSequence(remaining, remaining[0], True) == "card3" or specialSequence(remaining, remaining[0], True) == "card4" or specialSequence(remaining, remaining[0], True) == "card5":
			newAccumHand2.append({	'card1':{'suit':4,'number':8},
								'card2':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)},
								'card3':{'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)}})
			tempTiles = specialSequence(remaining, remaining[0], False, True)
			if different:
				helper(newAccumHand2, tempTiles, eyes, True)
			else:
				helper(newAccumHand2, tempTiles, eyes)
		else:
			pass

def makeHand(tiles, eyes):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempInside = list(tiles)
	# if eyes not in tempInside and {'suit':4,'number':8} in tempInside:
	# 	for i in range(2):
	# 		tempInside.remove({'suit':4,'number':8})
	# else:
	normal = True
	# print(tempInside, '\n\nthese are eyes', eyes)
	for i in range(2):
		try:
			tempInside.remove(eyes)
		except:
			tempInside.remove({'suit':4,'number':8})
			normal = False
	if normal:
		helper([], tempInside, eyes)
	else:
		helper([], tempInside, eyes, True)

def foo(wildcards):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	sCounter = 1
	nCounter = 1
	while True:
		tempWildcards = wildcards[:]
		if sCounter == 4 and nCounter == 8:
			break
		else:
			if len(tempWildcards) == (WILDCARD_COUNT):
				localInside = INSIDE[:]
				run = True
				for i in range(len(tempWildcards)):
					localInside.append(tempWildcards[i])
					if localInside.count(tempWildcards[i]) > 4:
						run = False
				if run:
					nickleNicklePoints(localInside)
					tempInside = localInside[:]
					implementWildcardHelper(localInside)

			else:
				currentWild = makeTile(sCounter, nCounter)
				tempWildcards.append(currentWild)
				foo(tempWildcards)

			if nCounter == 9:
				sCounter += 1
				nCounter = 1
			else:
				nCounter += 1
		

def implementWildcardHelper(tempInside):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	counter1 = 0
	counter2 = 0
	counter3 = 0
	counter4 = 0
	specCounter1 = 0
	specCounter2 = 0
	specCounter3 = 0
	specCounter4 = 0
	hasEyes = False
	valid = True

	for k in range(len(tempInside)):
		if tempInside[k]['suit'] == 1:
			counter1 += 1
		if tempInside[k]['suit'] == 2:
			counter2 += 1
		if tempInside[k]['suit'] == 3:
			counter3 += 1
		if tempInside[k]['suit'] == 4:
			counter4 += 1

	for k in range(len(tempInside)):
		if tempInside[k]['suit'] == 1:
			specCounter1 += 1
		if tempInside[k]['suit'] == 2:
			specCounter2 += 1
		if tempInside[k]['suit'] == 3:
			specCounter3 += 1
		if tempInside[k] == {'suit':4,'number':7}:
			if WILDCARD['suit'] == 1:
				specCounter1 += 1
			if WILDCARD['suit'] == 2:
				specCounter2 += 1
			if WILDCARD['suit'] == 3:
				specCounter3 += 1
			if WILDCARD['suit'] == 4:
				specCounter4 += 1
		elif tempInside[k]['suit'] == 4:
			specCounter4 += 1

	if counter1 % 3 == 2 or counter1 % 3 == 1:
		if hasEyes or counter1 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if counter2 % 3 == 2 or counter2 % 3 == 1:
		if hasEyes or counter2 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if counter3 % 3 == 2 or counter3 % 3 == 1:
		if hasEyes or counter3 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if counter4 % 3 == 2 or counter4 % 3 == 1:
		if hasEyes or counter4 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if valid and hasEyes:
		tempInside.sort(key=insideKeyNumber)
		tempInside.sort(key=insideKeySuit)
		findEyes(tempInside)

	hasEyes = False
	valid = True
	if specCounter1 % 3 == 2 or specCounter1 % 3 == 1:
		if hasEyes or specCounter1 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if specCounter2 % 3 == 2 or specCounter2 % 3 == 1:
		if hasEyes or specCounter2 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if specCounter3 % 3 == 2 or specCounter3 % 3 == 1:
		if hasEyes or specCounter3 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if specCounter4 % 3 == 2 or specCounter4 % 3 == 1:
		if hasEyes or specCounter4 % 3 == 1:
			valid = False
		else:
			hasEyes = True
	if valid and hasEyes:
		tempInside.sort(key=insideKeyNumber)
		tempInside.sort(key=insideKeySuit)
		findEyes(tempInside)



def nickleNicklePoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	points = 0
	if len(OUTSIDE) == 0:
		nickleTiles = []
		tempTiles = tiles[:]
		seen = []
		hasPong = False
		valid = True
		for i in range(len(tiles)):
			if isPair(tempTiles, tiles[i]) and tiles[i] not in seen:
				seen.append(tiles[i])
				nickleTiles.append({'card1':tiles[i],'card2':tiles[i]})
				while tiles[i] in tempTiles:
					tempTiles.remove(tiles[i])
			elif isPong(tempTiles, tiles[i]) and tiles[i] not in seen:
				if hasPong:
					valid = False
				else:
					nickleTiles.append({'card1':tiles[i],'card2':tiles[i],'card3':tiles[i]})
					hasPong = True
				seen.append(tiles[i])
				while tiles[i] in tempTiles:
					tempTiles.remove(tiles[i])
			elif isKong(tempTiles,tiles[i]):
				seen.append(tiles[i])
				nickleTiles.append({'card1':tiles[i],'card2':tiles[i]})
				nickleTiles.append({'card1':tiles[i],'card2':tiles[i]})
				while tiles[i] in tempTiles:
					tempTiles.remove(tiles[i])
			elif tiles[i] in seen:
				pass
			else:
				valid = False
		# for i in range(len(tiles)):

			# if i % 2 == 0:
			# 	if tiles[i] == tiles[i+1]:
			# 		if tiles
			# 	else:
			# 		valid = False
		if hasPong and valid:
			nickleTiles.append({'eyes1':{'suit':0,'number':0}})
			points += 20
			points += selfPickPoints()
			points += flowersWordsPoints(nickleTiles)
			points += nickleLastCardPoints(nickleTiles)
			points += wildcardPoints(nickleTiles)
			points += wildcardPickPoints()
			points += flowerPickPoints()
			points += sameSuitPoints(nickleTiles)
			points += dealerPoints()
			points += callingStartPoints()
			points += 3
		NICKLE_HANDS.append([nickleTiles, points])

def nickleLastCardPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	for i in range(len(tiles)):
		if i != len(tiles)-1:
			try:
				if LAST_PICKED == tiles[i]['card3']:
					return 1
			except:
				if LAST_PICKED == tiles[i]['card1']:
					return 2
	return 0

def flowerPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	return FLOWERS
def wordPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:]
	wordCounter = 0
	wordInEyes = False
	wordSeen = []
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		try:
			if tempTiles[i]['card1']['suit'] == 4 and tempTiles[i]['card1']['number'] != 8:
				if tempTiles[i]['card1'] not in wordSeen:
					wordSeen.append(tempTiles[i]['card1'])
					wordCounter += 1
		except:
			if tempTiles[i]['eyes1']['suit'] == 4 and tempTiles[i]['eyes1']['number'] != 8:
				if tempTiles[i]['eyes1'] not in wordSeen:
					wordSeen.append(tempTiles[i]['eyes1'])
					wordInEyes = True
					wordCounter += 1
	# if wordCounter == 0:
	# 	return 1
	if wordInEyes:
		return wordCounter-1
	return wordCounter
def flowersWordsPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	points = 0
	if flowerPoints() == 0 and wordPoints(tiles) == 0:
		points = 3
		return points
	if flowerPoints() == 0:
		points += 1
	else:
		points += flowerPoints()
	if wordPoints(tiles) == 0:
		points += 1
	# print(points)
	else:
		points += wordPoints(tiles)
	# print(points, 'jslkdfjlaksjflksdjflkjsdlkfjlksdjdflk')
	return points

# def findWildcards(tiles):
# 	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
# 	for i in range(len(tiles)-1):
# 		for i in range(3):
# 			cardName = 'card'+str(j)

def lastCardPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	pointCounter = 0
	tempLastPicked = dict(LAST_PICKED)
	hasOne = False
	# print(tempLastPicked, WILDCARD)
	# if tempLastPicked == WILDCARD:
	if tempLastPicked == WILDCARD:
		wildcards = []
		tempInside = INSIDE[:]
		countLst = []
		# print(tempInside)
		# print(len(tempInside), len(tiles))
		for i in range(len(tiles)-1):
			for j in range(3):
				cardName = 'card'+str(j+1)
				try:
				# if tiles[i][cardName] in tempInside:
					tempInside.remove(tiles[i][cardName])
				except:
				# else:
					wildcards.append(tiles[i][cardName])
					# print(len(wildcards))
					# print("hi goomby")
		try:
			if tiles[len(tiles)-1]['eyes'] == {'suit':4,'number':8}:
				tempInside.remove({{'suit':4,'number':7}})
			tempInside.remove(tiles[len(tiles)-1]['eyes1'])
		except:
			wildcards.append(tiles[len(tiles)-1]['eyes1'])
		try:
			if tiles[len(tiles)-1]['eyes'] == {'suit':4,'number':8}:
				tempInside.remove({{'suit':4,'number':7}})
			tempInside.remove(tiles[len(tiles)-1]['eyes2'])
		except:
			wildcards.append(tiles[len(tiles)-1]['eyes2'])
		# if len(wildcards) > 2:
			# print("inside", INSIDE)
			# print("wild", wildcards)
			# print('eyes', tiles[len(tiles)-1])
			# print('\n')
		for i in range(len(wildcards)):
			# print(wildcards[i])
			if tiles[len(tiles)-1]['eyes1'] == wildcards[i] or tiles[len(tiles)-1]['eyes1'] == wildcards[i]:
				pointCounter = 2
				return pointCounter
			for j in range(len(tiles)-1):
				if tiles[j]['card2'] == wildcards[i]:
					if tiles[j]['card1'] == wildcards[i]:
						if pointCounter == 0:
							pointCounter = 1
					else:
						pointCounter = 2
						break
				if tiles[j]['card1']['suit'] != 4 and tiles[j]['card1']['number'] == 1:
					if tiles[j]['card3']['number'] == tiles[j]['card1']['number']+2 and wildcards[i] == tiles[j]['card3']:
						pointCounter = 2
					elif tiles[j]['card3'] == {'suit':4,'number':8}:
						if WILDCARD['number'] == tiles[j]['card1']['number']+2 and wildcards[i] == {'suit':4,'number':7}:
							pointCounter = 2
				elif tiles[j]['card3']['suit'] != 4 and tiles[j]['card3']['number'] == 8:
					if tiles[j]['card1']['number'] == tiles[j]['card3']['number']-2 and wildcards[i] == tiles[j]['card1']:
						pointCounter = 2
					elif tiles[j]['card1'] == {'suit':4,'number':8}:
						if WILDCARD['number'] == tiles[j]['card3']['number']-2 and wildcards[i] == {'suit':4,'number':7}:
							pointCounter = 2
				if pointCounter == 2:
					return pointCounter
				elif pointCounter == 1:
					hasOne = True
		# print(wildcards)



	if tiles[len(tiles)-1]['eyes1'] == tempLastPicked:
		pointCounter = 2
		return pointCounter
	for i in range(len(tiles)-1):
		if tiles[i]['card2'] == tempLastPicked:
			# print('ljsdkfjkdjf')
			if tiles[i]['card1'] == tempLastPicked:
				if pointCounter == 0:
					pointCounter = 1
			else:
				pointCounter = 2
				break
		if tiles[i]['card1']['suit'] != 4 and tiles[i]['card1']['number'] == 1:
			if tiles[i]['card3']['number'] == tiles[i]['card1']['number']+2 and tempLastPicked == tiles[i]['card3']:
				pointCounter = 2
			elif tiles[i]['card3'] == {'suit':4,'number':8}:
				if WILDCARD['number'] == tiles[i]['card1']['number']+2 and tempLastPicked == {'suit':4,'number':7}:
					pointCounter = 2
		elif tiles[i]['card3']['suit'] != 4 and tiles[i]['card3']['number'] == 8:
			if tiles[i]['card1']['number'] == tiles[i]['card3']['number']-2 and tempLastPicked == tiles[i]['card1']:
				pointCounter = 2
			elif tiles[i]['card1'] == {'suit':4,'number':8}:
				if WILDCARD['number'] == tiles[i]['card3']['number']-2 and tempLastPicked == {'suit':4,'number':7}:
					pointCounter = 2
	if pointCounter == 0 and hasOne:
		return 1
	return pointCounter

def selfPickPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if SELF_PICK:
		return 1
	return 0

def flowerPickPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if FLOWER_PICK:
		return 1
	return 0

def wildcardPickPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if LAST_PICKED == WILDCARD:
		return 1
	return 0



def kongPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	points = 0
	for i in range(len(OUTSIDE)):
		try:
			if OUTSIDE[i]['card4'] != None:
				points += 1
		except:
			pass
	return points

def selfPickConcealedPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if SELF_PICK:
		tempOutside = []
		for i in range(len(OUTSIDE)):
			try:
				if OUTSIDE[i]['card4'] != None:
					pass
			except:
				tempOutside.append(OUTSIDE[i])
		if len(tempOutside) == 0:
			return 3
	return 0

def eyesPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if tiles[len(tiles)-1]['eyes1'] == {'suit':4,'number':8}:
		if WILDCARD['number'] == 8:
			return 1
	else:	
		if tiles[len(tiles)-1]['eyes1']['number'] == 2 or tiles[len(tiles)-1]['eyes1']['number'] == 5 or tiles[len(tiles)-1]['eyes1']['number'] == 8:
			return 1
	return 0

def runningWildHelper(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	eyesCount = 0
	outsideCount = 0
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1'] == tiles[len(tiles)-1]['eyes1']:
			eyesCount += 1
		if tempTiles[i]['card2'] == tiles[len(tiles)-1]['eyes1']:
			eyesCount += 1
		if tempTiles[i]['card3'] == tiles[len(tiles)-1]['eyes1']:
			eyesCount += 1
	if INSIDE.count(tiles[len(tiles)-1]['eyes1']) < eyesCount:
		return 4
	return 0
def runningWildPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	points = 0
	if SELF_PICK:
		if LAST_PICKED != WILDCARD:
			points = runningWildHelper(tiles)
	else:
		points = runningWildHelper(tiles)
	return points

def wildcardPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:len(tiles)-1]
	if WILDCARD_COUNT == 0: 
		return 5
	else:
		points = 0
		for i in range(len(tempTiles)):
			try:
				for cardNum in range(3):
					cardName = "card"+str(cardNum+1)
					if tempTiles[i][cardName] == WILDCARD:
						points += 5
			except:
				for cardNum in range(2):
					cardName = "card"+str(cardNum+1)
					if tempTiles[i][cardName] == WILDCARD:
						points += 5
		if WILDCARD_COUNT == 4:
			points += 15
	return points

def dealerPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	points = 0
	if DEALER_COUNT != 0:
		points = 1+((DEALER_COUNT-1)*2)
	return points

def callingStartPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if DEALER_COUNT == 0 and CALLING_FROM_START:
		return 40
	elif DEALER_COUNT != 0 and CALLING_FROM_START:
		return 20
	return 0

def concealedPoints():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if len(OUTSIDE) == 0:
		return 1
	return 0

def sameNumberPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	c = []
	d = []
	s = []
	w = []
	suits = [c,d,s,w]
	for i in range(len(tiles)-1):
		if tiles[i]['card1'] == tiles[i]['card2']:
			if tiles[i]['card1']['suit'] == 1:
				c.append(tiles[i]['card1']['number'])
			elif tiles[i]['card1']['suit'] == 2:
				d.append(tiles[i]['card1']['number'])
			elif tiles[i]['card1']['suit'] == 3:
				s.append(tiles[i]['card1']['number'])
			elif tiles[i]['card1']['suit'] == 4:
				w.append(tiles[i]['card1']['number'])

	for i in range(len(OUTSIDE)):
		if OUTSIDE[i]['card1'] == OUTSIDE[i]['card2']:
			if OUTSIDE[i]['card1']['suit'] == 1:
				c.append(OUTSIDE[i]['card1']['number'])
			elif OUTSIDE[i]['card1']['suit'] == 2:
				d.append(OUTSIDE[i]['card1']['number'])
			elif OUTSIDE[i]['card1']['suit'] == 3:
				s.append(OUTSIDE[i]['card1']['number'])
			elif OUTSIDE[i]['card1']['suit'] == 4:
				w.append(OUTSIDE[i]['card1']['number'])

	for i in range(len(c)):
		if c[i] in d and c[i] in s:
			return 10
		elif c[i] in d and c[i] in w:
			return 10
		elif c[i] in s and c[i] in w:
			return 10
	for i in range(len(d)):
		if d[i] in s and d[i] in w:
			return 10
	counter = 0
	for i in range(len(suits)):
		if tiles[len(tiles)-1]['eyes1']['number'] in suits[i]:
			counter += 1
	if counter == 2:
		return 5
	return 0 

def straightPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1'] == tempTiles[i]['card2']:
			return 0
		elif tempTiles[i]['card1'] == {'suit':4,'number':8} and tempTiles[i]['card2'] == WILDCARD:
			return 0
		elif tempTiles[i]['card1'] == WILDCARD and tempTiles[i]['card2'] == {'suit':4,'number':8}:
			return 0
		elif tempTiles[i]['card1']['suit'] == 4:
			return 0
	if FLOWERS == 0:
		return 10
	return 3

def eachSuitPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	c = 0
	d = 0
	s = 0
	w = 0
	m = 0
	suits = [0,0,0,0,0]
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1'] == {'suit':4,'number':8}:
			if WILDCARD['suit'] == 1:
				suits[0] += 1
			elif WILDCARD['suit'] == 2:
				suits[1] += 1
			elif WILDCARD['suit'] == 3:
				suits[2] += 1
			elif WILDCARD['suit'] == 4 and WILDCARD['number'] <= 4:
				suits[3] += 1
			elif WILDCARD['suit'] == 4 and WILDCARD['number'] >= 5:
				suits[4] += 1
		else:
			if tempTiles[i]['card1']['suit'] == 1:
				suits[0] += 1
			elif tempTiles[i]['card1']['suit'] == 2:
				suits[1] += 1
			elif tempTiles[i]['card1']['suit'] == 3:
				suits[2] += 1
			elif tempTiles[i]['card1']['suit'] == 4 and tempTiles[i]['card1']['number'] <= 4:
				suits[3] += 1
			elif tempTiles[i]['card1']['suit'] == 4 and tempTiles[i]['card1']['number'] >= 5:
				suits[4] += 1
	if tiles[len(tiles)-1]['eyes1']['suit'] == 1:
		suits[0] += 1
	elif tiles[len(tiles)-1]['eyes1']['suit'] == 2:
		suits[1] += 1
	elif tiles[len(tiles)-1]['eyes1']['suit'] == 3:
		suits[2] += 1
	elif tiles[len(tiles)-1]['eyes1']['suit'] == 4 and tiles[len(tiles)-1]['eyes1']['number'] <= 4:
		suits[3] += 1
	elif tiles[len(tiles)-1]['eyes1'] == {'suit':4,'number':8}:
		if WILDCARD['suit'] != 4:
			suits[WILDCARD['suit']-1] += 1
		else:
			if WILDCARD['number'] <= 4:
				suits[3] += 1
			else:
				suits[4] += 1
	elif tiles[len(tiles)-1]['eyes1']['suit'] == 4 and tiles[len(tiles)-1]['eyes1']['number'] >= 5:
		suits[4] += 1
	if 0 not in suits:
		return 3
	return 0

def insidePongPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:len(tiles)-1]
	counter = 0
	if len(OUTSIDE) != 0:
		for i in range(len(OUTSIDE)):
			try:
				if OUTSIDE[i]['card4'] != None:
					tempTiles.append({'card1':OUTSIDE[i]['card1'],'card2':OUTSIDE[i]['card2'],'card3':OUTSIDE[i]['card3']})
			except:
				pass
	for i in range(len(tempTiles)):
		if not SELF_PICK and LAST_PICKED == tempTiles[i]['card1']:
			pass
		else:
			if tempTiles[i]['card1'] == tempTiles[i]['card2']:
				counter += 1
			elif tempTiles[i]['card1'] == {'suit':4,'number':8} and tempTiles[i]['card2'] == WILDCARD:
				counter += 1
			elif tempTiles[i]['card1'] == WILDCARD and tempTiles[i]['card2'] == {'suit':4,'number':8}:
				counter += 1
	if counter == 2:
		return 3
	elif counter == 3:
		return 8
	elif counter == 4:
		return 20
	elif counter == 5:
		return 40
	return 0

def allPongPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		if OUTSIDE[i]['card1'] != OUTSIDE[i]['card2']:
			return 0
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1'] == tempTiles[i]['card2']:
			pass
		elif tempTiles[i]['card1'] == {'suit':4,'number':8} and tempTiles[i]['card2'] == WILDCARD:
			pass
		elif tempTiles[i]['card1'] == WILDCARD and tempTiles[i]['card2'] == {'suit':4,'number':8}:
			pass
		else:
			return 0
	return 10

def dragonPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	c = []
	d = []
	s = []
	suits = [[],[],[]]
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['number'] == 1 and tempTiles[i]['card2']['number'] == 2:
			if tempTiles[i]['card1']['suit'] == 1:
				suits[0].append(1)
			elif tempTiles[i]['card1']['suit'] == 2:
				suits[1].append(1)
			elif tempTiles[i]['card1']['suit'] == 3:
				suits[2].append(1)
		elif tempTiles[i]['card1']['number'] == 4 and tempTiles[i]['card2']['number'] == 5:
			if tempTiles[i]['card1']['suit'] == 1:
				suits[0].append(2)
			elif tempTiles[i]['card1']['suit'] == 2:
				suits[1].append(2)
			elif tempTiles[i]['card1']['suit'] == 3:
				suits[2].append(2)
		elif tempTiles[i]['card1']['number'] == 7 and tempTiles[i]['card2']['number'] == 8:
			if tempTiles[i]['card1']['suit'] == 1:
				suits[0].append(3)
			elif tempTiles[i]['card1']['suit'] == 2:
				suits[1].append(3)
			elif tempTiles[i]['card1']['suit'] == 3:
				suits[2].append(3)
		elif tempTiles[i]['card1'] == {'suit':4,'number':8}:
			if tempTiles[i]['card2']['number'] == 2:
				if tempTiles[i]['card2']['suit'] == 1:
					suits[0].append(1)
				elif tempTiles[i]['card2']['suit'] == 2:
					suits[1].append(1)
				elif tempTiles[i]['card2']['suit'] == 3:
					suits[2].append(1)
			if tempTiles[i]['card2']['number'] == 5:
				if tempTiles[i]['card2']['suit'] == 1:
					suits[0].append(2)
				elif tempTiles[i]['card2']['suit'] == 2:
					suits[1].append(2)
				elif tempTiles[i]['card2']['suit'] == 3:
					suits[2].append(2)
			if tempTiles[i]['card2']['number'] == 8:
				if tempTiles[i]['card2']['suit'] == 1:
					suits[0].append(3)
				elif tempTiles[i]['card2']['suit'] == 2:
					suits[1].append(3)
				elif tempTiles[i]['card2']['suit'] == 3:
					suits[2].append(3)
		elif tempTiles[i]['card2'] == {'suit':4,'number':8}:
			if tempTiles[i]['card1']['number'] == 1:
				if tempTiles[i]['card1']['suit'] == 1:
					suits[0].append(1)
				elif tempTiles[i]['card1']['suit'] == 2:
					suits[1].append(1)
				elif tempTiles[i]['card1']['suit'] == 3:
					suits[2].append(1)
			if tempTiles[i]['card1']['number'] == 4:
				if tempTiles[i]['card1']['suit'] == 1:
					suits[0].append(2)
				elif tempTiles[i]['card1']['suit'] == 2:
					suits[1].append(2)
				elif tempTiles[i]['card1']['suit'] == 3:
					suits[2].append(2)
			if tempTiles[i]['card1']['number'] == 7:
				if tempTiles[i]['card1']['suit'] == 1:
					suits[0].append(3)
				elif tempTiles[i]['card1']['suit'] == 2:
					suits[1].append(3)
				elif tempTiles[i]['card1']['suit'] == 3:
					suits[2].append(3)
	for i in range(len(suits)):
		if len(suits[i]) >= 3:
			if 1 in suits[i] and 2 in suits[i] and 3 in suits[i]:
				return 5
	return 0


def doubleDragonPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	sort = []
	c = []
	d = []
	s = []
	suits = [[],[],[]]
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['number'] != tempTiles[i]['card2']['number']:
			if tempTiles[i]['card1'] == {'suit':4,'number':8} and tempTiles[i]['card2'] == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}:
				sort.append({'suit':tempTiles[i]['card2']['suit'],'number':(tempTiles[i]['card2']['number']-1)})
			elif tempTiles[i]['card1'] == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)} and tempTiles[i]['card2'] == {'suit':4,'number':8}:
				sort.append(tempTiles[i]['card1'])
			elif tempTiles[i]['card1']['number'] == (tempTiles[i]['card2']['number']-1):
				sort.append(tempTiles[i]['card1'])
	for i in range(len(sort)):
		if sort[i]['suit'] == 1:
			suits[0].append(sort[i]['number'])
		elif sort[i]['suit'] == 2:
			suits[1].append(sort[i]['number'])
		elif sort[i]['suit'] == 3:
			suits[2].append(sort[i]['number'])
	for i in range(len(suits)):
		if len(suits[i]) >= 2:
			sameSuitCounter = 0
			for j in range(len(suits[i])-1):
				if suits[i].count(suits[i][j]) >= 2:
					sameSuitCounter += 1
					if sameSuitCounter == 3:
						return 20
					# tempSuit = suits[i][:]
					# for x in range(2):
					# 	tempSuit.remove(suits[i][j])
					# print(tempSuit)
					# if tempSuit.count(tempSuit[j-1]) >= 2:
					# 	return 20
				if len(suits[0]) >= 2 and i != 0:
					if suits[0].count(suits[i][j]) >= 2:
						return 20
				if len(suits[1]) >= 2 and i != 1:
					if suits[1].count(suits[i][j]) >= 2:
						return 20
				if len(suits[2]) >= 2 and i != 2:
					if suits[2].count(suits[i][j]) >= 2:
						return 20
	return 0

def sameSuitPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	word = False
	tileSuit = 0
	tempTiles = tiles[:len(tiles)-1]
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['suit'] != tempTiles[i]['card2']['suit']:
			if tempTiles[i]['card1'] == {'suit':4,'number':8}:
				if WILDCARD['suit'] == 4:
					word = True
				elif tileSuit == 0:
					tileSuit = WILDCARD['suit']
				else:
					if tileSuit != WILDCARD['suit']:
						return 0
		else:
			if tileSuit == 0:
				tileSuit = tempTiles[i]['card1']['suit']
			elif tempTiles[i]['card1']['suit'] == 4:
				word = True
			else:
				if tileSuit != tempTiles[i]['card1']['suit']:
					return 0
	if tiles[len(tiles)-1]['eyes1']['suit'] == 4:
		if tiles[len(tiles)-1]['eyes1']['number'] == 8:
			if WILDCARD['suit'] != tileSuit and WILDCARD['suit'] != 4:
				return 0
			elif WILDCARD['suit'] == 4:
				word = True
		else:
			word = True
	elif tiles[len(tiles)-1]['eyes1']['suit'] != tileSuit:
		return 0
	if word:
		return 10
	return 40

def consecutivePoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	sort = []
	c = []
	d = []
	s = []
	suits = [[],[],[]]
	tempTiles = tiles[:len(tiles)-1]
	valid = False
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['number'] != tempTiles[i]['card2']['number']:
			if tempTiles[i]['card1'] == {'suit':4,'number':8} and tempTiles[i]['card2'] == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}:
				sort.append({'suit':tempTiles[i]['card2']['suit'],'number':(tempTiles[i]['card2']['number']-1)})
			elif tempTiles[i]['card1'] == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)} and tempTiles[i]['card2'] == {'suit':4,'number':8}:
				sort.append(tempTiles[i]['card1'])
			elif tempTiles[i]['card1']['number'] == (tempTiles[i]['card2']['number']-1):
				sort.append(tempTiles[i]['card1'])
	for i in range(len(sort)):
		if sort[i]['suit'] == 1:
			suits[0].append(sort[i]['number'])
		elif sort[i]['suit'] == 2:
			suits[1].append(sort[i]['number'])
		elif sort[i]['suit'] == 3:
			suits[2].append(sort[i]['number'])
	if len(suits[0]) == 0 or len(suits[1]) == 0 or len(suits[2]) == 0:
		return 0
	for i in range(len(suits[0])):
		if suits[0][i] in suits[1] and suits[0][i] in suits[2]:
			valid = True
			break
	if valid:
		return 5
	return 0

def consecutivePongHelper(suit):
	# print(len(suit), 'hihih')
	if len(suit) >= 3:
		# print(suit, 'hello')
		for i in range(len(suit)):
			if (int(suit[i])+1) in suit and (int(suit[i])+2) in suit:
				return True
	return False
def consecutivePongPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, INSIDE_WINDOW_COUNTER
	sort = []
	c = []
	d = []
	s = []
	suits = [[],[],[]]
	tempTiles = tiles[:len(tiles)-1]
	validWild = False
	points = []
	if WILDCARD['suit'] != 4:
		validWild = True
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['number'] == tempTiles[i]['card2']['number']:
			if tempTiles[i]['card1'] == {'suit':4,'number':8} or tempTiles[i]['card2'] == {'suit':4,'number':8}:
				if validWild:
					sort.append(WILDCARD)
			else:
				if tempTiles[i]['card1'] == WILDCARD and validWild:
					sort.append(WILDCARD)
				elif tempTiles[i]['card1'] != WILDCARD:
					sort.append(tempTiles[i]['card1'])
		else:
			if validWild:
				if tempTiles[i]['card1'] == {'suit':4,'number':8}:
					sort.append(WILDCARD)
				elif tempTiles[i]['card2'] == {'suit':4,'number':8}:
					sort.append(WILDCARD)
	for i in range(len(sort)):
		if sort[i]['suit'] == 1:
			suits[0].append(sort[i]['number'])
		elif sort[i]['suit'] == 2:
			suits[1].append(sort[i]['number'])
		elif sort[i]['suit'] == 3:
			suits[2].append(sort[i]['number'])
	for i in range(len(suits)):
		if tiles[len(tiles)-1]['eyes1']['suit'] == (i+1):
			if (tiles[len(tiles)-1]['eyes1']['number']-1) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']-2) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']-3) in suits[i]:
				points.append(20)
			if (tiles[len(tiles)-1]['eyes1']['number']+1) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']+2) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']+3) in suits[i]:
				points.append(20)
			if (tiles[len(tiles)-1]['eyes1']['number']-1) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']-2) in suits[i]:
				points.append(5)
				tempNums = suits[i][:]
				tempNums.remove(tiles[len(tiles)-1]['eyes1']['number']-1)
				tempNums.remove(tiles[len(tiles)-1]['eyes1']['number']-2)
				for j in range(len(suits)):
					if i == j:
						if consecutivePongHelper(tempNums):
							points.append(15)
					else:
						if consecutivePongHelper(suits[j]):
							points.append(15)
			if (tiles[len(tiles)-1]['eyes1']['number']+1) in suits[i] and (tiles[len(tiles)-1]['eyes1']['number']+2) in suits[i]:
				points.append(5)
				tempNums = suits[i][:]
				tempNums.remove(tiles[len(tiles)-1]['eyes1']['number']+1)
				tempNums.remove(tiles[len(tiles)-1]['eyes1']['number']+2)
				for j in range(len(suits)):
					if i == j:
						if consecutivePongHelper(tempNums):
							points.append(15)
					else:
						if consecutivePongHelper(suits[j]):
							points.append(15)
		if consecutivePongHelper(suits[i]):
			points.append(10)
	if 20 in points:
		return 20
	elif 15 in points:
		return 15
	elif 10 in points:
		return 10
	elif 5 in points:
		return 5
	return 0

def wordPongPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	tempTiles = tiles[:len(tiles)-1]
	windCounter = 0
	miscCounter = 0
	points = 0
	for i in range(len(OUTSIDE)):
		tempTiles.append(OUTSIDE[i])
	for i in range(len(tempTiles)):
		if tempTiles[i]['card1']['suit'] == 4:
			if tempTiles[i]['card1']['number'] == 8 and WILDCARD['suit'] == 4 and WILDCARD['number'] <= 4:
				windCounter += 1
			elif tempTiles[i]['card1']['number'] <= 4:
				windCounter += 1
			elif tempTiles[i]['card1']['number'] == 8 and WILDCARD['suit'] == 4 and WILDCARD['number'] >= 5:
				miscCounter += 1
			elif tempTiles[i]['card1']['number'] >= 5 and tempTiles[i]['card1']['number'] < 8:
				miscCounter += 1
	if windCounter == 2:
		if tiles[len(tiles)-1]['eyes1'] == {'suit':4,'number':8} and WILDCARD['suit'] == 4 and WILDCARD['number'] <= 4:
			points += 8
		elif tiles[len(tiles)-1]['eyes1']['suit'] == 4 and tiles[len(tiles)-1]['eyes1']['number'] <= 4:
			points += 8
	elif windCounter == 3:
		points += 20
	elif windCounter == 4:
		points += 40
	if miscCounter == 2:
		if tiles[len(tiles)-1]['eyes1'] == {'suit':4,'number':8} and WILDCARD['suit'] == 4 and WILDCARD['number'] >= 5:
			points += 15
		elif tiles[len(tiles)-1]['eyes1']['suit'] == 4 and tiles[len(tiles)-1]['eyes1']['number'] >= 5:
			points += 15
	elif miscCounter == 3:
		points += 30
	return points
	
# def runningWildPoints(tiles):
# 	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
# 	if tiles[len(tiles)-1]['eyes1'] == WILDCARD:
# 		return 4
# 	return 0

def scoreHand(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	

#functions that work:
	# print(allPongPoints(tiles))
	# print(flowersWordsPoints(tiles))
	# print(flowerPoints())
	# print(consecutivePongPoints(tiles))
	# print(wordPongPoints(tiles))
	# print(consecutivePoints(tiles))
	# print(sameSuitPoints(tiles))
	# print(doubleDragonPoints(tiles))
	# print(dragonPoints(tiles))
	# print(straightPoints(tiles))
	# print(wildcardPoints(tiles))
	# print(allPongPoints(tiles))
	# print(insidePongPoints(tiles))
	# print(eachSuitPoints(tiles))
	# print(sameNumberPoints(tiles))
	# print(selfPickPoints())
	# print(selfPickConcealedPoints())
	# print(kongPoints())
	# print('hi')

def callingEyesPoints(tiles):
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	if len(OUTSIDE) == 5:
		if LAST_PICKED == tiles[len(tiles)-1]['eyes1'] or LAST_PICKED == tiles[len(tiles)-1]['eyes2']:
			if SELF_PICK:
				return 5
			return 10
		elif LAST_PICKED == {'suit':4,'number':8}:
			if WILDCARD == tiles[len(tiles)-1]['eyes1'] or WILDCARD == tiles[len(tiles)-1]['eyes1']:
				if SELF_PICK:
					return 5
				return 10
	return 0
		# if LAST_PICKED == tiles[len(tiles)-1]['eyes1']:
		# elif LAST_PICKED == WILDCARD:
		# 	for i in range(len(tiles)):
		# 		try:
		# 			tempTiles.append(tiles[i]['card1'])
		# 			tempTiles.append(tiles[i]['card2'])
		# 			tempTiles.append(tiles[i]['card3'])
		# 		except:
		# 			tempTiles.append(tiles[i]['eyes1'])
		# 			tempTiles.append(tiles[i]['eyes1'])
		# 	tempTiles = tiles[:]
		# 	tempInside = INSIDE[:]
		# 	for i in range(len(tiles)):
		# 		if tiles[i]['card1'] in tempInside:
		# 			tempTiles.remove(tiles[i]['card1'])
		# 			tempInside.remove(tiles[i]['card1'])
		# 		if tiles[i]['card2'] in tempInside:
		# 			tempTiles.remove(tiles[i]['card2'])
		# 			tempInside.remove(tiles[i]['card2'])
		# 		if tiles[i]['card3'] in tempInside:
		# 			tempTiles.remove(tiles[i]['card3'])
		# 			tempInside.remove(tiles[i]['card3'])
		# 	if tiles[len(tiles)-1]['eyes1'] in tempTiles:

def printScoring(tiles):
	if runningWildPoints(tiles) == 4:
		print("running wildcard: 4 points")
	else:
		print("last card picked points: %d points" % (lastCardPoints(tiles)))
	if straightPoints(tiles) == 10:
		print("big straight points: 10 points")
	else:
		print("small straight points: %d points" % (straightPoints(tiles)))
		print("flowers & words points: %d points" % (flowersWordsPoints(tiles)))
	if callingEyesPoints(tiles) == 5:
		print("calling eyes points: %d points" % (callingEyesPoints(tiles)))
	elif callingEyesPoints(tiles) == 10:
		print("calling eyes points: %d points" % (callingEyesPoints(tiles)))
	if selfPickConcealedPoints() == 3:
		print("self pick & concealed points: %d points" % (selfPickConcealedPoints()))
	else:
		print("self pick points: %d points" % (selfPickPoints()))
		print("concealed points: %d points" % (concealedPoints()))
	print("eyes points: %d points" % (eyesPoints(tiles)))
	print("wildcard points: %d points" % (wildcardPoints(tiles)))
	print("wildcard pick points: %d points" % (wildcardPickPoints()))
	print("flower self-pick points: %d points" % (flowerPickPoints()))
	print("consecutive sequences in differnet suits points: %d points" % (consecutivePoints(tiles)))
	print("consecutive pong points: %d points" % (consecutivePongPoints(tiles)))
	print("same number pong points: %d points" % (sameNumberPoints(tiles)))
	print("each suit points: %d points" % (eachSuitPoints(tiles)))
	print("inside pong points: %d points" % (insidePongPoints(tiles)))
	print("word pong points: %d points" % (wordPongPoints(tiles)))
	print("dragon points: %d points" % (dragonPoints(tiles)))
	print("double dragon points: %d points" % (doubleDragonPoints(tiles)))
	print("all pong points: %d points" % (allPongPoints(tiles)))
	print("calling from start points: %d points" % (callingStartPoints()))
	print("dealer points: %d points" % (dealerPoints()))
	print("kong points: %d points" % (kongPoints()))
	print("same suit points: %d points" % (sameSuitPoints(tiles)))
	print("base three points: 3 points")

def independentScoring(tiles):
	points = 0
	if runningWildPoints(tiles) == 4:
		points += 4
	else:
		points += lastCardPoints(tiles)
		# print(lastCardPoints(tiles))
	if straightPoints(tiles) == 10:
		points += 10
	else:
		points += straightPoints(tiles)
		points += flowersWordsPoints(tiles)
		# print(straightPoints(tiles), flowersWordsPoints(tiles))
	if callingEyesPoints(tiles) == 5:
		points += 5
	elif callingEyesPoints(tiles) == 10:
		points += 10
	if selfPickConcealedPoints() == 3:
		# print(selfPickConcealedPoints())
		points += 3
	else:
		points += selfPickPoints()
		points += concealedPoints()
	points += eyesPoints(tiles) #eyes are 2, 5, or 8
	# print(eyesPoints(tiles))
	points += wildcardPoints(tiles) #no wildcard | wildcard as itself | all wildcards
	points += wildcardPickPoints() #self pick wildcard
	# print(wildcardPickPoints())
	points += flowerPickPoints() #self pick flower
	points += consecutivePoints(tiles) #three consecutives in three suits
	points += consecutivePongPoints(tiles) #two consecutive pongs and eyes | three consecutive pongs | both previous cases | three consecutive pongs and eyes
	points += sameNumberPoints(tiles) #two pongs of the same number and eyes | three pongs of the same number
	points += eachSuitPoints(tiles) #at least one card of each suit (chinese, circles, sticks, winds, dragons)
	points += insidePongPoints(tiles) #inside pongs (kongs count)
	points += wordPongPoints(tiles) #wind pongs and eyes | wind pongs | dragon pongs and eyes | dragon pongs
	points += dragonPoints(tiles) #1-9 sequence of a suit
	points += doubleDragonPoints(tiles) #two sets of a sequence and two sets of another or same sequence
	points += allPongPoints(tiles) #all sets are pongs
	points += callingStartPoints() #able to win from the starting hand given
	points += dealerPoints() #additional points due to either the winner or loser being the dealer
	# print(dealerPoints())
	points += kongPoints()
	points += sameSuitPoints(tiles)
	# print(wildcardPoints(tiles))
	# print(wildcardPickPoints())
	# print(flowerPickPoints())
	# print(consecutivePoints(tiles))
	# print(consecutivePongPoints(tiles))
	# print(sameNumberPoints(tiles))
	# print(eachSuitPoints(tiles))
	# print(insidePongPoints(tiles))
	# print(wordPongPoints(tiles))
	# print(dragonPoints(tiles))
	# print(doubleDragonPoints(tiles))
	# print(allPongPoints(tiles))
	# print(callingStartPoints())
	# print(dealerPoints())
	# print(sameSuitPoints(tiles))









	if points == 1:
		points == 5
	points += 3
	return points






def main():
	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, SELF_PICK, FLOWER_PICK, DEALER_COUNT, CALLING_FROM_START, NICKLE_HANDS
	# win = GraphWin('Mahjong', 1000, 500)
	# win.getMouse()
	testName = "testcase16.csv"
	data = readwriteCSV(testName, "r")
	stopProgram = readData(data)
	if not stopProgram:
		foo([])
		unique = []
		for i in range(len(ALLHANDS)):
			if ALLHANDS[i] not in unique:
				unique.append(ALLHANDS[i])
		ALLHANDS = unique[:]
		outsideTiles = []
		for i in range(len(OUTSIDE)):
			outsideTiles.append(OUTSIDE[i]['card1'])
			outsideTiles.append(OUTSIDE[i]['card2'])
			outsideTiles.append(OUTSIDE[i]['card3'])
			try:
				outsideTiles.append(OUTSIDE[i]['card4'])
			except:
				pass
		validHands = ALLHANDS[:]
		for i in range(len(ALLHANDS)):
			tempTiles = outsideTiles[:]
			for j in range(len(ALLHANDS[i])):
				try:
					tempTiles.append(ALLHANDS[i][j]['card1'])
					tempTiles.append(ALLHANDS[i][j]['card2'])
					tempTiles.append(ALLHANDS[i][j]['card3'])
				except:
					tempTiles.append(ALLHANDS[i][j]['eyes1'])
					tempTiles.append(ALLHANDS[i][j]['eyes2'])
			for tile in tempTiles:
				if tempTiles.count(tile) > 4:
					validHands.remove(ALLHANDS[i])
					break
				if tile == {'suit':4,'number':8} and (tempTiles.count(tile)+tempTiles.count(WILDCARD)) > 4:
					validHands.remove(ALLHANDS[i])
					break


		ALLHANDS = validHands[:]
		highestPoints = 0
		highestHand = []
		if len(ALLHANDS) != 0:
			for i in range(len(ALLHANDS)):
				readwriteCSV('hand_storage.csv','a',ALLHANDS[i])
				points = independentScoring(ALLHANDS[i])
				print(ALLHANDS[i])
				if points > highestPoints:
					highestPoints = independentScoring(ALLHANDS[i])
					highestHand = ALLHANDS[i]
			for i in range(len(NICKLE_HANDS)):
				if NICKLE_HANDS[i][1] > highestPoints:
					highestPoints = NICKLE_HANDS[i][1]
					highestHand = NICKLE_HANDS[i][0]
			for i in range(len(highestHand)):
				print(highestHand[i])
			printScoring(highestHand)
			print("total points: " + str(highestPoints))
		else:
			print("invalid hand")
main()	

