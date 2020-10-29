from numpy import *

from tools import *

class Trajectory:
    def __init__(self, position, restrictions_x, restrictions_y, delta_time):
        self.time = delta_time

        self.planning_x = Planning(restrictions_x, delta_time)
        self.planning_y = Planning(restrictions_y, delta_time)

        self.vector = position

        self.x_t = 0
        self.v_x = 0
        self.a_x = 0

        self.y_t = 0
        self.v_y = 0
        self.a_y = 0

        self.gamma_error = 0
        self.old_gamma_error = 0

        self.k_x = .5
        self.k_y = .5
        self.k_gamma = 5

        self.r = 0.0247
        self.b = 0.0443

    def __calculateErrors__(self, robot_vector, robot_gamma, time):
        x_t, v_x, a_x = self.planning_x.calculatePolynomial(time)

        y_t, v_y, a_y = self.planning_y.calculatePolynomial(time)

        self.x_t = x_t
        self.v_x = v_x
        self.a_x = a_x

        self.y_t = y_t
        self.v_y = v_y
        self.a_y = a_y

        x_error = cos(robot_gamma) * (x_t - robot_vector.x) + sin(robot_gamma) * (y_t - robot_vector.y)
        y_error = -sin(robot_gamma) * (x_t - robot_vector.x) + cos(robot_gamma) * (y_t - robot_vector.y)

        gamma_error = normalizeRadian(atan2(v_y, v_x) - robot_gamma)

        self.old_gamma_error = self.gamma_error
        self.gamma_error = gamma_error

        return x_error, y_error, gamma_error

    def calculateVelocities(self, robot_vector, robot_gamma, time):
        x_error, y_error, gamma_error = self.__calculateErrors__(robot_vector, robot_gamma, time)

        v_s = sqrt(self.v_x ** 2 + self.v_y ** 2)
        w_s = (self.gamma_error - self.old_gamma_error) / time

        v_d = v_s * cos(gamma_error) + (self.k_x * x_error)
        w_d = w_s + v_s * ((self.k_y * y_error) + (self.k_gamma * sin(gamma_error)))

        theta_dd = (1 / self.r) * v_d + (self.b / self.r) * w_d

        theta_de = (1 / self.r) * v_d + (-self.b / self.r) * w_d

        return theta_dd, theta_de


class Planning:
    def __init__(self, restrictions, delta_time):
        self.restrictions = restrictions

        self.time = delta_time

        self.temporal = self.calculateTemporal()

        self.constants = self.calculateConstants()

    def calculateConstants(self):
        reverse = linalg.inv(self.temporal)

        constants = dot(reverse, self.restrictions)

        return constants

    def calculatePolynomial(self, time):
        x_t = self.constants[0] + self.constants[1] * time + self.constants[2] * pow(time, 2) + self.constants[3] * pow(
            time, 3) + self.constants[4] * pow(time, 4) + self.constants[5] * pow(time, 5)

        v_x = self.constants[1] + 2 * self.constants[2] * time + 3 * self.constants[3] * pow(time, 2) + 4 * \
              self.constants[4] * pow(time, 3) + 5 * self.constants[5] * pow(time, 4)

        a_x = 2 * self.constants[2] + 6 * self.constants[3] * time + 12 * self.constants[4] * pow(time, 2) + 20 * \
              self.constants[5] * pow(time, 3)

        return x_t, v_x, a_x

    def calculateTemporal(self):
        temporal = array(
            [
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 2, 0, 0, 0],
                [1, self.time, pow(self.time, 2), pow(self.time, 3), pow(self.time, 4), pow(self.time, 5)],
                [0, 1, (2 * self.time), 3 * pow(self.time, 2), 4 * pow(self.time, 3), 5 * pow(self.time, 4)],
                [0, 0, 2, 6 * self.time, 12 * pow(self.time, 2), 20 * pow(self.time, 3)]
            ]
        )

        return temporal