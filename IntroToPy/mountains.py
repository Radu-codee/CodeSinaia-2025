import pandas as pd
import matplotlib.pyplot as plt

dtype = {"Elevation": "float64", "Code": "category", "Country": "category"}
usecols = ["Elevation", "Country", "Code"]
df = pd.read_csv(
    "IntroToPy/mountains_db.tsv",
    sep="\t",
    header=None,
    names=["Name", "Elevation", "Country", "Code"],
    usecols=usecols,
    dtype=dtype
)

cod_count = df["Code"].value_counts().sort_index()
max_per_cod = df.groupby("Code", observed=True)["Elevation"].max().sort_index()

max_elev = df["Elevation"].max()
bins = [0, 0.25 * max_elev, 0.5 * max_elev, 0.75 * max_elev, max_elev]
labels = ["0-25%", "25-50%", "50-75%", "75-100%"]
df["Quartile"] = pd.cut(df["Elevation"], bins=bins, labels=labels, include_lowest=True)
data = [df.loc[df["Quartile"] == lab, "Elevation"].dropna() for lab in labels]

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 5))
plt.tight_layout(pad=4)

colors = plt.cm.plasma(cod_count.values / cod_count.values.max())
cod_count.plot.bar(ax=ax1, color=colors)
ax1.set_title("Număr elemente / cod")
ax1.set_xlabel("Cod")
ax1.set_ylabel("Frecvență")

max_per_cod.plot(ax=ax2, marker="o", linestyle="-", color="tab:blue")
ax2.set_title("Elevation max. / cod")
ax2.set_xlabel("Cod")
ax2.set_ylabel("Elev. maximă")

ax3.boxplot(data, labels=labels)
ax3.set_title("Distribuția elevărilor pe grupe de % din maxim")
ax3.set_xlabel("Grupe (%)")
ax3.set_ylabel("Elevatie")

stats_per_country = df.groupby("Country", observed=True)["Elevation"].agg(["min", "median", "max"])
data_per_country = [df[df["Country"] == country]["Elevation"].dropna() for country in stats_per_country.index]
fig, ax4 = plt.subplots(figsize=(20, 5))
ax4.boxplot(data_per_country, labels=stats_per_country.index)
positions = range(1, len(stats_per_country.index) + 1)
ax4.plot(positions, stats_per_country["min"], marker="o", linestyle="-", label="min")
ax4.plot(positions, stats_per_country["median"], marker="o", linestyle="-", label="median")
ax4.plot(positions, stats_per_country["max"], marker="o", linestyle="-", label="max")
ax4.set_title("Statisticile și distribuția elevărilor pe țări")
ax4.set_xlabel("Țară")
ax4.set_ylabel("Elevatie")
ax4.legend()

plt.show()