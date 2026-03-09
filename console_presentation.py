# 3/10/26 project tutorial:
# Getting started with Python in QGIS
# OR: noodling your way into QGIS automation
# Why? We don't actually have to open QGIS to do the trash join, which is pretty cool!
# But you need a little foundation to get there.

# Goals:
# 1. learn how to navigate the console
# 2. learn how to explore the active layer and change the layer name
# 3. learn how to copy a processing command from the toolbox and run it in the console

# 0: start by loading mappler trash pins as a point vector layer, so we have something
# to work with, as well as any second layer (parcels, baselayer, etc).
# click the blue/yellow Python icon on the toolbar to open the console

# Part 1. Exploring the console
# Read the output and follow its advice by inputing '?' and hitting enter
?

_cookbook

# REPL: Read, Evaluate, Print, Loop
1+1

# Errors: get used to it!
1+

# obligatory hello world
print("hello, world!")

# Part 2: exploring objects and getting help
# Mission 1: find out what the active layer is
# How do we do that again? enter '?' for a hint
?

# solution:
iface.activeLayer()

# click on a different layer and rerun the command
iface.activeLayer()
# select the points layer again

# store a reference to the layer in a variable, so no matter what's selected
# in the interface, we can reference the points layer
points_layer = iface.activeLayer()

# Mission 2: change the name of your layer using the console
# First, we need to find out more about our layer and what it can do
# Let's run through a few ways to do this, and learn about dir, pprint, and help
# Right click: context help OR
_pyqgis(points_layer)
# Hmmm... not really seeing anything about updating the name. We can obviously do a web
# search to learn more, but I find myself reaching for the following tools often!
# Start by exploring the points_layer object. dir() lets you see all of the attributes
dir(points_layer)
# uggh. Hard to read. Clean it up with Pretty-print!
# Import pprint from the Python Standard Library
from pprint import pprint

# use the help() function to understand how to use pprint
help(pprint)

# use pprint to format our output
pprint(dir(points_layer))

# setName looks promising! Let's see what that does
help(points_layer.setName)

# use it!
points_layer.setName("Trash pins")
# Take a look at the layer panel!

# Part 3. Coding processing commands
# Say we want to run our trash join without having to configure the join
# parameters each time. QGIS offers an easy way to copy commands.
# Mission 3: run a trash join through the console
#   1. Start by setting up a trash join. Go all the way through configuring the join
#       as we always do, but don't hit run.
#   2. In the lower left hand corner of the processing box,
#   3. Select "Advanced" > Copy as Python Command

#   4. Create a new file (click the plus/New Editor button above) and paste your command in there.
#   5. Run by clicking the green play/run button above.

# Food for thought:
#   What else do you need to know how to do to script the rest of the trash join in QGIS?
#   What about running the join without opening QGIS at all?
