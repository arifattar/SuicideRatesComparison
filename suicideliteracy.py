import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from mpldatacursor import datacursor

literacy_df = pd.read_csv('API_SE.ADT.LITR.ZS_DS2_en_csv_v2_247798.csv', header = 0, skiprows = 4)


literacy_df = literacy_df[['Country Name', '2018']]

literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('Korea, Rep.', 'Republic of Korea')
literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('Syria', 'Syrian Arab Republic')
literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('Tanzania', 'United Republic of Tanzania')
literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('United Kingdom', 'United Kingdom of Great Britain and Northern Ireland')
literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('United States', 'United States of America')
literacy_df['Country Name'] = literacy_df['Country Name'].str.replace('Vietnam', 'Viet Nam')

print(literacy_df)
suicide_df = pd.read_csv('SDGSUICIDE,SDG_SH_STA_SCIDEN.csv', header =1)

suicide_df = suicide_df[['Country', 'Sex', '2016']]

suicide_df['Country'] = suicide_df['Country'].str.replace(r'\s*\(.*\)s*', '')
suicide_df['Sex'] = suicide_df['Sex'].str.strip()

suicide_df = suicide_df.pivot(columns = 'Sex', index = 'Country', values = '2016')

print(suicide_df)

print(suicide_df)

literacysuicide_df = pd.merge(literacy_df, suicide_df, how = 'inner', left_on = 'Country Name', right_on = 'Country')
literacysuicide_df = literacysuicide_df.reset_index(drop = True)
print(literacysuicide_df)

literacysuicide_df = literacysuicide_df[np.isfinite(literacysuicide_df['2018'])]
literacysuicide_df = literacysuicide_df.reset_index(drop = True)
print(literacysuicide_df)

sc = plt.scatter(literacysuicide_df['2018'], literacysuicide_df['Both sexes'])

fig = plt.gcf()
ax = plt.gca()
DefaultSize = fig.get_size_inches()
fig.set_size_inches( (DefaultSize[0]*1.3, DefaultSize[1]*1.3) )

[s.set_visible(False) for s in ax.spines.values()]


ax.set_xlabel("Literacy rate, adult total (% of people ages 15 and above) (2018). Source: World Bank")
ax.set_ylabel("Suicide rate per 100,000 people by country (2016). Source: WHO")
ax.set_title("Suicide Rates vs Literacy Rates")

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
                           " ".join([literacysuicide_df['Country Name'][n] for n in ind["ind"]]))
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
fig.savefig('literacy2018suicide2016.png')
