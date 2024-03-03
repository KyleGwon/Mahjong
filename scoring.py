# # from mahjong import *
# def isMiddle(tiles, tile):
# 	for i in range(len(tiles)):
# 		if tile == tiles[i]['card2'] and isSequence(tiles, tile):
# 			return True
# 	return False

# def isSpecialMiddle(tiles, tile):
# 	for i in range(len(tiles)):
# 		try:
# 			if tile == tiles[i]['card2'] and specialSequence(tiles, tile):
# 				return True
# 		except:
# 			pass
# 	return False

# def isPong(tiles, tile):
# 	if tiles.count({'suit':tile['suit'],'number':tile['number']}) == 3:
# 		return True
# 	return False

# def isSequence(tiles, tile):
# 	if tiles.count({'suit':tile['suit'],'number':tile['number']}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+1)}) >= 1 and tiles.count({'suit':tile['suit'],'number':(tile['number']+2)}) >= 1:
# 		if tile['suit'] != 4:
# 			return True
# 	return False

# def specialSequence(tiles, tile, returnPlacement=False, remove=False):
# 	global INSIDE, FLOWERS, OUTSIDE, ALLHANDS, WILDCARD, WILDCARD_COUNT, LAST_PICKED, LAST_INSIDE, INSIDE_WINDOW_COUNTER
# 	if tiles.count({'suit':4,'number':8}) >= 1:
# 		if tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-2)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)}) >= 1:
# 			placement = "card1"
# 			if remove:
# 				tempTiles = tiles[:]
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-2)})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)})
# 				tempTiles.remove({'suit':4,'number':8})
# 		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1:
# 			placement = "card2"
# 			if remove:
# 				tempTiles = tiles[:]
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']-1)})
# 				tempTiles.remove({'suit':4,'number':8})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
# 		elif tile == {'suit':4,'number':8} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1 and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)}) >= 1:
# 			placement =  "card3"
# 			if remove:
# 				tempTiles = tiles[:]
# 				tempTiles.remove({'suit':4,'number':8})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
# 		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)}) >= 1:
# 			placement =  "card4"
# 			if remove:
# 				tempTiles = tiles[:]
# 				# print(tempTiles)
# 				tempTiles.remove({'suit':4,'number':8})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
# 		elif tile == {'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)} and tiles.count({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)}) >= 1:
# 			placement =  "card5"
# 			if remove:
# 				tempTiles = tiles[:]
# 				tempTiles.remove({'suit':4,'number':8})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+1)})
# 				tempTiles.remove({'suit':WILDCARD['suit'],'number':(WILDCARD['number']+2)})
# 		else:
# 			# print(tile)
# 			return False
# 		# if tiles.count({'suit':WILDCARD['suit'],'number':WILDCARD['number']+1}) >= 1 and tiles.count({'suit':WILDCARD['suit'],'number':WILDCARD['number']+2}) >= 1:
# 		# 		print('placement')
# 		if remove:
# 			if returnPlacement:
# 				return placement, tempTiles
# 			elif not returnPlacement:
# 				return tempTiles
# 		if not returnPlacement:
# 			return True
# 		return placement
# 	# if tiles[len(tiles)-1] == {'suit':4,'number':8}:
# 	# 	print(tiles[len(tiles)-1])
# 	return False

# def removePong(tiles, tile):
# 	# if tile['number'] == 3:
# 	# 	print(tiles)
# 	tempTiles = tiles[:]
# 	try:
# 		for i in range(3):
# 			tempTiles.remove({'suit':tile['suit'],'number':tile['number']})
# 			# print(tempTiles, "\t\t\t", tile)
# 		return tempTiles
# 	except:
# 		return False

# def removeSequence(tiles, tile):
# 	tempTiles = tiles[:]
# 	try:
# 		for i in range(3):
# 			tempTiles.remove({'suit':tile['suit'],'number':(tile['number']+i)})
# 		return tempTiles
# 	except:
# 		return False
# def flowerPoints(flowers):
# 	return flowers
# def wordPoints(tiles):
# 	wordCounter = 0
# 	wordSeen = []
# 	for i in range(len(tiles)):
# 		try:
# 			if tiles[i]['card1']['suit'] == 4 and tiles[i]['card1']['number'] != 8:
# 				if tiles[i]['card1'] not in wordSeen:
# 					wordSeen.append(tiles[i]['card1'])
# 					wordCounter += 1
# 		except:
# 			if tiles[i]['eyes1']['suit'] == 4 and tiles[i]['eyes1']['number'] != 8:
# 				if tiles[i]['card1'] not in wordSeen:
# 					wordSeen.append(tiles[i]['card1'])
# 					wordCounter += 1
# 	return wordCounter
# def flowersWordsPoints(tiles, flowers):
# 	if flowerPoints(flowers) == 0 and wordPoints(tiles) == 0:
# 		return 3
# 	pointSum = flowerPoints(flowers) + wordPoints(tiles)
# 	return pointSum
# def lastCardPoints(tiles, lastPicked):
# 	pointCounter = 0
# 	print(lastPicked, 'hihihihihi')
# 	for i in range(len(tiles)):
# 		for j in range(len(tiles[i])):
# 			if isSequence(tiles, {'suit':lastPicked['suit'],'number':(lastPicked['number']-1)}) :
# 				pointCounter = 2
# 				break
# 			elif isSpecialMiddle(tiles, lastPicked):
# 				pointCounter = 2
# 				break
# 			elif isPong(tiles, lastPicked):
# 				pointCounter = 1
# 	return pointCounter