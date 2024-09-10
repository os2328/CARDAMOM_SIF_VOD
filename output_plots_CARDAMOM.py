import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig_x = 6
fig_y = 4

def single_flux(data, flux_name, tag):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y)) #

    plt.plot(data.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data,axis=0),linewidth=1.5,color='black',label=tag)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()

def single_flux_and_towerdata(data, flux_name, tag, tower_data, tower_data_name):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y))
    plt.plot(data.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data,axis=0),linewidth=1.5,color='black',label=tag)
    plt.plot(tower_data, '.', color = 'tomato', linewidth=1,  ms = 5, label = tower_data_name)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()

def single_flux_and_towerdata2(data, flux_name, tag, tower_data1, tower_data_name1, tower_data2, tower_data_name2):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y)) #

    plt.plot(data.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data,axis=0),linewidth=1.5,color='black',label=tag)

    plt.plot(tower_data1, '.', color = 'tomato', linewidth=1,  ms = 5, label = tower_data_name1)
    plt.plot(tower_data2, '.', color = 'indigo', linewidth=1,  ms = 5, label = tower_data_name2)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()

def compare_fluxes(data1, data2, flux_name, tag1, tag2):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y)) #

    plt.plot(data1.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data1,axis=0),linewidth=1.5,color='black',label=tag1)
    plt.plot(np.median(data2,axis=0),linewidth=1.5,color='royalblue',label=tag2)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()


def compare_fluxes_and_towerdata(data1, data2, flux_name, tag1, tag2, tower_data, tower_data_name):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y))
    plt.plot(data1.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data1,axis=0),linewidth=1.5,color='black',label=tag)
    plt.plot(np.median(data2,axis=0),linewidth=1.5,color='royalblue',label=tag2)

    plt.plot(tower_data, '.', color = 'tomato', linewidth=1,  ms = 5, label = tower_data_name)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()

def compare_fluxes_and_towerdata2(data1, data2, flux_name, tag1, tag2, tower_data1, tower_data_name1, tower_data2, tower_data_name2):
    fig, ax = plt.subplots(1,1, figsize=(fig_x,fig_y)) #

    plt.plot(data1.T,color='silver',linewidth=0.4,alpha=.03,label='__nolabel__')
    plt.plot(np.median(data1,axis=0),linewidth=1.5,color='black',label=tag)
    plt.plot(np.median(data2,axis=0),linewidth=1.5,color='royalblue',label=tag2)

    plt.plot(tower_data1, '.', color = 'tomato', linewidth=1,  ms = 5, label = tower_data_name1)
    plt.plot(tower_data2, '.', color = 'indigo', linewidth=1,  ms = 5, label = tower_data_name2)

    ax.set_ylabel(flux_name)
    ax.set_xlabel('Time [months]')
    plt.legend(loc = 'upper right')
    plt.show()

def parameter_hist(list_n, cbr_load, name_ind, true_param = None):
    n = len(list_n)
    if n%5 ==0:
        a = n//5
    else:
        a= n//5+1
    fig = plt.figure(figsize=(9, 1.7*a))
    for ind, parname in enumerate(list_n):

        plt.subplot(a,5, ind+1)
        index = name_ind[ind]
        heights, bins = np.histogram(cbr_load[:,index],bins=10)
        vm = np.max(heights)

        plt.hist(cbr_load[:,index],  alpha = 0.7, edgecolor='navy', linewidth=0.6, bins=10)
        if true_param != None:
            plt.vlines(true_param[0][index], 0, vm, colors='red', linewidth=3)
        plt.title(parname)
        fig.tight_layout()

def parameter_hist_compare(list_n, cbr_load, cbr_load2, name_ind, labels, true_param = None):
    n = len(list_n)
    if n%5 ==0:
        a = n//5
    else:
        a= n//5+1
    fig = plt.figure(figsize=(9, 1.7*a))
    for ind, parname in enumerate(list_n):

        plt.subplot(a,3, ind+1)
        index = name_ind[ind]
        heights, bins = np.histogram(cbr_load[:,index], bins=10)
        vm = np.max(heights)

        plt.hist(cbr_load[:,index], alpha = 0.7, edgecolor='navy', linewidth=0.6, bins=10, label = labels[0])
        plt.hist(cbr_load2[:,index], alpha = 0.7, edgecolor='brown', linewidth=0.6, bins=10, label = labels[1])

        if parname==list_n[-1]:
            plt.legend(bbox_to_anchor=(5.04,1), loc="upper left" )
        if true_param != None:
            plt.vlines(true_param[0][index], 0, vm, colors='red', linewidth=3)
        plt.title(parname)
        fig.tight_layout()
