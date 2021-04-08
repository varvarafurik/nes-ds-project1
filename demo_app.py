import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("1310038301_territory.csv")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
for col in df.columns:
    print(col)
mean_ter = df[(df["GEO"] != "Canada") & (df['UOM'] == "Number")]
mean_ter = (mean_ter.groupby("GEO").mean())
print(mean_ter)
mean_ter.reset_index(level=0, inplace=True)
print(mean_ter['GEO'], mean_ter['VALUE'])
plt.scatter(mean_ter['GEO'], mean_ter['VALUE'])
plt.show()
#sns.barplot(x='GEO', y="VALUE", data=mean_ter)