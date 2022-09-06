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
	first = True
	options = []
	players = []
	with open(filename, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if first:
				# read options
				index = -1
				for col in row:
					if index >= 0:
						options.append(Option(col, index))
					index = index + 1
			else:
				# read players info
				index = -1
				player_options = []
				name = ""
				for col in row:
					if index >= 0:
						if col != "":
							player_options.append(options[index])
					else:
						name = col
					index = index + 1
				players.append(Player(name, player_options))
			first = False
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
		options = []
		for player in match.players:
			for option in player.options:
				options.append(option.index)
		match.var = model.NewIntVarFromDomain(cp_model.Domain.FromValues(options), match.name())
		variables.append(match.var)

	model.AddAllDifferent(variables)

	# Creates a solver and solves the model.
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	for match in matches:
		match.option = solver.Value(match.var)

options, players = readPlayers("data_player.csv")
matches = readMatches("data_match.csv", players)

allocateMatches(matches)

for match in matches:
		print("%s : %s" % (match.name() , options[match.option].name))


