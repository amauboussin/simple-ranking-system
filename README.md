simple-ranking-system
=====================


Simple Ranking System ranking generator by Andrew Mauboussin

Depends on Numpy (http://www.numpy.org)

Input: 
  A csv file containing all of the games to be analyzed with the following as the first four columns: 
  Team/Player 1, Team/Player 2, Team 1's points, Team 2's points

Output: 
  Prints ranked teams/players and the score each one received under the simple ranking 
  system in tab-delimited text (can be pasted into excel). 

  Each teams' score is determined by the following equation:
  score = average point differential + average score of opponents (strength of schedule)
  since each team's score depends on other teams' score these equations need to be solved simultaneously
  a more detailed description of the methodology is available at http://www.pro-football-reference.com/blog/?p=37

Usage: 

  Create csv file with the format specified by "Input".
  
  Change the settings by altering the variables in the beggining of the .py file. 
  
  Run the .py file

Settings (change by altering variables in the beggining of the .py file):

filepath = '/Users/Andrew/Desktop/mycsv.csv' # filepath of the csv file to be inputted

headers = False # if true ignore the first row of the csv 
