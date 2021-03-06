import cozmo, time, asyncio
from cozmo.util import degrees, Pose, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot) :
    robot.world.request_nav_memory_map(0.5)
    deg = 45
    while(True): #infinited loop starts here
        print("do the loop")
        try :
            event = robot.world.wait_for(cozmo.nav_memory_map.EvtNewNavMemoryMap, timeout=2)
            #print ("event = %s" % event)
            nav_map = event.nav_memory_map #use the nav_memory_map from the cozmo API you can check

            _posX = robot.pose.position.x #get cozmo's x cordinate
            _posY = robot.pose.position.y #get cozmo's y coordinate
            anglez = str(robot.pose.rotation.angle_z)
            atemp = anglez.split("(")
            atemp2 = atemp[1].split(" degree")
            _angle = float(atemp2[0])
            
            print("Robot info : x="+str(_posX)+" y="+str(_posY)+" angle="+str(_angle)) 
            state = scan_block(_posX, _posY, _angle, nav_map) .#to find the state cozmo is in using the coordinates and angle/ direction cozmo is facing
            #state = scan_block_test(-40.29963302612305, -199.53224182128906, -87.09, nav_map)
            if state[2] > 4: #check whether there is an obstacle in front of it or not
                robot.turn_in_place(degrees(45)).wait_for_completed() #turn if there is an obstacle
                print ("Turn") #printing turn so you know that cozmo is gonna turn
                
            else : #in this case, there is no obstacle near cozmo
                print ("Go") #prints go so that ya know it'g gonna start walking
                robot.drive_straight(distance_mm(100), speed_mmps(100)).wait_for_completed() #you know what this is
                
        except asyncio.TimeoutError : #for the timeout error 
            print("Time out waiting for map")
        time.sleep(0.2) #pause da program :D
        if deg == 45: 
            deg = 90
        else:
            deg = 45
        #robot.go_to_pose(Pose(100, 100, 0, angle_z=degrees(deg)), relative_to_robot=False).wait_for_completed()


def scan_block (posx, posy, angle, nav_map) : #ya so this is for scanning the block
    posx = int(posx) #x coordinate
    posy = int(posy) #y coordinate
    state = [0,0,0] #this is to get result of the the state cozmo is in
    sampling = 7 
    #the following lines are to check in which angle or direction to see if there is an obstacle in front of it
    if (angle >= 0 and angle <23) or (angle < 0 and angle > -23) :
        for i in range(posx, posx + 150, sampling) :
           for j in range(posy-25, posy+25, sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(convert_content(str(nav_map.get_content(i,j)))))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
                                  
               
    elif (angle >= 23 and angle <65) :
        for i in range(posx-10, posx + 120, sampling) :
           for j in range((posy-25)+(posx-i), (posy+25)+(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1

               
    elif (angle >= 65 and angle <115) :
        for i in range(posx-25, posx + 25, sampling) :
           for j in range((posy), (posy+150), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
               
    elif (angle >= 115 and angle <158) :
        for i in range(posx-120, posx + 10, sampling) :
           for j in range((posy-25), (posy+25), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    
    elif (angle >= 158 and angle <180) or (angle < -158 and angle > -180) :
        for i in range(posx - 150, posx + 0, sampling) :
           for j in range(posy-25, posy+25, sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
               
    elif (angle >= -158 and angle <-115) :
        for i in range(posx-120, posx+10, sampling ) :
           for j in range((posy-25)-(posx-i), (posy+25)-(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    
    elif (angle >= -115 and angle < -65) :
        for i in range(posx-25, posx + 25, sampling) :
            for j in range((posy-150), (posy), sampling) :
                #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
                content = str(nav_map.get_content(i,j))
                state[convert_content(content)] += 1
    
    elif (angle >= -65 and angle <-23) :
        for i in range(posx-10, posx + 120, sampling) :
           for j in range((posy-25)-(posx-i), (posy+25)-(posx-i), sampling) :
               #print ("scan "+str(i)+","+str(j)+" : "+str(nav_map.get_content(i,j)))
               content = str(nav_map.get_content(i,j))
               state[convert_content(content)] += 1
    print(state)
    return state #state is a list


    
def convert_content (content) : 
    if(content == "NodeContentTypes.ClearOfObstacle" or content == "NodeContentTypes.ClearOfCliff") :
        return 1 #if there is no obstacle or if there is no cliff, return 1 (color is green)
    elif(content == "NodeContentTypes.Unknown") :
        return 0 #for when you don't know the color of the grid (no color)
    else :
        return 2 #there is an obstacle (color is yellow/ orange)
    
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True) #lolol
