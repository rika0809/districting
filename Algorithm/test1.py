oldscore = 0
totalVariation = 450
totalCutEdge = 80

if totalVariation > 1000000:
    oldscore += (10 - int(totalVariation / 1000000))
if 100000 < totalVariation <= 1000000:
    oldscore += (10 - int(totalVariation / 100000))
    oldscore += 10
if 10000 < totalVariation <= 100000:
    oldscore += (10 - int(totalVariation / 10000))
    oldscore += 20
if 1000 < totalVariation <= 10000:
    oldscore += (10 - int(totalVariation / 1000))
    oldscore += 30
if 100 < totalVariation <= 1000:
    oldscore += (10 - int(totalVariation / 100))
    oldscore += 40
if 10 < totalVariation <= 100:
    oldscore += 50

if totalCutEdge > 100:
    oldscore += (10 - int(totalCutEdge / 100))
elif totalCutEdge >50:
    oldscore += 2 * (10 - int(totalCutEdge /10))
    oldscore += 10
else:
    oldscore += 20


print(oldscore)