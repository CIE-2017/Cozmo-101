import cozmo, time, asyncio
from cozmo.util import degrees, Pose, distance_mm, speed_mmps
from PIL import Image

def cozmo_take_pic(robot: cozmo.robot.Robot) :  
    cozmo.camera.Camera.image_stream_enabled = True #set to true so that images can be received
    latest_image = robot.world.latest_image #get the latest image from Cozmo's camera
    img = latest_image.annotate_image() #resize it, this will return an image
    print (latest_image) #not necessary
    img.show() #show the image


cozmo.run_program(cozmo_take_pic,use_viewer=True)
