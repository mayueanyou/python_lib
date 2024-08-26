import matplotlib.pyplot as plt
import numpy as np


def simple_plot_rgb(data,path):
    plt.imsave(path,data)

def mtplot(row,column,data,path):
    fig, axs = plt.subplots(row, column)
    for i in range(row):
        for j in range(column):
            if i*column+j >= len(data): break
            axs[i,j].imshow(data[i*column+j],cmap = 'gray')
            #axs[i,j].title.set_text(f'filter{i*4+j-2}')
    #fig.suptitle(f"label:{y},predict{x}")
    fig.set_size_inches(18.5, 10.5)
    plt.tight_layout()
    plt.savefig(path)

def plot_distribution(path,data,bins=20,ratio=(16,9),scale=1):
    fig, axs = plt.subplots(1)
    fig.set_size_inches(ratio[0]*scale,ratio[1]*scale)
    x_min,x_max = np.min(data),np.max(data)
    interval_count = bins + 1
    axs.xaxis.set_ticks(np.linspace(x_min,x_max,interval_count))
    plt.legend(title = f'total numbers:{len(data)}',title_fontsize = 'xx-large')
    axs.hist(data, color='lightgreen', ec='black', bins=bins,density=False,stacked=False,weights=np.ones(len(data)) / len(data))
    plt.savefig(path)


if __name__ == '__main__':
    pass