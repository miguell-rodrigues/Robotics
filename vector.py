from math import *


class Vector:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.z)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

        return self

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

        return self

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y
        self.z *= vector.z

        return self

    def divide(self, vector):
        self.x /= vector.x
        self.y /= vector.y
        self.z /= vector.z

        return self

    def length(self):
        return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def lengthSquared(self):
        return (self.x ** 2) + (self.y ** 2) + (self.z ** 2)

    def distance(self, vector):
        return hypot(self.x - vector.x, self.y - vector.y)

    def distanceSquared(self, vector):
        return self.distance(vector) ** 2

    def angle(self, other):
        dot = self.dot(other) / (self.length() * other.length())
        return acos(dot)

    def differenceAngle(self, other):
        return atan2(other.y - self.y, other.x - self.x)

    def midPoint(self, other):
        self.x = (self.x + other.x) / 2.0
        self.y = (self.y + other.y) / 2.0
        self.z = (self.z + other.z) / 2.0

        return self

    def getMidPoint(self, other):
        x = (self.x + other.x) / 2.0
        y = (self.y + other.y) / 2.0
        z = (self.z + other.z) / 2.0

        return Vector(x, y, z)

    def multiply(self, number):
        self.x *= number
        self.y *= number
        self.z *= number

        return self

    def divide(self, number):
        self.x /= number
        self.y /= number
        self.z /= number

        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def crossProduct(self, other):
        newX = self.y * other.z - other.y * self.z
        newY = self.z * other.x - other.z * self.x
        newZ = self.x * other.y - other.x * self.y

        self.x = newX
        self.y = newY
        self.z = newZ

        return self

    def getCrossProduct(self, other):
        x = self.y * other.z - other.y * self.z
        y = self.z * other.x - other.z * self.x
        z = self.x * other.y - other.x * self.y

        return Vector(x, y, z)

    def normalize(self):
        length = self.length()

        self.x /= length
        self.y /= length
        self.z /= length

        return self

    def zero(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        return self

    def isInAABB(self, min, max):
        return self.x >= min.x & self.x <= max.x & self.y >= min.y & self.y <= max.y & self.z >= min.z & self.z <= max.z

    def isInSphere(self, origin, radius):
        return (origin.x - self.x) ** 2 + (origin.y - self.y) ** 2 + (origin.z - self.z) ** 2 <= radius ** 2

    def setX(self, x):
        self.x = x
        return self

    def setY(self, y):
        self.y = y
        return self

    def setZ(self, z):
        self.z = z
        return self

    def clone(self):
        return Vector(self.x, self.y, self.z)