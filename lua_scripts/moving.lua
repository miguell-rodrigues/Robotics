radius = 0.3
wise = 1

discs = {}

function sysCall_threadmain()
    simRemoteApi.start(19999)
    
    sim.setUserParameter(sim.handle_self, '@enable', '')
 
    difficulty = sim.getUserParameter(sim.handle_self, 'difficulty', false)
    difficultyFactor = sim.getUserParameter(sim.handle_self, 'difficultyFactor', false)
 
    for i = 1, 16, 1 do
        disc = movingDisc(sim.getObjectHandle('target' .. i), difficulty * difficultyFactor)
       
        discs[i] = disc
    end
   
    for i = 1, #discs, 1 do
        sim.setShapeColor(discs[i].handle, '', sim.colorcomponent_ambient_diffuse, {0,0,0})
    end
   
    os.execute("sleep 1")
 
    robotHandle = sim.getObjectHandle('lumibot')
 
    position = 1
    actual = discs[position]
    
    sim.setShapeColor(actual.handle, '', sim.colorcomponent_ambient_diffuse, {1,0,0})
 
    while true do    
        robotPosition = sim.getObjectPosition(robotHandle, -1)
 
        robotVector = Vector(robotPosition[1], robotPosition[2], robotPosition[3])
        
        for i = 1, #discs do
            disc = discs[i]
           
            distance = robotVector.distance(robotVector, disc.vector)
           
            disc.updatePosition()
           
            if disc == actual then
                if distance <= 0.03 then
                    position = position + 1
                    
                    if position <= 16 then
                        actual = discs[position]
                    
                        sim.setShapeColor(actual.handle, '', sim.colorcomponent_ambient_diffuse, {1,0,0})
                    end
                
                    disc.canMove = false
                
                    radius = radius + 0.01
                
                    wise = -wise
                
                    disc.wise = wise
                end
            end
        end
    end
end

function sysCall_cleanup()
    for i = 1, #discs, 1 do
        sim.setShapeColor(discs[i].handle, '', sim.colorcomponent_ambient_diffuse, {0,0,0})
    end
end

function Vector(x, y, z)
    local vector = {}
 
    vector.x = x
    vector.y = y
    vector.z = z
 
    function vector:distance(other)
        return math.sqrt( math.pow(vector.x - other.x, 2) + math.pow(vector.y - other.y, 2) )
    end
 
    function vector:length()
        return math.sqrt( (math.pow(vector.x, 2)) + (math.pow(vector.y, 2)) + (math.pow(vector.z, 2)) )
    end
 
    function vector:normalize()
        local length = vector.length(vector)
 
        vector.x = vector.x / length
        vector.y = vector.y / length
        vector.z = vector.z / length
 
        return vector
    end
 
    function vector:multiply(value)
        vector.x = vector.x * value
        vector.y = vector.y * value
        vector.z = vector.z * value
 
        return vector
    end
   
    function vector:add(other)
        vector.x = vector.x + other.x
        vector.y = vector.y + other.y
        vector.z = vector.z + other.z
 
        return vector
    end
   
    function vector:subtract(other)
        vector.x = vector.x - other.x
        vector.y = vector.y - other.y
        vector.z = vector.z - other.z
 
        return vector
    end
   
    return vector
end

toMove = Vector(0, 0, 0.02)

function movingDisc(handle, difficulty)

    local movingDisc = {}
   
    movingDisc.handle = handle
    movingDisc.difficulty = difficulty
 
    movingDisc.position = {}
    movingDisc.vector = Vector(0, 0, 0)
    movingDisc.target = Vector(math.random(-2.0, 2.0), math.random(-2.0, 2.0), 0.02).normalize(movingDisc.target).multiply(movingDisc.target, difficulty)
 
    movingDisc.canMove = true
    movingDisc.angle = math.rad(math.random(0, 360))
    movingDisc.wise = 1
 
    function movingDisc:updateTarget()
        movingDisc.target = Vector(math.random(-2.0, 2.0), math.random(-2.0, 2.0), 0.02).subtract(movingDisc.target, movingDisc.vector).normalize(movingDisc.target).multiply(movingDisc.target,  movingDisc.difficulty)
    end
   
    function movingDisc:updatePosition()
        movingDisc.position = sim.getObjectPosition(movingDisc.handle, -1)
       
        if movingDisc.canMove == true then
            movingDisc.vector = Vector(movingDisc.position[1], movingDisc.position[2], movingDisc.position[3])
       
            posX = movingDisc.position[1]
            posY = movingDisc.position[2]
 
            target = movingDisc.target
           
            posX = posX + (target.x / 85.0)
            posY = posY + (target.y / 85.0)
           
            if (posX >= 2.0 or posX <= -2.0) or (posY >= 2.0 or posY <= -2.0) then
                movingDisc.updateTarget(movingDisc)  
            end
           
            movingDisc.position[1] = posX
            movingDisc.position[2] = posY
           
            sim.setObjectPosition(movingDisc.handle, -1, movingDisc.position)
        else
            sim.setShapeColor(movingDisc.handle, '', sim.colorcomponent_ambient_diffuse, {math.random(), math.random(), math.random()})
        
            x = radius * math.cos(movingDisc.angle)
            y = radius * math.sin(movingDisc.angle)
       
            toMove.add(toMove, Vector(x, y, 0))
           
            movingDisc.position[1] = x
            movingDisc.position[2] = y
           
            sim.setObjectPosition(movingDisc.handle, -1, movingDisc.position)
       
            toMove.subtract(toMove, Vector(x, y, 0))
       
            movingDisc.angle = movingDisc.angle + (math.rad(1) * movingDisc.wise)
        end
    end
   
    return movingDisc
 
end
