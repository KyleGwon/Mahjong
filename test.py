hands = []
cards = [{'suit':1,'number':1},{'suit':1,'number':1},{'suit':1,'number':1},
		{'suit':1,'number':2},{'suit':1,'number':2},{'suit':1,'number':2},
		{'suit':1,'number':3},{'suit':1,'number':3},{'suit':1,'number':3},
		{'suit':1,'number':4},{'suit':1,'number':4},{'suit':1,'number':4},
		{'suit':1,'number':5},{'suit':1,'number':5},{'suit':1,'number':5},
		{'suit':1,'number':6},{'suit':1,'number':6}]
ALLHANDS = []
# def isPong(tiles, tile):
# 	if tiles.count({'suit':tile['suit'],'number':tile[number]}) == 3:
# 		return True
# 	return False
# def isSequence(tiles, tile):
# 	if tiles.count({'suit':tile['suit'],'number':tile[number]}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile[number]+1)}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile[number]+2)}) >= 1:
# 		return True
# 	return False
# def removePong(tiles, tile):
# 	tempTiles = list(tiles)
# 	try:
# 		for i in range(3):
# 			tempTiles.remove({'suit':tile['suit'],'number':tile['number']})
# 		return tempTiles
# 	except:
# 		return False
# def removeSequence(tiles, tile):
# 	tempTiles = list(tiles)
# 	try:
# 		for i in range(3):
# 			tempTiles.remove({'suit':tile['suit'],'number':(tile['number']+i)})
# 		# for i in range(2, -1, -1):
# 		# 	cards.remove({'suit':tile['suit'],'number':(tile['number']+i)})
# 		return tempTiles
# 	except:
# 		return False
# print(isPong(cards, {'suit':1,'number':1}))
# def makeHandHelper(tiles, remaining, eyes, index):
	# if not stopHand and len(remaining) == 0:

	# else:
	# 	if len(remaining) == 0:
	# 		tempHand.append(eyes) #global var tempHand
	# 		totalHands.append(tempHand) #global var totalHands
	# 		tempHand = []
	# 	remaining1 = list(remaining)
	# 	remaining2 = list(remaining)
	# 	if isKong
	# 	if isPong(tiles[index]):
# makeHandHelper()
#	{'hand'+str(handStoreIndex):{'set'+{'card1':}}}

# def recursive(accumHand, remaining, eyes):
# 	if len(remaining) == 0:
# 		accumHand.append({'eyes1':eyes,'eyes2':eyes})
# 		allHands.append(accumHand)
# 	else:
# 		if isPong(remaining, remaining[0]):
# 			accumHand.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
# 								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])},
# 								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])}})
# 			tempTiles = removePong(remaining, remaining[0])
# 			if tempTiles != False:
# 				recursive(accumHand, remaining, eyes)
# 			else:
# 				pass
# 		if isSequence(remaining, remaining[0]):
# 			accumHand.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
# 								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+1)},
# 								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+2)}})
# 			tempTiles = removeSequence(remaining, remaining[0])
# 			if tempTiles != False:
# 				recursive(accumHand, remaining, eyes)
# 			else:
# 				pass

# def makeHandHelper(remaining, eyes, currentHand):
# 	if len(remaining) == 0:
# 		hands.append(currentHand)
# 	elif isPong(remaining[0]):
# 		if isSequence(remaining[0]):
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
from time import sleep as wait
def helper(accumHand, remaining, eyes):
	newPongAccum = accumHand[:]
	newSeqAccum = accumHand[:]
	# newAccumHand = accumHand[:]
	# print(newAccumHand)
	if len(remaining) == 0:
		# print("nice")
		newPongAccum.append({'eyes1':eyes,'eyes2':eyes})
		ALLHANDS.append(newPongAccum)
		for i in range(len(newPongAccum)):
			print(newPongAccum[i])
		# print("\n")
		for i in range(len(newSeqAccum)):
			print(newSeqAccum[i])
		print("\n")
		pass
	else:
		if isPong(remaining, remaining[0]):
			newPongAccum.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])},
								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number'])}})
			tempTiles = removePong(remaining, remaining[0])
			# print(tempTiles)
			if tempTiles != False:
				helper(newPongAccum, tempTiles, eyes)
			else:
				pass
		if isSequence(remaining, remaining[0]):
			# if remaining[0]['number'] == 1:
				# print('heloooo')
			# print(isSequence(remaining, remaining[0]), remaining[0])
			newSeqAccum.append({	'card1':{'suit':remaining[0]['suit'],'number':remaining[0]['number']},
								'card2':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+1)},
								'card3':{'suit':remaining[0]['suit'],'number':(remaining[0]['number']+2)}})
			# print(newAccumHand)
			tempTiles = removeSequence(remaining, remaining[0])
			if tempTiles != False:
				helper(newSeqAccum, tempTiles, eyes)
			else:
				pass
helper([], cards, cards[-1])
print(ALLHANDS)
# print(removePong(cards, cards[0]))
# print(cards)
# print(removeSequence(cards, cards[0]))
# print(cards)
