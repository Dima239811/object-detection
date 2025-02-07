import matplotlib.pyplot as plt
import os

def stats_car(a, b):
    # Создаем папку "output", если она не существует
    output_dir = "results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    variable1 = a   
    variable2 = b  
    fig, ax = plt.subplots()
    ax.bar([variable1, variable2], [variable1,variable2])
    ax.set_xticks([variable1, variable2])
    ax.set_xticklabels(["cars", "trucks"])
    ax.set_ylabel('Values')
    ax.set_ylim(bottom=0)
    plt.title('Stats')
    plt.savefig(os.path.join(output_dir, "stats_car.png"))
    #plt.show()

def stats_people(a, b):
    output_dir = "results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    variable1 = a   
    variable2 = b   
    fig, ax = plt.subplots()
    ax.bar([variable1, variable2], [variable1,variable2])
    ax.set_xticks([variable1, variable2])
    ax.set_xticklabels(["male", "female"])
    ax.set_ylabel('Values')
    ax.set_ylim(bottom=0)
    plt.title('Stats')
    plt.savefig(os.path.join(output_dir, "stats_people.png"))
    #plt.show()

#stats_car(1, 4)
#stats_people(3, 6)



    
