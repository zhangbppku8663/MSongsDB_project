import os
import glob
import tables
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np


subset_path = "C:/Users/zhang/OneDrive/DataScienceStudy/MillionSongSubset"
subset_data_path = os.path.join(subset_path, 'data')
subset_addf_path = os.path.join(subset_path, 'AdditionalFiles')

# generating the first figure (average duration of song track vs. year)
# taking advantage of provided database file from the dataset
database_path = os.path.join(subset_addf_path, 'subset_track_metadata.db')
conn = sqlite3.connect(database_path)
q = "SELECT DISTINCT track_id, year, duration FROM songs"
res = conn.execute(q)
pop_duration = res.fetchall()
conn.close()

df_ave_duration = pd.DataFrame(pop_duration, columns=['track_id','year','duration'])
df_ave_duration = df_ave_duration[df['year'] >0]
df_ave_duration_pivot = pd.pivot_table(df_ave_duration, values='duration', index='year', aggfunc=np.mean)
df_ave_duration_pivot.head(4)
plt.plot(df_ave_duration_pivot.index, df_ave_duration_pivot['duration'])
plt.xlabel("Year")
plt.ylabel("Average duration of songs (seconds)")
plt.show()


# Now, generating the second plot to find correlations among several parameters of song tracks
def apply_to_all_files(basedir, func=lambda x: x, ext ='.h5'):
    # helper function to apply operations to all files in the sub-folders containing HDF5 files
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*'+ext))
        for f in files:
            func(f)

all_songs_danceability = []
all_songs_tempo = []
all_songs_id = []
all_songs_energy = []
all_songs_hotttnesss = []
all_songs_loudness = []
all_songs_duration = []
all_songs_familiarity = []
all_songs_year = []

def get_song_parameters(filename):
    h5 = tables.open_file(filename, 'r')
    num_of_songs = h5.root.metadata.songs.nrows

    for i in range(num_of_songs):
        all_songs_id.append(h5.root.metadata.songs.cols.song_id[i].decode('UTF-8'))
        all_songs_danceability.append(h5.root.analysis.songs.cols.danceability[i])
        all_songs_tempo.append(h5.root.analysis.songs.cols.tempo[i])
        all_songs_energy.append(h5.root.analysis.songs.cols.energy[i])
        all_songs_hotttnesss.append(h5.root.metadata.songs.cols.artist_hotttnesss[i])
        all_songs_loudness.append(h5.root.analysis.songs.cols.loudness[i])
        all_songs_duration.append(h5.root.analysis.songs.cols.duration[i])
        all_songs_familiarity.append(h5.root.metadata.songs.cols.artist_familiarity[i])
        all_songs_year.append(h5.root.musicbrainz.songs.cols.year[i])

    h5.close()

# routine to get useful parameters from raw data and build a DataFrame
apply_to_all_files(subset_data_path, func=get_song_parameters)

df = pd.DataFrame.from_dict({'id': all_songs_id,
                                       'danceabiliy': all_songs_danceability,
                                       'tempo': all_songs_tempo,
                                       'energy': all_songs_energy,
                                       'hotttnesss': all_songs_hotttnesss,
                                       'loudness': all_songs_loudness,
                                       'duration': all_songs_duration,
                                       'familiarity': all_songs_familiarity,
                                       'year': all_songs_year
                                      })
df.head(5)

# 'danceability' and 'energy' contain only zeros
df_sub = df[['id','tempo','hotttnesss','loudness','duration','familiarity','year']]

# plot a heatmap to show the correlation between these parameters
corr = df_sub.corr()
sns.set(style='white')
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap)
plt.show()