import os,sys,sklearn,itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.manifold import TSNE

class Ploter:
    def __init__(self,row=None,column=None,ratio=(16,9),scale=1,dpi=400) -> None:
        self.dpi = dpi
        self.fig,self.axs =  plt.subplots(1) if row is None and column is None else plt.subplots(row, column)
        self.fig.set_size_inches(ratio[0]*scale,ratio[1]*scale)
        plt.rcParams['figure.dpi'] = self.dpi
        plt.rcParams['savefig.dpi'] = self.dpi
        self.fontsize = 20
        plt.rcParams['text.usetex'] = False
        plt.rcParams['lines.linewidth'] = 2
        self.linewidth = 2
        self.parameters = {'axes.labelsize':self.fontsize,
                           'axes.titlesize': self.fontsize,
                           'xtick.labelsize': self.fontsize,
                           'ytick.labelsize': self.fontsize}
    
    def __del__(self):
        plt.close(self.fig)
    
    def close(self):
        plt.close(self.fig)
    
    def savefig(self,path):
        folder_path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        if not os.path.exists(folder_path):os.makedirs(folder_path)
        #plt.tight_layout() 
        plt.savefig(path)
    
    def save_rgb(self,path,data,title='image'):
        data = np.array(data)
        folder_path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
        if not os.path.exists(folder_path):os.makedirs(folder_path)
        plt.title(title)
        plt.imshow(data)
        plt.savefig(path)
    
    def set_xlabel(self,text,fontsize = 20,idx=None):
        axs = self.axs if idx is None else self.axs[idx]
        axs.set_xlabel(text,fontsize = fontsize)
    
    def set_ylabel(self,text,fontsize = 20, idx=None):
        axs = self.axs if idx is None else self.axs[idx]
        axs.set_ylabel(text,fontsize = fontsize)
    
    def set_xticks(self,data=None,fontsize = 20, decimals = 1,tf=None,idx=None):
        axs = self.axs if idx is None else self.axs[idx]
        ticks =  axs.get_xticks() if data is None else data
        if tf is not None: ticks = tf(ticks)
        ticks = np.round(ticks,decimals=decimals)
        axs.set_xticklabels(ticks, fontsize=fontsize)
    
    def set_yticks(self,data=None,fontsize = 20, decimals = 1, tf=None, idx=None):
        axs = self.axs if idx is None else self.axs[idx]
        ticks =  axs.get_yticks() if data is None else data
        if tf is not None: ticks = tf(ticks)
        ticks = np.round(ticks,decimals=decimals)
        axs.set_yticklabels(ticks, fontsize=fontsize)
    
    def plot_lines(self,path,data):
        x = np.arange(0,len(data[0]),1)
        for line in data:
            self.axs.plot(x,line)
            self.axs.legend(x)
        self.savefig(path)
    
    def add_color_legend(self,label,color='black',idx=None):
        handles = mpatches.Patch(label=label,color=color) 
        if idx is None: self.axs.legend(handles=[handles],title_fontsize = 'xx-large')
        else: self.axs[idx].legend(handles=[handles],title_fontsize = 'xx-large')
        
    
    def plot_vertical_line(self,x,color='black',linestyle='-'):
        self.axs.axvline(x, color=color, linestyle=linestyle)
    
    def plot_distribution(self,data,bins=10,color='black',linestyle='-',mode='plt_plot',label='',idx=None):
        axs = self.axs if idx is None else self.axs[idx]
        hist, bin_edges = np.histogram(data, bins = bins, density=True)
        hist/= np.sum(hist)
        new_bin_edges = []
        for i in range(len(bin_edges)-1): new_bin_edges.append(np.mean([bin_edges[i],bin_edges[i+1]]))
        new_bin_edges = np.array(new_bin_edges)
        if mode == 'plt_hist': axs.hist(hist,bins=bins ,color=color,linestyle=linestyle)
        elif mode == 'plt_plot': axs.plot(new_bin_edges, hist,label=label,color=color,linestyle=linestyle)
        elif mode == 'sns_hist': sns.histplot(data, kde=True, stat='density',fill=True,ax=axs)
        #elif mode == 'sns_hist': sns.histplot(y=new_bin_edges,x=hist ,kde=True, stat='density',fill=True,ax=axs)
        elif mode == 'sns_dis': sns.displot(data, fill=True, kind="kde",ax=axs)
        elif mode == 'sns_kde': sns.kdeplot(data,fill=True,ax=axs,label=label,linewidth=self.linewidth)
    
    def plot_tsne(self,path,data,label=None,text=True,label_text=None,
                  p={'n_components':2,'perplexity':50,'random_state':0}):
        
        
        model = TSNE(n_components = p['n_components'], perplexity = p['perplexity'],random_state = p['random_state'])
        tsne_data = model.fit_transform(data)
        if label is None: 
            label = np.arange(0,len(data),1)
            color_num = len(data)
        else: color_num = np.max(np.array(label))+1
        
        tsne_data_pd = np.vstack((tsne_data.T, label)).T
        tsne_df = pd.DataFrame(data = tsne_data_pd,columns =("Dim_1", "Dim_2", "label"))
        #palette = sns.color_palette(None, n_colors = color_num)
        #palette = sns.color_palette("bright", color_num)
        palette = sns.color_palette("Spectral", n_colors = color_num, as_cmap=True)
        axs = sns.scatterplot(data=tsne_df, x='Dim_1', y='Dim_2',hue='label', legend = False, palette=palette)
        #axs = sns.scatterplot(data=tsne_df, x='Dim_1', y='Dim_2', palette=palette)
        if text: 
            for i in range(len(tsne_data)): axs.text(tsne_data[i][0]+0.01,tsne_data[i][1],str(int(label[i])),size='xx-small')
        #plt.legend(fontsize=20)
        self.savefig(path)
    
    def plot_log(self,path,data):
        self.axs.set_xscale('log')
        self.axs.plot(data, color='blue', lw=2)
        self.axs.legend()
        self.savefig(path)

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



if __name__ == '__main__':
    ploter = Ploter()
    
    ploter.plot_log('test.png',[1,2,3,4,5,6,7,8,9,10])
    pass