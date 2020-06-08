# %%
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# %%
dada = pd.read_csv('../cleaned_data/cleaned_data_ivan.csv') 
dada = dada.drop([0])

# %%
def hist_makeup(dat, y_ax_n, ylims, name, mc, title):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    sam_size = len(dat)

    plt.rcParams.update({'font.size': 40, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc)})

    ax.set_title(title, color = '{}'.format(mc))
    ax.hist(dat, bins = 100, color = '#F39242')
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))

    ax.xaxis.set_ticks(np.arange(0, 100.1, 50))
    ax.set_xlim([-10, 100])
    # ax.set_ylim(ylims)
    ax.set_ylabel(y_ax_n, labelpad = padlabel)

    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels[0] = 'Greatly decreased'
    labels[1] = "Hasn't changed"
    labels[2] = 'Greatly increased'

    ax.set_xticklabels(labels)

    ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)

    ax.text(70, 10, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    # plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name), transparent = True)

def bar_makeup(dat, y_labels, mc, sam_size, name, x_label):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 40, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'font.weight': 'bold'})

    # ax.set_title(title)
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = '#F39242')
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)

    ax.text(90, 10, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), transparent = True, bbox_inches = 'tight')

green_dnm = '#9DC299'
yellow_pos = '#F3CE6C'
red_pos = '#AB2D39'
blu_dnm = '#9ACACC'
ye_dnm = '#F5E070'
pin_dnm = '#F2ADCB'
red_dnm = '#DE6067'

def pie_makeup(dat, names, mc, pi_colors, name):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 40, 
                        'font.weight': 'bold', 
                        'axes.labelcolor' : "{}".format(mc), 
                        'text.color': "{}".format(mc)})

    ax.pie(dat, labels = names, autopct='%1.0f%%', colors = pi_colors)
    sam_size = np.sum(dat)
    ax.text(0.85, 0.85, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), transparent = True)

def bar_makeup_change(dat, y_labels, mc, sam_size, name, x_label, title):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'font.weight': 'bold'})

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = '#FE6700')
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)

    ax.text(90, -0.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    # plt.savefig('./../figures/blog_figures/{}.png'.format(name), transparent = True, bbox_inches = 'tight')


# %% OPIOD CHANGE

opioid_change = dada['ChangeUseOpioids']

opioid_change_counted = opioid_change.value_counts()

total_opioid = opioid_change_counted.sum()
opioid_change_perc = round(opioid_change_counted/total_opioid, 2)

opioid_change_perc = opioid_change_perc.reindex(["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"])

rows_names = ["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"]
y_pos = np.arange(len(rows_names))

op_changes = np.asarray(opioid_change_perc[0:5]) * 100

def bar_makeup_change_op(dat, y_labels, mc, sam_size, name, x_label, title, im, size, x_im, y_im):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'figure.facecolor': 'black',
                         'font.weight': 'bold'})
                
    cola = '#462882'

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = mc)
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)
    ax.set_facecolor(cola)
    fig.patch.set_facecolor(cola)

    size = size, size
    imOpen = Image.open(im)
    imOpen.thumbnail(size, Image.ANTIALIAS)
    fig.figimage(imOpen, x_im, y_im, alpha = 1, zorder = 1)

    for i, v in enumerate(dat):
        ax.text(v + 3, i + .10, str(int(v)) + '%', color= mc, fontweight='bold')

    # plt.subplots_adjust(left=1.9, right=2, top=2, bottom=1.9)
    ax.text(83, 4.2, 'Opioids', color = mc)
    ax.text(80, 0.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))
    # plt.tight_layout()
    # plt.subplots_adjust(top=1.2)
    plt.savefig('./../figures/blog_figures/{}.png'.format(name), transparent=False, bbox_inches = 'tight', facecolor=fig.get_facecolor())

x_imO = 1000
y_imO = 200
path_op = '/Users/ivanezqrom/OneDrive - University College London/Documentos/Coding/Python/MHEF/covid19_survey/media/blog_dnm/opioids.png'
bar_makeup_change_op(op_changes,rows_names, 'white', total_opioid, 'change_opioids_blog', '%', '', path_op, 200, x_imO, y_imO)

# %% CHANGE BEN

benz_change = dada['ChangeUseBenzos']

benz_change_counted = benz_change.value_counts()

total_benz = benz_change_counted.sum()
benz_change_perc = round(benz_change_counted/total_benz, 2)

benz_change_perc = benz_change_perc.reindex(["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"])

rows_names = ["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"]
y_pos = np.arange(len(rows_names))

benz_changes = np.asarray(benz_change_perc[0:5]) * 100

def bar_makeup_change_benz(dat, y_labels, mc, sam_size, name, x_label, title, im, size, x_im, y_im):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'figure.facecolor': 'black',
                         'font.weight': 'bold'})
                
    cola = '#CBC9E6'

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = mc)
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)
    ax.set_facecolor(cola)
    fig.patch.set_facecolor(cola)

    size = size, size
    imOpen = Image.open(im)
    imOpen.thumbnail(size, Image.ANTIALIAS)
    fig.figimage(imOpen, x_im, y_im, alpha = 1, zorder = 1)

    for i, v in enumerate(dat):
        ax.text(v + 3, i + .10, str(int(v)) + '%', color= mc, fontweight='bold')

    # print("HERE")
    ax.text(82, 4.2, 'Benzos', color = mc)
    ax.text(80, 0.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), bbox_inches = 'tight', transparent=False, facecolor=fig.get_facecolor())

x_imO = 1000
y_imO = 200
path_benz = '/Users/ivanezqrom/OneDrive - University College London/Documentos/Coding/Python/MHEF/covid19_survey/media/blog_dnm/benzos.png'
bar_makeup_change_benz(benz_changes,rows_names, 'white', total_benz, 'change_benz_blog', '%', '', path_benz, 150, x_imO, y_imO)

# %% CHANGE CANNABIS

cann_change = dada['ChangeUseCann']

cann_change_counted = cann_change.value_counts()

total_cann = cann_change_counted.sum()
cann_change_perc = round(cann_change_counted/total_cann, 2)

cann_change_perc = cann_change_perc.reindex(["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"])

rows_names = ["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"]
y_pos = np.arange(len(rows_names))

cann_changes = np.asarray(cann_change_perc[0:5]) * 100

def bar_makeup_change_cann(dat, y_labels, mc, sam_size, name, x_label, title, im, size, x_im, y_im):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'figure.facecolor': 'black',
                         'font.weight': 'bold'})
                
    cola = '#5ABE8A'

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = mc)
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)
    ax.set_facecolor(cola)
    fig.patch.set_facecolor(cola)

    size = size, size
    imOpen = Image.open(im)
    imOpen.thumbnail(size, Image.ANTIALIAS)
    fig.figimage(imOpen, x_im, y_im, alpha = 1, zorder = 1)

    for i, v in enumerate(dat):
        ax.text(v + 3, i + .10, str(int(v)) + '%', color= mc, fontweight='bold')

    # print("HERE")
    ax.text(80, 0.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))
    ax.text(82, 4.2, 'Cannabis', color = mc)

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), bbox_inches = 'tight', transparent=False, facecolor=fig.get_facecolor())

x_imO = 1000
y_imO = 200
path_cann = '/Users/ivanezqrom/OneDrive - University College London/Documentos/Coding/Python/MHEF/covid19_survey/media/blog_dnm/cann.png'
bar_makeup_change_cann(cann_changes, rows_names, 'white', total_cann, 'change_cann_blog2', '%', '', path_cann, 200, x_imO, y_imO)


# %% REASON DRUGS

rea_drug = ['ReaDuHaveFun', 'ReaDuIncreaCreativity', 'ReaDuRelaxNightOut', 'ReaDuCopeStress', 
        'ReaDuEscapeReality','ReaDuWorkStudy', 'ReaDuSexualPleasure', 'ReaDuCoupleTherapy', 
        'ReaDuManageMentalHealth','ReaDuCopeBoredom', 'ReaDuCopeLoneliness', 'ReaDuCopeAnx', 
        'ReaDuRelapsed']

drucovid_yes = dada[dada['DrugUseOutbreakBool'] == 1]

duducovid_yes = drucovid_yes[rea_drug]

duducovid_yes = duducovid_yes.apply(pd.Series.value_counts)

for i in duducovid_yes.columns:
    total_temp = duducovid_yes[i].sum()
    duducovid_yes[i] = round(duducovid_yes[i]/total_temp, 2) * 100

duducovid_yes = duducovid_yes.drop([0])

duducovid_yes_sorted = duducovid_yes.loc[1].sort_values(ascending=False)

perc_reasons_dru_use = np.asarray(duducovid_yes_sorted)

names_readru = ['To have fun', 'To relax/night out', 'To cope with boredom',
                'To cope with stress', 'To escape reality', 'To cope with\xa0anxiety',
                'To increase creativity', 'To cope with loneliness', 'To manage a mental health issue',
                 'To increase sexual pleasure', 'To work and/or study', 'Relapsed',
                   'As couple’s/Relationship therapy']


def bar_makeup_change_rea_dru(dat, y_labels, mc, sam_size, name, x_label, title, im, size, x_im, y_im):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'figure.facecolor': 'black',
                         'font.weight': 'bold'})
                
    cola = 'white'

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = mc)
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)
    ax.set_facecolor(cola)
    fig.patch.set_facecolor(cola)

    size = size, size
    imOpen = Image.open(im)
    imOpen.thumbnail(size, Image.ANTIALIAS)
    fig.figimage(imOpen, x_im, y_im, alpha = 0.7, zorder = 1)

    for i, v in enumerate(dat):
        ax.text(v + 3, i + .10, str(int(v)) + '%', color= mc, fontweight='bold')

    # print("HERE")
    ax.text(80, 2.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), bbox_inches = 'tight', transparent=False, facecolor=fig.get_facecolor())


x_imO = 1200
y_imO = 200
path_brain = '/Users/ivanezqrom/OneDrive - University College London/Documentos/Coding/Python/MHEF/covid19_survey/media/blog_dnm/brain.png'
bar_makeup_change_rea_dru(perc_reasons_dru_use, names_readru, 'black', 1616, 'take_drugs_rea', '%', '', path_brain, 150, x_imO, y_imO)



# %% REASON DRUGS

cols_selfmed = ['ReaSelfMedSleep', 'ReaSelfMedMood', 'ReaSelfMedAnx', 'ReaSelfMedConc', 
                'ReaSelfMedMenHea', 'ReaSelfMedEatDis', 'ReaSelfMedPho', 'ReaSelfMedAntiPer', 
                'ReaSelfMedOCD', 'ReaSelfMedPTSD', 'ReaSelfMedBiDis', 'ReaSelfMedPain', 
                'ReaSelfMedQuitOtherDrugs', 'ReaSelfMedPresDrugs']
 
selfmed_yes = dada[dada['SelfMedBool'] == 1]

duduselfmed = selfmed_yes[cols_selfmed]

dududuselfmed = duduselfmed.apply(pd.Series.value_counts)

for i in dududuselfmed.columns:
    total_temp = dududuselfmed[i].sum()
    dududuselfmed[i] = round(dududuselfmed[i]/total_temp, 2) * 100

dududuselfmed = dududuselfmed.drop([0])

sorted_dududuselfmed = dududuselfmed.loc[1].sort_values(ascending=False)

perc_reasons_self = np.asarray(sorted_dududuselfmed)

names_selfmed = ['To reduce anxiety', 'To heighten mood/ alleviate symptoms of depression', 'To sleep', 
            'To manage other mental health issues', 'To relieve pain', 'To improve concentration', 
            'Antisocial personality', 'Post-traumatic stress disorder', 'Eating disorder', 'Bipolar disorder',
            'To quit other drugs', 'Replace inaccessible prescribed drugs', 'Obsessive compulsive disorder', 
            'Phobias']

def bar_makeup_change_rea_self(dat, y_labels, mc, sam_size, name, x_label, title, im, size, x_im, y_im):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 30, 
                         'axes.labelcolor' : "{}".format(mc), 
                         'xtick.color': "{}".format(mc),
                         'ytick.color': "{}".format(mc), 
                         'figure.facecolor': 'black',
                         'font.weight': 'bold'})
                
    cola = 'white'

    ax.set_title(title, color = '{}'.format(mc))
    # sorted_array = np.sort(dat)
    ind = np.arange(0, len(dat), 1)
    plt.barh(ind, dat, color = mc)
 
    padlabel = 10
    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))
    ax.set_yticks(ind, minor=False)
    ax.set_yticklabels(y_labels)
    # ax.set_ylim([0, len(dat)])
    # print(len(dat))
    ax.invert_yaxis()

    ax.set_xlim([0, 100])
    
    ax.set_xlabel(x_label, labelpad = padlabel)

    # ax.set_xticklabels(labels)

    # ax.tick_params(axis='both', which='major', pad=padlabel)

    ax.yaxis.set_tick_params(width = lwD, length = lenD)
    ax.xaxis.set_tick_params(width = lwD, length = lenD)

    ax.spines['left'].set_linewidth(lwD)
    ax.spines['bottom'].set_linewidth(lwD)
    ax.set_facecolor(cola)
    fig.patch.set_facecolor(cola)

    size = size, size
    imOpen = Image.open(im)
    imOpen.thumbnail(size, Image.ANTIALIAS)
    fig.figimage(imOpen, x_im, y_im, alpha = 0.7, zorder = 1)

    for i, v in enumerate(dat):
        ax.text(v + 3, i + .10, str(int(v)) + '%', color= mc, fontweight='bold')

    # print("HERE")
    ax.text(80, 2.5, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), bbox_inches = 'tight', transparent=False, facecolor=fig.get_facecolor())


x_imO = 1550
y_imO = 200
path_brain = '/Users/ivanezqrom/OneDrive - University College London/Documentos/Coding/Python/MHEF/covid19_survey/media/blog_dnm/brain.png'
bar_makeup_change_rea_self(perc_reasons_self, names_selfmed, 'black', 700, 'self_med_rea', '%', '', path_brain, 150, x_imO, y_imO)


# %% Self-med

counts_selfmed = np.asarray(dada['SelfMedBool'].value_counts())

selfmed_names = ['No', 'Yes']

def pie_makeup_self_med(dat, names, mc, pi_colors, name):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)

    plt.rcParams.update({'font.size': 60, 
                        'font.weight': 'bold', 
                        'axes.labelcolor' : "{}".format(mc), 
                        'text.color': "{}".format(mc)})


    cola = 'white'

    ax.pie(dat, labels = names, autopct='%1.0f%%', colors = pi_colors)
    sam_size = np.sum(dat)
    ax.text(0.85, 0.85, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    # ax.set_facecolor(cola)
    # fig.patch.set_facecolor(cola)

    plt.savefig('./../figures/blog_figures/{}.png'.format(name), transparent=True)

pie_makeup_self_med(counts_selfmed, selfmed_names, 'black', [green_dnm, red_pos], 'pie_selfmed')


# %%
