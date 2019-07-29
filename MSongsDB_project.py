import os
import glob
import tables
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


subset_path = "C:/Users/zhang/OneDrive/DataScienceStudy/MillionSongSubset"
subset_data_path = os.path.join(subset_path, 'data')
subset_addf_path = os.path.join(subset_path, 'AdditionalFiles')

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
                                       'year': all_songs_year
                                      })
df.head(5)

# 'danceability' and 'energy' contain only zeros
df_sub = df[['id','tempo','hotttnesss','loudness','duration','year']]

# plot a heatmap to show the correlation between these parameters
corr = df_sub.corr()
sns.set(style='white')
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap)
plt.show()