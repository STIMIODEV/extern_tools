#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from threading import Thread
import sys
import getopt
from enum import IntEnum
import argparse

parseOpt = argparse.ArgumentParser(description="Acceleromer analysis tool")

parseOpt.add_argument("-input",      metavar="nom du fichier d'entree", default="data.txt", help="fichier d'entree")

args=parseOpt.parse_args()

X_LENGTH = 1000
Y_MIN = -150
Y_MAX = 150

var_i = 0
time_data = []
x_data = []
y_data = []
z_data = []
threshold_values=[-96,-80,-64,-48,48,64,80,96]

x=0
y=0
z=0
threshold = 64

fig = plt.figure(1)


def init_display(x_length):
    global x_graph, y_graph, z_graph, threshold
    global x_axe, y_axe, z_axe
    global X_LENGTH

    X_LENGTH = x_length

    x_axe = fig.add_subplot(3, 1, 1)
    plt.ylabel('x acceleration')
    plt.axhline(y=threshold, linestyle='--', color='y')
    plt.axhline(y=-threshold, linestyle='--', color='y')
    plt.axhline(y=48, linestyle='-.', color='c')
    plt.axhline(y=-48, linestyle='-.', color='c')
    x_axe.set_xlim(0, X_LENGTH)
    x_axe.set_ylim(Y_MIN, Y_MAX)
    x_axe.set_yticks(threshold_values, False)
    x_graph, = x_axe.plot(time_data, x_data, 'r-')

    y_axe = fig.add_subplot(3, 1, 2)
    plt.ylabel('y acceleration')
    plt.axhline(y=threshold, linestyle='--', color='y')
    plt.axhline(y=-threshold, linestyle='--', color='y')
    plt.axhline(y=48, linestyle='-.', color='c')
    plt.axhline(y=-48, linestyle='-.', color='c')
    y_axe.set_xlim(0, X_LENGTH)
    y_axe.set_ylim(Y_MIN, Y_MAX)
    y_axe.set_yticks(threshold_values, False)
    y_graph, = y_axe.plot(time_data, y_data, 'b-')

    z_axe = fig.add_subplot(3, 1, 3)
    plt.ylabel('z acceleration')
    plt.axhline(y=threshold, linestyle='--', color='y')
    plt.axhline(y=-threshold, linestyle='--', color='y')
    plt.axhline(y=48, linestyle='-.', color='c')
    plt.axhline(y=-48, linestyle='-.', color='c')
    z_axe.set_xlim(0, X_LENGTH)
    z_axe.set_ylim(Y_MIN, Y_MAX)
    z_axe.set_yticks(threshold_values, False)
    z_graph, = z_axe.plot(time_data, z_data, 'g-')

def update_axe(graph, axe, y, index):

    graph.set_xdata(time_data)
    graph.set_ydata(y)
    axe.set_xlim(-X_LENGTH + index, index)

def plot_data():
    global var_i
    global x_data
    global y_data
    global z_data

    plt.subplot(3, 1, 1)
    update_axe(x_graph, x_axe, x_data, var_i)
        
    plt.subplot(3, 1, 2)
    update_axe(y_graph, y_axe, y_data, var_i)
        
    plt.subplot(3, 1, 3)
    update_axe(z_graph, z_axe, z_data, var_i)


def plot_motion_detection_machine_state(i):
    global var_i
    global time_data
    global motion
    global interrupt
    global new_int
    global current_state
    global x, y, z

    data_read = fh.readlines()

    for line in data_read:
       if analyse_data(line) == 1:
          #new valid data to plot
          if var_i > X_LENGTH:
              time_data.pop(0)
              x_data.pop(0)
              y_data.pop(0)
              z_data.pop(0)
         
          time_data.append(var_i)
          x_data.append(int(x))
          y_data.append(int(y))
          z_data.append(int(z))
          
          var_i += 1

    plot_data()
    
    plt.pause(1e-17)
    time.sleep(0.01)
    plt.draw()      


def analyse_data(line):
    global x
    global y
    global z

    new_line = line.rstrip('\n');
    new_line = new_line.replace(' ','') ## remove all whitespace 

    if len(new_line.split(';')) == 4:
        date, x, y, z = new_line.strip().split(";")
            
        # new value to eventually plot
        return 1 

    # no new value to eventually plot
    return 0


if __name__ == '__main__':
    #ex: python3 liveaccelerometer.py -input data_valid.txt 

    input_file_name = args.input

    print("input file: " + str(input_file_name))

    x_length=1000

    fh = open(input_file_name, "r")
    
    init_display(x_length)

    print("Going to analyse a LIVE signal")
    # I only want new output, so seek to the end of the file
    fh.seek(0,2)
    ani = animation.FuncAnimation(fig, plot_motion_detection_machine_state, fargs=(), interval=80)

    plt.show()

