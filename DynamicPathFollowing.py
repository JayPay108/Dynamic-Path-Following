import math

# Steer type const values
STOP = 1
RESERVED = 2
SEEK = 3
FLEE = 4
ARRIVE = 5
PURSUE = 6
WANDER = 7
FOLLOW_PATH = 8


# Simple vector class, this is missing alot of methods a normal vector
# object should have but it has what is needed for this assignment
class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y  # Z in this sense

    def normalize(self):    # Normalize to unit vector
        magnitude = self.length()
        self.x /= magnitude
        self.y /= magnitude

    def length(self):   # Returns the vector's magnitude
        return math.sqrt(math.pow(self[0], 2) + math.pow(self[1], 2))

    def dot(self, vector2): # Will preform dot product on a second vector
        return (self.x * vector2.x) + (self.y * vector2.y)

    # Operator overloading
    def __add__(self, vector2):
        return Vector(self[0] + vector2[0], self[1] + vector2[1])

    def __sub__(self, vector2):
        return Vector(self[0] - vector2[0], self[1] - vector2[1])

    def __mul__(self, scalar):
        return Vector(self[0] * scalar, self[1] * scalar)

    def __truediv__(self, scalar):
        return Vector(self[0] / scalar, self[1] / scalar)

    def __getitem__(self, key): # Bracket overloading
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        return None

# Path object to store path data and preform calculations
class Path:
    # Constructor takes the path ID, a list of all X coordinates, and a list of all Y coordinates as input
    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = x
        self.y = y

        self.segments = len(x) - 1  # Path segments will always be the amount of nodes - 1
        self.distance = [0] * (self.segments + 1)   # Initializing distance to be an array of 0s (with length equal to the amount of nodes)

        # Setting distance to be correct values
        for i in range(1, self.segments + 1):
            distanceFromLastNode = distanceBetweenPoints(Vector(x[i - 1], y[i - 1]), Vector(x[i], y[i]))
            # Total distance travelled at any node is the total distance travelled from the last node plus the distance from the last node
            self.distance[i] = self.distance[i - 1] + distanceFromLastNode

        # The entire distance for the path will always be equal to the stored total distance of the last node in the path
        entirePathDistance = self.distance[-1]

        self.param = [0] * (self.segments + 1) # Initializing param to be an array of 0s (with length equal to the amount of nodes)
        for i in range(1, self.segments + 1):
            # param will be equal to the current distance travelled at any given node divided by the entire path distance
            self.param[i] = self.distance[i] / entirePathDistance
        
    # Given a normalized path paramater, getPosition will return the position coordinates on the path for that parameter
    def getPosition(self, param):
        # Finding the last node travelled to get to the given paramater
        for i in range(self.segments + 1):
            if param > self.param[i]:
                pointIndex = i                
            else:
                break
        
        # Defining the last and next nodes for the given parameter
        lineStart = Vector(self.x[pointIndex], self.y[pointIndex])
        lineEnd = Vector(self.x[pointIndex + 1], self.y[pointIndex + 1])

        # Calulating the position of the parameter
        T = (param - self.param[pointIndex]) / (self.param[pointIndex + 1] - self.param[pointIndex])
        return (lineStart + ((lineEnd - lineStart) * T))

    # Given a position somewhere on the graph (on or off the path), getParam will return the normalized parameter value closest to the given position
    def getParam(self, position):
        closestDistance = float('inf')  # Initializing the closest distance to infinity so it will immediately get overwritten

        for i in range(self.segments):  # Looping through all segments on path
            # Two ending nodes to current segment
            lineStart = Vector(self.x[i], self.y[i])
            lineEnd = Vector(self.x[i + 1], self.y[i + 1])

            checkPoint = closestPointOnSegment(position, lineStart, lineEnd)    # Getting the closest point on the current segment to the given position
            checkDistance = distanceBetweenPoints(position, checkPoint) # Getting the distance between the calculated closest point and the position

            if checkDistance < closestDistance: # If the last distance calculated was less than the previously lowest distance, overwrite the closest position and distance
                closestPoint = checkPoint
                closestDistance = checkDistance
                closestSegment = i

        # Setting up node variables to preform calculations with
        lineStart = Vector(self.x[closestSegment], self.y[closestSegment])
        startParam = self.param[closestSegment]

        lineEnd = Vector(self.x[closestSegment + 1], self.y[closestSegment + 1])
        endParam = self.param[closestSegment + 1]

        # Calculating the normalized path parameter given the position
        T = (closestPoint - lineStart).length() / (lineEnd - lineStart).length()
        return (startParam + ((endParam - startParam) * T))

# Data class to store linear and angular acceleration
class Steering:
    def __init__(self, linear = Vector(0, 0), angular = 0):
        self.linear = linear
        self.angular = angular

# Character class to store each individual character's movements
class Character:
    def __init__(self, ID = 0, steer = STOP, position = Vector(0, 0), velocity = Vector(0, 0), linear = Vector(0, 0), orientation = 0, rotation = 0,
                angular = 0, maxSpeed = 0, maxAccleration = 0, target = 0, targetRadius = 4, slowRadius = 20,
                timeToTarget = 1, align = False, collideRadius = 0.5, avoidRadius = 2, offset = 0, path = 0):

        self.id = ID
        self.steer = steer
        self.position = position
        self.velocity = velocity
        self.linear = linear
        self.orientation = orientation
        self.rotation = rotation
        self.angular = angular
        self.maxSpeed = maxSpeed
        self.maxAcceleration = maxAccleration
        self.target = target
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget
        self.align = align
        self.collideRadius = collideRadius
        self.avoidRadius = avoidRadius
        self.offset = offset
        self.path = path

    # Turns all relevant character data to a string (comma seperated) for the output file
    def toString(self, time):
        data = [time, self.id, self.position[0], self.position[1], self.velocity[0], self.velocity[1], self.linear[0], self.linear[1], self.orientation, self.steer]
        data = [str(i) for i in data] # Turns all data values (required for trajectory file) of character into a list of strings
        return ','.join(data) + '\n'  # Returns all data values in the form of a comma seperated string


# Takes two position coordinates as input in the form of vectors
# Returns the total distance between the two coordinates
def distanceBetweenPoints(pos1, pos2):
    return math.sqrt(math.pow(pos2.x - pos1.x, 2) + math.pow(pos2.y - pos1.y, 2))

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns the distance from the point to the line
def distanceToLine(point, lineStart, lineEnd): 
    numerator = abs(((lineEnd.x - lineStart.x) * (lineStart.y - point.y)) - ((lineStart.x - point.x) * (lineEnd.y - lineStart.y)))
    denominator = math.sqrt(math.pow(lineEnd.x - lineStart.x, 2) + math.pow(lineEnd.y - lineStart.y))

    return numerator / denominator

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns coordinates to a position (in the form of a vector) on the line that is closest to the given point
def closestPointOnLine(point, lineStart, lineEnd):
    T = (point - lineStart).dot(lineEnd - lineStart) / (lineEnd - lineStart).dot(lineEnd - lineStart)

    return (lineStart + ((lineEnd - lineStart) * T))

# Takes 3 vectors as input. A point, and the two ends for a line (all in the form of vectors)
# Returns coordinates to a position (in the form of a vector) on the line segment (between the two ends) that is closest to the given point
def closestPointOnSegment(point, lineStart, lineEnd):
    T = (point - lineStart).dot(lineEnd - lineStart) / (lineEnd - lineStart).dot(lineEnd - lineStart)

    if T <= 0: 
        return lineStart
    elif T >= 1:
        return lineEnd
    else:
        return (lineStart + ((lineEnd - lineStart) * T))




# Follow path algorithm
def getSteeringFollowPath(character, path):
    currentParam = path.getParam(character.position) # Getting the closest path parameter to the character's current position

    targetParam = currentParam + character.offset   # Adding the character's offset to the closest parameter, this is what makes the character progress along the path
    
    # If the the target param is greater than 1, set it to 1 so the character does not pass the ending point
    if targetParam > 1:
        targetParam = 1

    targetPos = path.getPosition(targetParam) # Getting the location on the graph of the path parameter

    target = Character(position = targetPos)  # Loading dummmy character with the target's position to pass into Dynamic Seek algorithm

    return getSteeringSeek(character, target)   # Returning the value of the Dynamic Seek algorithm targeting the new position on the path


# Seek algorithm described in book
def getSteeringSeek(character, target):
    result = Steering()

    # Get the direction to the target
    result.linear = target.position - character.position

    # Give full acceleration along this direction
    result.linear.normalize()
    result.linear *= character.maxAcceleration

    result.angular = 0
    return result

# Dynamically update the character's values using the new steering calculated from steering algorithms
def dynamicUpdate(character, steering, timeStep, hsPhysics = True):
    # Updating the character's position and orientation
    if hsPhysics:
        sq = 0.5 * math.pow(timeStep, 2)
        character.position += (character.velocity * timeStep) + (steering.linear * sq)
        character.orientation += (character.rotation * timeStep) + (steering.angular * sq)
    else:
        character.position += (character.velocity * timeStep)
        character.orientation += (character.rotation * timeStep)

    # Updating character's velocity and rotation using the current acceleration
    character.velocity += (steering.linear * timeStep)
    character.rotation += (steering.angular * timeStep)
    
    # If character's velocity is greater than their max speed
    if character.velocity.length() > character.maxSpeed:
        character.velocity.normalize()
        character.velocity *= character.maxSpeed

    # If the character's velocity has slowed down past stop speed
    if character.velocity.length() < stopSpeed:
        character.velocity = Vector(0, 0)
    
    # If the character's rotation speed has slowed down past stop rotation speed
    if character.rotation < stopRotate:
        character.rotation = 0

    return character    
        

# Hard coded characters with attributes described in Programming Assignment 2 Requirements
character1 = Character(ID = 171, steer = FOLLOW_PATH,
                       position = Vector(70, -40), velocity = Vector(0, 0),
                       orientation = 0, maxSpeed = 4, maxAccleration = 2,
                       align = True, offset = 0.05, path = 0)

characters = [character1] # List of all the characters (only 1 for this assignment)


# Hard coded paths with points described in Programming Assignment 2 Requirements
path1 = Path(171, [75, 45, 15, -15, -45, -75], [-20, 20, -40, 40, -60, 60])

paths = [path1] # List of all the paths (only 1 for this assignment)




time = 0            # Starting time of simulation
timeStep = 0.5      # Difference in time between moments in the simulation
stopSpeed = 0.01    # Speed at which a character will stop if going under
stopRotate = 0.01   # Speed at which a character will stop rotating if going under
hsPhysics = False   # Will calculate character's position and orientation using HS physics if set to true
stopTime = 100       # Time at which simulation will stop

outFile = open('MovementTrajectoryData.txt', 'w')   # Opening output file

# Write initial positions and movement variables for all characters to trajectory file
for character in characters:
    outFile.write(character.toString(time))


while time < stopTime:
    time += timeStep

    # No collision checking for this assignment

    for character in characters:

        if character.steer == FOLLOW_PATH: # This is the only steering type the characters have for this assinment, this IF isnt really needed 
            steering = getSteeringFollowPath(character, paths[character.path])



        # Update the movement variables
        character.linear = steering.linear
        character.angular = steering.angular
        character = dynamicUpdate(character, steering, timeStep, hsPhysics)

        # Aligning character orientation with the movement direction
        if character.align:
            character.orientation = math.atan2(character.velocity.y, character.velocity.x)

        # Write updated position and movement variables for current character to trajectory file
        outFile.write(character.toString(time))

outFile.close()
print('Saved Movement Trajectory Data as MovementTrajectoryData.txt')
# End of program

        

