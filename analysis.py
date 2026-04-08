import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# --- STEP 1: Load Data ---
gdp_data = {
    'Country': [
        'Luxembourg', 'Ireland', 'Denmark', 'Netherlands', 'Austria',
        'Sweden', 'Belgium', 'Finland', 'Germany', 'France',
        'Malta', 'Italy', 'Czechia', 'Slovenia', 'Cyprus',
        'Spain', 'Lithuania', 'Estonia', 'Portugal', 'Latvia',
        'Poland', 'Hungary', 'Slovakia', 'Croatia', 'Romania',
        'Greece', 'Bulgaria'
    ],
    'GDP_per_capita': [
        261, 214, 133, 131, 128,
        125, 119, 117, 116, 105,
        101, 96, 91, 91, 87,
        84, 88, 83, 79, 72,
        79, 76, 73, 74, 73,
        68, 57
    ]
}

unemp_data = {
    'Country': [
        'Luxembourg', 'Ireland', 'Denmark', 'Netherlands', 'Austria',
        'Sweden', 'Belgium', 'Finland', 'Germany', 'France',
        'Malta', 'Italy', 'Czechia', 'Slovenia', 'Cyprus',
        'Spain', 'Lithuania', 'Estonia', 'Portugal', 'Latvia',
        'Poland', 'Hungary', 'Slovakia', 'Croatia', 'Romania',
        'Greece', 'Bulgaria'
    ],
    'Unemployment': [
        4.7, 4.5, 5.1, 3.5, 4.8,
        8.5, 5.6, 7.1, 3.0, 7.3,
        2.9, 8.1, 2.2, 4.0, 7.1,
        12.9, 5.9, 5.6, 6.0, 6.8,
        2.9, 3.6, 6.1, 7.0, 5.6,
        12.4, 4.3
    ]
}

df_gdp = pd.DataFrame(gdp_data)
df_unemp = pd.DataFrame(unemp_data)

# --- STEP 2 & 3: Clean + Merge ---
df = pd.merge(df_gdp, df_unemp, on='Country')

north = ['Denmark', 'Sweden', 'Finland', 'Netherlands', 'Germany',
         'Austria', 'Belgium', 'Luxembourg', 'Ireland', 'France']
south = ['Italy', 'Spain', 'Greece', 'Portugal', 'Cyprus', 'Malta', 'Croatia', 'Slovenia']

def assign_region(country):
    if country in north:
        return 'North/West'
    elif country in south:
        return 'South'
    else:
        return 'East'

df['Region'] = df['Country'].apply(assign_region)

# --- STEP 4: Plot ---
colors = {'North/West': '#2166ac', 'South': '#d6604d', 'East': '#4dac26'}
region_order = ['North/West', 'South', 'East']

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#f9f9f9')
ax.set_facecolor('#f9f9f9')

for region in region_order:
    subset = df[df['Region'] == region]
    ax.scatter(
        subset['GDP_per_capita'],
        subset['Unemployment'],
        c=colors[region],
        s=90,
        alpha=0.85,
        edgecolors='white',
        linewidths=0.6,
        label=region,
        zorder=3
    )

for _, row in df.iterrows():
    ax.annotate(
        row['Country'],
        (row['GDP_per_capita'], row['Unemployment']),
        fontsize=7.5,
        xytext=(4, 4),
        textcoords='offset points',
        color='#333333'
    )

ax.axvline(100, color='gray', linestyle='--', linewidth=0.8, alpha=0.6, label='EU avg GDP (=100)')
eu_avg_unemp = df['Unemployment'].mean()
ax.axhline(eu_avg_unemp, color='gray', linestyle=':', linewidth=0.8, alpha=0.6,
           label=f'Sample avg unemployment ({eu_avg_unemp:.1f}%)')

ax.set_xlabel('GDP per Capita (PPS, EU27 = 100)', fontsize=12, labelpad=8)
ax.set_ylabel('Unemployment Rate (%)', fontsize=12, labelpad=8)
ax.set_title(
    'Is Europe Still Economically Divided?\nGDP per Capita vs Unemployment Rate by Country (2022)',
    fontsize=14, fontweight='bold', pad=14
)

ax.legend(fontsize=10, framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('europe_divide_scatter.png', dpi=150, bbox_inches='tight')
print("done! chart saved.")