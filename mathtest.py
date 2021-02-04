import math

for x in range(-1,2):
    for y in range(-1,2):
        rad = (math.atan2(x,y)) 
        if rad < 0:
            rad += (2*math.pi)
        angle = rad/math.pi*180
        print('x: {0}, y: {1}: {2}'.format(x,y,angle))