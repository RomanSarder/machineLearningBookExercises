from math import sqrt

#returns similarity estimations based on distance
def sim_distance(prefs,person1,person2):
 si={}
 #get items list that are voted by both
 for item in prefs[person1]:
  if item in prefs[person2]:
   si[item]=1
 #if no mutual mark return zero
 if len(si)==0: return 0
 #calculate difference between marks then pow it
 sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                    for item in prefs[person1] if item in prefs[person2]])

 #return reversed value
 return 1/(1+sum_of_squares)

# returns pierson correlation coefficient between p1 and p2
def sim_pearson(prefs,p1,p2):
 # get items list that are voted by both
 si={}
 for item in prefs[p1]:
    if item in prefs[p2]: si[item]=1
    # find elements number
 n = len(si)
 # if no mutual mark return zero
 if n == 0: return 0
 # preferences sum calculation
 sum1 = sum([prefs[p1][it] for it in si])
 sum2 = sum([prefs[p2][it] for it in si])
 # pow sum
 sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
 sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
 # multiplication sum
 pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
 # calculate pierson coefficient
 num = pSum - (sum1 * sum2 / n)
 den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
 if den == 0: return 0

 r = num / den
 return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
 scores=[(similarity(prefs, person, other), other)
 for other in prefs if other!=person]
 # Sort list desc
 scores.sort()
 scores.reverse()
 return scores[0:n]

# Get recommendations for current person using
# marks given by other users
def getRecommendations(prefs,person,similarity=sim_pearson):
 totals={}
 simSums={}
 for other in prefs:
 # dont compare me with myself
  if other==person: continue
  sim=similarity(prefs,person,other)
 # ignore null and zero marks
  if sim<=0: continue
  for item in prefs[other]:
   #mark only movies i havent seen
   if item not in prefs[person] or prefs[person][item]==0:
    #similarity coefficient * mark
    totals.setdefault(item,0)
    totals[item]+=prefs[other][item]*sim
    # similarity coefficient sum
    simSums.setdefault(item,0)
    simSums[item]+=sim
 # create normalized list
 rankings=[(total/simSums[item],item) for item,total in totals.items()]
 # return sorted list
 rankings.sort()
 rankings.reverse()
 return rankings

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree': 1.0,'Superman Returns': 4.0}}