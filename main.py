import eel
from track_people import *  
from car_counter import*
from stats import *
from PIL import Image

@eel.expose
def call_analiz():
    man, woman, unique_people_count = analiz()
    stats_people(man, woman)
    
    
@eel.expose
def call_analiz_car(file):
    det_cars, det_trucks = analiz_car(file)
    stats_car(det_cars, det_trucks)


@eel.expose
def show_stats(image_path):
    im = Image.open(image_path)
    im.show()



eel.init('src')
eel.start("index.html", size=(1920, 1080), mode="chrome")