import sys
import json
import random

'''
    This file selects a random theme from the available ones and
    sets it to be the current theme. This does not take into account
    a theme vote.
'''

name = sys.argv[1]

# Load the themes.
themes = json.loads(open(sys.path[0] + '/../json/themes.json').read())

# Select a random theme. If the random theme is 'None', continue
# selecting a random theme until it isn't.
if name in list(themes.keys()):
	theme = name
else:
	print("Not a theme, please try another.")

# Save the randomly selected theme as the current theme.
with open(sys.path[0] + "/current.txt", "w") as currentfile:
    currentfile.write(theme)
