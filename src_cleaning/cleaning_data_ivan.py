# %%
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

# %% Functions

def simpCollap(column, name):
    bo = draCI[column].isnull()
    indx = draCI[column][~bo].index
    draCI[column][indx] = name
    return indx

def expandCode(old, new, nameCol):
    for i, v in enumerate(old):
        indx = draCI[nameCol][draCI[nameCol] == v].index.tolist()
        draCI[new[i]] = 0
        draCI[new[i]][indx] = 1
   
def binariseYesNo(nameCol):
    yes_indx = draCI[nameCol][draCI[nameCol] == 'Yes'].index.tolist()
    no_indx = draCI[nameCol][draCI[nameCol] == 'No'].index.tolist()
    draCI[nameCol][0] = 666

    draCI[nameCol][yes_indx] = 1
    draCI[nameCol][no_indx] = 0


def binariseSimple(col, name):
    indx = draCI[col][draCI[col] == name].index.tolist()
    draCI[col] = 0
    draCI[col][indx] = 1

# %%
# Import raw data
raw = pd.read_csv('../rawdata/survey.csv') 
copyraw = raw
# pd.set_option("display.max_rows", None, "display.max_columns", None, "display.max_colwidth", 300)

# %% Remove empty/useless columns
toDelete = ['Respondent ID', 'Collector ID', 'Start Date', 'End Date', 'IP Address', 'Email Address', 'First Name', 'Last Name', 'Custom Data 1']
dra = raw.drop(columns = toDelete, axis= 1)

# %% Rename questions

dra.rename(columns={'In what country are you living?': 'Countries', 
                    'How would you describe your gender?': 'Gender',
                    'What is your biological sex?': 'Sex',
                    'How long ago did your life change most clearly as a result of the COVID-19 pandemic?': 'LifechangeTiming',
                    'Do you currently drink alcohol?': 'CurrentlyAlcohol',
                    'Did you drink alcohol before the outbreak?': 'BeforeAlcohol',
                    'Do you smoke tobacco?': 'SmokeNicotine',
                    'Do you vape nicotine?': 'VapeNicotine', 
                    'Did you vape nicotine before the outbreak?': 'BeforeVapeNicotine',
                    'Have you ever used any drug recreationally (to induce an altered state for enjoyment)?': 'DrugUseBool',
                    'Have you used any recreational drugs during the outbreak?': 'DrugUseOutbreakBool',
                    'Have you tried any new drugs while in the outbreak?': 'NewDrugsOutbreakBool',
                    'Do you use\xa0any drugs to self-medicate during the outbreak?': 'SelfMedBool',
                    'Do you currently\xa0consume\xa0nicotine?': 'CurrentlyNicotine',
                    'Did you\xa0smoke tobacco before the outbreak?': 'BeforeSmokeNicotine',
                    'Have you experienced unintended symptoms of withdrawal since the start of the pandemic?': 'WithdrawalBool',
                    'Have you bought any drugs from a new supplier since the outbreak?': 'NewSupplier',
                    'Are there any drugs you currently want to stop taking?': 'StopBool',
                    'Before the outbreak, was there sufficient support for drug-related issues at your workplace/university/school?': 'BeforeSufficientSupport',
                    'How has your life changed due to the coronavirus outbreak? (tick all that apply)': 'Lifechange',
                    'How many people are there in your household? (including you)': 'Household',
                    'What age are you?': 'Age',
                    'How has your alcohol consumption changed since the start of the outbreak?': 'ChangeAlcohol',
                    'How has your tobacco consumption changed since the start of the outbreak?': 'ChangeSmokeNicotine',
                    'How many nights\xa0a week do you\xa0consume this amount during the outbreak?': 'FrequencyAlcohol',
                    'How often do you smoke tobacco?': 'OftenSmokeNicotine',
                    'How often do you use a nicotine vape?': 'OftenVapeNicotine',
                    'On average, how many cigarettes/roll-ups do you smoke a day?': 'FrequencySmokeNicotine',
                    'On average, how many times do you vape\xa0a day?': 'FrequencyVapeNicotine',
                    'How has your nicotine vape use changed since the start of the outbreak?': 'ChangeVapeNicotine',
                    'If taking recreational drugs during the outbreak, do you drink alcohol as well?': 'AlcoholCombinationsBool',
                    'Are you knowledgeable about how the drugs you combine interact?': 'KnowCombinations',
                    'Do you currently feel dependent to any drug?': 'DependenceBool',
                    'How often during the outbreak have you found that you were not able to control your drug use?': 'WithoutControl',  
                    'How often during the\xa0outbreak have you needed a drug in the morning to get you going for the rest of the day?': 'MorningHit',  
                    'During the outbreak, have you failed to do something expected of you because of your drug use?': 'FailExpect',
                    'Has your employer/university/school provided you support concerning alcohol and other drugs during the outbreak?': 'SupportDrugsOutbreak',
                    'Would you consult your employer/university/school about your drug use?': 'ConsultDrugUse',
                    
                    'I am...': 'EmployStatus',

                    'Who do you live with?': 'LiveCompany',
                    'Why did you start drinking during the lockdown?': 'WhyStartAlcohol',
                    'Why did you start smoking tobacco during the outbreak? (tick all that apply)': 'WhyStartSmokeNicotine',
                    'Why did you start vaping nicotine during the outbreak? (tick all that apply)': 'WhyStartVapeNicotine',
                    'Which of the reasons listed below influence your drug use during the outbreak? (Tick all that apply)': 'WhyDrugUse',
                    'Which of the reasons below describe your motivation to self-medicate during the outbreak? (Tick all that apply)': 'WhySelfMed',
                    'How is drug taking affecting your home working/studying habits?': 'HomeWorkHabits',
                    'What discourages you from seeking support from your employer/university/school? (Tick all that apply)': 'DiscourageSupport',
                    'What would encourage you to seek support from your employer/university/school? (Tick all that apply)': 'EncourageSupport',
                    
                    'On a drinking session during the outbreak, how much of each drink would you consume?': 'AmountSeshAlcohol',
                    
                    'What drugs have you used during the outbreak? (Tick all that apply)': 'TypeDrugUse',
                    'How often do you take each drug during the outbreak?': 'OftenDrugUse',
                    'Do you use any of these techniques when buying from a new supplier?': 'TechNewSupplier',

                    'What would you consume alcohol with?': 'AlcoholCombinations',
                    'What are your most common drug combinations during the outbreak? (Leave blank if none. Complete up to 5 combinations)': 'DrugCombinations',
                    'Which ones? (Tick all that apply)': 'DependenceWhich',
                    'What withdrawal symptoms have you experienced?': 'WithdrawalSymptyoms',
                    'Which new drugs have you\xa0tried\xa0during the outbreak? (Tick all that apply)': 'NewDrugsOutbreak',
                    'How\xa0has\xa0your use of each drug changed during the outbreak?': 'ChangeDrugUse',
                    'Which ones? (Tick all that apply).1': 'StopDrugs',
                    },
          inplace=True, errors='raise')

# %% Manually delete rows with inadequate responses 
# 2469: wrote dummy in Others: response boxes
# 1193: Gender, replied 'Apachi attack helicopter'
# 941: Gender, replied ???
# 1653: Gender, replied 'ATTACK HELICOPTER'
# 1817: Gender, replied: Apache attack helicopter
# 1873: Gender, replied: Nos Boss
# 2034: Gender, replied: Emu
# 2091: Gender, replied: A tractor tire

# 380: Sex, replied: -
# 528: Sex, replied: No
# 559: Sex, replied: Prefer not to say
# 1375: Sex, replied: please cut this question out
# 1467: Sex, replied: normal
# 2060: Sex, replied: What the fuck's wrong with you people?
# 2145: Sex, replied: Counterintuitive question
# 1657: No reply for Sex
# 36: Replied: FIX YOUR FUCKING SURVEY. Every time I try to scroll down these massive checkbox lists on mobile, it automatically scrolls back up to the top. *confused screaming*

inaII = [2469, 1193, 941, 1653, 1817, 1873, 2034, 2091, 2145, 2060, 380, 528, 559, 1375, 1481, 1467, 1657, 36]

draCI = dra.drop(index = inaII)

# %% Collapsing GENDER columns
boGender = draCI['Unnamed: 11'].isnull()
indxGender = draCI['Unnamed: 11'][~boGender].index

# draCI['FemaleGender'] = 0
# draCI['MaleGender'] = 0
# draCI['OtherGender'] = 0

try:
    # Manual changes to achieve consistency
    draCI['Gender'][5] = 'Female (including transgender women)' #replied: 'Female '
    draCI['Gender'][8] = 'Non-binary' #replied: No gender
    draCI['Gender'][11] = 'Female (including transgender women)' #replied: Woman (adult human female)
    draCI['Gender'][88] = 'Non-binary' #replied: No gender
    draCI['Gender'][133] = 'Male (including transgender men)' #replied: a human who presents as male and doesn't bother...
    draCI['Gender'][218] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][228] = 'Non-binary' #replied: Nonbinary and genderqueer femme
    draCI['Gender'][301] = 'Male (including transgender men)' #replied: A male. Transgender men are not male. On a sur...
    draCI['Gender'][306] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][392] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][398] = 'Non-binary' #replied: 'Non-binary '
    draCI['Gender'][411] = 'Male (including transgender men)' #replied: Human male, born with penis 
    draCI['Gender'][419] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][470] = 'Other' #replied: queer
    draCI['Gender'][472] = 'Non-binary' #replied: Non binary
    draCI['Gender'][519] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][520] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][537] = 'Non-binary' #replied: Non binary
    draCI['Gender'][553] = 'Non-binary' #replied: Non binary
    draCI['Gender'][565] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][585] = 'Other' #replied: Agender
    draCI['Gender'][600] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][693] = 'Non-binary' #replied: Nonbinary
    draCI['Gender'][814] = 'Non-binary' #replied: Non binary
    draCI['Gender'][844] = 'Other' #replied: Fluid gender
    draCI['Gender'][878] = 'Male (including transgender men)' #replied: MALE
    draCI['Gender'][902] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][914] = 'Female (including transgender women)' #replied: 'Female '
    draCI['Gender'][959] = 'Other' #replied: Bisexual
    draCI['Gender'][1052] = 'Male (including transgender men)' #replied: Male (excluding transgender man)
    draCI['Gender'][1138] = 'Other' #replied: Bi
    draCI['Gender'][1140] = 'Female (including transgender women)' #replied: Just female :D
    draCI['Gender'][1202] = 'Other' #replied: Queer
    draCI['Gender'][1209] = 'Non-binary' #replied: Non binary
    draCI['Gender'][1219] = 'Other' #replied: Gender neutral
    draCI['Gender'][1265] = 'Non-binary' #replied: Non binary
    draCI['Gender'][1300] = 'Non-binary' #replied: NB
    draCI['Gender'][1313] = 'Other' #replied: Gender fluid
    draCI['Gender'][1360] = 'Non-binary' #replied: non-binary
    draCI['Gender'][1385] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][1401] = 'Other' #replied: Queer
    draCI['Gender'][1431] = 'Other' #replied: Queer male
    draCI['Gender'][1665] = 'Male (including transgender men)' #replied: Man
    draCI['Gender'][1700] = 'Male (including transgender men)' #replied: Male, trans men don't exist. Just a normal bloke
    draCI['Gender'][1731] = 'Other' #replied: Human
    draCI['Gender'][1744] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][1760] = 'Other' #replied: Genderqueer FtM
    draCI['Gender'][1898] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][2058] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][2062] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][2067] = 'Other' #replied: Strait
    draCI['Gender'][2070] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][2095] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][2103] = 'Non-binary' #replied: Non binary
    draCI['Gender'][2117] = 'Other' #replied: Agender
    draCI['Gender'][2145] = 'Non-binary' #replied: Non-binary
    draCI['Gender'][2156] = 'Male (including transgender men)' #replied: Male
    draCI['Gender'][2261] = 'Other' #replied: Hetro
    draCI['Gender'][2307] = 'Non-binary' #replied: non binary
    draCI['Gender'][2309] = 'Non-binary' #replied: Nonbinary- They/Them
    draCI['Gender'][2374] = 'Female (including transgender women)' #replied: Female
    draCI['Gender'][2397] = 'Other' #replied: GAY
    draCI['Gender'][2399] = 'Female (including transgender women)' #replied: Female
    draCI['Gender'][2414] = 'Male (including transgender men)' #replied: Male
except:
    pass

del draCI['Unnamed: 11']

# %% GENDER binary code

male_indx = draCI['Gender'][draCI['Gender'] == 'Male (including transgender men)'].index.tolist()
draCI['MaleGender'] = 0
draCI['MaleGender'][male_indx] = 1

female_indx = draCI['Gender'][draCI['Gender'] == 'Female (including transgender women)'].index.tolist()
draCI['FemaleGender'] = 0
draCI['FemaleGender'][female_indx] = 1

nb_indx = draCI['Gender'][draCI['Gender'] == 'Non-binary'].index.tolist()
draCI['NBGender'] = 0
draCI['NBGender'][nb_indx] = 1

other_indx = draCI['Gender'][draCI['Gender'] == 'Other'].index.tolist()
draCI['OtherGender'] = 0
draCI['OtherGender'][other_indx] = 1


# del draCI['Gender']

# %% Collapsing SEX columns
boSex = draCI['Unnamed: 13'].isnull()
indxSex = draCI['Unnamed: 13'][~boSex].index

# Manual changes to achieve consistency
draCI['Sex'][933] = 'Male' #replied: 'Male'

del draCI['Unnamed: 13']


# %% SEX binary code

sex_male_indx = draCI['Sex'][draCI['Sex'] == 'Male'].index.tolist()
draCI['MaleSex'] = 0
draCI['MaleSex'][sex_male_indx] = 1

sex_female_indx = draCI['Sex'][draCI['Sex'] == 'Female'].index.tolist()
draCI['FemaleSex'] = 0
draCI['FemaleSex'][sex_female_indx] = 1

del draCI['Sex']

# %% AGE binary code
n_ageNEW = ['Under18', '18_25', '26_30', '31_35', '36_40', '41_45', '46_50', '51_55', '56_60', '61_65', 'Over65']
n_ageOLD = ['Under 18', '18-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', 'Over 65']

expandCode(n_ageOLD, n_ageNEW, 'Age')

del draCI['Age']

# %% Collapsing LIFECHANGE columns

# Simplify names to then collapse

short_lifechange = ['JobLoss', 'LeaveShopping', 'Self-isolating', 'LovedLoss', 'NoChange', 'LeaveSports', 'LeaveHealth', 'GoingWork', 'MoreWork', 'LessWork']

indexChange = []
for i, j in zip(np.arange(16, 26, 1), short_lifechange):
    col = 'Unnamed: {}'.format(i)
    indx = simpCollap(col, j)
    indexChange.append(indx)

index_home = simpCollap('Lifechange', 'Home')
indexChange.insert(0, index_home)

short_lifechange.insert(0, 'Home')

# Create new column wiht empty lists 
for i, j in zip(indexChange, short_lifechange):
    draCI['{}'.format(j)] = 0
    for x in i:
        draCI['{}'.format(j)][i] = 1

for i in np.arange(16, 26, 1):
    del draCI['Unnamed: {}'.format(i)]
del draCI['Lifechange']

# %% Collapsing LIFECHANGE OTHER columns

boLifeChange = draCI['Unnamed: 26'].isnull()
indxSex = draCI['Unnamed: 26'][~boLifeChange].index

# New columns
try:
    draCI['Furloughed'] = 0

    draCI['Furloughed'][3] = 1 # Replied: Furloughed
    draCI['Furloughed'][18] = 1 # Replied: I am furloughed. No work no pay until further notice
    draCI['Furloughed'][68] = 1 # I am a furloughed worker
    draCI['Furloughed'][71] = 1 # No longer working at job - on furlough
    draCI['Furloughed'][168] = 1 # Furloughed
    draCI['Furloughed'][2436] = 1 # Furloughed
    draCI['Furloughed'][2317] = 1 # I’m furloughed
    draCI['Furloughed'][2312] = 1 # On furlough so at home, no work and only essential reasons to leave home 
    draCI['Furloughed'][2223] = 1 # Furloughed 
    draCI['Furloughed'][2066] = 1 # Furloughed 
    draCI['Furloughed'][2077] = 1 # On furlough at them moment
    draCI['Furloughed'][1903] = 1 # Got laid off for a certain time
    draCI['Furloughed'][1844] = 1 # Furloughed 
    draCI['Furloughed'][1771] = 1 # Furloughed, still gettin 80% of my wage
    draCI['Furloughed'][1681] = 1 # Furlough
    draCI['Furloughed'][1689] = 1 # Been put on furlough 
    draCI['Furloughed'][1571] = 1 # I’m furloughed from work
    draCI['Furloughed'][1563] = 1 # Been furloughed
    draCI['Furloughed'][1558] = 1 # Been furloughed, sitting at home not doing much
    draCI['Furloughed'][1505] = 1 # Furloughed
    draCI['Furloughed'][1425] = 1 # On furlough leave
    draCI['Furloughed'][1427] = 1 # Furlough 
    draCI['Furloughed'][955] = 1 # Furloughed
    draCI['Furloughed'][711] = 1 # Furloughed from job
    draCI['Furloughed'][718] = 1 # On furlough leave
    draCI['Furloughed'][699] = 1 # Furlough 
    draCI['Furloughed'][649] = 1 # 8 weeks unpaid leave 
    draCI['Furloughed'][605] = 1 # Uni work from home, part time job furloughed after a brief time of working from home 
    draCI['Furloughed'][215] = 1 # Furloughed
    draCI['Furloughed'][210] = 1 # Under furlough scheme
    draCI['Furloughed'][466] = 1 # Furlough

    draCI['Other'] = 0

    draCI['Other'][11] = 1 # Replied: I can't see my partner who lives abroad
    draCI['Other'][16] = 1 # Replied: I am disabled and cannot work a steady job. However, I do volunteer when able. I have had to stop volunteering as a result of the outbreak.
    draCI['Other'][37] = 1 # I had to move back to my parent’s house
    draCI['Other'][95] = 1 # Life has changes a bit, being more strategic when going shopping
    draCI['Other'][185] = 1 # No studying or work
    draCI['Other'][193] = 1 # unable to attend family funeral
    draCI['Other'][203] = 1 # crossdressing
    draCI['Other'][212] = 1 # Community outreach - but with tighter controls
    draCI['Other'][217] = 1 # Retired
    draCI['Other'][281] = 1 # It’s been an inconvenience and it’s annoying and not necessary
    draCI['Other'][287] = 1 # Reading more books
    draCI['Other'][293] = 1 # I'm exercising more
    draCI['Other'][329] = 1 # Taking a voluntary leave of absence from work
    draCI['Other'][434] = 1 #`increasingly targated by gangstalkers and hategroup
    draCI['Other'][458] = 1 # Summer break sucks cause I have to stay at home
    draCI['Other'][2311] = 1 # Temporarily off part time job 
    draCI['Other'][2094] = 1 # unable to work my regular job, work voluntarily from home
    draCI['Other'][1913] = 1  # im exercising
    draCI['Other'][1922] = 1 # Trapping more
    draCI['Other'][1655] = 1 # Moved to a position working directly with unhoused folks doing medical screenings
    draCI['Other'][1512] = 1 # Started junior doctor job ahead of time instead of final medical student placement
    draCI['Other'][1521] = 1 # Moved houses
    draCI['Other'][1440] = 1 # Medical doctor
    draCI['Other'][938] = 1 # All my job applications got cancelled 
    draCI['Other'][907] = 1 # Leaving the house to visit work families who need support 
    draCI['Other'][676] = 1 # Homeschooling my child 
    draCI['Other'][540] = 1 # im bored out of my mind and USPS takes forever to ship drugs right now.
    draCI['Other'][565] = 1 # I’ve started to spend more time with myself and It’s cool
    draCI['Other'][588] = 1 # My work has extensively changed in nature
    draCI['Other'][618] = 1 # Had to return from Erasmus 
    draCI['Other'][650] = 1 # I'm working about my artistics activities for change my actual job (that I haven't lost during the coronavirus outbreak) for a future day
    draCI['Other'][964] = 1 # Lost two jobs in one time, and for quarantine time find another extra job
    draCI['Other'][1567] = 1 # sleeping more
    draCI['Other'][1731] = 1 # I’m missing my grandbabies 
    draCI['Other'][1739] = 1 # Sleeping from 4 to 12 instead of 11 to 8
    draCI['Other'][1984] = 1 # Reading a lot
    draCI['Other'][1991] = 1 # I have more free time which is super
    draCI['Other'][2173] = 1 # Had to come back from Thailand early
    draCI['Other'][2257] = 1 # Doing things i never had time to do
    draCI['Other'][2266] = 1 # Boyfriend and I broke up. My workplace (shop) is currently closed.
    draCI['Other'][2407] = 1 # Ruined vacations

    draCI['MentalHealth'] = 0

    draCI['MentalHealth'][45] = 1 # depressed
    draCI['MentalHealth'][301] = 1 # Feeling trapped/mental health is suffering due to lack of socializing
    draCI['MentalHealth'][953] = 1 # Completely lost all productivity, sleep schedule is non existent.
    draCI['MentalHealth'][2406] = 1 # I am v lonely
    draCI['MentalHealth'][2271] = 1 # Feeling lonely 247 since I use to go out a lot 
    draCI['MentalHealth'][1909] = 1 # my home life is much more stressful
    draCI['MentalHealth'][1445] = 1 # I can't seem to focus or find motivation.
    draCI['MentalHealth'][1163] = 1 # I decided to change my life, quit job and go to volunteer abroad... But now I'm stuck at home with no real future plan.. Which makes me depressed as fu...k
    draCI['MentalHealth'][789] = 1 # Stress-napping
    draCI['MentalHealth'][548] = 1   # Depression has gotten much worse
    draCI['MentalHealth'][561] = 1 # depression worsened
    draCI['MentalHealth'][1755] = 1 # It's harder to get my DOC so I'm spending more money on not getting withdrawals. I'm also washing my hands a lot more.
    draCI['MentalHealth'][1933] = 1 # Weight gain/overeating
    draCI['MentalHealth'][829] = 1 # i am a doctor, feel a lot of pressure
    draCI['MentalHealth'][1429] = 1 # Kinda just hanging out when I can and waiting for things to be easier going and stressing over school

    draCI['Social'] = 0

    draCI['Social'][29] = 1 # 'hasn\'t changed "at all" is a bit strong since i would normally go out socially maybe once a month but otherwise my  lifestyle is little different, already used to WFH and rarely leave house except shopping'
    draCI['Social'][67] = 1 # My everyday life hasn't changed too much, but I see friend less, I can not meet with my boyfriend, because he moved to another country recently (in February) and I do not go to public events. I fe
    draCI['Social'][115] = 1 # I’m only leaving the house for shopping and seeing family
    draCI['Social'][228] = 1 # Less human touch
    draCI['Social'][241] = 1 # Meet with 1 friend at a time still occasionally and for exercise
    draCI['Social'][290] = 1 # Haven't seen friends or relatives since this started. Since March 14
    draCI['Social'][408] = 1 # Dislocated home life
    draCI['Social'][674] = 1 # Hard find a job. Not going out for parties but still hanging out with friends. 
    draCI['Social'][1032] = 1 # My life has only changed in terms of social gatherings 
    draCI['Social'][1341] = 1 # i’m leaving the house for good friends
    draCI['Social'][1580] = 1 # flatmate is super anxious and irritable
    draCI['Social'][1650] = 1 # Hanging out with friends (I know, not smart)
    draCI['Social'][1152] = 1 # Limited social life
    draCI['Social'][1160] = 1 # I'm leaving home a lot less and seeing far fewer people in person. Still shopping, exercising and occasionally seeing a small contained group.
    draCI['Social'][975] = 1 # I can’t go out to see my friends, weekends aren’t as joyfull as it was before
    draCI['Social'][1003] = 1 # I'm not talking with friends
    draCI['Social'][729] = 1 # I'm being social
    draCI['Social'][732] = 1 # I'm losing my sociability
    draCI['Social'][581] = 1 # I socialise less
    draCI['Social'][581] = 1
    draCI['Social'][1179] = 1 # I just switched to workout at home and stopped going to restaurants
    draCI['Social'][1230] = 1 # Feels like a never ending stay’cation
    draCI['Social'][1283] = 1 # I’m not seeing my friends
    draCI['Social'][1290] = 1 # I'm talking to people I shouldn't talk to
    draCI['Social'][1760] = 1 # Being quarantined together caused my domestic partner to move out and back to her parents
    draCI['Social'][1951] = 1 # Not as much contact to other people, and if so with precautions
    draCI['Social'][1807] = 1 # I‘m leaving the house to meet my family 
    draCI['Social'][1996] = 1  # Can’t chill with friends 
    draCI['Social'][2239] = 1 # I’m not travelling to see my family (which I used to do often)

    draCI['Financial'] = 0

    draCI['Financial'][205] = 1 # i lost a contract and have reduced income
    draCI['Financial'][123] = 1 # My parents are sending me less money
    draCI['Financial'][824] = 1 # I'm still working, but with no salary. I'm my own boss
    draCI['Financial'][1065] = 1 # I lost my job at agency but I am still working freelace, but it is difficult as hell, because I mainly work with events and we all know how many event we have in this situation
    draCI['Financial'][1401] = 1 # Landlord has given me rent free 4 months! 
    draCI['Financial'][2200] = 1 # Before the outbreak i was working part-time with children which has been stopped (therefore no pay) and I was also in the process of finding a full-time job, which is now more challenging to do.

    draCI['Living'] = 0

    draCI['Living'][103] = 1 # I went to live with my mom for some weeks
    draCI['Living'][165] = 1  # Moved back in with my parents after losing my job (was a college senior) now working at my dad’s law firm for him
    draCI['Living'][204] = 1 # Living at my mother’s. She’s having multiple paranoïa crisis a day.
    draCI['Living'][231] = 1 # Lost my dream job and my SO, stuck inside with my alcoholic mother who screams at me every night
    draCI['Living'][553] = 1 # I was homeless b4, but with all this going on some of my friends housed me up till its over. Have not be able to isolate at all
    draCI['Living'][1562] = 1 # Still homeless..
    draCI['Living'][1568] = 1 # My visa and move to another country got completely delayed.
    draCI['Living'][2099] = 1 # I have moved from the UK to my home country
    draCI['Living'][2115] = 1 # I had to move back in with my parents. I’m disabled, don’t feel comfortable cooking so when my university closed it’s cafeteria I need to go back home. 
    draCI['Living'][2124] = 1 # had to leave residential college and move back home
    draCI['Living'][2352] = 1 # i’ve moved back into parents home from uni
    draCI['Living'][2372] = 1 # I am in shielding and have had to leave shared accommodation
    draCI['Living'][2380] = 1 # Stay at home dad
    draCI['Living'][1694] = 1 # Lost my house to a flood, living in a hotel with my two kids, lost my job, and lost my best friend to the virus in less than a month
    draCI['Living'][1014] = 1 # Had to move home and get a supermarket job
    draCI['Living'][758] = 1  # Had to come back from a foreign country where I studied
    draCI['Living'][607] = 1  # came to Spain due to the COVID but I live in the Netherlands
    draCI['Living'][1140] = 1  # I have classes online, I came back to my hometown and I don’t lost my job

    draCI['Covid'] = 0

    draCI['Covid'][133] = 1 # was still working until covid-19 got me
    draCI['Covid'][445] = 1 # I have had coronavirus
    draCI['Covid'][1021] = 1 # I got the virus

    # More of the predetermined columns

    draCI['LessWork'][674] = 1 # Hard find a job. Not going out for parties but still hanging out with friends. 
    draCI['LessWork'][759] = 1 # I don’t leave the house unless my parents want me to go to the dump and I’m out of school and work
    draCI['LessWork'][1092] = 1 # I still have my job and I'm getting paid for it but I'm not working
    draCI['LessWork'][1092] = 1
    draCI['LessWork'][1145] = 1 # not studying or working at all 
    draCI['LessWork'][1442] = 1 # Studying from home, still going to work (reduced 1 hour)
    draCI['LessWork'][1540] = 1 # Not allowed to work during lockdown will be back when things have calmed down
    draCI['LessWork'][1774] = 1 # I m not working but still i get paid
    draCI['LessWork'][1804] = 1 # My final exams have been cancelled so my education is in hold until I start university
    draCI['LessWork'][1995] = 1 # I work in the live events industry, and while I have not lost my job, my hours have been temporarily reduced to zero. However, my employer is compensating me for all hours lost due to our industry...

    draCI['LeaveShopping'][1701] = 1 # I’m leaving the house to shop and take walks
    draCI['LeaveShopping'][2312] = 1 # On furlough so at home, no work and only essential reasons to leave home 
    draCI['LeaveShopping'][1385] = 1
    draCI['LeaveShopping'][952] = 1 # Im only leaving the house to buy drugs
    draCI['LeaveShopping'][625] = 1
    draCI['LeaveShopping'][115] = 1 # I’m only leaving the house for shopping and seeing family
    draCI['LeaveShopping'][174] = 1 # Only leaving for excercise and shopping
    draCI['LeaveShopping'][44] = 1 # 'In only leaning the house for essential purposes (necessary groceries, exercise) and have been maintaing social distancing'

    draCI['LeaveSports'][44] = 1 # 'In only leaning the house for essential purposes (necessary groceries, exercise) and have been maintaing social distancing'
    draCI['LeaveSports'][174] = 1 # Only leaving for excercise and shopping
    draCI['LeaveSports'][241] = 1 # Meet with 1 friend at a time still occasionally and for exercise
    draCI['LeaveSports'][625] = 1 # Only leaving the house for groceries and sports
    draCI['LeaveSports'][700] = 1 # I leave my house for exercise such as walking, biking, and skating.
    draCI['LeaveSports'][727] = 1 # I'm going out for sports more often
    draCI['LeaveSports'][739] = 1 # Dog walking
    draCI['LeaveSports'][929] = 1 # I leave the house for exercise
    draCI['LeaveSports'][1042] = 1 # I go for a walk each day
    draCI['LeaveSports'][1060] = 1 # I'm only leaving the house for walking the dog
    draCI['LeaveSports'][1385] = 1 # I'm leaving my house for shopping and exercise
    draCI['LeaveSports'][1450] = 1 # Leaving house for daily exercise
    draCI['LeaveSports'][1841] = 1 # Walking the dog daily 
    draCI['LeaveSports'][2143] = 1 # I'm only leaving the house for taking my dog for a walk
    draCI['LeaveSports'][2422] = 1 # Still getting out for exercise also 
    draCI['LeaveSports'][2204] = 1 # I’m only leaving my house for dog walks
    draCI['LeaveSports'][1701] = 1 # I’m leaving the house to shop and take walks
    draCI['LeaveSports'][1572] = 1 # I'm leaving the house for take muy dog for a walk
    draCI['LeaveSports'][1301] = 1 # I fish when I can

    draCI['LovedLoss'][231] = 1 # Lost my dream job and my SO, stuck inside with my alcoholic mother who screams at me every night

    draCI['MoreWork'][332] = 1  # Significantly more work from university

    draCI['Home'][378]  = 1  # I'm stuck inside smoking weed all day playing video games with my gf
    draCI['Home'][2409] = 1  # Send home with full wages
    draCI['Home'][1442] = 1 # Studying from home, still going to work (reduced 1 hour)

    draCI['JobLoss'][601] = 1 # Business has been closed

    draCI['NoChange'][1280] = 1 # Hasn’t. Current at an iboga and ibogaine clinic getting sober. Detoxed about 4 weeks ago 

    draCI['MoreWork'][1323] = 1 # I'm studying more hours since I have a hard time studying home (always have gone to the library)

    del draCI['Unnamed: 26']
except:
    pass

# 2249# ignore   59
# Ignore 2250  # Social - Distancing
# Ignore 2253  # Leaving house for mental wellbeing
# Ignore 2203  # I have fibromyalga and can't do much anyhow, 
# Ignore 2041  # I'm using the extra 80 sick hours work has given me to stay home as much as possible. I'm not an essential / hero (home depot) 
# Ignore 2055  # I'm not leaving home
# Ignore 1666  # leaving the house for dog walking
# Ignore 1826  # I work in retail so I’m not in work at all
# # Ignore 1849  # I'm working the same hours
# Ignore 1899  # It hasn't, disabled and on SSDI, I've been living like this for years. People are finally starting to see what my life is like every single day and I have no control over it. Some of the comments ...
# Ignore 1918  # only leaving the house for essential things
# Ignore 1795  # Go to the park 
# 50: said "I'm only leainb my house for a walk" Ignored as already replied with multiple choices
# 206 ignored: My life slightly changed, I do not go out as often as I did before
# 248, ignored: more drugs
# 253, ignored: Cannot get a job, due to Contracts being on-hold
# ignore 339   # In between jobs and new job start date pushed back 2 weeks.
# ignore 363   # Curfew is impossed so i cant leave house
# ignore 382   # i am a paitet at a MAT program and i am only going one day a week.  
# Ignore 409   # More household chores, cleaning, childcare, home schooling
# Ignore 412   # I'm physically disabled
# Ignore 464   # I'm using drugs every day 
# Ignore 490   # Our Venue has had to temporarily close but I still have a job once we are allowed to re open.
# Ignore 524   # I still go to work once a week
# Ignore 634 Actually working a lot more hours. Covid communications
# Ignore 684   # do grocery once for two weeks LOL
# Ignore 847   # student keyworker, only leaving the house to go to my tesco job
# Ignore 850   # I’m basically only studying 
# Ignore 885   # I leave to go get marijuana.
# Ignore 908   # Recreational drug use
# Ignore 959   # I am not getting drugs
# Ignore 1013 I took redundancy about a week before this hit!
#Ignore 1052  # My life changed only very slightly. I'm working from home anyway
# Ignore 1086  # Unemployed 
# Ignore 1172  # CHILLING
# Ignore 1219  I joined a dating app and am falling in love with someone I can't see in person until all this is over!
# Ignore 1343  # Stop working full time as essential worker 
#Ignore 1391  # I am a nurse
#Ignore 1418  # I‘m working 0 hours, but haven’t officially lost my job
# Ignore 1595 # Just landed a new job at a hospital before quarantine and it got put on hold so I’m unemployed 
# Ignore 1292  # They closed the club but it was low quality so it's alright
# Ignore 1103  # I'm only leaving the house to buy drugs
# Ignore 1947  # Home with the kids every day

# %% Expanding HOUSEHOLD columns
n_householdNEW = ['OwnHousehold', 'OneHousehold', 'TwoHousehold', 'ThreeHousehold', 'FourHousehold', 'OverFiveHouseld']
n_householdOLD = ['I live on my own', '2', '3', '4', 'Over 5']

     
expandCode(n_householdOLD, n_householdNEW, 'Household')

del draCI['Household']

# %% Collapsing LIVECOMPANY columns
live_companyNEW = ['LiveFamily', 'LivePartner', 'LiveFriends', 'LiveAlone', 'LivePartnerChildren', 'LiveChildren', 'LiveResidence']
live_companyOLD = ['Family', 'Partner', 'Friends', 'On my own', 'Partner and children', 'Children', 'Residence with students']

expandCode(live_companyOLD, live_companyNEW, 'LiveCompany')

draCI['LiveOther'] = 0

boLiveCompany = draCI['Unnamed: 29'].isnull()
indxLiveCompany = draCI['Unnamed: 29'][~boLiveCompany].index

draCI['LivePartner'][39] = 1 # Partner and flat mates
draCI['LiveOther'][39] = 1 # Partner and flat mates
draCI['LiveOther'][40] = 1 # flatmate
draCI['LivePartner'][72] = 1 # roommates and boyfriend
draCI['LiveOther'][72] = 1 # roommates and boyfriend
draCI['LivePartner'][76] = 1 # Partner and friends 
draCI['LiveFriends'][76] = 1 # Partner and friends 
draCI['LiveOther'][109] = 1 # Housemates random
draCI['LivePartner'][163] = 1 # Partner and partner's family
draCI['LiveFamily'][163] = 1 # Partner and partner's family
draCI['LiveOther'][194] = 1 # Lodgers 
draCI['LiveOther'][209] = 1 # Housemates
draCI['LiveFriends'][228] = 1 # Flatmates / friends / squat
draCI['LiveOther'][232] = 1 # Shared house 
draCI['LivePartner'][306] = 1 # Partner and roommates
draCI['LiveOther'][306] = 1 # Partner and roommates
draCI['LiveOther'][348] = 1 # Roomate
draCI['LiveOther'][356] = 1 # cat
draCI['LiveFamily'][392] = 1 # Mother
draCI['LivePartner'][416] = 1 # Boyfriend and his family 
draCI['LiveFamily'][416] = 1 # Boyfriend and his family 
draCI['LivePartner'][426] = 1 # Partner and Parents
draCI['LiveFamily'][426] = 1 # Partner and Parents
draCI['LiveOther'][434] = 1 # non-tenant residing in unhealthy housing on SSD
draCI['LivePartner'][488] = 1 # Partner and roommates
draCI['LiveOther'][488] = 1 # Partner and roommates
draCI['LiveAlone'][498] = 1 # I live alone
draCI['LivePartner'][511] = 1 # Partner and father-in-law
draCI['LiveFamily'][511] = 1 # Partner and father-in-law
draCI['LiveOther'][515] = 1 # Owner of property
draCI['LivePartner'][524] = 1 # Partner and brother
draCI['LiveFamily'][524] = 1 # Partner and brother
draCI['LiveOther'][545] = 1 # roommates
draCI['LiveOther'][553] = 1 # I live in a punk house with 10-15 people at any given time
draCI['LivePartner'][686] = 1 # Partner and friends
draCI['LiveFriends'][686] = 1 # Partner and friends
draCI['LivePartner'][693] = 1 # Partner and friend
draCI['LiveFriends'][693] = 1 # Partner and friend
draCI['LiveOther'][697] = 1 # Roommates
draCI['LiveFamily'][711] = 1 # My sister and her partner
draCI['LiveOther'][723] = 1 # Army barracks 
draCI['LiveOther'][755] = 1 # Boarding house
draCI['LiveOther'][828] = 1 # two flatmates
draCI['LivePartner'][829] = 1 # my boyfreind and my extended family
draCI['LiveFamily'][829] = 1 # my boyfreind and my extended family
draCI['LiveFamily'][878] = 1 # Mom
draCI['LiveOther'][938] = 1 # I live in a guardianship with other 90 people, of which 7 in my household
draCI['LiveOther'][962] = 1 # Housemates
draCI['LiveFamily'][1014] = 1 # Have a flat in London but moved back to parents for lockdown
draCI['LiveOther'][1016] = 1 # cat
draCI['LiveOther'][1019] = 1 # Dog
draCI['LiveOther'][1044] = 1 #     House sharing
draCI['LiveOther'][1101] = 1 #     On my own, with two cats
draCI['LiveAlone'][1109] = 1 #     Alone
draCI['LiveOther'][1142] = 1 #     Roommate
draCI['LivePartner'][1144] = 1 #     Partner and a flatmate
draCI['LiveOther'][1144] = 1 #     housemates in a coop
draCI['LiveOther'][1160] = 1 #     Roommate
draCI['LiveOther'][1187] = 1 #     grandmother
draCI['LiveFamily'][1203] = 1 #     Colleagues
draCI['LiveOther'][1212] = 1 #     Professional House Share
draCI['LiveOther'][1214] = 1 #     Roommate
draCI['LivePartner'][1264] = 1 #     Partner and maid
draCI['LiveOther'][1264] = 1 #     Partner and maid
draCI['LiveOther'][1290] = 1 #     Flatmate
draCI['LiveOther'][1295] = 1 #     Pet chihuahua
draCI['LiveOther'][1306] = 1 #     Ex-boyfriend and his new boyfriend
draCI['LiveOther'][1325] = 1 #     Flatmate
draCI['LiveOther'][1363] = 1 #     My ex partner
draCI['LiveOther'][1370] = 1 #     Roommate
draCI['LivePartner'][1373] = 1 #     Husband and friends 
draCI['LiveOther'][1373] = 1 #     Husband and friends 
draCI['LiveOther'][1376] = 1 #     Lodger
draCI['LiveFriends'][1464] = 1 #     Friend and partner
draCI['LivePartner'][1464] = 1 #     Friend and partner
draCI['LivePartner'][1466] = 1 #     wife
draCI['LiveOther'][1468] = 1 #     Roommates
draCI['LiveOther'][1508] = 1 #     Work
draCI['LiveFamily'][1567] = 1 #     Parents and partner
draCI['LivePartner'][1567] = 1 #     Parents and partner
draCI['LivePartner'][1594] = 1 #     Partner and partner's younger sibling (who's college is online now, so no more dorm)
draCI['LiveOther'][1594] = 1 #     Partner and partner's younger sibling (who's college is online now, so no more dorm)
draCI['LiveFamily'][1647] = 1 #     Friend and his family 
draCI['LiveFriends'][1647] = 1
draCI['LiveFamily'][1666] = 1 #     close friend's family
draCI['LiveFriends'][1666] = 1  #     close friend's family
draCI['LiveFamily'][1743] = 1 #     I’m currently staying with my mother to help her with groceries and use her kitchen, my primary residence is a back house without full kitchen. Lost my job and am staying here to save $$ on dining out, while also paying rent at home. 
draCI['LivePartner'][1759] = 1 #     Partner and two friends who are also a de facto 
draCI['LiveFriends'][1759] = 1 #     Partner and two friends who are also a de facto 
draCI['LiveFamily'][1865] = 1 #     Parents
draCI['LivePartner'][1921] = 1 #     Partner and their family
draCI['LiveFamily'][1921] = 1 #     Partner and their family
draCI['LiveAlone'][1923] = 1 #     Live on my own but need to use my friends house to access a computer for classes
draCI['LiveFamily'][1939] = 1 #     parents
draCI['LivePartner'][1993] = 1 #     Partner and sibling
draCI['LiveFamily'][1993] = 1 #     Partner and sibling
draCI['LiveOther'][2036] = 1 #     Roommate
draCI['LiveFamily'][2046] = 1 #     Sister and partner 
draCI['LivePartner'][2046] = 1 #     Sister and partner 
draCI['LivePartner'][2076] = 1 #     Partner + their family
draCI['LiveFamily'][2076] = 1 #     Partner + their family
draCI['LiveOther'][2095] = 1 #     Flat share 
draCI['LiveOther'][2158] = 1 #     Teenagers
draCI['LiveOther'][2183] = 1 #     Flatmate
draCI['LiveOther'][2189] = 1 #     roommates
draCI['LiveOther'][2234] = 1 #     4 cats and a dog
draCI['LiveOther'][2239] = 1 #     Flatmate
draCI['LiveFamily'][2258] = 1 #     Relatives 
draCI['LiveAlone'][2262] = 1 #     No one
draCI['LiveFamily'][2274] = 1 #     Cousin
draCI['LivePartner'][2278] = 1 #     Partner and flatmates
draCI['LiveOther'][2278] = 1 #     Partner and flatmates
draCI['LiveFamily'][2319] = 1 #     I usually live with students. Because of COVID Im living with my family right now
draCI['LivePartner'][2347] = 1 #     Partner and family
draCI['LiveFamily'][2347] = 1 #     Partner and family
draCI['LiveOther'][2356] = 1 #     Community
draCI['LiveFamily'][2365] = 1 #     Mother and lodgers
draCI['LiveOther'][2365] = 1 #     Mother and lodgers
draCI['LiveOther'][2406] = 1 #     Random people who also lease rooms from landlord
draCI['LiveAlone'][2423] = 1 #     On my own in a tower block of flats
draCI['LiveFamily'][2424] = 1 #     Parent/step parent
draCI['LivePartner'][2426] = 1 #     Moved to boyfriends
draCI['LivePartner'][2437] = 1 #     Partner and 2 flat mates
draCI['LiveOther'][2437] = 1 #     Partner and 2 flat mates

del draCI['LiveCompany']
# del draCI['Unnamed: 29']

# %% Expanding Life Changetiming columns
n_lifechangetimingNEW = ['ChangeLifeLessWeek', 'ChangeLifeOneTwo', 'ChangeLifeTwoFour', 'ChangeLifeOverFour']
n_lifechangetimingOLD = ['Less than a week ago', 'Between 1-2 weeks ago', 'Between 2-4 weeks ago', 'More than 4 weeks ago']

expandCode(n_lifechangetimingOLD, n_lifechangetimingNEW, 'LifechangeTiming')

del draCI['LifechangeTiming']

# %% Binarising binarisables

binarisables = ['CurrentlyAlcohol', 'BeforeAlcohol', 'SmokeNicotine', 'VapeNicotine', 
                  'BeforeVapeNicotine', 'DrugUseBool', 'DrugUseOutbreakBool', 'NewDrugsOutbreakBool',
                   'SelfMedBool', 'CurrentlyNicotine', 'BeforeSmokeNicotine', 'NewSupplier', 
                   'StopBool', 'BeforeSufficientSupport']

for i in binarisables:
    binariseYesNo(i)

# %% Numeric change Alcohol
draCI['ChangeAlcohol'][0] = '666'
draCI['ChangeAlcohol'] = pd.to_numeric(draCI['ChangeAlcohol'], downcast="integer")


# %% Numeric change Nicotine
draCI['ChangeSmokeNicotine'][0] = '999'
draCI['ChangeSmokeNicotine'] = pd.to_numeric(draCI['ChangeSmokeNicotine'], downcast="integer")


# %% dirty check Nic

nic_change = np.asarray(draCI['ChangeSmokeNicotine'])

nic_change = nic_change[~np.isnan(nic_change)]
nic_change = nic_change[1:]

plt.hist(nic_change, bins = 10)

# %% Numeric change Nicotine
draCI['ChangeVapeNicotine'][0] = '999'
draCI['ChangeVapeNicotine'] = pd.to_numeric(draCI['ChangeVapeNicotine'], downcast="integer")

# %% Expand Frequency of units sesh
n_freqalcNEW = ['FreqAlcLessWeek', 'FreqAlcOnceWeek', 'FreqAlc2_3Week', 'FreqAlc4_5Week', 'FreqAlc6_7Week']
n_freqalcOLD = ['Less than once a week', 'Once a week', '2-3 times a week', '4-5 times a week', '6-7 times a week']

expandCode(n_freqalcOLD, n_freqalcNEW, 'FrequencyAlcohol')

# del draCI['FrequencyAlcohol']

# %% Expand Frequency of smoke tobacco
n_freqsmoNEW = ['FrecSmoOneOff', 'FrecSmoSocially', 'FrecSmoHabitually']
n_freqsmoOLD = ['Only on one-off occasions', 'Socially', 'Habitually']

expandCode(n_freqsmoOLD, n_freqsmoNEW, 'OftenSmokeNicotine')

# del draCI['OftenSmokeNicotine']

# %% Expand Frequency of vape nicotine
n_freqsmoNEW = ['FrecVapOneOff', 'FrecVapSocially', 'FrecVapHabitually']
n_freqsmoOLD = ['Only on one-off occasions', 'Socially', 'Habitually']

expandCode(n_freqsmoOLD, n_freqsmoNEW, 'OftenVapeNicotine')

# del draCI['OftenVapeNicotine']

# %% Expand Frequency of vape nicotine
n_freqsmoNEW = ['FrecVapOneOff', 'FrecVapSocially', 'FrecVapHabitually']
n_freqsmoOLD = ['Only on one-off occasions', 'Socially', 'Habitually']

expandCode(n_freqsmoOLD, n_freqsmoNEW, 'OftenVapeNicotine')

# %% Expand Average of frequency Smoke Nicotine
n_freqsmodayNEW = ['FrecSmoDayOneOff', 'FrecSmoDaySocially', 'FrecSmoDayHabitually']
n_freqsmodayOLD = ['Only on one-off occasions', 'Socially', 'Habitually']

expandCode(n_freqsmodayOLD, n_freqsmodayNEW, 'FrequencySmokeNicotine')

# %% Expand Average of frequency Vape Nicotine
n_freqvapdayNEW = ['FrecVapDayOneOff', 'FrecVapDaySocially', 'FrecVapDayHabitually']
n_freqvapdayOLD = ['Only on one-off occasions', 'Socially', 'Habitually']

expandCode(n_freqvapdayOLD, n_freqvapdayNEW, 'FrequencyVapeNicotine')

# %% Expand Alcohol Combinations
n_alccomNEW = ['AlcComNo', 'AlcComYesSame', 'AlcComYesLess']
n_alccomOLD = ['No, I do not drink alcohol if I am taking other drugs', 'Yes, as much as I usually would without other drugs', 'Yes, but a lot less than I usually would']

expandCode(n_alccomOLD, n_alccomNEW, 'AlcoholCombinationsBool')


# %% Expand Knowledge Combinations
n_knowcomNEW = ['KnowComYes', 'KnowComNo', 'KnowComLittle', 'KnowComDont']
n_knowcomOLD = ['Yes', 'No', 'I know a little', "I don’t combine drugs" ]

expandCode(n_knowcomOLD, n_knowcomNEW, 'KnowCombinations')

# %% Expand Dependence Semi-boolean
n_depenNEW = ['DepenNo', 'DepenYes', 'DepenYesPotentially', 'DepenDontKnow']
n_depenOLD = ['No', 'Yes', 'Potentially', 'I don’t know']

expandCode(n_depenOLD, n_depenNEW, 'DependenceBool')

# %% Expand Out of control
n_outconNEW = ['OutConNever', 'OutConOnce', 'OutConWeekly', 'OutConDaily', 'OutConEOD']
n_outconOLD = ['Never', 'Once', 'Weekly', 'Daily', 'Every other day']

expandCode(n_outconOLD, n_outconNEW, 'WithoutControl')

# %% Expand Un buenos dias
n_morhitNEW = ['MorHitNever', 'MorHitOnce', 'MorHitWeekly', 'MorHitDaily', 'MorHitEOD']
n_morhitOLD = ['Never', 'Once', 'Weekly', 'Daily', 'Every other day']

expandCode(n_morhitOLD, n_morhitNEW, 'MorningHit')

# %% Expand Failed to do stuff drug use
n_failxNEW = ['FaExNever', 'FaExOnce', 'FaExWeekly', 'FaExDaily', 'FaExEOD']
n_failxOLD = ['Never', 'Once', 'Weekly', 'Daily', 'Every other day']

expandCode(n_failxOLD, n_failxNEW, 'FailExpect')

# %% Expand Employer/univeristy/school semi-boolean
n_suporgNEW = ['SupOrgNo', 'SupOrgYes', 'SupOrgSelfEmp', 'SupOrgLead']
n_suporgOLD = ['No', 'Yes', "I'm self-employed", "I'm the leader of my organisation/I make these decisions in my organisation"]

expandCode(n_suporgOLD, n_suporgNEW, 'SupportDrugsOutbreak')

# %% Expand Consult your organisation about drug use
n_conuseNEW = ['CoUseNo', 'CoUseYes', 'CoUseSelfEmp', 'CoUseLead', 'CoUseConNo']
n_conuseOLD = ['No', 'Yes', "I'm self-employed", "I'm the leader of my organisation", "I don't use any\xa0recreational\xa0drugs"]

expandCode(n_conuseOLD, n_conuseNEW, 'ConsultDrugUse')

# %% Amend Student/work status

col_names = np.asarray(draCI.columns)

ind_col_ws = np.where(col_names == 'EmployStatus')

draCI.rename(columns={'EmployStatus':'StudentStatus', #a student
                     'Unnamed: 323': 'UnemployedStatus', # unemployed
                     'Unnamed: 324': 'SelfEmpStatus', # self-employed
                     'Unnamed: 325': 'RetiredStatus', # retired
                     'Unnamed: 326': 'EmployedStatus' # employed
                    },
          inplace=True, errors='raise')

names = ['a student', 'unemployed', 'self-employed', 'retired', 'employed']
col_status = ['StudentStatus', 'UnemployedStatus', 'SelfEmpStatus', 'RetiredStatus','EmployedStatus']

for c, n in zip(col_status, names):
    binariseSimple(c, n)


# %% Amend reasons to start driking alcohol
ind_col_whyAlc = np.where(col_names == 'WhyStartAlcohol')
cols_why_alc = col_names[5:19]

draCI.rename(columns={'WhyStartAlcohol': 'ReaAlcHaveFun',          
                      'Unnamed: 34':     'ReaAlcIncreaCreativity', 
                      'Unnamed: 35':     'ReaAlcRelaxNightOut',    
                      'Unnamed: 36':     'ReaAlcCopeStress',    
                      'Unnamed: 37':     'ReaAlcEscapeReality',   
                      'Unnamed: 38':     'ReaAlcWorkStudy',   
                      'Unnamed: 39':     'ReaAlcSexualPleasure',   
                      'Unnamed: 40':     'ReaAlcCoupleTherapy',   
                      'Unnamed: 41':     'ReaAlcManageMentalHealth',   
                      'Unnamed: 42':     'ReaAlcCopeBoredom',   
                      'Unnamed: 43':     'ReaAlcCopeLoneliness',   
                      'Unnamed: 44':     'ReaAlcCopeFear',   
                      'Unnamed: 45':     'ReaAlcRelapsed',   
                      'Unnamed: 46':     'ReaAlcOther'    
                    },  
          inplace=True, errors='raise')

names = ['To have fun', 'To increase creativity', 'To relax/night out', 'To cope with stress',
          'To escape reality', 'To work and/or study', 'To increase sexual pleasure', 'As couple’s/Relationship therapy',
           'To manage a mental health issue', 'To cope with boredom', 'To cope with loneliness', 'To cope with fear',
           'Relapsed']

cols = ['ReaAlcHaveFun', 'ReaAlcIncreaCreativity', 'ReaAlcRelaxNightOut', 'ReaAlcCopeStress', 
        'ReaAlcEscapeReality','ReaAlcWorkStudy', 'ReaAlcSexualPleasure', 'ReaAlcCoupleTherapy', 
        'ReaAlcManageMentalHealth','ReaAlcCopeBoredom', 'ReaAlcCopeLoneliness', 'ReaAlcCopeFear', 
        'ReaAlcRelapsed']

for c, n in zip(cols, names):
    binariseSimple(c, n)

boReaAlcOther = draCI['ReaAlcOther'].isnull()
indxRealAlcOther = draCI['ReaAlcOther'][~boReaAlcOther].index
draCI['ReaAlcOther'] = 0
draCI['ReaAlcOther'][indxRealAlcOther] = 1

#Other Reasons Alcohol
# "emergency soul numbing solution"                                                                                                                                                                                                                                    
# Drinking because cant get cannabis and cocaine                                                                                                                                                                                                                       
# .                                                                                                                                                                                                                                                                    
# Other (please specify):                                                                                                                                                                                                                                              
# Reduce anxiety about non-covid related things that I was less in control of because I didn't feel safe going out because of the virus                                                                                                                                
# Alcohol slows my thought down and lets me zone out in front of the TV when I'm too wound up to do anything else and too careless to deliberately go to sleep. The more I drink, the more this verbose pattern or behaviour repeats itself. So subtle. Oh alcohol.    
# Replace Recreational Cannabis use                                                                                                                                                                                                                                    
# Other substances became less available                                                                                                                                                                                                                               

# %% Amend reasons to start smoking tobacco
ind_col_whySmo = np.where(col_names == 'WhyStartSmokeNicotine')
cols_why_smo = col_names[35:49]

draCI.rename(columns={'WhyStartSmokeNicotine': 'ReaSmoHaveFun',          
                      'Unnamed: 64':     'ReaSmoIncreaCreativity', 
                      'Unnamed: 65':     'ReaSmoRelaxNightOut',    
                      'Unnamed: 66':     'ReaSmoCopeStress',    
                      'Unnamed: 67':     'ReaSmoEscapeReality',   
                      'Unnamed: 68':     'ReaSmoWorkStudy',   
                      'Unnamed: 69':     'ReaSmoSexualPleasure',   
                      'Unnamed: 70':     'ReaSmoCoupleTherapy',   
                      'Unnamed: 71':     'ReaSmoManageMentalHealth',   
                      'Unnamed: 72':     'ReaSmoCopeBoredom',   
                      'Unnamed: 73':     'ReaSmoCopeLoneliness',   
                      'Unnamed: 74':     'ReaSmoCopeAnx',   
                      'Unnamed: 75':     'ReaSmoRelapsed',   
                      'Unnamed: 76':     'ReaSmoOther'    
                    },  
          inplace=True, errors='raise')

names = ['To have fun', 'To increase creativity', 'To relax/night out', 'To cope with stress',
          'To escape reality', 'To work and/or study', 'To increase sexual pleasure', 'As couple’s/Relationship therapy',
           'To manage a mental health issue', 'To cope with boredom', 'To cope with loneliness', 'To cope with anxiety',
           'Relapsed']

cols = ['ReaSmoHaveFun', 'ReaSmoIncreaCreativity', 'ReaSmoRelaxNightOut', 'ReaSmoCopeStress', 
        'ReaSmoEscapeReality','ReaSmoWorkStudy', 'ReaSmoSexualPleasure', 'ReaSmoCoupleTherapy', 
        'ReaSmoManageMentalHealth','ReaSmoCopeBoredom', 'ReaSmoCopeLoneliness', 'ReaSmoCopeAnx', 
        'ReaSmoRelapsed']

for c, n in zip(cols, names):
    binariseSimple(c, n)

# Other (please specify):      #THIS ROW WILL BE REMOVED AT THE END  
# Because I can’t find electronic cigarrete juices seller that ship to Switzerland           
# Social                                                                                                                                                   
# Vape juice wasn’t readily available to purchase and I didn’t want to go without nicotine     

boReaSmoOther = draCI['ReaSmoOther'].isnull()
indxRealSmoOther = draCI['ReaSmoOther'][~boReaSmoOther].index
draCI['ReaSmoOther'] = 0
draCI['ReaSmoOther'][indxRealSmoOther] = 1

# %% Amend reasons to start vaping
ind_col_whyVap = np.where(col_names == 'WhyStartVapeNicotine')
cols_why_vap = col_names[54:(54+14)]

draCI.rename(columns={'WhyStartVapeNicotine': 'ReaVapHaveFun',          
                      'Unnamed: 83':     'ReaVapIncreaCreativity', 
                      'Unnamed: 84':     'ReaVapRelaxNightOut',    
                      'Unnamed: 85':     'ReaVapCopeStress',    
                      'Unnamed: 86':     'ReaVapEscapeReality',   
                      'Unnamed: 87':     'ReaVapWorkStudy',   
                      'Unnamed: 88':     'ReaVapSexualPleasure',   
                      'Unnamed: 89':     'ReaVapCoupleTherapy',   
                      'Unnamed: 90':     'ReaVapManageMentalHealth',   
                      'Unnamed: 91':     'ReaVapCopeBoredom',   
                      'Unnamed: 92':     'ReaVapCopeLoneliness',   
                      'Unnamed: 93':     'ReaVapCopeAnx',   
                      'Unnamed: 94':     'ReaVapRelapsed',   
                      'Unnamed: 95':     'ReaVapOther'    
                    },  
          inplace=True, errors='raise')

names = ['To have fun', 'To increase creativity', 'To relax/night out', 'To cope with stress',
          'To escape reality', 'To work and/or study', 'To increase sexual pleasure', 'As couple’s/Relationship therapy',
           'To manage a mental health issue', 'To cope with boredom', 'To cope with loneliness', 'To cope with anxiety',
           'Relapsed']

cols = ['ReaVapHaveFun', 'ReaVapIncreaCreativity', 'ReaVapRelaxNightOut', 'ReaVapCopeStress', 
        'ReaVapEscapeReality','ReaVapWorkStudy', 'ReaVapSexualPleasure', 'ReaVapCoupleTherapy', 
        'ReaVapManageMentalHealth','ReaVapCopeBoredom', 'ReaVapCopeLoneliness', 'ReaVapCopeAnx', 
        'ReaVapRelapsed']

for c, n in zip(cols, names):
    binariseSimple(c, n)

boReaVapOther = draCI['ReaVapOther'].isnull()
indxRealVapOther = draCI['ReaVapOther'][~boReaVapOther].index
draCI['ReaVapOther'] = 0
draCI['ReaVapOther'][indxRealVapOther] = 1


# %% Amend influence drug taking during outbreak
ind_col_whyDU = np.where(col_names == 'WhyDrugUse')
cols_why_DU = col_names[ind_col_whyDU[0][0]:(ind_col_whyDU[0][0]+14)]

draCI.rename(columns={'WhyDrugUse':       'ReaDuHaveFun',          
                      'Unnamed: 184':     'ReaDuIncreaCreativity', 
                      'Unnamed: 185':     'ReaDuRelaxNightOut',    
                      'Unnamed: 186':     'ReaDuCopeStress',    
                      'Unnamed: 187':     'ReaDuEscapeReality',   
                      'Unnamed: 188':     'ReaDuWorkStudy',   
                      'Unnamed: 189':     'ReaDuSexualPleasure',   
                      'Unnamed: 190':     'ReaDuCoupleTherapy',   
                      'Unnamed: 191':     'ReaDuManageMentalHealth',   
                      'Unnamed: 192':     'ReaDuCopeBoredom',   
                      'Unnamed: 193':     'ReaDuCopeLoneliness',   
                      'Unnamed: 194':     'ReaDuCopeAnx',   
                      'Unnamed: 195':     'ReaDuRelapsed',   
                      'Unnamed: 196':     'ReaDuOther'    
                    },  
          inplace=True, errors='raise')

names = ['To have fun', 'To increase creativity', 'To relax/night out', 'To cope with stress',
          'To escape reality', 'To work and/or study', 'To increase sexual pleasure', 'As couple’s/Relationship therapy',
           'To manage a mental health issue', 'To cope with boredom', 'To cope with loneliness', 'To cope with\xa0anxiety',
           'Relapsed']

cols = ['ReaDuHaveFun', 'ReaDuIncreaCreativity', 'ReaDuRelaxNightOut', 'ReaDuCopeStress', 
        'ReaDuEscapeReality','ReaDuWorkStudy', 'ReaDuSexualPleasure', 'ReaDuCoupleTherapy', 
        'ReaDuManageMentalHealth','ReaDuCopeBoredom', 'ReaDuCopeLoneliness', 'ReaDuCopeAnx', 
        'ReaDuRelapsed']

for c, n in zip(cols, names):
    binariseSimple(c, n)

draCI['ReaDuPain'] = 0
draCI['ReaDuOther'] = 0
draCI['ReaDuSpiritual'] = 0
draCI['ReaDuMed'] = 0
draCI['ReaDuCope'] = 0

boReaDuOther = draCI['ReaDuOther'].isnull()
indxRealDuOther = draCI['ReaDuOther'][~boReaDuOther].index

# Other
draCI['ReaDuPain'][16] = 1 # To manage chronic pain
draCI['ReaDuSpiritual'][20] = 1 #  Search my soul
draCI['ReaDuOther'][29] = 1 #  force of habit
draCI['ReaDuSpiritual'][52] = 1 #  To have an introspective / therapeutic psychedelic trip
draCI['ReaDuHaveFun'][185] = 1 #  To celebrate events
draCI['ReaDuOther'][193] = 1 #  spending more time around other people smoking joints
draCI['ReaDuRelaxNightOut'][205] = 1 #  to appreciate my surroundings and increase well being
draCI['ReaDuMed'][245] = 1 #  Chronic illness
draCI['ReaDuRelaxNightOut'][290] = 1 #  To focus, to stay positive
draCI['ReaDuWorkStudy'][290] = 1 #  To focus, to stay positive
draCI['ReaDuWorkStudy'][293] = 1 #  To exercise
draCI['ReaDuOther'][302] = 1 #  I feel normal
draCI['ReaDuOther'][308] = 1 #  for sciencce
draCI['ReaDuMed'][320] = 1 #  Prescription
draCI['ReaDuPain'][327] = 1 #  To cope with chronic pain 
draCI['ReaDuOther'][338] = 1 #  Im lost
draCI['ReaDuOther'][366] = 1 #  To try and use it to impose a sense of weekend or even my now long overdue holiday 
draCI['ReaDuPain'][372] = 1 #  Pain management
draCI['ReaDuEscapeReality'][379] = 1 #  Mostly to escape reality 
draCI['ReaDuCope'][16] = 1 # 434 unsafe living conditions ongoing harassment
draCI['ReaDuManageMentalHealth'][438] = 1 #  Junkie
draCI['ReaDuRelaxNightOut'][449] = 1 #  Sleep aid
draCI['ReaDuSpiritual'][458] = 1 #  To learn more about myself
draCI['ReaDuOther'][474] = 1 #  Been nice weather
draCI['ReaDuOther'][491] = 1 #  To cope with people who become unhinged talking about LSD
draCI['ReaDuOther'][504] = 1 #  To try something new
draCI['ReaDuManageMentalHealth'][510] = 1 #  Slow suicide by 4-5 grams of heroin weekly
draCI['ReaDuManageMentalHealth'][534] = 1 #  Addiction
draCI['ReaDuSpiritual'][549] = 1 #  Spiritual openness and entunement
draCI['ReaDuIncreaCreativity'][639] = 1 #  To produce electronic music
draCI['ReaDuPain'][683] = 1 #  Pain
draCI['ReaDuMed'][700] = 1 #  I have a prescription for adderall 
draCI['ReaDuPain'][728] = 1 #  To cope with chronic pain
draCI['ReaDuSpiritual'][768] = 1 #  DMT induced Spiritual Awakening
draCI['ReaDuSpiritual'][777] = 1 #  Self exploration
draCI['ReaDuOther'][822] = 1 #  being an impulsive bitch
draCI['ReaDuPain'][824] = 1 # Back ache, essentially
draCI['ReaDuCope'][839] = 1 #  Cope with unrequited love
draCI['ReaDuRelaxNightOut'][844] = 1 #  Sleep
draCI['ReaDuSpiritual'][846] = 1 #  to connect deeper
draCI['ReaDuManageMentalHealth'][865] = 1 #  to cope with depression
draCI['ReaDuSpiritual'][873] = 1 #  To rethink my life and make myself proud of the things I am doing or I will do. 
draCI['ReaDuMed'][885] = 1 #  Daily medicine intake
draCI['ReaDuSpiritual'][886] = 1 #  for meditation, inner exploration
draCI['ReaDuRelaxNightOut'][929] = 1 #  To sleep
draCI['ReaDuSpiritual'][956] = 1 #  Clean the body
draCI['ReaDuPain'][1005] = 1 #  Pain
draCI['ReaDuPain'][1006] = 1 #  Pain management 
draCI['ReaDuCope'][1021] = 1 #  To help get through this shit and life in general
draCI['ReaDuOther'][1052] = 1 #  To submit to social pressure. Most of my friends had time-off and started consuming drugs out of boredom, I submitted to this practice once in the very beginning of the outbreak.
draCI['ReaDuSpiritual'][1127] = 1 #  Not cope with stress but to feel into emotions more 
draCI['ReaDuSpiritual'][1139] = 1 #  To gain new insights about my life, behavioral patterns and universe in general. Psychedelics is may way to deeper understanding. 
draCI['ReaDuCope'][1160] = 1 #  To help process what's happening, to bond with friends 
draCI['ReaDuOther'][1204] = 1 #  I knew I had ketamine at home and it felt easier to get high than to walk out to the shops for alcohol since we're supposed to be social distancing etc
draCI['ReaDuPain'][1209] = 1 #  Pain relief 
draCI['ReaDuOther'][1222] = 1 #  (microdosing LSD - not full dosing weekly)
draCI['ReaDuRelaxNightOut'][1226] = 1 #  To lift mood. To connect with my emotions. To feel and act on impulse. To be the loving person I become after the fact of behaving in a lovely way on a holiday from the self I left behind so that in the future I have fond memories of this time. To enhance the now ever so slightly so as to be positive, fearless and imaginative.
draCI['ReaDuSpiritual'][1236] = 1 #  personal growth & development
draCI['ReaDuIncreaCreativity'][1273] = 1 # Coke gives me some energy, weed helps me playing guitar
draCI['ReaDuWorkStudy'][1273] = 1 #  Coke gives me some energy, weed helps me playing guitar
draCI['ReaDuMed'][1280] = 1 #  Detox 
draCI['ReaDuPain'][1300] = 1 #  Autism, chronic pain, OSA, sensory overload issues
draCI['ReaDuManageMentalHealth'][1300] = 1 #  Autism, chronic pain, OSA, sensory overload issues
draCI['ReaDuPain'][1407] = 1 #  Informal pain management 
draCI['ReaDuRelaxNightOut'][1429] = 1 #  General self betterment and seeking happiness and wisdom
draCI['ReaDuPain'][1455] = 1 #  To manage chronic pain
draCI['ReaDuWorkStudy'][1469] = 1 #  To stay focused 
draCI['ReaDuSpiritual'][1486] = 1 #  Explore the fabric of “reality”
draCI['ReaDuSpiritual'][1492] = 1 #  To better appreciate nature 
draCI['ReaDuOther'][1518] = 1 #  New experience
draCI['ReaDuManageMentalHealth'][1560] = 1 #  paranoia
draCI['ReaDuManageMentalHealth'][1580] = 1 #  was a GHB addict and stay off of GABAergics and haen't figured out how too sooth my nerves without any drug yet, what I'm prescribed is not enough
draCI['ReaDuManageMentalHealth'][1625] = 1 #  to cope with addiction 
draCI['ReaDuOther'][1694] = 1 #  Honestly.. It's just something to do
draCI['ReaDuOther'][1721] = 1 #  Can’t usually eat edibles when I have work the next day but now I have the time and opportunity 
draCI['ReaDuPain'][1731] = 1 #  Chronic pain
draCI['ReaDuPain'][1735] = 1 #  Pain
draCI['ReaDuRelaxNightOut'][1755] = 1 #  To stay well 
draCI['ReaDuCope'][1760] = 1 #  So I wouldn't constantly sleep
draCI['ReaDuManageMentalHealth'][1791] = 1 #  I smoke weed when the bad voices become overwhelming 
draCI['ReaDuOther'][1866] = 1 #  On the last day of normal life when the lockdown was announced had a smoke sesh
draCI['ReaDuSpiritual'][1869] = 1 #  Personal development
draCI['ReaDuSpiritual'][1918] = 1 #  experimentation, exploration & entertainment
draCI['ReaDuMed'][1946] = 1 #  Medical Reasons
draCI['ReaDuPain'][2076] = 1 #  Cope with physical Pain
draCI['ReaDuOther'][2078] = 1 # Skype with friend
draCI['ReaDuOther'][2177] = 1 #  I finally had the time to
draCI['ReaDuPain'][2203] = 1 #  Helps ease my fibromyalgia
draCI['ReaDuOther'][2218] = 1 #  It's just my daily routine
draCI['ReaDuOther'][2248] = 1 #  why the fuck not.
draCI['ReaDuMed'][2265] = 1 #  also helps my chronic illness
draCI['ReaDuOther'][2423] = 1 #  To carry on
draCI['ReaDuOther'][1400] = 1 #  Home with parents so can’t 
draCI['ReaDuOther'][2425] = 1 #  Since outbreak taken nothing
draCI['ReaDuOther'][2458] = 1 #  I’ve not been able to get any


# %% Amend reasons to self-medicate
ind_col_whySelfMed = np.where(col_names == 'WhySelfMed')
cols_why_SelfMed = col_names[ind_col_whySelfMed[0][0]:(ind_col_whySelfMed[0][0]+15)]

draCI.rename(columns={'WhySelfMed':       'ReaSelfMedSleep',          
                      'Unnamed: 199':     'ReaSelfMedMood', 
                      'Unnamed: 200':     'ReaSelfMedAnx',    
                      'Unnamed: 201':     'ReaSelfMedConc',    
                      'Unnamed: 202':     'ReaSelfMedMenHea',   
                      'Unnamed: 203':     'ReaSelfMedEatDis',   
                      'Unnamed: 204':     'ReaSelfMedPho',   
                      'Unnamed: 205':     'ReaSelfMedAntiPer',   
                      'Unnamed: 206':     'ReaSelfMedOCD',   
                      'Unnamed: 207':     'ReaSelfMedPTSD',   
                      'Unnamed: 208':     'ReaSelfMedBiDis',   
                      'Unnamed: 209':     'ReaSelfMedPain',   
                      'Unnamed: 210':     'ReaSelfMedQuitOtherDrugs',
                      'Unnamed: 211':     'ReaSelfMedPresDrugs',   
                      'Unnamed: 212':     'ReaSelfMedOther'    
                    },  
          inplace=True, errors='raise')

names = ['To sleep', 'To heighten mood/ alleviate symptoms of depression', 'To reduce anxiety', 'To improve concentration',
          'To manage other mental health issues', 'Eating disorder', 'Phobias', 'Antisocial personality',
          'Obsessive compulsive disorder', 'Post-traumatic stress disorder', 'Bipolar disorder', 'To relieve pain', 
          'To quit other drugs', 'Replace inaccessible prescribed drugs']

cols = ['ReaSelfMedSleep', 'ReaSelfMedMood', 'ReaSelfMedAnx', 'ReaSelfMedConc', 
        'ReaSelfMedMenHea', 'ReaSelfMedEatDis', 'ReaSelfMedPho', 'ReaSelfMedAntiPer', 
        'ReaSelfMedOCD', 'ReaSelfMedPTSD', 'ReaSelfMedBiDis', 'ReaSelfMedPain', 
        'ReaSelfMedQuitOtherDrugs', 'ReaSelfMedPresDrugs', 'ReaSelfMedOther']
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

boReaSelfMedOther = draCI['ReaSelfMedOther'].isnull()
indxRealSelfMedOther = draCI['ReaSelfMedOther'][~boReaSelfMedOther].index

draCI['ReaSelfMedOthers'] = 0

draCI['ReaSelfMedMenHea'][89] = 1 # Adhd
draCI['ReaSelfMedOthers'][156] = 1 #     Multiple Sclerosis management
draCI['ReaSelfMedMenHea'][204] = 1 #     Probably undiagnosed ADHD
draCI['ReaSelfMedOthers'][245] = 1 #     Chronic illness
draCI['ReaSelfMedQuitOtherDrugs'][286] = 1 #     To reduce cravings  
draCI['ReaSelfMedQuitOtherDrugs'][297] = 1 #     Haven’t used benzos after consuming a lot before quarantine. I’ve compensated a bit more than usual with alcohol.
draCI['ReaSelfMedPresDrugs'][329] = 1 #     I started the modafinil to help me get through until my Adderall connection gets his refill.
draCI['ReaSelfMedOthers'][345] = 1 #     relief from gender dysphoria
draCI['ReaSelfMedOthers'][378] = 1 #     To live in a different world for a while 
draCI['ReaSelfMedOthers'][379] = 1 #     To feel normal to an extent 
draCI['ReaSelfMedConc'][434] = 1 #     can deal w/problems singly not overwelmed keep focus 
draCI['ReaSelfMedPain'][491] = 1 #     Something in Cannabis prevents me suffering the agony of regular 'night cramps' in my legs :-)
# IGNORED 540    im bored as fuckall.
draCI['ReaSelfMedMenHea'][549] = 1 #     Make meaning of current trauma occurring in our world at this time
draCI['ReaSelfMedMenHea'][728] = 1 #     Trying to numb my feelings which I have no control on 
#IGNORED 730    fun
draCI['ReaSelfMedOthers'][780] = 1 #     Complete and utter boredom and to relieve stress of isolation
draCI['ReaSelfMedMenHea'][874] = 1 #     technically I have BPD/EUPD, not PTSD. similar though!
#IGNORE 885    Marijuana is medicine.
draCI['ReaSelfMedMenHea'][898] = 1 #     manage BPD
draCI['ReaSelfMedMenHea'][959] = 1 #     Schizophrenia
draCI['ReaSelfMedMenHea'][1034] = 1 #    Epilepsy
draCI['ReaSelfMedMenHea'][1044] = 1 #    Borderline Personality Disorder
#IGNORE 1208   Boredom
draCI['ReaSelfMedMenHea'][1217] = 1 #    To avoid urges to self harm
draCI['ReaSelfMedMenHea'][1300] = 1 #    Autism, chronic pain, OSA, sensory overload issues
draCI['ReaSelfMedMenHea'][1337] = 1 #    Weed/hash for ADHD
draCI['ReaSelfMedPain'][1387] = 1 #    Relieve migraine pain
#IGNORE 1444   Boredom 
#IGNORE 1477   playing music with friends
draCI['ReaSelfMedMenHea'][1548] = 1 #    suffer from bpd stuck home with my family/ ket addict with no money for daily use 
#IGNORE 1712   I'm so goddamn bored
draCI['ReaSelfMedOthers'][1760] = 1 #    Frequent nightmares
draCI['ReaSelfMedMenHea'][1842] = 1 #    ADD
draCI['ReaSelfMedMenHea'][1886] = 1 #    Autism related social issues
draCI['ReaSelfMedMenHea'][1898] = 1 #    To avoid self-harm
draCI['ReaSelfMedQuitOtherDrugs'][1907] = 1 #    Stop withdrawal
draCI['ReaSelfMedConc'][1918] = 1 #  to be present in the moment and focus on whats in front of me rather than worrying about the outbreak
draCI['ReaSelfMedMenHea'][1922] = 1 #    Schizophrenia
#IGNORE 1947   Boredom
draCI['ReaSelfMedMood'][1966] = 1 #    Depression
draCI['ReaSelfMedMenHea'][1969] = 1 #    borderline personality disorder
#IGNORE 1980   to alleviate boredom
#IGNORE 2064   All and none of the above
#IGNORE 2200   Everything just gets better
draCI['ReaSelfMedOthers'][2265] = 1 #    helps my ulcerative colitis
#IGNORE 2345   Balance
draCI['ReaSelfMedAnx'][2370] = 1 #    Existential anxiety

# del draCI['ReaSelfMedOther']


# %% Amend How is drug taking affecting working-studying working
ind_col_HWhabits = np.where(col_names == 'HomeWorkHabits')
cols_hw_habits = col_names[ind_col_HWhabits[0][0]:(ind_col_HWhabits[0][0]+2)]

n_whNEW = ['HWhNo', 'HWhProduc', 'HWhConc', 'HWhWorkDone', 'HWhNoUse']
n_whOLD = ['Not affecting at all', 'It’s helping me to stay productive', "It’s deteriorating my concentration", "It’s stopping me to get any work done", "I don't take recreational drugs"]

expandCode(n_whOLD, n_whNEW, 'HomeWorkHabits')

draCI.rename(columns={'Unnamed: 328': 'HWhOther',   
                    },  
          inplace=True, errors='raise')

boHWhOther = draCI['HWhOther'].isnull()
indxHWhOther = draCI['HWhOther'][~boHWhOther].index

draCI['HWhOther'] = 0
draCI['HWhNegEff'] = 0
draCI['HWhPosEff'] = 0

draCI['HWhNoUse'][24] = 1 #    Not using recreational drugs during lockdown
draCI['HWhProduc'][27] = 1 #    Increasing concentration (Adderall)
draCI['HWhNegEff'][29] = 1 #  sometimes it distracts me / makes me lazy, other times it puts me 'in the zone'.  I like to think it balances out to broadly neutral
draCI['HWhOther'][58] = 1 #    For all I know , it's only lifting up my mood 
#IGNORE 68   Not currently working/studying.
draCI['HWhNegEff'][71] = 1 #    Sometimes struggle to stick to study structure as recreational use gets in the way or sets me back
draCI['HWhNoUse'][73] = 1 #    I haven’t taken any since lockdown
draCI['HWhOther'][78] = 1 #    I feel like a pretty distracted person usually so I feel indifferent 
draCI['HWhNegEff'][92] = 1 #    Sometimes I sleep when I shouldnt (during work hours), but I only smoke during the day when I am unbearably depressed
draCI['HWhOther'][123] = 1 #   Just take longer than usual but everything gets done 
draCI['HWhOther'][127] = 1 #   ritalin = helps because i think i have adhd weed = helps because it helps me relax. but i'm still unproductive because pandemic stress is a lot
draCI['HWhNoUse'][129] = 1 #   I’ve not been able to take any 
draCI['HWhNegEff'][205] = 1 #   they increase creativity but feed off my energy
draCI['HWhOther'][205] = 1 #   they increase creativity but feed off my energy
#IGNORE 223  I miss it lol
#IGNORE 236  not sure 
draCI['HWhOther'][291] = 1 # Keeps me busy on my downtime
draCI['HWhNegEff'][297] = 1 # Hasn’t effected me besides the fact that I wake up hungover sometimes. In that case I usually start work an hour or two late and work late to compensate 
#IGNORE 312  I don't take drugs when on duty
draCI['HWhNoUse'][341] = 1 #  Not taken during isolation
draCI['HWhNegEff'][406] = 1 # More productive at times, but also lacking concentration a times
draCI['HWhProduc'][406] = 1 # More productive at times, but also lacking concentration a times
draCI['HWhNo'][419] = 1 #   Neither helping nor hindering
draCI['HWhNegEff'][428] = 1 #   Harder to focus when stoned but more motivated
draCI['HWhProduc'][428] = 1 #   Harder to focus when stoned but more motivated
draCI['HWhNegEff'][436] = 1 # Slight lack of motivation 
draCI['HWhOther'][443] = 1 #   I’m still attending all my scheduled lectures and seminars online, but I am not doing as much work as I possibly should be. Whether that’s directly related to drug use, or is due to everything els...
draCI['HWhNegEff'][447] = 1 #   sometimes it helps me to relax, others it doesn't. It's hit and miss, so sometimes it really helps me concentrate and others it makes me tired/sleepy.
draCI['HWhProduc'][447] = 1 #   sometimes it helps me to relax, others it doesn't. It's hit and miss, so sometimes it really helps me concentrate and others it makes me tired/sleepy.
draCI['HWhPosEff'][501] = 1 #   it is helping me to relax
draCI['HWhNegEff'][510] = 1 #   I lock myself in my room and get so high I feel my heart begin to fail every night
draCI['HWhNegEff'][556] = 1 #  Depend on drug. Some force me to take a slower day the day after, others can be used to be more productive
draCI['HWhProduc'][556] = 1 #  Depend on drug. Some force me to take a slower day the day after, others can be used to be more productive
#IGNORE 590  If we count my gaming stream watching habit as "drugs", then it's definitely affecting me negatively.
draCI['HWhPosEff'][592] = 1 #   It helps me unwind
draCI['HWhNoUse'][631] = 1 #   Not having drugs
draCI['HWhNegEff'][634] = 1 #   Affecting my ability to sleep on weekends when I should be resting from long work week
draCI['HWhNegEff'][639] = 1 #   Sometimes tired after weekend
draCI['HWhNoUse'][704] = 1 #   Not taking drugs
draCI['HWhNoUse'][705] = 1 #   I'm not using any kind of drugs
draCI['HWhPosEff'][727] = 1 #   It brings some change in the daily routine
draCI['HWhNoUse'][729] = 1 #   Not takin drugs
draCI['HWhNoUse'][732] = 1 #   I don't take drugs
#IGNORE 759  I don’t work or study from home but I get chores done normal 
draCI['HWhPosEff'][768] = 1 #   It keeps the boredom away, and helps me have a positive outlook
#IGNORE 782  i am not required to work or study
draCI['HWhPosEff'][789] = 1 #   Helping me cope
draCI['HWhNoUse'][838] = 1 #   I'm not taking any drugs at the moment in the outbreak so this isn't applicable
draCI['HWhNegEff'][855] = 1 #   its shifting my sleep schedule 
draCI['HWhPosEff'][873] = 1 #   Well if we talking about magic mushrooms definitely it`s about the more perosnal experience so it`s about the time which you spend for you not for someone else :)  
draCI['HWhPosEff'][924] = 1 #   Improves, if used correctly 
#IGNORE 957  Not sure
draCI['HWhPosEff'][958] = 1 # I increased my self-development (mentally and physically) but decreased my studying habits
draCI['HWhNegEff'][958] = 1 # I increased my self-development (mentally and physically) but decreased my studying habits
draCI['HWhNegEff'][987] = 1 #   it is more difficult to work after weekends if i take some drugs
draCI['HWhPosEff'][1022] = 1 #  helps me release stress every now and then
draCI['HWhPosEff'][1061] = 1 #  I am choosing to only smoke on the weekends to unwind from the week
draCI['HWhOther'][1112] = 1 # It depends on the amount taken.
draCI['HWhNoUse'][1140] = 1 #  I don’t use any drugs now during quarantine
draCI['HWhPosEff'][1061] = 1 #  Parts from normal life continuing during the quarantine helps me get through it
draCI['HWhNoUse'][1152] = 1 #  Not a drug user 
draCI['HWhNegEff'][1168] = 1 #  It has made me a little complacent in my job at times
draCI['HWhPosEff'][1200] = 1 #  it's help me relax
draCI['HWhPosEff'][1234] = 1 #  It’s helping to stay less anxious 
draCI['HWhPosEff'][1236] = 1 #  periods of intense productivity followed by rest, sometimes more balanced in productivity
#IGNORE 1247 I don’t drink when i work
#IGNORE 1252 I'm not sure
draCI['HWhNoUse'][1276] = 1 #  I’m not taking drugs 
draCI['HWhPosEff'][1287] = 1 #  Relieves anxiety 
draCI['HWhNoUse'][1385] = 1 #  I am not taking recreational drugs
draCI['HWhNoUse'][1501] = 1 #  Not taking any at the moment
draCI['HWhNegEff'][1518] = 1 #  Barely have an appetite 
draCI['HWhOther'][1548] = 1 #  the problem is i dont have all the ket and weed i want to stay home and feel ok but i drink my mind off daily haha
draCI['HWhNegEff'][1550] = 1 #  Deteriorated my mental health 
draCI['HWhNegEff'][1567] = 1 #  some days i end up doing no work because i’m high, but mostly i’ll do my work then smoke
#IGNORE 1575 I’m just chilling all day 
draCI['HWhNegEff'][1621] = 1 #  Decreasing productivity and motivation
draCI['HWhNegEff'][1698] = 1 #  It might affect me on a certain day but not all the time
draCI['HWhNegEff'][1764] = 1 #  i don't have access to any drugs and am going through withdrawl
draCI['HWhNegEff'][1791] = 1 #  It’s affecting me as an athlete 
#IGNORE 1795 Don’t have any work 
draCI['HWhNegEff'][1839] = 1 #  worse memory recall
draCI['HWhPosEff'][1880] = 1 #  Sativa helps me concentrate; I think I have undiagnosed ADHD
#IGNORE (fair point) 1896 Unclear.  All work habits have changed, lifestyles has changed.  We've gone from seflemployed with teens in school to no work and teens at home growing a garden and raising chickens.  Grateful we ...
draCI['HWhNegEff'][1909] = 1 #  I prioritize work less
draCI['HWhNegEff'][1918] = 1 #  sometimes helps and sometimes hinders
draCI['HWhPosEff'][1918] = 1
draCI['HWhOther'][1927] = 1 #  Makes me stay up late and get up late
#IGNORE CANT KNOW ORDER COS THEY WERE RANDOMISED 1991 It is a mix of 2) 3) and 4)
draCI['HWhNegEff'][1993] = 1 #  Ruins my sleep and relationships
draCI['HWhPosEff'][1995] = 1 #  Its keeping me sane and helping to deal with extreme anxiety
draCI['HWhNegEff'][2041] = 1 #  I've made an effort to stop smoking weed during the outbreak. I'm definitely not doing well in school, but I don't think that's because of the drugs. More so, the outbreak destroying my daily rout...
#IGNORE 2064 None of above-don’t know
draCI['HWhNegEff'][2066] = 1 #  Makes me tired 
draCI['HWhPosEff'][2090] = 1 #  i try to only use drugs when i know i have already handled my responsibilities. sometimes they can be motivating factors
draCI['HWhNo'][2100] = 1 #  I am a key worker and do not work from home. My drug use is not effecting my work
#IGNORE 2117 I don't study because my classes have stoped
draCI['HWhNoUse'][2136] = 1 #  I dont have any
draCI['HWhNoUse'][2143] = 1 #  I'm not smoking weed, but it usually helps me to study
draCI['HWhPosEff'][2225] = 1 #  It’s keeping me sane and calm 
draCI['HWhPosEff'][2235] = 1 #  Helps me think outside the box
draCI['HWhNegEff'][2272] = 1 #  It only impacts in the days following use (1-3 days after) and I feel unmotivated
#IGNORE 2307 not sure
#IGNORE 2370 I haven't done any study but not because of drugs, because I'm a serial procrastinator without the correct environment to so work in
#IGNORE 2374 I haven't been taking as much 
draCI['HWhNoUse'][2391] = 1 #  I do not take drugs 
draCI['HWhNoUse'][2399] = 1 #  I dont take drugs anymore
draCI['HWhNoUse'][2426] = 1 #  Have no taken anything during outbreak
#IGNORE 2456 Not sure

# # %% Amend amount of alc in each session  # problem with +10 Can't convert to int cos of it, so leaving them as strings for now
ind_col_AmountSeshAlc = np.where(col_names == 'AmountSeshAlcohol')
cols_AmountSeshAlc = col_names[ind_col_AmountSeshAlc[0][0]:(ind_col_AmountSeshAlc[0][0] + 8)]

draCI.rename(columns={'AmountSeshAlcohol': 'Beer568',
                      'Unnamed: 48':       'Beer330',
                      'Unnamed: 49':       'Cider568',
                      'Unnamed: 50':       'Wine175',
                      'Unnamed: 51':       'Prosecco125',
                      'Unnamed: 52':       'Spirits25',
                      'Unnamed: 53':       'Alcopops275',
                      'Unnamed: 54':       'Cocktail330'  
                    },  
          inplace=True, errors='raise')

units =  ['Beer568', 'Beer330', 'Cider568', 'Wine175', 
            'Prosecco125', 'Spirits25', 'Alcopops275', 'Cocktail330']


# %% Amend drugs used during outbreak
ind_col_Drug = np.where(col_names == 'TypeDrugUse')
cols_Drug = col_names[ind_col_Drug[0][0]:(ind_col_Drug[0][0] + 21)]

draCI.rename(columns={'TypeDrugUse':      'DrugsUse2C_X',          
                      'Unnamed: 99':      'DrugsUseAdderall', 
                      'Unnamed: 100':     'DrugsUseAmphe',    
                      'Unnamed: 101':     'DrugsUseBenzos',    
                      'Unnamed: 102':     'DrugsUseCannabis',   
                      'Unnamed: 103':     'DrugsUseCoke',   
                      'Unnamed: 104':     'DrugsUseMeth',   
                      'Unnamed: 105':     'DrugsUseDMT',   
                      'Unnamed: 106':     'DrugsUseDXM',   
                      'Unnamed: 107':     'DrugsUseIbo',   
                      'Unnamed: 108':     'DrugsUseKet',   
                      'Unnamed: 109':     'DrugsUseLSD',   
                      'Unnamed: 110':     'DrugsUseShrooms',
                      'Unnamed: 111':     'DrugsUseMAOIs',   
                      'Unnamed: 112':     'DrugsUseMDMA',
                      'Unnamed: 113':     'DrugsUseModafinil',
                      'Unnamed: 114':     'DrugsUseNO',
                      'Unnamed: 115':     'DrugsUseOpioids',
                      'Unnamed: 116':     'DrugsUseSSRIs',
                      'Unnamed: 117':     'DrugsUsePoppers',
                      'Unnamed: 118':     'DrugsUseOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Amphetamine (aka\xa0‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis\xa0(aka weed/marijuana/hash/skunk/grass)', 'Cocaine (aka “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (i.e. Ayahuasca, Changa,\xa05-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (aka ‘K’, ‘Ket’, ‘Special K’)', 'LSD (aka “Acid”)', 'Magic Mushrooms (or other forms of Psilocybin,\xa0e.g. 4-AcO-DMT)',
          'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'MDMA (aka “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 
          'Nitrous Oxide (aka ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (aka antidepressants)', 'Poppers']

cols = ['DrugsUse2C_X', 'DrugsUseAdderall', 'DrugsUseAmphe', 'DrugsUseBenzos',
        'DrugsUseCannabis', 'DrugsUseCoke', 'DrugsUseMeth', 'DrugsUseDMT',
        'DrugsUseDXM', 'DrugsUseIbo', 'DrugsUseKet', 'DrugsUseLSD', 'DrugsUseShrooms',
        'DrugsUseMAOIs','DrugsUseMDMA', 'DrugsUseModafinil', 'DrugsUseNO',
        'DrugsUseOpioids', 'DrugsUseSSRIs', 'DrugsUsePoppers']
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

draCI['DrugsUseOthers'] = 0
draCI['DrugsUseGHBL'] = 0
draCI['DrugsUsePhenibut'] = 0

boUseOthers = draCI['DrugsUseOthers'].isnull()
indxUseOthers = draCI['DrugsUseOthers'][~boUseOthers].index


draCI['DrugsUseOpioids'][63] = 1 #  Codiene
draCI['DrugsUseOthers'][77] = 1 #  Salvia 
draCI['DrugsUseOthers'][94] = 1 #  DPH
draCI['DrugsUseOthers'][133] = 1 #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['DrugsUseOpioids'][133] = 1 #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['DrugsUseOthers'][141] = 1 #   3-meo-pce, dck, 2f-dck, 4-aco-met
draCI['DrugsUseOpioids'][203] = 1 #   kratom
draCI['DrugsUseOthers'][211] = 1 #   blue lotus
draCI['DrugsUseCannabis'][214] = 1 #  THC vape liquid
draCI['DrugsUseGHBL'][224] = 1 #   Magic Mushrooms, GHB
draCI['DrugsUseShrooms'][224] = 1 #   Magic Mushrooms, GHB
draCI['DrugsUseOpioids'][228] = 1 #   Kratom n sleeping pills (seroquel)
draCI['DrugsUseOthers'][228] = 1 #   Kratom n sleeping pills (seroquel)
draCI['DrugsUseOthers'][236] = 1 #   kanna
draCI['DrugsUseGHBL'][238] = 1 #   Ghb
draCI['DrugsUseOthers'][251] = 1 #   Sceletium
draCI['DrugsUseOpioids'][275] = 1 #   Kratom, phenibut, kava
draCI['DrugsUseOpioids'][280] = 1 #  Kratom
draCI['DrugsUseOthers'][281] = 1 #   Testosterone 
draCI['DrugsUseOpioids'][283] = 1 #  kanna, kava kava, kratom, sida cordifolia
draCI['DrugsUseOthers'][289] = 1 #   gabapentin
draCI['DrugsUseOthers'][293] = 1 #   Salvia
draCI['DrugsUseOthers'][298] = 1 #   Doxylamine
draCI['DrugsUseOpioids'][304] = 1 #   Kratom
draCI['DrugsUseOpioids'][317] = 1 #   Kratom
draCI['DrugsUseDXM'][320] = 1  #   Dexamphetamine
draCI['DrugsUseOthers'][338] = 1 #   ETH-LAD, MD-PHP, A-PHP, A-PiHP, A-PCyP, 5-Bromo-DMT (yes, you read that correctly. Fucking sea sponges!) 
draCI['DrugsUseOthers'][345] = 1 # mescaline
draCI['DrugsUseOpioids'][351] = 1 #   Kratom, phenibut
draCI['DrugsUsePhenibut'][351] = 1  #  Kratom, phenibut
draCI['DrugsUseOthers'][353] = 1 #  Synthetic stimulants ( amph and Cath)
draCI['DrugsUseOthers'][359] = 1 #  ambien
draCI['DrugsUsePhenibut'][368] = 1 #   Phenibut
draCI['DrugsUseOpioids'][370] = 1 #   kratom
draCI['DrugsUseOthers'][379] = 1 #   Gabapentin and adderall(prescribed)
draCI['DrugsUseOthers'][397] = 1 #   4f-mph
draCI['DrugsUseOthers'][401] = 1 #   2-FMA, 3-MMC, mianserin 
draCI['DrugsUseOpioids'][411] = 1 #   Kratom 
draCI['DrugsUseOpioids'][450] = 1 #   Tramadol
draCI['DrugsUseOthers'][458] = 1 #   pregabalin
draCI['DrugsUseOthers'][484] = 1 #   Dimenhydrinate and caffein
draCI['DrugsUseOthers'][500] = 1 #   Crack cocaine
draCI['DrugsUseGHBL'][540] = 1 #   Gamma Hydroxybutyrate
draCI['DrugsUseOpioids'][546] = 1 #   Kratom
draCI['DrugsUseOthers'][547] = 1 #   NEP
draCI['DrugsUseGHBL'][556] = 1 #   GHB
draCI['DrugsUseOthers'][637] = 1 #   3-MMC
draCI['DrugsUseLSD'][647] = 1 #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['DrugsUseKet'][647] = 1 #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['DrugsUseOthers'][697] = 1 #   Salvia, mescaline
draCI['DrugsUsePhenibut'][713] = 1 #   Phenibut
draCI['DrugsUseOthers'][728] = 1 #   Gabapentinoids
draCI['DrugsUsePhenibut'][730] = 1 #   Phenibut
draCI['DrugsUseOthers'][771] = 1 #   Buprenorphine
draCI['DrugsUseOpioids'][777] = 1 #   Kratom
draCI['DrugsUseOpioids'][778] = 1 #   Kratom Daily 2x11.5g
draCI['DrugsUseOthers'][780] = 1 #   3-MMC, N-Ethylhexedrone
draCI['DrugsUseOthers'][798] = 1 #   Salvia divinorum 
draCI['DrugsUseGHBL'][818] = 1 #   gbl 
draCI['DrugsUseOthers'][822] = 1 #   nutmeg
draCI['DrugsUseOthers'][836] = 1 #   wild dagga
draCI['DrugsUse2C_X'][861] = 1 #   2C-B (nexus)
draCI['DrugsUseOthers'][874] = 1 #   prescribed depression meds
draCI['DrugsUseOthers'][929] = 1 #   Quetiapine
draCI['DrugsUseOthers'][956] = 1 #   Ayahuasca, San Pedro, Coca Leaves
draCI['DrugsUseCoke'][956] = 1 #   Ayahuasca, San Pedro, Coca Leaves
draCI['DrugsUseOthers'][18111232] = 1 #  Nutmeg
draCI['DrugsUsePhenibut'][1135] = 1 #  Phenibut
draCI['DrugsUseOthers'][1214] = 1 #  3-meo-pcp
draCI['DrugsUseOpioids'][1237] = 1 #  Kratom
draCI['DrugsUseGHBL'][1278] = 1 #  Ghb
draCI['DrugsUseOthers'][1299] = 1 #  tetrahydroharmine, kanna, blue lotus, 
draCI['DrugsUseCannabis'][1300] = 1 #  CBD
draCI['DrugsUseGHBL'][1321] = 1 #  GHB
draCI['DrugsUseGHBL'][1347] = 1 #  Ghb
draCI['DrugsUseOthers'][1358] = 1 #  3MMC
draCI['DrugsUseBenzos'][1387] = 1 #  1.5x doses of Xanax to achieve altered state
draCI['DrugsUseGHBL'][1415] = 1 #  G
draCI['DrugsUseOthers'][1444] = 1 #  Cyclobenzaprine (muscle relaxers)
draCI['DrugsUseOthers'][1458] = 1 #  pregabalin
draCI['DrugsUseOthers'][1459] = 1 #  Mescaline
draCI['DrugsUseOpioids'][1463] = 1 #  Kratom
draCI['DrugsUsePhenibut'][1471] = 1 #  Phenibut
draCI['DrugsUseOpioids'][1472] = 1 #  kratom
draCI['DrugsUseSSRIs'][1494] = 1  #  (currently on SSRIs)
draCI['DrugsUseOthers'][1500] = 1 #  SNRI
draCI['DrugsUseOthers'][1502] = 1 #  3-MMC, 4-CMC
draCI['DrugsUseOthers'][1512] = 1 #  salvia, GBL
draCI['DrugsUseGHBL'][1512] = 1 #  salvia, GBL
draCI['DrugsUseBenzos'][1546] = 1 #  xanax
draCI['DrugsUseOthers'][1581] = 1 #  4f-MPH
draCI['DrugsUseOpioids'][1585] = 1 # Cyclobenzaprine, kratom
draCI['DrugsUseOthers'][1585] = 1 #  Cyclobenzaprine, kratom
draCI['DrugsUseOthers'][1594] = 1 #  Lyrica (pregabalin), Bronkaid (ephedrine), tons of energy drinks
draCI['DrugsUseOthers'][1596] = 1 #  LSA
draCI['DrugsUseOpioids'][1612] = 1 #  Kratom
draCI['DrugsUseGHBL'][1613] = 1 #  GHB
draCI['DrugsUseOthers'][1615] = 1 #  DPH
draCI['DrugsUseOthers'][1617] = 1 #  Kanna
draCI['DrugsUseOthers'][1633] = 1 #  SOMA, GHB
draCI['DrugsUseGHBL'][1633] = 1 #  SOMA, GHB
draCI['DrugsUseOpioids'][1638] = 1 #  Kratom
draCI['DrugsUseOpioids'][1655] = 1 #  Kratom
draCI['DrugsUseOthers'][1692] = 1 #  Dph
draCI['DrugsUseGHBL'][1699] = 1 #  Ghb
draCI['DrugsUseOthers'][1710] = 1 #  Nutmeg
draCI['DrugsUseOthers'][1712] = 1 #  Miscellaneous inhalants
draCI['DrugsUseCannabis'][1722] = 1 #  cbd
draCI['DrugsUseOthers'][1729] = 1 #  Pregabalin
draCI['DrugsUseOpioids'][1731] = 1 #  Kratom 
draCI['DrugsUseOthers'][1735] = 1 #  Gabapentin 
draCI['DrugsUseOthers'][1744] = 1 #  25I-NBOMe
draCI['DrugsUseOthers'][1755] = 1 #  Pregabalin
draCI['DrugsUseOpioids'][1776] = 1 #  Codiene
draCI['DrugsUseOthers'][1809] = 1 #  Why is my boy O-PCE not here😤
draCI['DrugsUseCannabis'][1822] = 1 #  Weed
draCI['DrugsUseOpioids'][1832] = 1 #  Kratom, deschloroketamine, 4F-MPH 
draCI['DrugsUseOthers'][1832] = 1 #  Kratom, deschloroketamine, 4F-MPH 
#IGNORE 1886 Others
draCI['DrugsUseOpioids'][1887] = 1 #  Kratom
draCI['DrugsUseOthers'][1890] = 1 #  LSA
draCI['DrugsUseOpioids'][1892] = 1 #  Kratom
draCI['DrugsUseOpioids'][1901] = 1 #  Hydrocodone 
draCI['DrugsUseGHBL'][1907] = 1 #  Gbl
draCI['DrugsUseGHBL'][1911] = 1 #  Ghb/GBL
draCI['DrugsUseOpioids'][1918] = 1 #  kratom
draCI['DrugsUseOthers'][1922] = 1 #  DPH
draCI['DrugsUseBenzos'][1923] = 1 #  Etizolam 
draCI['DrugsUseOthers'][1929] = 1 #  Belladonna 
draCI['DrugsUseOpioids'][1947] = 1 #  Kratom
draCI['DrugsUseOthers'][1949] = 1 #  4-fma
draCI['DrugsUseOthers'][1954] = 1 #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['DrugsUseGHBL'][1954] = 1 #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['DrugsUsePhenibut'][1954] = 1 #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['DrugsUseOpioids'][1954] = 1 #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['DrugsUseOthers'][1966] = 1 #  Quetiapine
draCI['DrugsUseCannabis'][1968] = 1 #  Weed
draCI['DrugsUseOpioids'][1995] = 1 #  Daily kratom use
draCI['DrugsUseOthers'][2016] = 1 #  Cathinones
draCI['DrugsUseOthers'][2025] = 1 #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['DrugsUsePhenibut'][2025] = 1 #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['DrugsUseOpioids'][2025] = 1 #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['DrugsUseOthers'][2045] = 1  #  Salvia divinorum
draCI['DrugsUseOthers'][2058] = 1 #  RCs
draCI['DrugsUseOthers'][2076] = 1 #  Caffeine
draCI['DrugsUseCannabis'][2170] = 1 #  Hash
draCI['DrugsUseOthers'][2248] = 1 #  Speed (base)
draCI['DrugsUseOthers'][2320] = 1 #  MXE, MPA
draCI['DrugsUseCannabis'][2378] = 1 #  THC oil vape 
draCI['DrugsUseOthers'][2383] = 1 #  drone
draCI['DrugsUseOthers'][2421] = 1 #  Promethazine

#IGNORE 346  So many drugs
#IGNORE 156  Cannabis should'nt really be on this list. 
#IGNORE 227  jhkh
#IGNORE 241  Was gonna try acid but they were duds
#IGNORE 329  By "opioids" I mean strictly kratom. I do not use any other drugs in that class.
#IGNORE 337  you should add xanax under benzodiazepines in case people are unsure what it is. altho every time i take xanax i am somewhat unsure of what it is #pressed🙏
#IGNORE 408  Private
#IGNORE 474  Alcohol
#IGNORE 515  With ex partner 
#IGNORE 638  Alcohol and nicotine
#IGNORE 1386 3
#IGNORE 824  No other, but I want to say that this comsumptions is not recreational, but for health. It's not precise to consider illegal drugs only as "recreational"
#IGNORE 1967 Probably going to do LSD again soon but I need to straighten out my prescription meds first
#IGNORE 2127 Alcohol
#IGNORE 2407 Alcohol
#IGNORE 2414 None
#IGNORE 2420 None
#IGNORE 2425 None
#IGNORE 2427 Alcohol
#IGNORE 2436 None
#IGNORE 2458 None since the outbreak started
#IGNORE 2468 none

# %% Amend Frequency of each drug during the outbreak 
ind_col_OftenDrug = np.where(col_names == 'OftenDrugUse')
cols_OftenDrug = col_names[ind_col_OftenDrug[0][0]:(ind_col_OftenDrug[0][0] + 21)]

draCI.rename(columns={'OftenDrugUse':     'OftenUse2C_X',          
                      'Unnamed: 120':     'OftenUseAdderall', 
                      'Unnamed: 121':     'OftenUseAmphe',    
                      'Unnamed: 122':     'OftenUseBenzos',    
                      'Unnamed: 123':     'OftenUseCannabis',   
                      'Unnamed: 124':     'OftenUseCoke',   
                      'Unnamed: 125':     'OftenUseMeth',   
                      'Unnamed: 126':     'OftenUseDMT',   
                      'Unnamed: 127':     'OftenUseDXM',   
                      'Unnamed: 128':     'OftenUseIbo',   
                      'Unnamed: 129':     'OftenUseKet',   
                      'Unnamed: 130':     'OftenUseLSD',   
                      'Unnamed: 131':     'OftenUseShrooms',
                      'Unnamed: 132':     'OftenUseMAOIs',   
                      'Unnamed: 133':     'OftenUseMDMA',
                      'Unnamed: 134':     'OftenUseModafinil',
                      'Unnamed: 135':     'OftenUseNO',
                      'Unnamed: 136':     'OftenUseOpioids',
                      'Unnamed: 137':     'OftenUseSSRIs',
                      'Unnamed: 138':     'OftenUsePoppers',
                      'Unnamed: 139':     'OftenUseOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Amphetamine (aka\xa0‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis\xa0(aka weed/marijuana/hash/skunk/grass)', 'Cocaine (aka “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (i.e. Ayahuasca, Changa,\xa05-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (aka ‘K’, ‘Ket’, ‘Special K’)', 'LSD (aka “Acid”)', 'Magic Mushrooms (or other forms of Psilocybin,\xa0e.g. 4-AcO-DMT)',
          'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'MDMA (aka “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 
          'Nitrous Oxide (aka ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (aka antidepressants)', 'Poppers']

cols = ['OftenUse2C_X', 'OftenUseAdderall', 'OftenUseAmphe', 'OftenUseBenzos',  
        'OftenUseCannabis', 'OftenUseCoke', 'OftenUseMeth', 'OftenUseDMT',   
        'OftenUseDXM', 'OftenUseIbo', 'OftenUseKet', 'OftenUseLSD',   
        'OftenUseShrooms', 'OftenUseMAOIs', 'OftenUseMDMA', 'OftenUseModafinil'
        'OftenUseNO', 'OftenUseOpioids', 'OftenUseSSRIs', 'OftenUsePoppers']
 
draCI['OftenUseOthers'] = 0
draCI['OftenUseGHBL'] = 0
draCI['OftenUsePhenibut'] = 0

boOftenDrugs = draCI['OftenUseOthers'].isnull()
indxOftenDrug = draCI['OftenUseOthers'][~boOftenDrugs].index

draCI['OftenUseOpioids'][63] = 'Once a week' #  Codiene
draCI['OftenUseOthers'][77] = 'Once a week' #  Salvia 
draCI['OftenUseOthers'][94] = 'Only once' #  DPH
draCI['OftenUseOthers'][133] = 'Every day' #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['OftenUseOpioids'][133] = 'Every day' #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['OftenUseOthers'][141] = 'Only twice' #   3-meo-pce, dck, 2f-dck, 4-aco-met
draCI['OftenUseOpioids'][203] = 'Every day' #   kratom
draCI['OftenUseOthers'][211] = 'Twice a week' #   blue lotus
draCI['OftenUseCannabis'][214] = 'Every day' #  THC vape liquid
draCI['OftenUseGHBL'][224] = 'Only once' #   Magic Mushrooms, GHB
draCI['OftenUseShrooms'][224] = 'Only once' #   Magic Mushrooms, GHB
draCI['OftenUseOpioids'][228] = 'Every other day' #   Kratom n sleeping pills (seroquel)
draCI['OftenUseOthers'][228] = 'Every other day' #   Kratom n sleeping pills (seroquel)
draCI['OftenUseOthers'][236] = 'Three times a week' #   kanna
draCI['OftenUseGHBL'][238] = 'Every day' #   Ghb
draCI['OftenUseOthers'][251] = 'Every day' #   Sceletium
draCI['OftenUseOpioids'][275] = 'Every day' #   Kratom, phenibut, kava
draCI['OftenUseOpioids'][280] = 'Twice a week' #  Kratom
draCI['OftenUseOthers'][281] = 'Once a week' #   Testosterone 
draCI['OftenUseOpioids'][283] = 'Once a week' #  kanna, kava kava, kratom, sida cordifolia
draCI['OftenUseOthers'][289] = 'Every day' #   gabapentin
draCI['OftenUseOthers'][293] = 'Once a week' #   Salvia
draCI['OftenUseOthers'][298] = 'Only once' #   Doxylamine
draCI['OftenUseOpioids'][304] = 'Only twice' #   Kratom
draCI['OftenUseOpioids'][317] = 'Once a week' #   Kratom
draCI['OftenUseDXM'][320] = 'Every day'  #   Dexamphetamine
 
draCI['OftenUseOthers'][338] = 'Twice a week' #   ETH-LAD, MD-PHP, A-PHP, A-PiHP, A-PCyP, 5-Bromo-DMT (yes, you read that correctly. Fucking sea sponges!) 
draCI['OftenUseOthers'][345] = 'Only once' # mescaline
draCI['OftenUseOpioids'][351] = 'Every day' #   Kratom, phenibut
draCI['OftenUsePhenibut'][351] = 'Every day'  #  Kratom, phenibut
draCI['OftenUseOthers'][353] = 'Three times a week' #  Synthetic stimulants ( amph and Cath)
draCI['OftenUseOthers'][359] = 'Twice a week' #  ambien
draCI['OftenUsePhenibut'][368] = 'Every day' #   Phenibut
draCI['OftenUseOpioids'][370] = 'Only once' #   kratom
draCI['OftenUseOthers'][379] = 'Every day' #   Gabapentin and adderall(prescribed)
draCI['OftenUseOthers'][397] = 'Every other day' #   4f-mph
draCI['OftenUseOthers'][401] = 'Every day' #   2-FMA, 3-MMC, mianserin 
draCI['OftenUseOpioids'][411] = 'Three times a week' #   Kratom 
draCI['OftenUseOpioids'][450] = 'Twice a week' #   Tramadol
draCI['OftenUseOthers'][458] = 'Only once' #   pregabalin
draCI['OftenUseOthers'][484] = 'Every day' #   Dimenhydrinate and caffein
draCI['OftenUseOthers'][500] = 'Every other day' #   Crack cocaine
draCI['OftenUseGHBL'][540] = 'Every day' #   Gamma Hydroxybutyrate
draCI['OftenUseOpioids'][546] = 'Once a week' #   Kratom
draCI['OftenUseOthers'][547] = 'Only once' #   NEP
              

draCI['OftenUseGHBL'][556] = 'Twice a week' #   GHB
draCI['OftenUseOthers'][637] = 'Once a week' #   3-MMC
draCI['OftenUseLSD'][647] = 'Only once' #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['OftenUseKet'][647] = 'Only once' #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['OftenUseOthers'][697] = 'Only once' #   Salvia, mescaline
draCI['OftenUsePhenibut'][713] = 'Twice a week' #   Phenibut
draCI['OftenUseOthers'][728] = 'Only once' #   Gabapentinoids
draCI['OftenUsePhenibut'][730] = 'Twice a week' #   Phenibut
draCI['OftenUseOthers'][771] = 'Every other day' #   Buprenorphine
draCI['OftenUseOpioids'][777] = 'Every other day' #   Kratom
draCI['OftenUseOpioids'][778] = 'Every day' #   Kratom Daily 2x11.5g
draCI['OftenUseOthers'][780] = 'Once a week' #   3-MMC, N-Ethylhexedrone
draCI['OftenUseOthers'][798] = 'Only once' #   Salvia divinorum 
draCI['OftenUseGHBL'][818] = 'Only once' #   gbl 
draCI['OftenUseOthers'][822] = 'Only once' #   nutmeg
draCI['OftenUseOthers'][836] = 'Only twice' #   wild dagga
draCI['OftenUse2C_X'][861] = 'Only once' #   2C-B (nexus)
draCI['OftenUseOthers'][874] = 'Every day' #   prescribed depression meds
draCI['OftenUseOthers'][929] = 'Only twice' #   Quetiapine
draCI['OftenUseOthers'][956] = 'Every other day' #   Ayahuasca, San Pedro, Coca Leaves
draCI['OftenUseCoke'][956] = 'Every other day' #   Ayahuasca, San Pedro, Coca Leaves
draCI['OftenUseOthers'][1112] = 'Twice a week' #  Nutmeg
draCI['OftenUsePhenibut'][1135] = 'Only once' #  Phenibut
draCI['OftenUseOthers'][1214] = 'Every other day' #  3-meo-pcp
                         
draCI['OftenUseOpioids'][1237] = 'Only twice' #  Kratom
draCI['OftenUseGHBL'][1278] = 'Once a week' #  Ghb
draCI['OftenUseOthers'][1299] = 'Only once' #  tetrahydroharmine, kanna, blue lotus, 
draCI['OftenUseCannabis'][1300] = 'Once a week' #  CBD
draCI['OftenUseGHBL'][1321] = 'Once a week' #  GHB
draCI['OftenUseGHBL'][1347] = 'Only once' #  Ghb
draCI['OftenUseOthers'][1358] = 'Every day' #  3MMC
draCI['OftenUseBenzos'][1387] = 'Only twice' #  1.5x doses of Xanax to achieve altered state
draCI['OftenUseGHBL'][1415] = 'Only twice' #  G
draCI['OftenUseOthers'][1444] = 'Only once' #  Cyclobenzaprine (muscle relaxers)
draCI['OftenUseOthers'][1458] = 'Only twice' #  pregabalin
draCI['OftenUseOthers'][1459] = 'Once a week' #  Mescaline
draCI['OftenUseOpioids'][1463] = 'Every day' #  Kratom
draCI['OftenUsePhenibut'][1471] = 'Only twice' #  Phenibut
draCI['OftenUseOpioids'][1472] = 'Three times a week' #  kratom

draCI['OftenUseOthers'][1500] = 'Every day' #  SNRI
draCI['OftenUseOthers'][1502] = 'Once a week' #  3-MMC, 4-CMC
draCI['OftenUseOthers'][1512] = 'Only once' #  salvia, GBL
draCI['OftenUseGHBL'][1512] = 'Only once' #  salvia, GBL
draCI['OftenUseBenzos'][1546] = 'Only once' #  xanax
draCI['OftenUseOthers'][1581] = 'Only twice' #  4f-MPH
draCI['OftenUseOpioids'][1585] = 'Twice a week' # Cyclobenzaprine, kratom
draCI['OftenUseOthers'][1585] = 'Twice a week' #  Cyclobenzaprine, kratom
draCI['OftenUseOthers'][1594] = 'Every day' #  Lyrica (pregabalin), Bronkaid (ephedrine), tons of energy drinks
draCI['OftenUseOthers'][1596] = 'Only once' #  LSA
draCI['OftenUseOpioids'][1612] = 'Only twice' #  Kratom
draCI['OftenUseGHBL'][1613] = 'Only twice' #  GHB 

draCI['OftenUseOthers'][1615] = 'Only twice' #  DPH
draCI['OftenUseOthers'][1617] = 'Only twice' #  Kanna
draCI['OftenUseOthers'][1633] = 'Twice a week' #  SOMA, GHB
draCI['OftenUseGHBL'][1633] = 'Twice a week' #  SOMA, GHB

draCI['OftenUseOpioids'][1655] = 'Every day' #  Kratom
draCI['OftenUseOthers'][1692] = 'Twice a week' #  Dph
draCI['OftenUseGHBL'][1699] = 'Only once' #  Ghb
draCI['OftenUseOthers'][1710] = 'Only once' #  Nutmeg
draCI['OftenUseOthers'][1712] = 'Twice a week' #  Miscellaneous inhalants
draCI['OftenUseCannabis'][1722] = 'Every day' #  cbd
draCI['OftenUseOthers'][1729] = 'Once a week' #  Pregabalin
draCI['OftenUseOpioids'][1731] = 'Every day' #  Kratom 
draCI['OftenUseOthers'][1735] = 'Three times a week' #  Gabapentin 
draCI['OftenUseOthers'][1744] = 'Only once' #  25I-NBOMe
draCI['OftenUseOthers'][1755] = 'Three times a week' #  Pregabalin
draCI['OftenUseOpioids'][1776] = 'Every other day' #  Codiene
draCI['OftenUseOthers'][1809] = 'Once a week' #  Why is my boy O-PCE not here😤
draCI['OftenUseCannabis'][1822] = 'Every day' #  Weed
draCI['OftenUseOpioids'][1832] = 'Every other day' #  Kratom, deschloroketamine, 4F-MPH 
draCI['OftenUseOthers'][1832] = 'Every other day' #  Kratom, deschloroketamine, 4F-MPH 
draCI['OftenUseOpioids'][1887] = 'Every other day' #  Kratom
draCI['OftenUseOthers'][1890] = 'Once a week' #  LSA
draCI['OftenUseOpioids'][1892] = 'Every day' #  Kratom
draCI['OftenUseOpioids'][1901] = 'Only once' #  Hydrocodone 
draCI['OftenUseGHBL'][1907] = 'Every day' #  Gbl
draCI['OftenUseGHBL'][1911] = 'Every day' #  Ghb/GBL
draCI['OftenUseOpioids'][1918] = 'Only twice' #  kratom
draCI['OftenUseOthers'][1922] = 'Every other day' #  DPH
draCI['OftenUseBenzos'][1923] = 'Every day' #  Etizolam 
draCI['OftenUseOthers'][1929] = 'Twice a week' #  Belladonna 
draCI['OftenUseOpioids'][1947] = 'Every day' #  Kratom
draCI['OftenUseOthers'][1949] = 'Every day' #  4-fma
draCI['OftenUseOthers'][1954] = 'Twice a week' #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['OftenUseGHBL'][1954] = 'Twice a week' #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['OftenUsePhenibut'][1954] = 'Twice a week' #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['OftenUseOpioids'][1954] = 'Twice a week' #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['OftenUseOthers'][1966] = 'Every day' #  Quetiapine
draCI['OftenUseCannabis'][1968] = 'Every day' #  Weed
draCI['OftenUseOpioids'][1995] = 'Every day' #  Daily kratom use
draCI['OftenUseOthers'][2016] = 'Once a week' #  Cathinones
draCI['OftenUseOthers'][2025] = 'Three times a week' #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['OftenUsePhenibut'][2025] = 'Three times a week' #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['OftenUseOpioids'][2025] = 'Three times a week' #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['OftenUseOthers'][2045] = 'Only twice'  #  Salvia divinorum
draCI['OftenUseOthers'][2058] = 'Once a week' #  RCs
draCI['OftenUseOthers'][2076] = 'Every day' #  Caffeine
draCI['OftenUseCannabis'][2170] = 'Every day' #  Hash
draCI['OftenUseOthers'][2248] = 'Only twice' #  Speed (base)
draCI['OftenUseOthers'][2320] = 'Only once' #  MXE, MPA
draCI['OftenUseCannabis'][2378] = 'Every day' #  THC oil vape 
draCI['OftenUseOthers'][2383] = 'Only once' #  drone
draCI['OftenUseOthers'][2421] = 'Three times a week' #  Promethazine

  
#IGNORE 638     Three times a week
#IGNORE 156  Cannabis should'nt really be on this list. 
# IGNORE 227  Only twice
# IGNORE 241   Only once
# IGNORE 329    Every day
# IGNORE 337    Twice a week
# IGNORE 408    Only once
# IGNORE 474    Once a week
# IGNOREE 515    Only once
# IGNORE 1638    Three times a week
# IGNORE 824   Only twice
# IGNORE 1386   Only once
# IGNORE 1967    Only twice
# IGNORE 2127    Three times a week
# IGNORE 2407    Three times a week
# IGNORE 2414    Every day
# IGNORE 2420    Only once
# IGNORE 2425     Every day
# IGNORE 2427     Only once
# IGNORE 2436    Every day
# IGNORE 2458    Only once
#IGNORE 2468 none


# %% Amend Harm reduction techniques
ind_col_newSupp = np.where(col_names == 'TechNewSupplier')
cols_newSupp = col_names[ind_col_newSupp[0][0]:(ind_col_newSupp[0][0] + 8)]

draCI.rename(columns={'TechNewSupplier':  'TechNewHomeRea',          
                      'Unnamed: 289':     'TechNewLabSer', 
                      'Unnamed: 290':     'TechNewEye',
                      'Unnamed: 291':     'TechNewRev',    
                      'Unnamed: 292':     'TechNewFriPre',    
                      'Unnamed: 293':     'TechNewSmaller',  
                      'Unnamed: 294':     'TechNewNotMix', 
                      'Unnamed: 295':     'TechNewAskFriends'
                    },  
          inplace=True, errors='raise')


names = ['Testing using home reagent tests', 'Testing by sending to a lab service', 
        'Carefully examining the substance by eye', 'Checking for reviews of online sellers',
        'Only using the substance when a friend is present', 'Starting with a smaller dose than normal',
        'Not mixing with other drugs', 'Asking friends about the seller']

cols = ['TechNewHomeRea', 'TechNewLabSer', 'TechNewEye', 'TechNewRev',    
        'TechNewFriPre',  'TechNewSmaller', 'TechNewNotMix', 'TechNewAskFriends']
 

# %% Amend combination of alcohol with other drugs NOT FINISHED
ind_col_comAlc = np.where(col_names == 'AlcoholCombinations')
cols_comAlc = col_names[ind_col_comAlc[0][0]:(ind_col_comAlc[0][0] + 22)]

draCI.rename(columns={'AlcoholCombinations':  'AlcCom2C_X',          
                      'Unnamed: 215':         'AlcComAdderall', 
                      'Unnamed: 216':         'AlcComAmphe',    
                      'Unnamed: 217':         'AlcComBenzos',    
                      'Unnamed: 218':         'AlcComCannabis',  
                      'Unnamed: 219':         'AlcComCoke',   
                      'Unnamed: 220':         'AlcComMeth',   
                      'Unnamed: 221':         'AlcComDMT',   
                      'Unnamed: 222':         'AlcComDXM',   
                      'Unnamed: 223':         'AlcComIbo',   
                      'Unnamed: 224':         'AlcComKet',   
                      'Unnamed: 225':         'AlcComLSD',   
                      'Unnamed: 226':         'AlcComShrooms',
                      'Unnamed: 227':         'AlcComMAOIs',   
                      'Unnamed: 228':         'AlcComMDMA',
                      'Unnamed: 229':         'AlcComModafinil',
                      'Unnamed: 230':         'AlcComNO',
                      'Unnamed: 231':         'AlcComOpioids',
                      'Unnamed: 232':         'AlcComSSRIs',
                      'Unnamed: 233':         'AlcComPoppers',
                      'Unnamed: 234':         'AlcComNicotine',
                      'Unnamed: 235':         'AlcComOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Amphetamine (aka\xa0‘speed’ but NOT crystal meth)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis (aka weed/marijuana/hash/skunk/grass)', 'Cocaine (aka coke, Charlie snow)', 
          'Crystal Meth', 'DMT (including Ayahuasca, Changa and 5-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine\xa0(aka K, Ket, Special K)', 'LSD (aka Acid)', 'Magic Mushrooms (or other forms of Psilocybin, including 4-AcO-DMT)',
          'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'MDMA (aka\xa0MD, Ecstasy, Mandy, Molly, Magic)', 'Modafinil',
          'Nitrous Oxide (aka balloons or laughing gas)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (aka antidepressants)', 'Poppers', 'Nicotine\xa0(tobacco or nicotine vapes)']

cols = ['AlcCom2C_X', 'AlcComAdderall', 'AlcComAmphe', 'AlcComBenzos',  
        'AlcComCannabis', 'AlcComCoke', 'AlcComMeth', 'AlcComDMT',   
        'AlcComDXM', 'AlcComIbo', 'AlcComKet', 'AlcComLSD', 'AlcComShrooms',
        'AlcComMAOIs','AlcComMDMA','AlcComModafinil', 'AlcComNO', 
        'AlcComOpioids', 'AlcComSSRIs', 'AlcComPoppers', 'AlcComNicotine']
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

boAlcCom = draCI['AlcComOthers'].isnull()
indxAlcCom = draCI['AlcComOthers'][~boAlcCom].index

draCI['AlcComOthers'] = 0  

draCI['AlcComOthers'][228] = 1   #    Seroquel
draCI['AlcComDXM'][320] = 1  #    Dexamphetamine
draCI['AlcComOpioids'][351] = 1  #    Kratom
draCI['AlcComOthers'][359] = 1   #    ambien
draCI['AlcComOthers'][368] = 1   #    Phenibut
draCI['AlcComOthers'][379] = 1   #    Gabapentin
#IGNORE 422   Toast
#IGNORE 497   None 
#IGNORE 725   Ambien
draCI['AlcComOpioids'][778] = 1  #    Kratom
draCI['AlcComOthers'][780] = 1  #    3-mmc, n-ethylhexedrone
draCI['AlcComCannabis'][790] = 1  #    I might have had 1 or 2 drinks, then if I smoke I would stop drinking
#IGNORE 858   Nothing
draCI['AlcComOthers'][979] = 1  #    Spice
draCI['AlcComBenzos'][1066] = 1  #    im fully aware of the dangers of combining some of the substances up here w alcohol, but damn, the high is just too mesmerizing, especially benzos.
draCI['AlcComOthers'][1096] = 1  #    Bbd
draCI['AlcComOthers'][1112] = 1   #    Nutmeg
draCI['AlcComOthers'][1172] = 1 #    Mephedrone
draCI['AlcComOpioids'][1237] = 1  #    Kratom
draCI['AlcComOthers'][1420] = 1  #    Caffeine
draCI['AlcComOpioids'][1463] = 1 #    Kratom
draCI['AlcComOthers'][1585] = 1 #    Kratom, cyclobenzaprine 
draCI['AlcComOthers'][1617] = 1 #    Phenibut, Kanna
#IGNORE 1886   Others
draCI['AlcComOpioids'][1918] = 1 # kratom (occasionally/rarely)
draCI['AlcComOpioids'][1947] = 1 #  Kratom
draCI['AlcComOthers'][1995] = 1  #    4-fma
draCI['AlcComCannabis'][2203] = 1  #    Normally I would have maybe 2/3 vodkas and 7 up early evening and then a joint for bed
draCI['AlcComAmphe'][2248] = 1  #    Speed
#IGNORE 2251   None
draCI['AlcComCannabis'][2378] = 1  #    THC VAPE
#IGNORE 2436   No drugs

# %% Most common drug combinations
ind_col_comDru = np.where(col_names == 'DrugCombinations')
cols_comDru = col_names[ind_col_comDru[0][0]:(ind_col_comDru[0][0] + 21)]

draCI.rename(columns={'DrugCombinations':  'DrugCom1Dru1',          
                      'Unnamed: 238':      'DrugCom1Dru2', 
                      'Unnamed: 239':      'DrugCom1Dru3',
                      'Unnamed: 240':      'DrugCom1Dru4',    
                      'Unnamed: 241':      'DrugCom2Dru1',    
                      'Unnamed: 242':      'DrugCom2Dru2',  
                      'Unnamed: 243':      'DrugCom2Dru3', 
                      'Unnamed: 244':      'DrugCom2Dru4',   
                      'Unnamed: 245':      'DrugCom3Dru1',   
                      'Unnamed: 246':      'DrugCom3Dru2',   
                      'Unnamed: 247':      'DrugCom2Dru3',   
                      'Unnamed: 248':      'DrugCom3Dru4',   
                      'Unnamed: 249':      'DrugCom4Dru1',   
                      'Unnamed: 250':      'DrugCom4Dru2',   
                      'Unnamed: 251':      'DrugCom4Dru3',
                      'Unnamed: 252':      'DrugCom4Dru4',
                      'Unnamed: 253':      'DrugCom5Dru1',
                      'Unnamed: 254':      'DrugCom5Dru2',   
                      'Unnamed: 255':      'DrugCom5Dru3',
                      'Unnamed: 256':      'DrugCom5Dru4',
                      'Unnamed: 257':      'DrugComDruOther',
                    },  
          inplace=True, errors='raise')


# %% Amend dependent to what drugs
ind_col_Depwhich = np.where(col_names == 'DependenceWhich')
cols_depWhich = col_names[ind_col_Depwhich[0][0]:(ind_col_Depwhich[0][0] + 24)]

draCI.rename(columns={'DependenceWhich':  'DrugDep2C_X',          
                      'Unnamed: 260':     'DrugDepAdderall', 
                      'Unnamed: 261':     'DrugDepAlc',
                      'Unnamed: 262':     'DrugDepAmphe',    
                      'Unnamed: 263':     'DrugDepBenzos',    
                      'Unnamed: 264':     'DrugDepCannabis',  
                      'Unnamed: 265':     'DrugDepCaffeine', 
                      'Unnamed: 266':     'DrugDepCoke',   
                      'Unnamed: 267':     'DrugDepMeth',   
                      'Unnamed: 268':     'DrugDepDMT',   
                      'Unnamed: 269':     'DrugDepDXM',   
                      'Unnamed: 270':     'DrugDepIbo',   
                      'Unnamed: 271':     'DrugDepKet',   
                      'Unnamed: 272':     'DrugDepLSD',   
                      'Unnamed: 273':     'DrugDepShrooms',
                      'Unnamed: 274':     'DrugDepMDMA',
                      'Unnamed: 275':     'DrugDepModafinil',
                      'Unnamed: 276':     'DrugDepMAOIs',   
                      'Unnamed: 277':     'DrugDepNO',
                      'Unnamed: 278':     'DrugDepOpioids',
                      'Unnamed: 279':     'DrugDepSSRIs',
                      'Unnamed: 280':     'DrugDepNicotine',
                      'Unnamed: 281':     'DrugDepPoppers',
                      'Unnamed: 282':     'DrugDepOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Alcohol', 'Amphetamine (also known as ‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis (also known as weed/marijuana/skunk/grass)', 'Caffeine (coffee, tea, energy drinks)', 'Cocaine (also known as “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (including Ayahuasca, Changa and 5-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (also known as ‘K’, ‘Ket’, ‘Special K’)', 'LSD (also known as “Acid”)', 'Magic mushrooms (or other forms of Psilocybin, including 4-AcO-DMT)',
          'MDMA (also known as “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)',
          'Nitrous Oxide (also known as ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (also known as antidepressants)', 'Nicotine (tobacco or nicotine vapes)', 'Poppers']

cols = ['DrugDep2C_X','DrugDepAdderall','DrugDepAlc','DrugDepAmphe',
        'DrugDepBenzos', 'DrugDepCannabis','DrugDepCaffeine','DrugDepCoke',
        'DrugDepMeth','DrugDepDMT','DrugDepDXM','DrugDepIbo','DrugDepKet',
        'DrugDepLSD','DrugDepShrooms', 'DrugDepMDMA', 'DrugDepModafinil', 
        'DrugDepMAOIs', 'DrugDepNO', 'DrugDepOpioids', 'DrugDepSSRIs', 
        'DrugDepNicotine', 'DrugDepPoppers']
   
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

boDrugDep = draCI['DrugDepOthers'].isnull()
indxDrugDep = draCI['DrugDepOthers'][~boDrugDep].index

draCI['DrugDepOther'] = 0  
draCI['DrugDepGB'] = 0 

draCI['DrugDepOpioids'][133] = 1 #   kratom
draCI['DrugDepBenzos'][204] = 1 #   Not sure about the benzos but I don’t want to feel the withdrawals! I don’t know what to do, almost no benzo anymore
draCI['DrugDepOther'][228] = 1  #   Seroquel
draCI['DrugDepGB'][238] = 1  #   Ghb
draCI['DrugDepNicotine'][251] = 1  #   Nic
draCI['DrugDepCaffeine'][267] = 1  #   Caffeine, melatonin
draCI['DrugDepOther'][267] = 1  #   Caffeine, melatonin
draCI['DrugDepCaffeine'][329] = 1  #   In the "combinations" section of this survey, when I say "other" I mean caffeine  
draCI['DrugDepOpioids'][351] = 1 #   Kratom
draCI['DrugDepOther'][368] = 1  #   Phenibut
draCI['DrugDepOther'][379] = 1  #   Gabapentin
draCI['DrugDepAmphe'][400] = 1  #   2-FMA
draCI['DrugDepOther'][401] = 1  #   Mianserin 
draCI['DrugDepOpioids'][608] = 1 #   Tramadol
draCI['DependenceBool'][700] = 0 #   I do not feel addicted to any drugs 
draCI['DrugDepOpioids'][771] = 1 #   Buprenorphine
draCI['DrugDepOpioids'][778] = 1 #   Kratom
draCI['DrugDepOther'][1112] = 1  #  Nutmeg
draCI['DrugDepOpioids'][1236] = 1 #  Kratom, which could be considered an opioid
draCI['DrugDepOther'][1254] = 1  #  Advil
draCI['DrugDepOther'][1358] = 1  #  3MMC 
draCI['DrugDepOpioids'][1463] = 1 #  Kratom
#IGNORE 1548 love
draCI['DrugDepOpioids'][1585] = 1 #  Kratom
draCI['DrugDepOther'][1594] = 1  #  high dose caffeine and ephedrine, wellbutrin (but that one is prescribed)
draCI['DrugDepCaffeine'][1594] = 1  #  high dose caffeine and ephedrine, wellbutrin (but that one is prescribed)
draCI['DrugDepOther'][1615] = 1  #  DPH
#IGNORE 1674 Not any particular drug, just the altered state that comes with a drug
draCI['DrugDepOpioids'][1684] = 1 #  Kratom
draCI['DrugDepOpioids'][1731] = 1 #  Kratom 
draCI['DrugDepOther'][1735] = 1  #  Gabapentin 
draCI['DependenceBool'][1894] = 0 #  Not dependent
draCI['DrugDepGB'][1907] = 1 #  Gbl
draCI['DrugDepGB'][1911] = 1  #  GHB/GBL
draCI['DrugDepCannabis'][1918] = 1  #  cannabis + nicotine together
draCI['DrugDepNicotine'][1918] = 1  #  cannabis + nicotine together
draCI['DrugDepOpioids'][1931] = 1 #  suboxone
draCI['DrugDepOpioids'][1947] = 1 # 1947 Kratom 
draCI['DrugDepOpioids'][1956] = 1 #  tramadol
draCI['DrugDepOpioids'][1985] = 1 #  Kratom
draCI['DrugDepOpioids'][1995] = 1 #  Kratom
#IGNORE 2019 And just trying other stuff, opioids, and soon maybe benzos and other stuff
#IGNOREE 2020 Any drug that can get me high. 


# %% Amend what withdrawal symptoms
# 'What withdrawal symptoms have you experienced?': 'WithdrawalSymptyoms',
boWithSymp = draCI['WithdrawalSymptyoms'].isnull()
indxWithSymp = draCI['WithdrawalSymptyoms'][~boWithSymp].index

draCI['WithdrawalSymptyoms'][indxWithSymp]

# 4    feeling tired and unable to concentrate
# 8    Agitation, nervousness
# 10   Clammy skin, ill appetite, inability to sleep
# 23   Body ache
# 33   irritable
# 45   insomnia
# 49   Dizzy and agitated 
# 56   Anxiety headaches
# 63   Anger, anxiety, paranoia 
# 66   Irritable 
# 71   Anxiety, paranoia, difficulty sleeping
# 80   Longing for ket, irritability and loss of focus 
# 91   The feeling that I have wanted to have the high of a certain drug
# 94   Loss of appetite, moodiness
# 105  Alergies respiratory
# 125  Depression, irritability, oversleeping, increased appetite, fatigue, nightmares, difficulty concentrating, anxiety
# 134  with
# 139  Irritability and headaches
# 142  Pains in the body, panic, Anxiety, low mood
# 162  Mood swings 
# 198  Dizziness
# 204  Extreme sweating, depression, diarrheal, restless legs syndrome, headaches, nausea. (Was out of Tramadol)
# 216  shaking
# 219  Lack of motivation, irritability, mood swings, and sleep difficulty.
# 220  Anxiety 
# 222  cravings, irritation
# 228  Insomnia,cold sweat, shakiness
# 231  Low energy, sweaty, restless body ,irritation ,throwing up,
# 236  insomnia, depression, mood swings
# 239  Insomnia, anxiety, tremors, fatigue
# 258  Sleepless, back pain 
# 267  Fatigue, depression, low mood, anxiety
# 268  All of them
# 294  Soreness, lack energy, more anxiety when straight
# 296  Before I had access to cannabis, the first week of this situation I had a terrible time sleeping and eating 
# 298  Extreme sleepiness, increased appetite, severe fatigue
# 299  just straight pain 
# 313  insomnia
# 321  Headaches and loss of appetite, difficulties falling asleep
# 329  I had withdrawals from the Adderall which doesn't usually happen to me but sheer boredom during lock-down made it inevitable. I have depression and anxiety and complete lack of motivation which is usually fixed up with kratom but that did not work after this last round of Adderall.This is why I ...
# 332  Cognitive impairment, worsening depression/anhedonia, avolition, improper sleep schedule
# 333  Tremors, nausea, sweating, anxiety, fatigue, confusion, irritability, sore muscles
# 359  nausea, memory loss
# 368  Anxiety, depression
# 379  Anxiety, dizziness, lethargy, depression, manic episodes 
# 386  Diarrhea, panic, suicidal thoughts
# 387  Anxiety, hopelessness, suicidal thoughts 
# 410  Headache
# 426  Cold sweats and no sleep
# 434  tiredness, hopelessness, depression, loneliness, ect.
# 445  Increased anxiety, sweating, shaking
# 456  Opioid withdrawal - vomiting, nausea, sleeplessness, insomnia, depression, agitation/aggressive behaviour, short term memory loss, fever, cold sweats, body aches
# 457  Not many, as I try not to run out.... when I do: rls, depression, anxiety, feelings of hopelessness, cramping, chills/fever, anxiety, racing heart, depression 
# 458  not being able to function and getting irritated or angry and sad
# 469  Lack of sleep and bad mood
# 471  Shakes and headaches
# 472  Anger, Stress
# 487  Tiredness, lack of hunger
# 495  Agitation, depression, nausea
# 500  Anxiety, vivid dreams, cravings, anger, agitated, sweating
# 511  Opiate withdrawal symptoms 
# 514  Feeling down
# 527  Moody
# 532  Opiate withdrawal
# 547  Fever, Migraines, Insomnia, Cold sweats, Brain zaps, Chills, Appetite suppression, Depression, Anger issues
# 548  Depression is much worse, struggle to get out of bed, don't enjoy activities I normally love
# 549  Increased desire two consecutive days and alongside of anxiety and desire to get insight or spiritual insight and understanding into whats going on and choices of How to respond 
# 553  I went camping and did coke and meth, hardly slept. When I got home I crashed and slept over 12 hours. I was very groggy tired even after that, and am extremely low energy and motivation. All I can think about is how. ad I want another bag of meth. I am persevering tho, not gonna get one
# 555  Severe Depression
# 558  anger
# 561  depression
# 562  Fever sweating insomnia headache night terrors 
# 566  Headaches, anxiety
# 570  tachycardia
# 608  depression, anxiety, fatigue, changes in appetite, nasal congestion, headaches, muscle weakness
# 639  Just wanna take some lines
# 657  Happy to stop that shit 
# 682  Shakes, nausea, 
# 730  Cravings
# 743  Anxiety, restlessness, mood shifts
# 744  Dizzy
# 764  Headaches
# 771  Coldness, Headaches, Exhaustion, Anxiety
# 779  Extra need of love & extra missing of everybody. Usually I don’t give a fuck and try not to die.
# 781  Sweats irritability 
# 828  amphetamine
# 829  lack of energy, no motivation 
# 833  anxiety 
# 839  Trouble sleeping when not consuming alcohol and/or cannabis 
# 852  Sweats 
# 859  Anxiety
# 867  Irritability, mood swings, lack of sleep
# 869  Feeling depressed and anxious
# 870  Increased depression
# 880  Anxiety
# 892  lack of motivation, clear thinking, ability to execute on desired goals
# 914  Sweating,  shaking,  panicking 
# 919  Withdrawal 
# 921  Hangover
# 927  Depression 
# 929  Hazy thoughts
# 939  None
# 953  Mostly anxiety and paranoia
# 959  Pain, anxiety, depression, stress, less work, no sexual desire , chest pain, body pain, no mind relaxation, 
# 971  anxiety, anger
# 979  Cough
# 982  Sweating, heightened emotions, anxiety
# 989  non stop crying,emptyness
# 992  Anxiety, psychosis
# 1002 Lack of socialism
# 1021 Opioid withdrawal
# 1095 Anxiety, dizziness, headache, apathy
# 1110 Headaches, lost focus
# 1124 Anxiety
# 1151 Bad mood and headaches
# 1174 Restlessness, constipation, anxiety, need for a certain drug, brain fog, mood swings, mania, loss of appetite
# 1176 Insomnia and depression
# 1197 Anxiety 
# 1203 cough
# 1211 Anxiety, irritation, dizziness, headache
# 1217 Heightened anxiety (not knowing if my weed is safe to consume + breaking lockdown rules), mood swings, depression feelings, difficulties sleeping, short temper
# 1254 Head aches
# 1295 None
# 1301 Unable to sleep anxiety mood swings
# 1321 Irritability, Depression
# 1387 Quite vivid, repeated, almost traumatising nightmares about me committing violent crimes or losing all of my loved ones
# 1438 Depression, Mood Swing
# 1444 Insomnia, irritability 
# 1451 Skakes, sweats, body aches and gerks, muscle spasms, unable to sleep, chills, fatigue, restlessness, anxiety  
# 1456 Shaking, anger, irritability, feeling of emptiness 
# 1460 Standard nicotine withdrawal symptoms, increased anxiety due to inaccessibility of cannabis and prescription SSRIs
# 1472 Quit drinking so: insomnia, chills, depression, anxiety
# 1509 Just urging cocaine when I drink
# 1526 Opiate withdrawals
# 1536 Anxiety, clammy skin
# 1546 shakiness, unable to balance, vomiting, sweating
# 1548 restless leg syndrome, insomnia, rashes, bigg boii time rebound anxiety, muscle spasms, 
# 1551 Panic attacks, decreased productivity + slight headaches, unable to sleep 
# 1560 HELL LITERAL HELL I SEE THINGS :(
# 1580 anxiety, tachychardia, dry mouth, bodily sensations, restlessness, lost appetite, trouble urinating, shaky hands
# 1585 Fatigue, lethargy
# 1587 Headaches
# 1590 Tired 
# 1594 wellbutrin withdrawal (mail order prescription system failed for a few weeks)
# 1597 slight benzo withdrawel
# 1600 anxiety and panic related symptoms
# 1613 Fatigue, irritatibility, body/muscle pain and stiffness
# 1614 Insomnia, no appetite 
# 1615 Drowsiness, mood swings
# 1620 Chills+ extreme fatigue+ anxiety+depression+irritability+stomach issues 
# 1625 restlessness, pain, insomnia, nausea, throwing up, sweating
# 1633 Cravings, Depression, Lethargy 
# 1692 Cold sweats and shakes
# 1704 shortness of breath
# 1709 Anxiety, hallucinations, confusion, delusions
# 1712 Insomnia, loss of appetite, general lethargy and dysphoria
# 1717 Depression, suicidal thoughts, anxiety
# 1722 headache body ace stomach pains anxiety 
# 1735 Hot flashes, chills, anxiety, insomnia and depression 
# 1745 Fatigue from discontinuation of adderall
# 1748 Nervousness
# 1837 Depression low energy anxiety anger suicidal thoughts mood swings extreme lethargy 
# 1839 Insomnia 
# 1847 headache apetite los took tramadol to cope with back pain
# 1886 Shaking depression anxiety seizures appetite fluctuation
# 1899 Flu like symptoms, diarrhea 
# 1907 Blood pressure, heart rate, pain in chest, muscle pain, headaches, shakes, delirium, confusion, restlessness, trouble sleeping, waking every hour, nightmares, needing to redose every half hour to feel sober
# 1911 Hypotension, Sweeling of joints, restlessness, anxiety, unable to sleep for days, burning sensation in the head, 
# 1912 Anxiety and pain
# 1915 sleeplessness and poor mood
# 1925 Nausea, headaches
# 1933 Depression
# 1947 Classic Opiate/Kratom WD & Malaise is no weed or alcohol
# 1955 Anxiety 
# 1962 Headache, anxiety, insomnia 
# 1965 Not being able to sleep and feeling restless
# 1969 shakes, chills, depression, insomnia, headaches, nausea, low energy/mood, loss of appetite, fluctuating temperature, hallucinations
# 1970 Anxiety
# 1979 not sure cuz but i think, abdominal cramps and severe headaches
# 1993 Sleepyness, anxiety, craving
# 1995 Lethargy and anxiety since I dont have access to adderall during the outbreak.
# 1996 Rebound anxiety, headaches, paranoia 
# 2005 Anxiousness 
# 2028 Nauseous 
# 2037 Chills, sweats, rls, insomnia, body aches, anxiety
# 2044 Headaches, irritability, anxiety
# 2045 no dopamine left
# 2066 Headache, nausea 
# 2077 Vast temperature changing, and stomach ache
# 2085 Not being able to sleep (potential cannabis withdrawal?)
# 2108 nervousness
# 2112 Fatigue
# 2117 A bit of anxiety
# 2120 Anxiety, sleeping more, being angry, crying everyday...
# 2123 Insomnia as a result of no access to zolpidem
# 2133 Sadness 
# 2139 Depresión, insomnio, despersonalización... 
# 2170 Sadnes
# 2185 Insomia and Depression
# 2191 Headache 

# %% Amend New drugs tried
# 'Which new drugs have you\xa0tried\xa0during the outbreak? (Tick all that apply)': '',
ind_col_NewDrug = np.where(col_names == 'NewDrugsOutbreak')
cols_ChanDrug = col_names[ind_col_NewDrug[0][0]:(ind_col_NewDrug[0][0] + 21)]

draCI.rename(columns={'NewDrugsOutbreak': 'NewDrugs2C_X',          
                      'Unnamed: 163':     'NewDrugsAdderall', 
                      'Unnamed: 164':     'NewDrugsAmphe',    
                      'Unnamed: 165':     'NewDrugsBenzos',    
                      'Unnamed: 166':     'NewDrugsCannabis',   
                      'Unnamed: 167':     'NewDrugsCoke',   
                      'Unnamed: 168':     'NewDrugsMeth',   
                      'Unnamed: 169':     'NewDrugsDMT',   
                      'Unnamed: 170':     'NewDrugsDXM',   
                      'Unnamed: 171':     'NewDrugsIbo',   
                      'Unnamed: 172':     'NewDrugsKet',   
                      'Unnamed: 173':     'NewDrugsLSD',   
                      'Unnamed: 174':     'NewDrugsShrooms',
                      'Unnamed: 175':     'NewDrugsMAOIs',   
                      'Unnamed: 176':     'NewDrugsMDMA',
                      'Unnamed: 177':     'NewDrugsModafinil',
                      'Unnamed: 178':     'NewDrugsNO',
                      'Unnamed: 179':     'NewDrugsOpioids',
                      'Unnamed: 180':     'NewDrugsSSRIs',
                      'Unnamed: 181':     'NewDrugsPoppers',
                      'Unnamed: 182':     'NewDrugsOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Amphetamine (aka\xa0‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis\xa0(aka weed/marijuana/hash/skunk/grass)', 'Cocaine (aka “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (i.e. Ayahuasca, Changa,\xa05-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (aka ‘K’, ‘Ket’, ‘Special K’)', 'LSD (aka “Acid”)', 'Magic Mushrooms (or other forms of Psilocybin,\xa0e.g. 4-AcO-DMT)',
          'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'MDMA (aka “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 
          'Nitrous Oxide (aka ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (aka antidepressants)', 'Poppers']

cols = ['NewDrugs2C_X', 'NewDrugsAdderall', 'NewDrugsAmphe', 'NewDrugsBenzos',
        'NewDrugsCannabis', 'NewDrugsCoke', 'NewDrugsMeth', 'NewDrugsDMT', 'NewDrugsDXM',
        'NewDrugsIbo', 'NewDrugsKet', 'NewDrugsLSD', 'NewDrugsShrooms', 'NewDrugsMAOIs',  
        'NewDrugsMDMA', 'NewDrugsModafinil', 'NewDrugsNO', 'NewDrugsOpioids',
        'NewDrugsSSRIs', 'NewDrugsPoppers']
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

boNewDrugs = draCI['NewDrugsOthers'].isnull()
indxNewDrugsOthers = draCI['NewDrugsOthers'][~boNewDrugs].index

# 49   Kanna 
# 133  euphylone, apcyp, md-pep
# 141  dck
# 146  St Johns wort
# 236  kanna
# 238  Ghb
# 251  Sceletium 
# 326  Baclofen
# 332  Prolintane (1-phenyl-2-pyrrolidinylpentane) 
# 338  MD-PHP freebase vaped, 5-Bromo-DMT vaped 
# 359  ambien
# 397  4f-mph
# 400  2-FMA
# 401  2-FMA
# 458  Pregabalin
# 470  DXM
# 547  NEP
# 668  Kratom
# 676  I answered "no" to trying new drugs
# 697  Mescaline
# 725  DPH, recreational ambien
# 728  Gabapentinoids
# 780  3-MMC
# 798  Salvia divinorum
# 822  nutmeg
# 1110 THC in vapor form
# 1165 4aco dmt fumerate salt
# 1236 DOC
# 1299 kanna
# 1386 3
# 1459 Mescaline
# 1512 salvia
# 1594 Lyrica (pregabalin)
# 1596 LSA
# 1638 Experimented with DPH and caffiene
# 1679 2-MAP-237
# 1710 Nutmeg
# 1712 Miscellaneous inhalants 
# 1744 25I-NBOMe
# 1755 I haven't tried any new drugs
# 1803 Nutmeg
# 1832 Deschloroketamine, 4F-MPH 
# 1888 O-DSMT
# 1890 LSA
# 1894 3-FEA , 4-HO-MET
# 1909 Morning glory seeds (LSA)
# 1954 1,4 BDO
# 2025 Pseudoephedrine, Phenylpiracetam 
# 2160 none
# 2383 drone, mephedrone


# %% Amend change to each drug
ind_col_ChanDrug = np.where(col_names == 'ChangeDrugUse')
cols_ChanDrug = col_names[ind_col_ChanDrug[0][0]:(ind_col_ChanDrug[0][0] + 21)]

draCI.rename(columns={'ChangeDrugUse':    'ChangeUse2C_X',          
                      'Unnamed: 141':     'ChangeUseAdderall', 
                      'Unnamed: 142':     'ChangeUseAmphe',    
                      'Unnamed: 143':     'ChangeUseBenzos',    
                      'Unnamed: 144':     'ChangeUseCann',   
                      'Unnamed: 145':     'ChangeUseCocaine',   
                      'Unnamed: 146':     'ChangeUseMeth',   
                      'Unnamed: 147':     'ChangeUseDMT',   
                      'Unnamed: 148':     'ChangeUseDXM',   
                      'Unnamed: 149':     'ChangeUseIbo',   
                      'Unnamed: 150':     'ChangeUseKet',   
                      'Unnamed: 151':     'ChangeUseLSD',   
                      'Unnamed: 152':     'ChangeUseMush',
                      'Unnamed: 153':     'ChangeUseMAOIs',   
                      'Unnamed: 154':     'ChangeUseMDMA',
                      'Unnamed: 155':     'ChangeUseMod',
                      'Unnamed: 156':     'ChangeUseNO',
                      'Unnamed: 157':     'ChangeUseOpioids',
                      'Unnamed: 158':     'ChangeUseSSRIs',
                      'Unnamed: 159':     'ChangeUsePoppers',
                      'Unnamed: 160':     'ChangeUseOther',    
                    },  
          inplace=True, errors='raise')



names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Amphetamine (aka\xa0‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis\xa0(aka weed/marijuana/hash/skunk/grass)', 'Cocaine (aka “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (i.e. Ayahuasca, Changa,\xa05-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (aka ‘K’, ‘Ket’, ‘Special K’)', 'LSD (aka “Acid”)', 'Magic Mushrooms (or other forms of Psilocybin,\xa0e.g. 4-AcO-DMT)',
          'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'MDMA (aka “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 
          'Nitrous Oxide (aka ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (aka antidepressants)', 'Poppers']

cols = ['ChangeUse2C_X', 'ChangeUseAdderall', 'ChangeUseAmphe', 'ChangeUseBenzos', 
        'ChangeUseCann', 'ChangeUseCocaine', 'ChangeUseMeth', 'ChangeUseDMT',   
        'ChangeUseDXM', 'ChangeUseIbo', 'ChangeUseKet', 'ChangeUseLSD',   
        'ChangeUseMush', 'ChangeUseMAOIs', 'ChangeUseMDMA', 'ChangeUseMod',
        'ChangeUseNO', 'ChangeUseOpioids', 'ChangeUseSSRIs',  'ChangeUsePoppers']
        

boChangeDrugs = draCI['ChangeUseOther'].isnull()
indxChangeDrugsOthers = draCI['ChangeUseOther'][~boChangeDrugs].index


draCI['ChangeUseOthers'] = 0
draCI['ChangeUseGHBL'] = 0
draCI['ChangeUsePhenibut'] = 0


draCI['ChangeUseOpioids'][63] = 'Increased' #  Codiene
draCI['ChangeUseOthers'][77] = 'Increased' #  Salvia 
draCI['ChangeUseOthers'][94] = "Hasn't changed" #  DPH
draCI['ChangeUseOthers'][133] = "Hasn't changed" #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['ChangeUseOpioids'][133] = "Hasn't changed" #   a-php, a-pcyp, 2fma, 4fmph, flualprazolam, flubromazolam, diclazepam, pyrazolam, gabapentin, euphylone, md-pep, kratom
draCI['ChangeUseOthers'][141] = "Hasn't changed" #   3-meo-pce, dck, 2f-dck, 4-aco-met
draCI['ChangeUseOpioids'][203] = 'Increased' #   kratom
draCI['ChangeUseOthers'][211] = "Hasn't changed" #   blue lotus
draCI['ChangeUseCann'][214] = "Hasn't changed" #  THC vape liquid
draCI['ChangeUseGHBL'][224] = "Greatly increased" #   Magic Mushrooms, GHB
draCI['ChangeUseMush'][224] = "Greatly increased" #   Magic Mushrooms, GHB
draCI['ChangeUseOpioids'][228] = "Increased" #   Kratom n sleeping pills (seroquel)
draCI['ChangeUseOthers'][228] = "Increased" #   Kratom n sleeping pills (seroquel)
draCI['ChangeUseOthers'][236] = "Greatly increased" #   kanna
draCI['ChangeUseGHBL'][238] = "Greatly increased" #   Ghb
draCI['ChangeUseOthers'][251] = "Greatly increased" #   Sceletium
draCI['ChangeUseOpioids'][275] = "Greatly increased" #   Kratom, phenibut, kava
draCI['ChangeUseOpioids'][280] = "Increased" #  Kratom
draCI['ChangeUseOthers'][281] = "Hasn't changed" #   Testosterone 
draCI['ChangeUseOpioids'][283] = "Increased" #  kanna, kava kava, kratom, sida cordifolia
draCI['ChangeUseOthers'][289] = "Greatly increased" #   gabapentin
draCI['ChangeUseOthers'][293] = "Greatly increased" #   Salvia
draCI['ChangeUseOthers'][298] = "Hasn't changed" #   Doxylamine
draCI['ChangeUseOpioids'][304] = "Greatly increased" #   Kratom
draCI['ChangeUseOpioids'][317] = "Hasn't changed" #   Kratom
draCI['ChangeUseDXM'][320] = "Hasn't changed"  #   Dexamphetamine
draCI['ChangeUseOthers'][338] = 'Increased' #   ETH-LAD, MD-PHP, A-PHP, A-PiHP, A-PCyP, 5-Bromo-DMT (yes, you read that correctly. Fucking sea sponges!) 
draCI['ChangeUseOthers'][345] = "Hasn't changed" # mescaline
draCI['ChangeUseOpioids'][351] = "Decreased" #   Kratom, phenibut
draCI['ChangeUsePhenibut'][351] = "Decreased"  #  Kratom, phenibut
draCI['ChangeUseOthers'][353] = "Hasn't changed" #  Synthetic stimulants ( amph and Cath)
draCI['ChangeUseOthers'][359] = "Greatly increased" #  ambien
draCI['ChangeUsePhenibut'][368] = "Greatly increased" #   Phenibut
draCI['ChangeUseOpioids'][370] = "Hasn't changed" #   kratom
draCI['ChangeUseOthers'][379] = "Greatly increased" #   Gabapentin and adderall(prescribed)
draCI['ChangeUseOthers'][397] = "Increased" #   4f-mph
draCI['ChangeUseOthers'][401] = "Greatly increased" #   2-FMA, 3-MMC, mianserin 
draCI['ChangeUseOpioids'][411] = "Greatly increased" #   Kratom 
draCI['ChangeUseOpioids'][450] = "Increased" #   Tramadol
draCI['ChangeUseOthers'][458] = "Decreased" #   pregabalin
draCI['ChangeUseOthers'][484] = "Increased" #   Dimenhydrinate and caffein
draCI['ChangeUseOthers'][500] = "Greatly increased" #   Crack cocaine
draCI['ChangeUseGHBL'][540] = "Hasn't changed" #   Gamma Hydroxybutyrate
draCI['ChangeUseOpioids'][546] = "Increased" #   Kratom
draCI['ChangeUseOthers'][547] = "Greatly increased" #   NEP
       
draCI['ChangeUseGHBL'][556] = "Hasn't changed" #   GHB
draCI['ChangeUseOthers'][637] = "Hasn't changed" #   3-MMC
draCI['ChangeUseLSD'][647] = "Greatly decreased" #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['ChangeUseKet'][647] = "Greatly decreased" #   I plan on the judicious and sub-psychedelic use of ketamine/LSD to help manage my depression and anxiety. 
draCI['ChangeUseOthers'][697] = "Increased" #   Salvia, mescaline
draCI['ChangeUsePhenibut'][713] = "Increased" #   Phenibut
draCI['ChangeUseOthers'][728] = "Greatly increased" #   Gabapentinoids
draCI['ChangeUsePhenibut'][730] = "Hasn't changed" #   Phenibut
draCI['ChangeUseOthers'][771] = "Greatly increased" #   Buprenorphine
draCI['ChangeUseOpioids'][777] = "Increased" #   Kratom
draCI['ChangeUseOpioids'][778] = "Increased" #   Kratom Daily 2x11.5g
draCI['ChangeUseOthers'][780] = "Greatly increased" #   3-MMC, N-Ethylhexedrone
draCI['ChangeUseOthers'][798] = "Hasn't changed" #   Salvia divinorum 
draCI['ChangeUseGHBL'][818] = "Hasn't changed" #   gbl 
draCI['ChangeUseOthers'][822] = "Increased" #   nutmeg
draCI['ChangeUseOthers'][836] = "Increased" #   wild dagga
draCI['ChangeUse2C_X'][861] = "Hasn't changed" #   2C-B (nexus)
draCI['ChangeUseOthers'][874] = "Hasn't changed" #   prescribed depression meds
draCI['ChangeUseOthers'][929] = "Increased" #   Quetiapine
draCI['ChangeUseOthers'][956] = "Increased" #   Ayahuasca, San Pedro, Coca Leaves
draCI['ChangeUseCocaine'][956] = "Increased" #   Ayahuasca, San Pedro, Coca Leaves
draCI['ChangeUseOthers'][1112] = "Hasn't changed" #  Nutmeg
draCI['ChangeUsePhenibut'][1135] = "Greatly decreased" #  Phenibut
draCI['ChangeUseOthers'][1214] = "Increased" #  3-meo-pcp
draCI['ChangeUseOpioids'][1237] = "Hasn't changed" #  Kratom
draCI['ChangeUseGHBL'][1278] = "Hasn't changed" #  Ghb
draCI['ChangeUseOthers'][1299] = "Hasn't changed" #  tetrahydroharmine, kanna, blue lotus, 
draCI['ChangeUseCann'][1300] = "Increased" #  CBD
draCI['ChangeUseGHBL'][1321] = "Hasn't changed" #  GHB
draCI['ChangeUseGHBL'][1347] = "Greatly decreased" #  Ghb
draCI['ChangeUseOthers'][1358] = "Greatly increased" #  3MMC
draCI['ChangeUseBenzos'][1386] = "Increased" #  1.5x doses of Xanax to achieve altered state
draCI['ChangeUseGHBL'][1415] = "Increased" #  G
draCI['ChangeUseOthers'][1444] = "Increased" #  Cyclobenzaprine (muscle relaxers)
draCI['ChangeUseOthers'][1458] = "Hasn't changed" #  pregabalin
draCI['ChangeUseOthers'][1459] = "Greatly increased" #  Mescaline
draCI['ChangeUseOpioids'][1463] = "Greatly increased" #  Kratom
draCI['ChangeUsePhenibut'][1471] = "Decreased" #  Phenibut
draCI['ChangeUseOpioids'][1472] = "Hasn't changed" #  kratom
draCI['ChangeUseOthers'][1500] = "Increased" #  SNRI
draCI['ChangeUseOthers'][1502] = "Increased" #  3-MMC, 4-CMC
draCI['ChangeUseOthers'][1512] = "Increased" #  salvia, GBL
draCI['ChangeUseGHBL'][1512] = "Increased" #  salvia, GBL
draCI['ChangeUseBenzos'][1546] = "Increased" #  xanax
draCI['ChangeUseOthers'][1581] = "Hasn't changed" #  4f-MPH
draCI['ChangeUseOpioids'][1585] = "Increased" # Cyclobenzaprine, kratom
draCI['ChangeUseOthers'][1585] = "Increased" #  Cyclobenzaprine, kratom
draCI['ChangeUseOthers'][1594] = "Increased" #  Lyrica (pregabalin), Bronkaid (ephedrine), tons of energy drinks
draCI['ChangeUseOthers'][1596] = "Increased" #  LSA
draCI['ChangeUseOpioids'][1612] = "Increased" #  Kratom
draCI['ChangeUseGHBL'][1613] = "Hasn't changed" #  GHB
draCI['ChangeUseOthers'][1615] = "Increased" #  DPH

draCI['ChangeUseOthers'][1617] = "Hasn't changed" #  Kanna
draCI['ChangeUseOthers'][1633] = "Greatly increased" #  SOMA, GHB
draCI['ChangeUseGHBL'][1633] = "Greatly increased" #  SOMA, GHB
draCI['ChangeUseOpioids'][1638] = "Greatly increased" #  Kratom
draCI['ChangeUseOpioids'][1655] = "Increased" #  Kratom
draCI['ChangeUseOthers'][1692] = "Greatly increased" #  Dph
draCI['ChangeUseGHBL'][1699] = "Hasn't changed" #  Ghb
draCI['ChangeUseOthers'][1710] = "Increased" #  Nutmeg
draCI['ChangeUseOthers'][1712] = "Greatly increased" #  Miscellaneous inhalants
draCI['ChangeUseCann'][1722] = "Increased" #  cbd
draCI['ChangeUseOthers'][1729] = "Hasn't changed" #  Pregabalin
draCI['ChangeUseOpioids'][1731] = "Hasn't changed" #  Kratom 
draCI['ChangeUseOthers'][1735] = "Hasn't changed" #  Gabapentin 
draCI['ChangeUseOthers'][1744] = "Increased" #  25I-NBOMe
draCI['ChangeUseOthers'][1755] = "Increased" #  Pregabalin
draCI['ChangeUseOpioids'][1776] = "Increased" #  Codiene
draCI['ChangeUseOthers'][1809] = "Increased" #  Why is my boy O-PCE not here😤
draCI['ChangeUseCann'][1822] = "Greatly increased" #  Weed
draCI['ChangeUseOpioids'][1832] = "Hasn't changed" #  Kratom, deschloroketamine, 4F-MPH 
draCI['ChangeUseOthers'][1832] = "Hasn't changed" #  Kratom, deschloroketamine, 4F-MPH 
draCI['ChangeUseOpioids'][1887] = "Increased" #  Kratom
draCI['ChangeUseOthers'][1890] = "Greatly increased" #  LSA
draCI['ChangeUseOpioids'][1892] = "Hasn't changed" #  Kratom
draCI['ChangeUseOpioids'][1901] = "Greatly decreased" #  Hydrocodone 
draCI['ChangeUseGHBL'][1907] = "Greatly increased" #  Gbl
draCI['ChangeUseGHBL'][1911] = "Increased" #  Ghb/GBL
draCI['ChangeUseOpioids'][1918] = "Decreased" #  kratom
draCI['ChangeUseOthers'][1922] = "Increased" #  DPH
draCI['ChangeUseBenzos'][1923] = "Greatly increased" #  Etizolam 
draCI['ChangeUseOthers'][1929] = "Hasn't changed" #  Belladonna 
draCI['ChangeUseOpioids'][1947] = "Greatly increased" #  Kratom
draCI['ChangeUseOthers'][1949] = "Greatly increased" #  4-fma
draCI['ChangeUseOthers'][1954] = "Increased" #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['ChangeUseGHBL'][1954] = "Increased" #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['ChangeUsePhenibut'][1954] = "Increased" #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['ChangeUseOpioids'][1954] = "Increased" #  kratom, phenibut, caffeine, GHB, “1,4 BDO”
draCI['ChangeUseOthers'][1966] = "Greatly increased" #  Quetiapine
draCI['ChangeUseCann'][1968] = "Decreased" #  Weed
draCI['ChangeUseOpioids'][1995] = "Hasn't changed" #  Daily kratom use
draCI['ChangeUseOthers'][2016] = "Hasn't changed" #  Cathinones
draCI['ChangeUseOthers'][2025] = "Greatly increased" #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['ChangeUsePhenibut'][2025] = "Greatly increased" #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['ChangeUseOpioids'][2025] = "Greatly increased" #  Phenibut, kratom, kava, Phenylpiracetam 
draCI['ChangeUseOthers'][2045] = "Increased"  #  Salvia divinorum
draCI['ChangeUseOthers'][2058] = "Increased" #  RCs
draCI['ChangeUseOthers'][2076] = "Hasn't changed" #  Caffeine
draCI['ChangeUseCann'][2170] = "Greatly decreased" #  Hash
draCI['ChangeUseOthers'][2248] = "Decreased" #  Speed (base)
draCI['ChangeUseOthers'][2320] = "Hasn't changed" #  MXE, MPA
draCI['ChangeUseCann'][2378] = "Increased" #  THC oil vape 
draCI['ChangeUseOthers'][2383] = "Greatly increased" #  drone
draCI['ChangeUseOthers'][2421] = "Greatly increased" #  Promethazine

#IGNOREE 2407            Decreased
#IGNOREE 2414       Hasn't changed
#IGNOREE 2420            Decreased
#IGNOREE 2421    
#IGNOREE 2425    Greatly decreased
#IGNOREE 2427       Hasn't changed
#IGNOREE 2436       Hasn't changed
#IGNOREE 2458    Greatly decreased

#IGNORE 346  So many drugs
#IGNORE 156  Cannabis should'nt really be on this list. 
#IGNORE 227  jhkh
#IGNORE 241  Was gonna try acid but they were duds
#IGNORE 329  By "opioids" I mean strictly kratom. I do not use any other drugs in that class.
#IGNORE 337  you should add xanax under benzodiazepines in case people are unsure what it is. altho every time i take xanax i am somewhat unsure of what it is #pressed🙏
#IGNORE 408  Private
#IGNORE 474  Alcohol
#IGNORE 515  With ex partner 
#IGNORE 638  Alcohol and nicotine
#IGNORE 1386 3
#IGNORE 824  No other, but I want to say that this comsumptions is not recreational, but for health. It's not precise to consider illegal drugs only as "recreational"
#IGNORE 1967 Probably going to do LSD again soon but I need to straighten out my prescription meds first
#IGNORE 2127 Alcohol
#IGNORE 2407 Alcohol
#IGNORE 2414 None
#IGNORE 2420 None
#IGNORE 2425 None
#IGNORE 2427 Alcohol
#IGNORE 2436 None
#IGNORE 2458 None since the outbreak started
#IGNORE 2468 none


# %% Amend which drugs wanna stop taking
ind_col_StopDru = np.where(col_names == 'StopDrugs')
cols_StopDru = col_names[ind_col_StopDru[0][0]:(ind_col_StopDru[0][0] + 24)]


draCI.rename(columns={'StopDrugs':        'StopDru2C_X',          
                      'Unnamed: 299':     'StopDruAdderall', 
                      'Unnamed: 300':     'StopDruAlc',
                      'Unnamed: 301':     'StopDruAmphe',    
                      'Unnamed: 302':     'StopDruBenzos',    
                      'Unnamed: 303':     'StopDruCannabis',  
                      'Unnamed: 304':     'StopDruCaffeine', 
                      'Unnamed: 305':     'StopDruCoke',   
                      'Unnamed: 306':     'StopDruMeth',   
                      'Unnamed: 307':     'StopDruDMT',   
                      'Unnamed: 308':     'StopDruDXM',   
                      'Unnamed: 309':     'StopDruIbo',   
                      'Unnamed: 310':     'StopDruKet',   
                      'Unnamed: 311':     'StopDruLSD',   
                      'Unnamed: 312':     'StopDruShrooms',
                      'Unnamed: 313':     'StopDruMDMA',
                      'Unnamed: 314':     'StopDruModafinil',
                      'Unnamed: 315':     'StopDruMAOIs',   
                      'Unnamed: 316':     'StopDruNicotine',
                      'Unnamed: 317':     'StopDruNO',
                      'Unnamed: 318':     'StopDruOpioids',
                      'Unnamed: 319':     'StopDruSSRIs',
                      'Unnamed: 320':     'StopDruPoppers',
                      'Unnamed: 321':     'StopDruOthers'
                    },  
          inplace=True, errors='raise')

names = [ '2C-X (e.g. 2C-B, 2C-E, 2CB-FLY)', 'Adderall or Ritalin', 'Alcohol', 'Amphetamine (also known as ‘speed’ but NOT crystal methamphetamine)', 
          'Benzos (e.g. Valium, Diazepam)', 'Cannabis (also known as weed/marijuana/skunk/grass)', 'Caffeine (coffee, tea, energy drinks)', 'Cocaine (also known as “Coke”, “Charlie”, “Snow”)', 
          'Crystal Meth', 'DMT (including Ayahuasca, Changa and 5-MeO-DMT)', 'DXM', 'Ibogaine (or Iboga)', 
          'Ketamine (also known as ‘K’, ‘Ket’, ‘Special K’)', 'LSD (also known as “Acid”)', 'Magic mushrooms (or other forms of Psilocybin, including 4-AcO-DMT)',
          'MDMA (also known as “MD”, “Ecstasy”, “Mandy”, “Molly”, “Magic”)', 'Modafinil', 'MAOIs (aka harmala alkaloids, e.g. Syrian Rue)', 'Nicotine (tobacco or nicotine vapes)',
          'Nitrous Oxide (also known as ‘balloons’ or ‘laughing gas’)', 'Opioids (e.g. heroin, morphine, fentanyl, methadone, oxycodone, opium)',
          'SSRIs (also known as antidepressants)', 'Poppers']

cols = ['StopDru2C_X','StopDruAdderall','StopDruAlc','StopDruAmphe',
        'StopDruBenzos', 'StopDruCannabis','StopDruCaffeine','StopDruCoke',
        'StopDruMeth','StopDruDMT','StopDruDXM','StopDruIbo','StopDruKet',
        'StopDruLSD','StopDruShrooms', 'StopDruMDMA', 'StopDruModafinil', 
        'StopDruMAOIs', 'StopDruNicotine', 'StopDruNO', 'StopDruOpioids', 
        'StopDruSSRIs', 'StopDruPoppers']
   
 
for c, n in zip(cols, names):
    binariseSimple(c, n)

boStopDru = draCI['StopDruOthers'].isnull()
indxStopDru = draCI['StopDruOthers'][~boStopDru].index

draCI['StopDruOthers'] = 0

#IGNORE 204   I 99% have ADHD which lead to depression (I just realized I was diagnosed as a kid, but in France ADHD in adult isn’t considered a true issue... and cannot consult a psychiatrist for it during the outbreak)
draCI['StopDruOthers'][216] = 1 # khat
draCI['StopDruOthers'][338] = 1 #    Pyrovalerones
draCI['StopDruOthers'][368] = 1 #    Phenibut
#IGNORE 434   steady safe reliable safe supply is nonexistent
draCI['StopDruOthers'][608] = 1 #    Tramadol
draCI['StopDruOthers'][877] = 1 #    Sugar
draCI['StopDruOthers'][878] = 1 #    Chocolate, snickers
draCI['StopDruOpioids'][1086] = 1 #   Buprenorphine subutex 
#IGNORE 1098  I’m sober
draCI['StopDruOthers'][1226] = 1 #   Sugar. Television. Pornography.
draCI['StopDruOpioids'][1236] = 1 #   kratom
draCI['StopDruOthers'][1321] = 1 #   GHB
#IGNORE 1386  None
draCI['StopDruNicotine'][1431] = 1  #   Nicotine
draCI['StopDruOpioids'][1463] = 1 #   Kratom
draCI['StopDruOthers'][1580] = 1 #   GHB
draCI['StopDruOthers'][1615] = 1 #   DPH
draCI['StopDruNicotine'][1628] = 1  #   Tabacco
draCI['StopDruOpioids'][1684] = 1 #   Kratom
draCI['StopDruOthers'][1692] = 1 #   Dph
draCI['StopDruOpioids'][1731] = 1 #   Kratom 
draCI['StopDruOpioids'][1896] = 1 #   kratom
draCI['StopDruOthers'][1907] = 1 #   Gbl
draCI['StopDruOthers'][1911] = 1 #   GHB/GBL
draCI['StopDruOpioids'][1931] = 1  #   suboxone
draCI['StopDruAlc'][1933] = 1  #   Alcohol
draCI['StopDruOpioids'][1947] = 1 #   Kratom
draCI['StopDruNicotine'][2203] = 1  #   Tabacco

#########################################################################################################
# %% Amend discouraged to seek help from organisation
ind_col_DisSupp = np.where(col_names == 'DiscourageSupport')
cols_DisSupp = col_names[ind_col_DisSupp[0][0]:(ind_col_DisSupp[0][0]+6)]

draCI.rename(columns={'DiscourageSupport':    'DisSuppLackAwa',          
                      'Unnamed: 333':         'DisSuppFearPun', 
                      'Unnamed: 334':         'DisSuppFearPol',    
                      'Unnamed: 335':         'DisSuppFearJudg',    
                      'Unnamed: 336':         'DisSuppNotSure',   
                      'Unnamed: 337':         'DisSuppOther',      
                    },  
          inplace=True, errors='raise')

names = [ 'Lack of awareness of what is available', 'Fear of punishment (eg exclusion, removal from studies)', 
            'Fear of the police being contacted', 'Fear of judgment', 'I don’t know']

cols = ['DisSuppLackAwa', 'DisSuppFearPun', 'DisSuppFearPol', 
        'DisSuppFearJudg', 'DisSuppNotSure']

boDisSupp = draCI['DisSuppOther'].isnull()
indxDisSupp = draCI['DisSuppOther'][~boDisSupp].index

draCI['DisSuppNoNeed'] = 0
draCI['DisSuppOther'] = 0
draCI['DisSuppFromOthers'] = 0
draCI['DisSuppNoTrust'] = 0

draCI['DisSuppNoNeed'][12] = 1 # Don’t feel the need for help as I’m not addicted
draCI['DisSuppNoNeed'][15] = 1 #    I don't want to
draCI['DisSuppNoNeed'][18] = 1 #    I don’t have a problem? It’s recreational 
draCI['DisSuppNoNeed'][20] = 1 #    I don't want their support.
draCI['DisSuppNoNeed'][27] = 1 #    I do not want “support” for my recreational activities
draCI['DisSuppOther'][28] = 1 #    I work for a Harm-Reduction service for U18
draCI['DisSuppOther'][29] = 1 #    my employer cant find their arse from their elbow, they can't even decide what their website should look like, I'd no more trust them to support a personal/drug problem than fly to the fucking moon
draCI['DisSuppNoNeed'][35] = 1 #    I don’t need support
draCI['DisSuppNoNeed'][37] = 1 #    I don’t use so much that I feel the need to contact support
draCI['DisSuppNoNeed'][40] = 1 #    I dont particularly feel the need since I dont feel dependant on any drug
draCI['DisSuppNoNeed'][44] = 1 #    I don't need it, but if I did I would dear kids of job due to revocation of security clearance
draCI['DisSuppNoNeed'][50] = 1 #    I don't feel I need support
draCI['DisSuppNoNeed'][52] = 1 #    I don't need support
draCI['DisSuppNoNeed'][61] = 1 #    Not in need of support. 
draCI['DisSuppNoNeed'][88] = 1 #    I just don’t think that I need support
draCI['DisSuppNoNeed'][92] = 1 #    I have no need to
draCI['DisSuppFromOthers'][100] = 1 #   There are many reputable drug information/mental health charities in the UK with expertise I don’t think UCL has
draCI['DisSuppFromOthers'][103] = 1 #   Have others supports if needed
draCI['DisSuppNoNeed'][104] = 1 #   i don't need support
draCI['DisSuppNoNeed'][109] = 1 #   I never used cannabis this frequently and never needed help. 
draCI['DisSuppFearJudg'][120] = 1 #   Fear that some of my lecturers would find out
draCI['DisSuppOther'][133] = 1 #   being forced to stop before steps were taken to minimize withdrawals or find other coping methods
draCI['DisSuppFromOthers'][138] = 1 #   Used to self-managing various issues through friends and research, generally find that 'official' channels can only work on their terms and I have a tendancy to fall out of schedules/miss meetings
draCI['DisSuppNoNeed'][148] = 1 #   I don't have a problem?
draCI['DisSuppNoNeed'][162] = 1 #   Don’t find it That much of an issue
draCI['DisSuppNoNeed'][165] = 1 #   Don’t feel I need it
draCI['DisSuppOther'][171] = 1 #   impossible to access - long waiting lists. 
draCI['DisSuppNoNeed'][174] = 1 #   I do not wish to seek university guidance for quitting smoking
draCI['DisSuppNoNeed'][175] = 1 #   Do not want support from my employer.
draCI['DisSuppFromOthers'][183] = 1 #   Rather seek support from friends or family 
draCI['DisSuppNoNeed'][185] = 1 #   Don’t feel it is necessary
draCI['DisSuppNoNeed'][190] = 1 #   I dont want it
draCI['DisSuppNoNeed'][192] = 1 #   Don't need any
draCI['DisSuppNoNeed'][205] = 1 #   i have no intention of making changes to my drug use
draCI['DisSuppOther'][212] = 1 #   My job is dependent on maintaining recovery 
draCI['DisSuppFearPun'][229] = 1 #   Losing Job
draCI['DisSuppNoNeed'][247] = 1 #   No reason to seek sipport
draCI['DisSuppNoNeed'][250] = 1 #   I don't feel I need support at this stage.
draCI['DisSuppNoNeed'][262] = 1 #   None of their business
draCI['DisSuppNoTrust'][265] = 1 #   They know nothing about drugs 
draCI['DisSuppFearPun'][271] = 1 #   I'd lose my job
draCI['DisSuppOther'][287] = 1 #   We do not touch this topics
draCI['DisSuppFearJudg'][289] = 1  #   Making others aware of my drug use, forced into treatment
draCI['DisSuppFearPun'][289] = 1  #   Making others aware of my drug use, forced into treatment
draCI['DisSuppNoNeed'][295] = 1 #   Not needing their support
draCI['DisSuppNoNeed'][297] = 1 #   Don’t feel the need
draCI['DisSuppNoNeed'][302] = 1 #   I don't want support
draCI['DisSuppOther'][312] = 1 #   My employer doesn't give a fuck
draCI['DisSuppNoNeed'][322] = 1 #   I don’t require support from my employer
draCI['DisSuppNoNeed'][332] = 1 #   I do not need it. I study and research Biochem and Pharmacology-Toxicology, I know what I'm doing.
draCI['DisSuppNoNeed'][701] = 1 #   Don’t want to
draCI['DisSuppNoNeed'][715] = 1 #   I don't feel the need to do so
draCI['DisSuppNoNeed'][727] = 1 #   I don't feel in need of it. In case I needed help I'd probably talk to friends and family first
draCI['DisSuppOther'][728] = 1 #   People never understand why I use those drugs, which most of them are prescribed 
#IGNORE 729  I don't do drugs
draCI['DisSuppFromOthers'][759] = 1 #   I have more reliable sources of information and usually do own research including anecdotes from friends and online harm reduction websites before taking any substance 
draCI['DisSuppNoNeed'][760] = 1 #   no need
draCI['DisSuppNoNeed'][763] = 1 #   I dont need support
draCI['DisSuppFearPol'][768] = 1 #   No one helps, they just call the cops
draCI['DisSuppNoNeed'][770] = 1 #   I don't need support, I use drugs responsibly
draCI['DisSuppNoNeed'][772] = 1 #   I don’t need help, not addicted 
draCI['DisSuppNoNeed'][773] = 1 #   Unnecessary
draCI['DisSuppNoNeed'][774] = 1 #   I don't need support because I don't have an issue
draCI['DisSuppNoNeed'][780] = 1 #   I am not in need of support
draCI['DisSuppNoNeed'][783] = 1 #   They don't care about it
draCI['DisSuppNoNeed'][790] = 1 #   I don't want support. 
draCI['DisSuppNoNeed'][794] = 1 #   I m not looking for any help
draCI['DisSuppNoTrust'][803] = 1 #   Non-adequate reaction, knowledge or support
draCI['DisSuppNoNeed'][828] = 1 #   don't need support at the moment
draCI['DisSuppFromOthers'][831] = 1 #   I do not think this is where on should look for support
draCI['DisSuppNoTrust'][845] = 1 #   I don't think it would be helpful/quality
draCI['DisSuppNoTrust'][846] = 1 #   I know more than they do
draCI['DisSuppNoNeed'][853] = 1 #   My drug use isn't a problem and I don't need the help.
draCI['DisSuppNoNeed'][855] = 1 #   I don't care
draCI['DisSuppOther'][873] = 1 #   I don`t want to share about these type of things cause it`s not for everyone and I don`t want to influence people do this things if they are not ready :)
draCI['DisSuppFromOthers'][874] = 1 #   I have a great therapist.
draCI['DisSuppNoNeed'][881] = 1 #   I do not feel I need support
draCI['DisSuppNoNeed'][885] = 1 #   I have no fear, as I only use marijuana.
draCI['DisSuppNoNeed'][890] = 1 #   I don't need support 
draCI['DisSuppNoNeed'][899] = 1 #   not necessary
draCI['DisSuppNoNeed'][901] = 1 #   I don't think I need a support
draCI['DisSuppFearPun'][907] = 1 #   I would lose my job! 
draCI['DisSuppNoNeed'][909] = 1 #   I don't need support other than quiting smoking
draCI['DisSuppNoNeed'][910] = 1 #   Don’t need it
draCI['DisSuppNoNeed'][913] = 1 #   I don't think I need support
draCI['DisSuppNoNeed'][916] = 1 #   It’s my personal life
draCI['DisSuppFromOthers'][924] = 1 #   There are plenty of other places to get support i.e party people & harm redux orgs 
draCI['DisSuppFromOthers'][930] = 1 #   We have an independent counsellor service but I wouldnt use it for substance issues. Prefer to find my own person as EAP is pretty superficial.
draCI['DisSuppNoNeed'][945] = 1 #   it's not needed
draCI['DisSuppNoNeed'][955] = 1 #   My drug use isn't a problem
draCI['DisSuppNoNeed'][957] = 1 #   Don't feel the need to
draCI['DisSuppFearPol'][959] = 1  #   Fear of jail
draCI['DisSuppNoNeed'][974] = 1 #   Not everyone who enjoys drugs is masking an issue that needs support
draCI['DisSuppNoNeed'][984] = 1 #   I’m fine
draCI['DisSuppNoNeed'][987] = 1 #   i dont need one
draCI['DisSuppNoTrust'][995] = 1 #   They have no clue.
draCI['DisSuppNoTrust'][996] = 1 #   I don't think they would offer me any support.
draCI['DisSuppNoNeed'][1016] = 1 #  no point
draCI['DisSuppNoNeed'][1017] = 1 #  I do not require support but would seek help if use became an unhealthy crutch.
draCI['DisSuppOther'][1022] = 1 #  I am generally a private person
draCI['DisSuppNoNeed'][1031] = 1 #  Not discouraged as I don't need support 
draCI['DisSuppNoNeed'][1032] = 1 #  Doesn’t really affect my work life
draCI['DisSuppNoNeed'][1067] = 1 #  I have no problems with drug abuse whatsoever
draCI['DisSuppNoNeed'][1092] = 1 #  I don't need it
draCI['DisSuppFromOthers'][1101] = 1 #  I don't that kind of support, can handle things on my own, if were to ask support it would be from friends of relatives
draCI['DisSuppNoNeed'][1109] = 1 #  I don't need support
draCI['DisSuppNoNeed'][1116] = 1 #  Really dont need to talk about weed and alcohol
draCI['DisSuppNoNeed'][1127] = 1 #  I don't see it as a problem , I don't drink and I'm seen at the one at work who should engage in heavy drink more in outtings and social events but I dislike feeling out of control 
draCI['DisSuppFearJudg'][1147] = 1  #  It would change the opinion of my colleagues towards me
draCI['DisSuppNoNeed'][1149] = 1 #  Not sure if needed.
draCI['DisSuppOther'][1152] = 1 #  Nothing is available
draCI['DisSuppNoTrust'][121159] = 1 #  my now ex coworkers were cokeheads, they dont care about anyone elses drug use, all they care about is getting dust
draCI['DisSuppNoNeed'][1160] = 1 #  Don't currently need to
draCI['DisSuppFearPun'][1170] = 1 #  it's illegal
draCI['DisSuppNoNeed'][1175] = 1 #  I dont need it
draCI['DisSuppFearPun'][1208] = 1 #  I might lose job
draCI['DisSuppNoTrust'][1217] = 1 #  The university treats me like a number therefore they don’t need to know about my life/dependencies 
draCI['DisSuppNoTrust'][1226] = 1 #  Whilst I was at University I wasn't even aware that I had a drinking problem. It was plain to see but there was no support. The lecturers taught and then fucked off without caring much to help in any pastoral sense
draCI['DisSuppNoNeed'][1231] = 1  #  I dont need support from these facilities. I have peer support
draCI['DisSuppFromOthers'][1231] = 1 #  I dont need support from these facilities. I have peer support
draCI['DisSuppNoNeed'][1237] = 1 #  Not needed
draCI['DisSuppNoNeed'][1238] = 1 #  No need
draCI['DisSuppNoNeed'][1247] = 1 #  There is no need to. 
draCI['DisSuppNoNeed'][1249] = 1 #  Don't feel the need for support
draCI['DisSuppNoNeed'][1253] = 1 #  I'm not looking for any support 
draCI['DisSuppNoNeed'][1255] = 1 #  Not needed 
draCI['DisSuppNoTrust'][1259] = 1 #  Feel like there isn’t good support offered 
draCI['DisSuppOther'][1263] = 1 #  Always too fucked to get out of bed and seek help :(
draCI['DisSuppNoNeed'][1266] = 1 #  Support not needed 
draCI['DisSuppNoNeed'][1277] = 1 #  I do not need support
draCI['DisSuppFearJudg'][1278] = 1  #  Stigma, prejudice against substances other than alcohol
draCI['DisSuppNoNeed'][1282] = 1 #  I don't use a lot of drugs 
draCI['DisSuppNoNeed'][1283] = 1 #  I don’t feel it is a problem
draCI['DisSuppNoNeed'][1288] = 1 #  I don't have a problem
draCI['DisSuppNoNeed'][1292] = 1 #  None of their business
draCI['DisSuppNoNeed'][1339] = 1 #  I don’t feel I need specific support
draCI['DisSuppNoNeed'][1341] = 1 #  no need
draCI['DisSuppNoTrust'][1360] = 1 #  Expectation that they wouldn't have any useful information or support.
draCI['DisSuppNoNeed'][1386] = 1 #  I don’t need it
draCI['DisSuppNoNeed'][1391] = 1 #  Don't trust the emoloyer to have a meaningful insight
draCI['DisSuppNoNeed'][1392] = 1 #  I don't need support 
draCI['DisSuppNoNeed'][1405] = 1 #  I don't feel I nded any support
draCI['DisSuppNoNeed'][1411] = 1 #  No need for harm reduction with level of use
draCI['DisSuppNoNeed'][1413] = 1 #  I’d rather talk to my family or friends
draCI['DisSuppNoNeed'][1414] = 1 #  I don’t feel my use warrants help
draCI['DisSuppNoNeed'][1416] = 1 #  I do once in a year
draCI['DisSuppFromOthers'][1420] = 1 #  I don't need support, b/c my drug use doesn't have an adverse effect on my work. However, *IF* I wanted support, all those things would be reasons not to contact my employer about it. Also, my driver's license would get revoked if some regulatory body would know about my drug use.
draCI['DisSuppFearPun'][1455] = 1 #  fear it would impact future employment opportunities
draCI['DisSuppNoNeed'][1459] = 1 #  No need for support
draCI['DisSuppNoNeed'][1474] = 1 #  I don’t need support. It’s not a problem. Work and college have no business in anything I do outside.
draCI['DisSuppNoNeed'][1475] = 1 #  don’t feel that i need outside support
draCI['DisSuppNoNeed'][1479] = 1 #  dont feel its necessary
draCI['DisSuppNoNeed'][1492] = 1 #  I don’t need help or support!
draCI['DisSuppNoNeed'][1506] = 1 #  Don't feel the need to, yet
draCI['DisSuppNoNeed'][1510] = 1 #  I don’t need support
draCI['DisSuppFearPun'][1511] = 1 #  Very Zero Tolerance if found to have drugs in possession at university immediate expulsion 
draCI['DisSuppNoTrust'][1512] = 1 #  doubtful of knowledgeable help
draCI['DisSuppFearJudg'][1519] = 1  #  The stigma and taboo of drug use 
draCI['DisSuppNoNeed'][1528] = 1 #  Don't have issues with addiction
draCI['DisSuppNoNeed'][1532] = 1 #  Not required
draCI['DisSuppNoNeed'][1539] = 1 #  I don’t need support as I’m not addicted or dependant on anything.
draCI['DisSuppNoNeed'][1548] = 1 #  because i dont want to caz i feel good with myself 
draCI['DisSuppFromOthers'][1550] = 1 #  I can cope with my mental state by myself and the support from my friends.
draCI['DisSuppFearPun'][1558] = 1 #  They drug test and sack people for it 
draCI['DisSuppFromOthers'][1567] = 1 #  would rather go to a professional 
draCI['DisSuppNoTrust'][1571] = 1 #  They’ve no experience 
draCI['DisSuppFearPun'][1581] = 1 #  They'd fire my ass.
draCI['DisSuppFromOthers'][1583] = 1 #  I have psychiatrist 
draCI['DisSuppNoNeed'][1588] = 1 #  I am not addicted or dependent on any drug, I don't need my employers help with that. 
draCI['DisSuppNoNeed'][1600] = 1 #  no desire 
draCI['DisSuppNoNeed'][1608] = 1 #  Don’t need it
draCI['DisSuppNoNeed'][1612] = 1 #  Not in need of support
draCI['DisSuppNoNeed'][1614] = 1 #  I don’t need support 
draCI['DisSuppNoNeed'][1617] = 1 #  I don't feel I have a problem
draCI['DisSuppNoNeed'][1621] = 1 #  I don't feel I need support
draCI['DisSuppNoNeed'][1636] = 1 #  don’t need it
draCI['DisSuppNoNeed'][1642] = 1 #  I don't need support
draCI['DisSuppNoNeed'][1654] = 1 #  Haven't needed support.
draCI['DisSuppNoNeed'][1655] = 1 #  I don’t feel the need for support; my organization would be very supportive if I did though
#IGNORE 1661 lol
draCI['DisSuppNoTrust'][1670] = 1 #  Lack of adequate medical care available
draCI['DisSuppNoNeed'][1679] = 1 #  Not required 
draCI['DisSuppFromOthers'][1688] = 1 #  i just wouldn't ask for help at university as a first option, i'd reach a friend first
draCI['DisSuppNoNeed'][1690] = 1 #  I don't think I need it (yet)
draCI['DisSuppNoNeed'][1696] = 1 #  don’t want if
draCI['DisSuppNoNeed'][1698] = 1 #  It’s not at a bad point where I would need to seek any support
draCI['DisSuppNoNeed'][1705] = 1 #  i don’t believe i need support because my drug use isn’t out of hand 
draCI['DisSuppNoNeed'][1714] = 1 #  I use drugs for fun. I don’t see a reason to tell my university I enjoy drugs. 
draCI['DisSuppNoNeed'][1716] = 1 #  No need
draCI['DisSuppNoNeed'][1728] = 1 #  dont need it
draCI['DisSuppNoNeed'][1733] = 1 #  Their limited knowledge and biased/cliché opinions
draCI['DisSuppNoNeed'][1736] = 1 #  Don’t feel it is necessary 
draCI['DisSuppNoNeed'][1740] = 1 #  I don’t believe I need it, but if I did I wouldn’t be bothered enough
draCI['DisSuppFearPun'][1764] = 1 #  my narcologist warned me that i'll get expelled if i seek for support
draCI['DisSuppFromOthers'][1769] = 1 #  I have my family which supports me
draCI['DisSuppFearPun'][1770] = 1 #  Losing my job
draCI['DisSuppNoNeed'][1781] = 1 #  Not necessary. 
draCI['DisSuppNoNeed'][1785] = 1 #  I feel it is under control and I am sensible
draCI['DisSuppNoNeed'][1834] = 1 #  I don’t feel like 
draCI['DisSuppNoNeed'][1844] = 1 #  General control over my habbits
draCI['DisSuppFromOthers'][1847] = 1 #  Id go to a psychiatrist or psychologist 
draCI['DisSuppOther'][1858] = 1 #  It’s a personal problem that I need to manage my time better 
draCI['DisSuppNoNeed'][1861] = 1 #  don’t feel i need to
#IGNORE 1886 Other
draCI['DisSuppNoNeed'][1901] = 1 #  I don’t care if they know, but I’m not going to willingly tell them otherwise
draCI['DisSuppNoNeed'][1904] = 1 #  I feel I do not require the resources offered
draCI['DisSuppNoNeed'][1909] = 1 #  why would i?
draCI['DisSuppNoTrust'][1915] = 1 #  their resources are not helpful
draCI['DisSuppFearPun'][1919] = 1 
draCI['DisSuppNoTrust'][1919] = 1 # 1919 I was actually arrested on campus and had to do this, I wouldn't recommend it to anyone at University of North Dakota because they dont know shit about drugs.
draCI['DisSuppNoTrust'][1927] = 1 #  Lack of available resources, councillors aren't very educated on substance abuse
draCI['DisSuppNoNeed'][1929] = 1 #  I don't need support. 100% of my drug misuse can be traced back to simply being broke. Other kinds of support would not suffice.
draCI['DisSuppFearPun'][1931] = 1 #  losing my job
draCI['DisSuppNoNeed'][1936] = 1 #  I don’t want/need help 
draCI['DisSuppFromOthers'][1942] = 1 #  Would seek help some other place
draCI['DisSuppOther'][1943] = 1 #  I don’t feel like they should be involved
draCI['DisSuppNoNeed'][1946] = 1 #  I don't feel I need to seek support
draCI['DisSuppNoNeed'][1951] = 1 #  I would lose my job as apprentice
draCI['DisSuppFromOthers'][1954] = 1 #  i don’t need help from them. if i wanted help, i could get it elsewhere. 
draCI['DisSuppNoNeed'][1958] = 1 #  I don't need any kind of support.  This is a weirdly biased survey.
draCI['DisSuppFromOthers'][1959] = 1 #  I would rather go to someone else, like a family member or a friend
draCI['DisSuppNoNeed'][1971] = 1 #  I don’t need support 
draCI['DisSuppNoTrust'][1972] = 1 #  Their ignorance 
draCI['DisSuppNoNeed'][1978] = 1 #  dont want it
draCI['DisSuppNoNeed'][1986] = 1 #  I don't need any support since I am not addicted
draCI['DisSuppNoNeed'][1991] = 1 #  I don't have a reason to seek that, I don't have a problem with drugs. I am responsible, I take drugs only when I can. I think that it is my privacy 
draCI['DisSuppFearPun'][1995] = 1 #  Fear of losing my job, due to the nature of the work I do.
draCI['DisSuppOther'][2025] = 1 #  I’m a psych major, been through rehab, been through the programs. Not helpful for me. If I want to quit it has to be my decision, nothing else works. 
draCI['DisSuppNoTrust'][2029] = 1 #  Lack of understanding of substance use in the institution.
draCI['DisSuppNoNeed'][2042] = 1 #  I don't feel I need any nor do I believe it would be available if I needed it.  I sell alcohol and am a non-drinker.
draCI['DisSuppOther'][2051] = 1 #  Employers interests do not align
draCI['DisSuppNoNeed'][2055] = 1 #  Unneeded
draCI['DisSuppNoNeed'][2064] = 1 #  I don’t want support
draCI['DisSuppNoNeed'][2085] = 1 #  I don't want support
draCI['DisSuppNoNeed'][2090] = 1 #  i don’t need it 
draCI['DisSuppNoNeed'][2102] = 1 #  Don't require support
draCI['DisSuppNoNeed'][2114] = 1 #  i dont need to at the moment
draCI['DisSuppNoNeed'][2128] = 1 #  I don't feel my use is problematic - is only recreationally and does not impact on my work/personal life negatively.  I would never go to work or study under the influence of substances & never have.
draCI['DisSuppNoNeed'][2146] = 1 #  Lack of need
draCI['DisSuppFearPun'][2162] = 1 #  parents would find out
draCI['DisSuppNoNeed'][2165] = 1 #  Absolutely no need 
draCI['DisSuppNoNeed'][2172] = 1 #  I don’t need support 
draCI['DisSuppNoNeed'][2188] = 1 #  I don’t need support, but if I did, I wouldn’t got to my workplace or university
draCI['DisSuppNoNeed'][2194] = 1 #  information available online
draCI['DisSuppNoNeed'][2202] = 1 #  I like smoking cannabis and I don't want to stop. 
draCI['DisSuppNoNeed'][2225] = 1 #  It’s manageable 
draCI['DisSuppNoNeed'][2230] = 1 #  I do not feel needed. 
draCI['DisSuppFromOthers'][2239] = 1 #  It feels private. I would have better support elsewhere (family, friends, specialists).
draCI['DisSuppFearPun'][2245] = 1 #  Get fired loose job !
draCI['DisSuppNoNeed'][2248] = 1 #  none of their business
draCI['DisSuppNoNeed'][2253] = 1 #  Personal life is none of the employers business as long as it doesnt affect my work ethic and flow.
draCI['DisSuppNoNeed'][2260] = 1 #  Don't smoke enough weed to merit seeking support
draCI['DisSuppNoNeed'][2264] = 1 #  I self-limit my drug intake, and i don't need support
draCI['DisSuppNoNeed'][2266] = 1 #  I don't need support
draCI['DisSuppFearPun'][2270] = 1 #  Zero tolarance and get tested
draCI['DisSuppNoNeed'][2278] = 1 #  I don’t feel that I need support
draCI['DisSuppNoNeed'][2291] = 1 #  Not in need of support, I am in control
draCI['DisSuppNoNeed'][2307] = 1 #  i don’t feel that it’s necessary 
draCI['DisSuppNoNeed'][2311] = 1 #  I don’t need to, I can educate myself. 
draCI['DisSuppNoNeed'][2319] = 1 #  Dont think I need to seek support
draCI['DisSuppNoNeed'][2326] = 1 #  Doesn’t constitute a problem for me, I took it once a month but not anymore.
draCI['DisSuppNoNeed'][2334] = 1 #  Dont want support 
draCI['DisSuppNoNeed'][2347] = 1 #  They don’t need to know
draCI['DisSuppOther'][2357] = 1 #  My alcohol problems push me back
draCI['DisSuppNoNeed'][2359] = 1 #  don't feel like I need it 
draCI['DisSuppNoNeed'][2372] = 1 #  I don’t feel I need support as I have a sensible relationship with alcohol and other drugs I choose to use recreationally
draCI['DisSuppFearPun'][2374] = 1 #  It is illegal and I would be fired 
draCI['DisSuppNoNeed'][2378] = 1 #  I am not addicted I smoke thc vape once in a while
draCI['DisSuppNoNeed'][2386] = 1 #  I dont wish to seek support
draCI['DisSuppOther'][2396] = 1 #  Very small organisation
draCI['DisSuppNoNeed'][2398] = 1 #  I don’t need it
draCI['DisSuppNoNeed'][2403] = 1 #  Don't need it
draCI['DisSuppNoNeed'][2415] = 1 #  Don’t need to as I know resources myself 
draCI['DisSuppNoNeed'][2420] = 1 #  I don’t need any
draCI['DisSuppFearPun'][2422] = 1 #  Chance of not being taken on after apprenticeship
draCI['DisSuppNoTrust'][2438] = 1 #  They are not very knowledgeable about this topic 
draCI['DisSuppNoNeed'][2447] = 1 #  It being under control
draCI['DisSuppNoNeed'][2451] = 1 #  I am not addicted 
draCI['DisSuppFearPun'][2455] = 1 #  Being sent to student support so counciling and ringing parents 
draCI['DisSuppNoNeed'][2461] = 1 #  I don't want to

# %% Amend encouraged to seek help from organisation 
ind_col_EnSupp = np.where(col_names == 'EncourageSupport')
cols_EnSupp = col_names[ind_col_EnSupp[0][0]:(ind_col_EnSupp[0][0]+6)]

draCI.rename(columns={'EncourageSupport':    'EncSuppOpenDeb',          
                      'Unnamed: 339':        'EncSuppRedStig', 
                      'Unnamed: 340':        'EncSuppDrugPoli',    
                      'Unnamed: 341':        'EncSuppHR',    
                      'Unnamed: 342':        'EncSuppNotSure',   
                      'Unnamed: 343':        'EncSuppOther',      
                    },  
          inplace=True, errors='raise')

names = ['An open debate about drug use', 'Reduced social stigma surrounding drugs',
        'A wellness oriented drug policy (as opposed to a punitive one)',
        'Non-judgemental and accessible harm reduction/wellbeing events',
        'I’m not sure']

cols = [ 'EncSuppOpenDeb', 'EncSuppRedStig', 
            'EncSuppDrugPoli', 'EncSuppHR', 'EncSuppNotSure']

    
for c, n in zip(cols, names):
    binariseSimple(c, n)

boEncSupp = draCI['EncSuppOther'].isnull()
indxEncSupp = draCI['EncSuppOther'][~boEncSupp].index

draCI['EncSuppNoNeed'] = 0
draCI['EncSuppNothing'] = 0
draCI['EncSuppServices'] = 0
draCI['EncSuppOther'] = 0

draCI['EncSuppNoNeed'][11] = 1 # nothing on earth
draCI['EncSuppServices'][12] = 1  # Stronger mental health team
#IGNORE 18    ...
draCI['EncSuppNoNeed'][27] = 1 #     None—it’s none of their business 
draCI['EncSuppNoNeed'][35] = 1 #     If I needed support 
draCI['EncSuppNoNeed'][37] = 1 #     If I felt like I needed support
draCI['EncSuppDrugPoli'][44] = 1  #     Nothing, given I don't need it and if I did it would require complete change of policy and maybe legislation - not going to happen
draCI['EncSuppDrugPoli'][89] = 1  #     No cops 
draCI['EncSuppServices'][100] = 1  #    Generally support services don’t seem to be that visible at UCL in my opinion
#IGNORE 121   N/a
draCI['EncSuppNoNeed'][131] = 1 #    If I needed help 
draCI['EncSuppDrugPoli'][136] = 1  #    True anonymity is the ONLY reason I would be okay sharing my drug use with my school
draCI['EncSuppNoNeed'][205] = 1 #    i have no intention of making changes to my drug use
draCI['EncSuppNothing'][207] = 1  #    I wouldn’t discuss with my employer
draCI['EncSuppDrugPoli'][214] = 1  #    Being able to get care anonymously 
draCI['EncSuppDrugPoli'][231] = 1  #    No punishment or prosecution 
draCI['EncSuppDrugPoli'][236] = 1  #    MANDATORY EDUCATION IN ALL SCHOOLS
draCI['EncSuppNoNeed'][247] = 1 #    No reason to seek support
draCI['EncSuppNoNeed'][262] = 1 #    Having a drug problem would be a good start
draCI['EncSuppDrugPoli'][276] = 1  #    Job security 
draCI['EncSuppNothing'][302] = 1  #    nothing
draCI['EncSuppNoNeed'][322] = 1 #    If I felt like I needed support
draCI['EncSuppOther'][332] = 1  #    We already have the options I've left blank
draCI['EncSuppOther'][338] = 1  #    Intervention 
draCI['EncSuppNoNeed'][342] = 1 #    Drugs can be enjoyed if taken on a balanced/controlled manner. If taken in controlled manner, employer doesn’t need to know. 
draCI['EncSuppNoNeed'][344] = 1 #    I am not addicted
draCI['EncSuppNoNeed'][353] = 1 #    Only. Applies if I was looking to stop using
draCI['EncSuppNothing'][378] = 1  #    Nothing 
#IGNORE 427   Free drugs?
draCI['EncSuppNoNeed'][435] = 1 #    Needing support
draCI['EncSuppNoNeed'][444] = 1 #    I don't need help so difficult to answer 
draCI['EncSuppOther'][524] = 1  #    also if I agreed with their views. Because if they wouldn't admit that psychedelics have potential benefits I wouldn't bother getting "help" from them as they would not be well informed enough to help
draCI['EncSuppNoNeed'][544] = 1 #    Only if I thought I needed it
#IGNORE 565   Same answer
draCI['EncSuppNoNeed'][625] = 1 #    If it started effecting my work I would turn to sb
draCI['EncSuppNoNeed'][657] = 1 #    Because I don’t need It anymore 
draCI['EncSuppDrugPoli'][677] = 1  #    If i found the drug problem became worse and justified possibly getting a punishment
draCI['EncSuppServices'][727] = 1  #    The lack of other ways to get help
draCI['EncSuppOther'][763] = 1  #    Work is not the place for support.
draCI['EncSuppNoNeed'][770] = 1 #    I don't want support or to discuss drugs with anyone other than my friends or those who need advice.
draCI['EncSuppNoNeed'][774] = 1 #    I don't want support because that is my private life, and I don't have an issue with drugs
draCI['EncSuppOther'][846] = 1  #    If they knew more about it
draCI['EncSuppNoNeed'][853] = 1 #    If I thought that my drug use was affecting my studies or wellbeing I would access help.
draCI['EncSuppNoNeed'][881] = 1 #    I do not feel I need support
draCI['EncSuppDrugPoli'][907] = 1  #    Not losing my job 😂😂😂
draCI['EncSuppNothing'][916] = 1  #    Nothing
draCI['EncSuppOther'][924] = 1  #    Anti capitalist anti authoritarian revolution 
draCI['EncSuppNoNeed'][930] = 1 #    Our policy is already great. I would use the service if I needed something as it is free and I just ring the hotline.
draCI['EncSuppNoNeed'][945] = 1 #    Why the fuck would I need help for taking molly in a festival once a year, this is a joke.
draCI['EncSuppOther'][959] = 1  #    Caring every one
draCI['EncSuppNothing'][987] = 1  #    i wont go
#IGNORE 1016  free weed
draCI['EncSuppDrugPoli'][1021] = 1  #   Decriminalisation
draCI['EncSuppOther'][1022] = 1  #   It would help if I feel I could gain something other than harm reduction (how I could more effectively microdose LSD etc. - something that I've been doing during self-isolation)
draCI['EncSuppDrugPoli'][1061] = 1  #   An open policy where individuals are encouraged to speak about their habits in an anonymised manner
draCI['EncSuppNoNeed'][1067] = 1 #   If i had a problem with drug abuse
draCI['EncSuppNoNeed'][1116] = 1 #   Dont need it for
draCI['EncSuppNothing'][1156] = 1  #   nothing
draCI['EncSuppOpenDeb'][1159] = 1  #   asking am i alright just once in a while
draCI['EncSuppRedStig'][1160] = 1  #   If I needed to, and I was confident it would be treated like any other health issue
draCI['EncSuppDrugPoli'][1208] = 1  #   Decriminalisation/legalisation of at least cannabis but ideally all drugs
draCI['EncSuppDrugPoli'][1236] = 1  #   decriminalisation of all drugs
draCI['EncSuppNoNeed'][1237] = 1 #   These are all desirable things but I do not see them as concerning me directly
draCI['EncSuppNothing'][1266] = 1  #   Absolutely NOTHING 
draCI['EncSuppNoNeed'][1277] = 1 #   If I needed support I would seek it
draCI['EncSuppNoNeed'][1283] = 1 #   I don’t feel it is necessary
draCI['EncSuppNoNeed'][1287] = 1 #   Feeling I had a problem 
draCI['EncSuppServices'][1292] = 1  #   Free and open medical study on recreational drugs effects would increase a chance of me visiting their website and looking at the results
draCI['EncSuppNoNeed'][1341] = 1 #   there is no need
draCI['EncSuppNothing'][1435] = 1  #   None. I'd be struck off.
draCI['EncSuppOther'][1459] = 1  #   I believe even if those event would be offered, I would seek help from different places than my employer, but this may be different in other professions (i.e. healthcare, education etc)
draCI['EncSuppNoNeed'][1477] = 1 #   i dont think i need support 
draCI['EncSuppOther'][1504] = 1  #   Test kits
draCI['EncSuppNoNeed'][1532] = 1 #   No issues
draCI['EncSuppOther'][1533] = 1  #   Easily available drug testing kits/services
draCI['EncSuppDrugPoli'][1538] = 1  #   If they actively say ‘you will not be punished for your drug use
#IGNORE 1539  Same answer as above.
draCI['EncSuppDrugPoli'][1558] = 1  #   Knowing there was no repercussions 
draCI['EncSuppNoNeed'][1588] = 1 #   I don't need my employers help.
draCI['EncSuppNoNeed'][1612] = 1 #   I am not in need of support
draCI['EncSuppNothing'][1613] = 1  #   Probably nothing really
draCI['EncSuppNoNeed'][1636] = 1 #   don’t need it
draCI['EncSuppNoNeed'][1652] = 1 #   Nothing, not nessecary
draCI['EncSuppNoNeed'][1655] = 1 #   All of the above DO apply to my organization already. But like mentioned before, I don’t feel the need for help from them. 
#IGNORE 1661  lol 
draCI['EncSuppServices'][1670] = 1  #   Improved detox procedure
draCI['EncSuppDrugPoli'][1695] = 1  #   Parents not knowing 
draCI['EncSuppDrugPoli'][1700] = 1  #   I couldn’t, I’d get sacked 
draCI['EncSuppNoNeed'][1764] = 1 #   i don't want to seek support from my school
draCI['EncSuppNoNeed'][1834] = 1 #   I don’t feel like I need support 
draCI['EncSuppOther'][1847] = 1  #   None id go see a doctor instead of the school guys
draCI['EncSuppNothing'][1897] = 1  #   Nothing I love psychedelics
draCI['EncSuppNoNeed'][1958] = 1 #   If I needed support on this issue.  Again with the weird bias, is this an 'just say no' kinda site?
draCI['EncSuppNothing'][1991] = 1  #   Nothing
draCI['EncSuppNothing'][2029] = 1  #   Nothing, prefer to keep it private.
draCI['EncSuppNothing'][2051] = 1  #   I wouldn't see support from employer. Could make things worse.
draCI['EncSuppNoNeed'][2055] = 1 #   A need for it
draCI['EncSuppNoNeed'][2064] = 1 #   A breakdown in everything in my life
draCI['EncSuppDrugPoli'][2075] = 1  #   (Honest) insurance that the authorities will not be involved.
draCI['EncSuppNoNeed'][2114] = 1 #   if i was worried about it
draCI['EncSuppNoNeed'][2128] = 1 #   All of the above, if I felt I needed to. 
#IGNORE 2137  V
draCI['EncSuppServices'][2162] = 1  #   something that makes school daily life easier to cope with
draCI['EncSuppNothing'][2172] = 1  #   Nothing 
draCI['EncSuppNoNeed'][2188] = 1 #   I wouldn’t.
draCI['EncSuppNothing'][2202] = 1  #   None 
draCI['EncSuppServices'][2207] = 1  #   the stigma is too big to trust the employer 
draCI['EncSuppNoNeed'][2225] = 1 #   Nothing support isn’t wanted 
draCI['EncSuppNoNeed'][2248] = 1 #   I'm not interested.
draCI['EncSuppNothing'][2253] = 1  #   Honestly, these are the three places I would seek support last.
draCI['EncSuppNothing'][2270] = 1  #   Will never change 
draCI['EncSuppServices'][2309] = 1  #   SSDP
draCI['EncSuppNoNeed'][2318] = 1 #   I don’t want support
draCI['EncSuppNoNeed'][2334] = 1 #   If it started to affect my work and health 
draCI['EncSuppNoNeed'][2398] = 1 #   I don’t need it

# %% SAVE into a csv
draCI.to_csv('../cleaned_data/cleaned_data_ivan.csv', index=False, header=True)

# %% TRASH

# try:
#     del raw['Respondent ID'] # same number for every row
#     del raw['Collector ID'] # same number for every row
#     del raw['Start Date'] # with date + time or hashes
#     del raw['End Date'] # with data + time or hashes
#     del raw['IP Address'] # empty
#     del raw['Email Address'] # empty
#     del raw['First Name'] # empty
#     del raw['Last Name'] # empty
#     del raw['Custom Data 1'] # NaNs
# except:
#     print('Already deleted')

# # %%

# dra.rename(columns={'In what country are you living?': 'Countries', 
#                     'How would you describe your gender?': 'Gender',
#                     'What is your biological sex?': 'Sex',
#                     'What age are you?': 'Age',
#                     'How has your life changed due to the coronavirus outbreak? (tick all that apply)': 'Lifechange',
#                     'How many people are there in your household? (including you)': 'Household',
#                     'Who do you live with?': 'LiveCompany',
#                     'How long ago did your life change most clearly as a result of the COVID-19 pandemic?': 'LifechangeTiming',
#                     'Do you currently drink alcohol?': 'CurrentlyAlcohol',
#                     'Did you drink alcohol before the outbreak?': 
#                     },
#           inplace=True, errors='raise')

