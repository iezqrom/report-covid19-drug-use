# %%
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns

# %%
dada = pd.read_csv('../cleaned_data/cleaned_neurosoc_talk_ivan.csv') 
dada = dada.drop([0])

# %% Plotting funcs
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

    plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name), transparent = True, bbox_inches = 'tight')

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

    plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name), transparent = True)

############## EVERYONE TOGEDA
# %% Histogram EVERYONE alcohol change

alc_change = np.asarray(dada['ChangeAlcohol'])

alc_change = alc_change[~np.isnan(alc_change)]
alc_change = alc_change[1:]

def seaborn_dist(dat, mc, name):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    sam_size = len(dat)

    plt.rcParams.update({'font.size': 30, 
                            'axes.labelcolor' : "{}".format(mc), 
                            'xtick.color': "{}".format(mc),
                            'ytick.color': "{}".format(mc), 
                            'font.weight': 'bold'})
    padlabel = 10

    sns.distplot(dat, hist=False, kde=True, color = blu_dnm,
                bins=100, kde_kws={'linewidth': 4, 'shade': True}, ax = ax)

    lwD = 5
    lenD = 20

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines["bottom"].set_color("{}".format(mc))
    ax.spines["left"].set_color("{}".format(mc))

    ax.xaxis.set_ticks(np.arange(-20, 120.1, 70))
    ax.yaxis.set_ticks(np.arange(0, 0.031, 0.01))
    ax.set_xlim([-20, 120])
    ax.set_ylim([0, 0.03])

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

    ax.text(100, 0.0175, 'n = {}'.format(sam_size), color = '{}'.format(mc))

    plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name), transparent = True)



# alc_dist.set_xticks(np.arange(-20, 120.1, 70)) 
# alc_dist.set_xticklabels(['Greatly decreased',"Hasn't changed",'Greatly increased'])

seaborn_dist(alc_change, 'white', 'alc_change_every')


# %% Histogram EVERYONE nicotine smoke change
smo_change = np.asarray(dada['ChangeSmokeNicotine'])

smo_change = smo_change[~np.isnan(smo_change)]
smo_change = smo_change[1:]

seaborn_dist(smo_change, 'white', 'smo_change_every')


# %%
# %% Histogram EVERYONE nicotine vape change
vap_change = np.asarray(dada['ChangeVapeNicotine'])

vap_change = vap_change[~np.isnan(vap_change)]
vap_change = vap_change[1:]

seaborn_dist(vap_change, 'white', 'vap_change_every')

# hist_makeup(vap_change, 'Number of respondents', [0, 300], 'vap_change', 'white', 'Vaping nicotine change')

########## PREDICTORS?
# %% Histogram alcohol Life change
# short_lifechange = ['JobLoss', 'LeaveShopping', 'Self-isolating', 'LovedLoss', 'NoChange', 'LeaveSports', 'LeaveHealth', 'GoingWork', 'MoreWork', 'LessWork']

short_lifechange = ['NoChange', 'LeaveSports']
label_lifechange = ['No change', 'Exercise']
mc = 'white'

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111)
# sam_size = len(dat)

plt.rcParams.update({'font.size': 30, 
                        'axes.labelcolor' : "{}".format(mc), 
                        'xtick.color': "{}".format(mc),
                        'ytick.color': "{}".format(mc), 
                        'font.weight': 'bold'})
padlabel = 10

lwD = 5
lenD = 20

for n, i in enumerate(short_lifechange):

    job_loss = dada[dada[i] == 1]

    job_loss_alc_change = np.asarray(job_loss['ChangeAlcohol'])

    job_loss_alc_change = job_loss_alc_change[~np.isnan(job_loss_alc_change)]
    job_loss_alc_change = job_loss_alc_change[1:]

    sns.distplot(job_loss_alc_change, hist=False, kde=True, 
             bins=100, label = label_lifechange[n], kde_kws={'linewidth': 4, 'shade': True}, ax = ax)

sns.distplot(alc_change, hist=False, kde=True, color = blu_dnm,
        bins=100, label = 'Pooled', kde_kws={'linewidth': 4, 'shade': True}, ax = ax)

leg = plt.legend(prop={'size': 30}, frameon=False)
for text in leg.get_texts():
    plt.setp(text, color = '{}'.format(mc))

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines["bottom"].set_color("{}".format(mc))
ax.spines["left"].set_color("{}".format(mc))

ax.xaxis.set_ticks(np.arange(-20, 120.1, 70))
ax.yaxis.set_ticks(np.arange(0, 0.031, 0.01))
ax.set_xlim([-20, 120])
ax.set_ylim([0, 0.03])

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

# ax.text(100, 0.0175, 'n = {}'.format(sam_size), color = '{}'.format(mc))

name_change_alc_pred = 'no_change_exercise'
plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name_change_alc_pred), transparent = True)


    # hist_makeup(job_loss_alc_change, 'Number of respondents', [0, 300], 'job_loss_alc_change', 'black', i)

# %% Histogram alcohol Life change

# live_company = ['Family', 'Partner', 'Friends', 'On my own', 'Partner and children', 'Residence with students', 'Childrens']
# live_company = ['Family', 'On my own']
live_company = ['Partner', 'Family', 'On my own']
# live_company = ['Friends', 'Family']

mc = 'white'

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(111)
# sam_size = len(dat)

plt.rcParams.update({'font.size': 30, 
                        'axes.labelcolor' : "{}".format(mc), 
                        'xtick.color': "{}".format(mc),
                        'ytick.color': "{}".format(mc), 
                        'font.weight': 'bold'})
padlabel = 10

lwD = 5
lenD = 20

for i in live_company:

    job_loss = dada[dada['LiveCompany'] == i]

    job_loss_alc_change = np.asarray(job_loss['ChangeAlcohol'])

    job_loss_alc_change = job_loss_alc_change[~np.isnan(job_loss_alc_change)]
    job_loss_alc_change = job_loss_alc_change[1:]

    # hist_makeup(job_loss_alc_change, 'Number of respondents', [0, 150], 'job_loss_alc_change', 'black', i)
    sns.distplot(job_loss_alc_change, hist=False, kde=True, 
            bins=100, label = i, kde_kws={'linewidth': 4, 'shade': True}, ax = ax)

sns.distplot(alc_change, hist=False, kde=True, color = blu_dnm,
        bins=100, label = 'Pooled', kde_kws={'linewidth': 4, 'shade': True}, ax = ax)

leg = plt.legend(prop={'size': 30}, frameon=False)
for text in leg.get_texts():
    plt.setp(text, color = '{}'.format(mc))

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines["bottom"].set_color("{}".format(mc))
ax.spines["left"].set_color("{}".format(mc))

ax.xaxis.set_ticks(np.arange(-20, 120.1, 70))
ax.yaxis.set_ticks(np.arange(0, 0.031, 0.01))
ax.set_xlim([-20, 120])
ax.set_ylim([0, 0.03])

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

# ax.text(100, 0.0175, 'n = {}'.format(sam_size), color = '{}'.format(mc))

name_change_alc_pred = 'company_alc'
plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name_change_alc_pred), transparent = True)


############# REASONS
# %% START ALCOHOL

rea_alc = ['ReaAlcHaveFun', 'ReaAlcIncreaCreativity', 'ReaAlcRelaxNightOut', 'ReaAlcCopeStress', 'ReaAlcEscapeReality', 'ReaAlcWorkStudy', 'ReaAlcSexualPleasure',
            'ReaAlcCoupleTherapy', 'ReaAlcManageMentalHealth', 'ReaAlcCopeBoredom', 'ReaAlcCopeLoneliness', 'ReaAlcCopeFear', 'ReaAlcRelapsed']
   
counting_reasons_alc = []

for i in rea_alc:
    temp_count = dada[i].value_counts()[1]
    counting_reasons_alc.append(temp_count)

# bar_makeup(counting_reasons_alc, rea_alc, 'black')

# %% TAKING DRUGS

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

bar_makeup(perc_reasons_dru_use, names_readru, 'white', 1616, 'take_drugs_rea', x_label='%')


# counting_reasons_drug = []

# for i in rea_drug:
#     temp_count = dada[i].value_counts()
#     counting_reasons_drug.append(temp_count)

# %% Other drugs CHANGE

change_drugs = ['ChangeUse2C_X', 'ChangeUseAdderall', 'ChangeUseAmphe',
                'ChangeUseBenzos', 'ChangeUseCann', 'ChangeUseCocaine', 
                'ChangeUseMeth', 'ChangeUseDMT', 'ChangeUseDXM', 'ChangeUseIbo',
                'ChangeUseKet', 'ChangeUseLSD','ChangeUseMush',   
                'ChangeUseMAOIs', 'ChangeUseMDMA', 'ChangeUseMod',
                'ChangeUseNO', 'ChangeUseOpioids', 'ChangeUseSSRIs',
                'ChangeUsePoppers', 'ChangeUseOther']

duduchange = dada[change_drugs]

duchanges_counted = duduchange.apply(pd.Series.value_counts)

n_drugs = []
duchanges_counted = duchanges_counted.append(pd.Series(name='samples'))

for i in duchanges_counted.columns:
    total_temp = duchanges_counted[i].sum()
    duchanges_counted[i] = round(duchanges_counted[i]/total_temp, 2)
    duchanges_counted[i]['samples'] = total_temp

# duchanges_counted = duchanges_counted.append({'sample':  np.asarray(n_drugs)}, ignore_index=True)

duchanges_counted = duchanges_counted.reindex(["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased", "samples"])


# %%

se_change_drugs = ['ChangeUseBenzos', 'ChangeUseCann', 'ChangeUseCocaine', 
                'ChangeUseKet', 'ChangeUseLSD','ChangeUseMush', 
                'ChangeUseMDMA', 'ChangeUseOpioids']

se_drugs = ['Benzodiazepine', 'Cannabis', 'Cocaine', 
                'Ketamine', 'LSD','Mushrooms', 
                'MDMA', 'Opioids']

rows_names = ["Greatly increased", "Increased", "Hasn't changed", "Decreased", "Greatly decreased"]
y_pos = np.arange(len(rows_names))


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

    plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name), transparent = True, bbox_inches = 'tight')


for ds, cs in zip(se_drugs, se_change_drugs):
    temp_changes = np.asarray(duchanges_counted[cs][0:5]) * 100
    temp_sample = int(duchanges_counted[cs][5])
    bar_makeup_change(temp_changes, rows_names, 'white', temp_sample, cs, '%', ds)

ben_post = duchanges_counted['ChangeUseBenzos'][0:5]*100

bar_makeup_change(ben_post, rows_names, 'black', int(duchanges_counted['ChangeUseBenzos'][5]), 'ben_change_post', '%', '')


# fig, ax = plt.subplots(2, 2)

# se_first_half = se_change_drugs[:4]

# for i, su in enumerate(se_first_half):
#     temp_changes = np.asarray(duchanges_counted[su])
#     ax.flatten()[i].barh(y_pos, temp_changes)
#     ax.flatten()[i].set_title(su)
#     ax.flatten()[i].set_yticks(y_pos)
#     ax.flatten()[i].set_yticklabels(rows_names)
#     ax.flatten()[i].invert_yaxis()

# fig, ax = plt.subplots(2, 2)
# se_second_half = se_change_drugs[4:]

# for i, su in enumerate(se_second_half):
#     temp_changes = np.asarray(duchanges_counted[su])
#     ax.flatten()[i].barh(y_pos, temp_changes)
#     ax.flatten()[i].set_title(su)
#     ax.flatten()[i].set_yticks(y_pos)
#     ax.flatten()[i].set_yticklabels(rows_names)
#     ax.flatten()[i].invert_yaxis()


# %% Withdrawal Drugs
counts_with = np.asarray(dada['WithdrawalBool'].value_counts())


with_names = ['No', 'Yes']
pie_makeup(counts_with, with_names, 'white', [green_dnm, red_pos], 'pie_withdrawal')

# %% Dependence Drugs
counts_dep = np.asarray(dada['DependenceBool'].value_counts())

dep_names = ['No', 'Potentially', 'Yes', "I don't know"]

pie_makeup(counts_dep, dep_names, 'white', [green_dnm, red_pos, yellow_pos, pin_dnm], 'pie_dependence')

# %% Self-medicate
counts_selfmed = np.asarray(dada['SelfMedBool'].value_counts())

selfmed_names = ['No', 'Yes']

pie_makeup(counts_selfmed, selfmed_names, 'white', [green_dnm, red_pos], 'pie_selfmed')

# %% Reasons to self-medicate
cols_selfmed = ['ReaSelfMedSleep', 'ReaSelfMedMood', 'ReaSelfMedAnx', 'ReaSelfMedConc', 
                'ReaSelfMedMenHea', 'ReaSelfMedEatDis', 'ReaSelfMedPho', 'ReaSelfMedAntiPer', 
                'ReaSelfMedOCD', 'ReaSelfMedPTSD', 'ReaSelfMedBiDis', 'ReaSelfMedPain', 
                'ReaSelfMedOtherDrugs', 'ReaSelfMedPresDrugs']
 

selfmed_yes = dada[dada['SelfMedBool'] == 1]

duduselfmed = selfmed_yes[cols_selfmed]

dududuselfmed = duduselfmed.apply(pd.Series.value_counts)

for i in dududuselfmed.columns:
    total_temp = dududuselfmed[i].sum()
    dududuselfmed[i] = round(dududuselfmed[i]/total_temp, 2) * 100

dududuselfmed = dududuselfmed.drop([0])

sorted_dududuselfmed = dududuselfmed.loc[1].sort_values(ascending=False)

perc_reasons_self = np.asarray(sorted_dududuselfmed)

names = ['To reduce anxiety', 'To heighten mood/ alleviate symptoms of depression', 'To sleep', 
            'To manage other mental health issues', 'To relieve pain', 'To improve concentration', 
            'Antisocial personality', 'Post-traumatic stress disorder', 'Eating disorder', 'Bipolar disorder',
            'To quit other drugs', 'Replace inaccessible prescribed drugs', 'Obsessive compulsive disorder', 
            'Phobias']

bar_makeup(perc_reasons_self, names, 'white', 700, 'self_med', x_label='%')

# %% DEMOGRAPHICS COUNTRIES

dada['Countries'].value_counts().plot(kind='pie', labels = None)

name_demo = 'countries_demo'
plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name_demo), transparent = True)

# %%

cols_gender = ['FemaleGender', 'MaleGender', 'OtherGender', 'NBGender']
 
dudugender = dada[cols_gender]

dududugender = dudugender.apply(pd.Series.value_counts)

for i in dududugender.columns:
    total_temp = dududugender[i].sum()
    dududugender[i] = round(dududugender[i]/total_temp, 2) * 100

dududugender = dududugender.drop([0])

sorted_dududugender = dududugender.loc[1].sort_values(ascending=False)

perc_reasons_self = np.asarray(sorted_dududugender)

names_gender = ['Male', 'Female', 'Non-binary', 'Other']

pie_makeup(perc_reasons_self, names_gender, 'white', [green_dnm, red_pos, blu_dnm, yellow_pos], 'pie_gender')


# plt.savefig('./../figures/neurosoc_talk/{}.png'.format(name_demo), transparent = True)


# %% WithdrawalSymptyoms
boWithSymp = dada['WithdrawalSymptyoms'].isnull()
indxWithSymp = dada['WithdrawalSymptyoms'][~boWithSymp].index

pd.set_option("display.max_rows", None, "display.max_columns", None, "display.max_colwidth", 300)

dada['WithdrawalSymptyoms'][indxWithSymp][100:150]

