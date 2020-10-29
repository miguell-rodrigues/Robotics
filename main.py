try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

import time

from planning import *
from tools import *

print('Program started')
sim.simxFinish(-1)  # just in case, close all opened connections
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to CoppeliaSim

robot = "lumibot"

state = "stop"


def getSimulationTime():
    response, ints, floats, strings, buffers = sim.simxCallScriptFunction(
        clientID,
        'lumibot',
        sim.sim_scripttype_childscript,
        'simulationTime',
        [],  # ints
        [],  # floats
        [],  # strings
        bytearray(),  # buffer
        sim.simx_opmode_blocking
    )

    if response == sim.simx_return_ok:
        return floats[0]
    else:
        return 0


if clientID != -1:
    print('Connected to remote API server')

    sim.simxAddStatusbarMessage(clientID, "Ativo e operante", sim.simx_opmode_oneshot_wait)

    # Handle

    res, robotHandle = sim.simxGetObjectHandle(clientID, robot + "_body", sim.simx_opmode_oneshot_wait)

    res, leftMotor = sim.simxGetObjectHandle(clientID, robot + "_leftMotor", sim.simx_opmode_oneshot_wait)
    res, rightMotor = sim.simxGetObjectHandle(clientID, robot + "_rightMotor", sim.simx_opmode_oneshot_wait)

    # Streaming

    res, robotPosition = sim.simxGetObjectPosition(clientID, robotHandle, -1, sim.simx_opmode_streaming)
    res, robotOrientation = sim.simxGetObjectOrientation(clientID, robotHandle, -1, sim.simx_opmode_streaming)

    res, handles, intData, floatData, stringData = sim.simxGetObjectGroupData(clientID, sim.sim_appobj_object_type, 0,
                                                                              sim.simx_opmode_blocking)

    target_vectors = []
    targets = []

    trajectories = []

    sort = []

    for name in stringData:
        if name.startswith('target'):
            res, targetHandle = sim.simxGetObjectHandle(clientID, name, sim.simx_opmode_oneshot_wait)

            res, [targetX, targetY, targetZ] = sim.simxGetObjectPosition(clientID, targetHandle, -1,
                                                                         sim.simx_opmode_blocking)

            target_vectors.append(Vector(targetX, targetY, targetZ))

    res, [robotX, robotY, robotZ] = sim.simxGetObjectPosition(clientID, robotHandle, -1, sim.simx_opmode_buffer)

    for a in target_vectors:
        sort.append(a)

    robot = Vector(robotX, robotY, robotZ)

    sort.sort(key=lambda target: target.distance(robot), reverse=True)

    actual = sort[0]

    for a in sort:
        target_vectors.sort(key=lambda target: target.distance(Vector(robotX, robotY, robotZ)), reverse=False)

        actual = target_vectors.pop()

        targets.append(actual)

    for targetVector in targets:
        index = targets.index(targetVector)

        x, y = 0, 0

        if index == 0:
            x = robotX
            y = robotY
        else:
            x = targets[index - 1].x
            y = targets[index - 1].y

        restrictions_x = array(
            [
                x,
                0.5,
                0,
                targetVector.x,
                0,
                0
            ]
        )

        restrictions_y = array(
            [
                y,
                0.5,
                0,
                targetVector.y,
                0,
                0
            ]
        )

        trajectories.append(Trajectory(targetVector, restrictions_x, restrictions_y, 0.7))

    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)

    time.sleep(0.1)

    minimum_distance, maximum_distance = 0.03, 0.1

    running = True

    res, [robotAlpha, robotBeta, robotGamma] = sim.simxGetObjectOrientation(clientID, robotHandle, -1,
                                                                            sim.simx_opmode_buffer)

    last_time = 0

    actual_trajectory = trajectories.pop()

    while running:
        res, [robotX, robotY, robotZ] = sim.simxGetObjectPosition(clientID, robotHandle, -1, sim.simx_opmode_buffer)

        res, [robotAlpha, robotBeta, robotGamma] = sim.simxGetObjectOrientation(clientID, robotHandle, -1,
                                                                                sim.simx_opmode_buffer)
        robotVector = Vector(robotX, robotY, robotZ)

        if getSimulationTime() - last_time >= actual_trajectory.time:
            if len(trajectories) == 0:
                break

            last_time = getSimulationTime()

            actual_trajectory = trajectories.pop()

        rightVelocity, leftVelocity = actual_trajectory.calculateVelocities(robotVector, robotGamma,
                                                                            getSimulationTime() - last_time)

        # sim.simxPauseCommunication(clientID, True)
        # sim.simxSetJointTargetVelocity(clientID, rightMotor, rightVelocity, sim.simx_opmode_oneshot)
        # sim.simxSetJointTargetVelocity(clientID, leftMotor, leftVelocity, sim.simx_opmode_oneshot)
        # sim.simxPauseCommunication(clientID, False)

        sim.simxSetObjectPosition(clientID, robotHandle, -1, [actual_trajectory.x_t, actual_trajectory.y_t, robotZ], sim.simx_opmode_oneshot)

    sim.simxPauseSimulation(clientID, sim.simx_opmode_oneshot_wait)

    sim.simxFinish(clientID)
else:
    print('Failed connecting to remote API server')

print('Program ended')