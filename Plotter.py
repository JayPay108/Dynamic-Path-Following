from matplotlib import pyplot as plt
import math


inFileName = 'MovementTrajectoryData.txt' # Change to any file name, if left empty the user will be prompted for the file name upon execution

class Character:
    def __init__(self, steerType):
        self.rows = 0
        self.steerType = steerType
        self.posX = []
        self.posZ = []
        self.velX = []
        self.velZ = []
        self.linX = []
        self.linZ = []
        self.orientationX = []
        self.orientationZ = []

    def plotLocation(self):
        plt.plot(self.posX, self.posZ, color = 'red', linewidth = 2)

        startPos = (self.posX[0] , self.posZ[0])

        circle = plt.Circle(startPos, 2, color = 'red', fill = True) 
        plt.gcf().gca().add_artist(circle)

        steeringBehaviorCode = {1 : 'Stop', 2 : 'Reserved', 3 : 'Seek', 4 : 'Flee', 5 : 'Arrive', 8 : 'Follow Path'}
        plt.text(startPos[0] + 3, startPos[1] + 1, steeringBehaviorCode[self.steerType], fontsize = 10, color = 'red')

    def plotVelocity(self):
        for i in range(self.rows):
            x = [self.posX[i], self.posX[i] + self.velX[i] * 5] # Multiplying velocity times 5 because Petty's plot looks like this
            z = [self.posZ[i], self.posZ[i] + self.velZ[i] * 5]

            plt.plot(x, z, color = 'lime', linewidth = 1)

    def plotLinear(self):
        for i in range(self.rows):
            x = [self.posX[i], self.posX[i] + self.linX[i] * 4]
            z = [self.posZ[i], self.posZ[i] + self.linZ[i] * 4]

            plt.plot(x, z, color = 'blue', linewidth = 1)

    def plotOrientation(self):
        for i in range(self.rows):
            x = [self.posX[i], self.posX[i] + self.orientationX[i]]
            z = [self.posZ[i], self.posZ[i] + self.orientationZ[i]]

            plt.plot(x, z, color = 'blue', linewidth = 1)

# Setting up graph design
plt.figure(edgecolor = 'black', figsize = [10, 10])
plt.xlim([-100, 100])
plt.ylim([-100, 100])
plt.plot([-100, 100], [0, 0], color = 'lightgrey', linestyle = 'dashed', linewidth = 2)
plt.plot([0, 0], [-100, 100], color = 'lightgrey', linestyle = 'dashed', linewidth = 2)
plt.title('Movement Trajectory', fontsize = 20)
plt.xlabel('X', fontsize = 20)
plt.ylabel('Z', fontsize = 20)

# Graphing path
plt.plot([75, 45, 15, -15, -45, -75], [-20, 20, -40, 40, -60, 60], color = 'grey', linestyle = 'dashed', linewidth = 3) # This is hard coded because the path isnt stored in the trajectory file

# Setting up legend
plt.plot([0, 0], [0, 0], color = 'red', label = 'position')
plt.plot([0, 0], [0, 0], color = 'lime', label = 'velocity')
plt.plot([0, 0], [0, 0], color = 'blue', label = 'linear')
plt.plot([0, 0], [0, 0], color = 'yellow', label = 'orientation')
plt.legend(loc = 'lower right')

# Opening input file
if inFileName == '':
    inFileName = input('Enter the name of the input file: ')

inFile = open(inFileName, 'r')
lines = inFile.readlines()




characters = {} # Dictionary of all characters to be plotted

for line in lines: # Reading through input file line by line
    data = line.split(',') # Splitting line up into an array of values
    data = [float(i) for i in data] 

    ID = data[1]
    
    # If character is not already in dict, add it
    if ID not in characters:
        steerType = data[9]
        characters[ID] = Character(steerType)

    # Adding all line data to specified character
    characters[ID].rows += 1
    characters[ID].posX.append(data[2])
    characters[ID].posZ.append(data[3])
    characters[ID].velX.append(data[4])
    characters[ID].velZ.append(data[5])
    characters[ID].linX.append(data[6])
    characters[ID].linZ.append(data[7])
    characters[ID].orientationX.append(math.cos(data[8]) + data[2])
    characters[ID].orientationZ.append(math.sin(data[8]) + data[3])

# Looping through all characters and plotting their data
for ID in characters:
    character = characters[ID]

    character.plotVelocity()
    character.plotLinear()
    character.plotLocation()


plt.gca().invert_yaxis()
plt.savefig('MovementTrajectoryPlot.png')
print('Saved Movement Trajectory Plot as MovementTrajectoryPlot.png')
plt.close()
