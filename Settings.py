import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')



class Settings:
	screen_size = (600, 600)

	safe_borders_width = 200 #width of space, on which balls cannot appear at start
	max_speed =15 #max speed IN ONE DIRECTION
	min_start_speed = 3 #min starting speed IN ONE DIRECTION
	max_start_speed = 7 #max starting speed IN ONE DIRECTION
	racket_distance = 20 #distance from border to racket
	max_racket_speed = 2*max_speed
	racket_accel = 4
	racket_brake = 2*racket_accel
	racket_friction = 0.6 #used during collision with balls
	sounds = True
	helpLines = True
	show_fps = True
