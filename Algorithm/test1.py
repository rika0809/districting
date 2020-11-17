score = 0
variation = 80000
totalCutEdge = 90

if variation > 1000000:
    score += 2 * (10 - int(variation / 1000000))
if 100000 < variation <= 1000000:
    score += 2 * (10 - int(variation / 100000))
    score += 20
if 10000 < variation <= 100000:
    score += 2 * (10 - int(variation / 10000))
    score += 40
if variation <= 10000:
    score += 50

if totalCutEdge > 100:
    score += (10 - int(totalCutEdge / 100))
elif totalCutEdge >50:
    score += 2 * (10 - int(totalCutEdge /10))
    score += 10
else:
    score += 20


print(score)