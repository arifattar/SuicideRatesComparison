
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from mpldatacursor import datacursor


fh = open('cow.txt', encoding = 'utf8')

l = list()
for line in fh:
    if line.startswith('#'):
        continue
    else:
        l.append(line)

l.pop(0)

rows = list()

for row in l:
    r = row.split(';')
    rows.append(r)




latitude_df = pd.DataFrame(rows)



headers = latitude_df.iloc[0]
latitude_df = pd.DataFrame(latitude_df.values[1:], columns = headers)



latitude_df = latitude_df[['UNGEGNen_name','UNGEGNen_longname','latitude', 'maxlatitude', 'minlatitude']].reset_index(drop = True)



latitude_df['UNGEGNen_name'] = latitude_df['UNGEGNen_name'].str.replace(r'\s*\(.*\)s*', '')
latitude_df['UNGEGNen_name'] = latitude_df['UNGEGNen_name'].str.strip()



suicide_df = pd.read_csv('SDGSUICIDE,SDG_SH_STA_SCIDEN.csv', header =1)

suicide_df = suicide_df[['Country', 'Sex', '2010']]

suicide_df['Country'] = suicide_df['Country'].str.replace(r'\s*\(.*\)s*', '')
suicide_df['Sex'] = suicide_df['Sex'].str.strip()

suicide_df = suicide_df.pivot(columns = 'Sex', index = 'Country', values = '2010')

topsuicide_df = suicide_df.sort_values('Both sexes', ascending = False)
print(topsuicide_df)

latitudesuicide_df = pd.merge(latitude_df, suicide_df, how = 'inner', left_on = 'UNGEGNen_name', right_index = True)



latitudesuicide_df = latitudesuicide_df.reset_index(drop = True)

latitudesuicide_df['latitude'] = latitudesuicide_df['latitude'].astype(float)
latitudesuicide_df['maxlatitude'] = latitudesuicide_df['maxlatitude'].astype(float)
latitudesuicide_df['minlatitude'] = latitudesuicide_df['minlatitude'].astype(float)

print(latitudesuicide_df)


pew_df = pd.read_excel('Religious_Composition_by_Country_2010-2050.xlsx', sheet_name = 'rounded_percentage')
pew_df = pew_df[pew_df['Year'] == 2010]
pew_df = pew_df[7:]
pew2010_df = pew_df[['Country', 'Region', 'Muslims']].reset_index(drop = True)
pew2010_df['Muslims'] = pew2010_df['Muslims'].str.replace(r'\s*\<.*\s*', '0.0')
pew2010_df['Muslims'] = pew2010_df['Muslims'].str.replace(r'\s*\>.*\s*', '100.0')

pew2010_df['Country'] = pew2010_df['Country'].str.replace('Bosnia-Herzegovina', 'Bosnia and Herzegovina')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Brunei', 'Brunei Darussalam')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Cape Verde', 'Cabo Verde')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Republic of the Congo', 'Congo')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Czech Republic', 'Czechia')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Laos', "Lao People's Democratic Republic")
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Republic of Macedonia', 'Republic of North Macedonia')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Federated States of Micronesia', 'Micronesia (Federated States of)')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Moldova', 'Republic of Moldova')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Burma (Myanmar)', 'Myanmar')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('North Korea', "Democratic People's Republic of Korea")
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Russia', 'Russian Federation')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('St. Lucia', 'Saint Lucia')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('South Korea', 'Republic of Korea')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Syria', 'Syrian Arab Republic')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Tanzania', 'United Republic of Tanzania')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('United Kingdom', 'United Kingdom of Great Britain and Northern Ireland')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('United States', 'United States of America')
pew2010_df['Country'] = pew2010_df['Country'].str.replace('Vietnam', 'Viet Nam')

pew2010_df['Muslims'] = pew2010_df['Muslims'].astype(float)


#print(pew2010_df[150:200])
print(pew2010_df.dtypes)

muslimssuicide_df = pd.merge(pew2010_df, suicide_df, how = 'inner', left_on = 'Country', right_index = True)
muslimssuicide_df = muslimssuicide_df.reset_index(drop = True)
print(muslimssuicide_df)

intermediate_df = pd.merge(pew2010_df, suicide_df, how = 'outer', left_on = 'Country', right_index = True, indicator = True)
nonmuslimssuicide_df = intermediate_df[intermediate_df['_merge'] == 'left_only'][pew2010_df.columns]
#print(nonmuslimssuicide_df['Country'].to_string())

print('length of suicide_df', len(suicide_df))
print('length of pew2010_df', len(pew2010_df))
print('length of muslimssuicide_df', len(muslimssuicide_df))



sc = plt.scatter(muslimssuicide_df['Muslims'], muslimssuicide_df['Both sexes'])
#sc = muslimssuicide_df.plot('Muslims', 'Both sexes', kind = 'scatter')
#plt.scatter(latitudesuicide_df['Both sexes'], latitudesuicide_df['latitude'])

fig = plt.gcf()
ax = plt.gca()
DefaultSize = fig.get_size_inches()
fig.set_size_inches( (DefaultSize[0]*1.3, DefaultSize[1]*1.3) )

[s.set_visible(False) for s in ax.spines.values()]

ax.set_xlabel("Percentage of Muslim population by country (2010). Source: Pew Research")
ax.set_ylabel("Suicide rate per 100,000 people by country (2010). Source: WHO")
ax.set_title("Suicide Rates vs Proportion of Muslims by Country")

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
                           " ".join([muslimssuicide_df['Country'][n] for n in ind["ind"]]))
    annot.set_text(text)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()

fig.savefig('muslimssuicide.png')
