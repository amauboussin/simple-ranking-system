#Simple Ranking System ranking generator by Andrew Mauboussin
#
#Depends on Numpy (http://www.numpy.org)
#
#Input: a csv file containing all of the games to be analysed. 
#	Column1 - Team/Player 1, Column2 - Team/Player 2, 
#	Column 3 - Team 1's points, Column 4 = Team 2's points
#
#Output: Prints ranked teams/players and the score each one received under the simple ranking 
#	system in tab-delimited text (can be pasted into excel). 
#
#	Each teams' score is determined by the following equation:
#	score = average point differential + average score of opponents (strength of schedule)
#	since each team's score depends on other teams' score these equations need to be solved simultaneously
#	a more detailed description of the methodology is available at http://www.pro-football-reference.com/blog/?p=37
#
#
# Settings
filepath = 'nfl05.csv' #filepath of the csv file to be inputted
headers = False #ignore the first row of the csv file?



import csv
import numpy as np

def mean(list):
	return (float(sum(list))/len(list))

class Team(object):
	def __init__(self, name, spreads, opponents):
		self.name = name
		self.spreads = spreads
		self.opponents = opponents
		
	def set_average_spread(self):
		self.spread = mean(self.spreads)

def main():
	
	#read csv file
	csvfile = open(filepath, 'rU')
	gamereader = csv.reader(csvfile, dialect = 'excel')
	if headers:
		gamereader.next()
	
	#store all teams in a dict as "team name": team object
	teams = {}
	
	#loop through games and construct team objects
	for game in gamereader:
		t1 = game[0]
		t2 = game[1]
		t1spread = int(game[2]) - int(game[3])
		t2spread = -t1spread
		
		if t1 in teams:
			teams[t1].spreads.append(t1spread)
			teams[t1].opponents.append(t2)
		else:
			teams[t1] = Team(t1, [t1spread], [t2])
		
		if t2 in teams:
			teams[t2].spreads.append(t2spread)
			teams[t2].opponents.append(t1)
		else:
			teams[t2] = Team(t2, [t2spread], [t1])
			
	csvfile.close()

	#calculate the means
	for team in teams.keys():
		teams[team].set_average_spread()


	#first matrix with the coefficients of each of the variables
	terms = []
	#seccond matrix with the constant term (-average spread)
	solutions = []
	
	
	for team in teams.keys():
		#add in a row for each team
		row = []
		
		
		#rating = average spread + average opponent rating
		#-> -average spread = -rating + average opponent rating
		#-> -average spread = -rating + 
		#(number of opponents/1) * (opponent 1 rating+opponent 2 rating...)
		#each row of the matrix describes right side equation
		for opp in teams.keys():
			if opp == teams[team].name:
				row.append(-1)
			elif opp in teams[team].opponents:
				row.append(1.0/len(teams[team].opponents))
			else:
				row.append(0)
		terms.append(row)
		
		#each row of this matrix describes the left side of the above equation
		solutions.append(-teams[team].spread )
	
	#solve the simultaneous equations using numpy
	array1 = np.array(terms)
	array2 = np.array(solutions)
	solutions  = np.linalg.solve(array1, array2)

	#print output
	print "Rank\tTeam\tScore"
	rankings = zip( [teams[team].name for team in teams.keys()], [ solution for solution in solutions] )
	for rank, pair in zip(range(1,len(rankings)+1), sorted(rankings, reverse = True, key = lambda x: x[1])):
		print '%s\t%s\t%.2f' % (rank,pair[0],pair[1])

if __name__=="__main__":
	main()
	
	
