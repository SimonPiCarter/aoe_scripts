"""Simple solve."""
from ortools.sat.python import cp_model
import csv

class Option:
	"""Une option d'horaire de match"""
	name = "un jour et une heure"
	index = 1

	def __init__(self, name, index):
		self.name = name
		self.index = index

class Player:
	"""un joueur avec son nom et ses options disponibles"""
	name = "nom_du_joueur"
	options = []

	def __init__(self, name, options):
		self.name = name
		self.options = options

class Match:
	"""Un match avec la liste des joueurs impliqués"""
	players = []
	option = None
	var = None

	def __init__(self, players):
		self.players = players


	def name(self):
		name = ""
		first = True
		for player in self.players:
			if not first:
				name = name + " vs "
			first = False
			name = name + player.name
		return name


def readPlayers(filename):
	line = -1
	options = []
	players = []
	with open(filename, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if line < 0:
				# read players info
				index = -1
				for col in row:
					if index >= 0:
						players.append(Player(col,[]))
					index = index + 1
			else:
				# read options info
				index = -1
				option = None
				for col in row:
					if index >= 0:
						if col != "":
							players[index].options.append(option)
					else:
						option = Option(col, line)
						options.append(option)
					index = index + 1
			line = line + 1
			print(', '.join(row))
	return options, players

def readMatches(filename, players):
	first = True
	playersMap = {}
	for player in players:
		playersMap[player.name] = player

	matches = []

	with open(filename, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			match_players = []
			if not first:
				# read match
				for col in row:
					match_players.append(playersMap[col])
				matches.append(Match(match_players))
			first = False
			print(', '.join(row))
	return matches

def allocateMatches(matches):
	# Creates the model.
	model = cp_model.CpModel()
	variables = []

	for match in matches:
		options = set()
		indexOptions = []
		first = True
		for player in match.players:
			if first:
				options = set(player.options)
			else:
				options = options.intersection(set(player.options))
			first = False
		for option in options:
			indexOptions.append(option.index)

		if len(indexOptions) == 0:
			print("Error match %s is ignored because no matching availability" % match.name())
		else:
			match.var = model.NewIntVarFromDomain(cp_model.Domain.FromValues(indexOptions), match.name())
			variables.append(match.var)

	model.AddAllDifferent(variables)

	# Creates a solver and solves the model.
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
		for match in matches:
			match.option = solver.Value(match.var)


options, players = readPlayers("data_player.csv")
matches = readMatches("data_match.csv", players)

for player in players:
	print("%s : " % player.name)
	for option in player.options:
		print("\t - %s %i" % (option.name, option.index))

allocateMatches(matches)

def matchKey(a):
	if a.option is not None:
		return a.option
	else:
		return 0

matches.sort(key=matchKey)

for match in matches:
	if match.option is not None:
		print("%s\t : %s" % (options[match.option].name, match.name()))
	else:
		print("%s : undefined" % match.name())
