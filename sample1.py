import sys
import aicv

data_file_name = "C:/Users/deeya/Downloads/200413_nitrous_oxide_cycling_regimes_data_for_repositories.csv"

# mapping of the column names to desired name
column_names_mapping = {'d15N_N2Oa_mean': "d15N-N2Oa_mean (per mil vs. atm N2)",
                        'd15N_N2Ob_mean': "d15N-N2Ob_mean (per mil vs. atm. N2)",
                        'd18O_N2O_mean': "d18O-N2O_mean (per mil vs. VSMOW)",
                        'N2O_mean': "N2O_mean (nM)",
                        'd18O_NO3_mean': 'd18O-NO3 avg (per mil vs. VSMOW)',
                        'd15N_NO3_mean': 'd15N-NO3 avg (per mil vs. atm. N2)',
                        'd15N_NO2': 'd15N-NO2 (per mil vs. atm N2)',
                        'd18O_NO2': 'd18O-NO2 (per mil vs. VSMOW)',
                        'Nitrite': "Nitrite [uM]",
                        'Oxygen': "Seabird Oxygen [umol/L]",
                        'NO3_mean': 'NO3_mean (uM)',
                        'Depth': 'Target Depth [m]'}

df = aicv.core.DataFrame(data_file_name)
df.map_columns(column_names_mapping)
df.add_derived_column("inv_N2O_mean = 1/N2O_mean")

av_config = {
    "total_width": 1200,
    "total_height": 680,
    "tsne_heightfrac": 0.4,
    "tsne_widthfrac": 0.2,
    "fontsize": 10,
    "padding_guess": 45,
    "legend_selection": ['clusters']
    # "legend_selection": []
}

# list of column names participating in histograms/clustering
column_names_for_histograms = [
    'd15N_N2Oa_mean', 'd15N_N2Ob_mean', 'd18O_N2O_mean',
    'N2O_mean', 'd18O_NO3_mean', 'd15N_NO3_mean',
    'd15N_NO2', 'd18O_NO2', 'Nitrite',
    'Oxygen', 'NO3_mean', 'Depth']


av = aicv.altairviz.AltairViz(df)
av.set_config(av_config)

a = aicv.altairviz.AltairHorizontalStacking(av,
                                            aicv.altairviz.AltairVerticalStacking(av,
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "Target Depth [m]"),
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "Seabird Oxygen [umol/L]"),
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "inv_N2O_mean")
                                                                                  ),
                                            aicv.altairviz.AltairVerticalStacking(av,
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "d15N-N2Oa_mean (per mil vs. atm N2)"),
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "d15N-N2Ob_mean (per mil vs. atm. N2)"),
                                                                                  aicv.altairviz.AltairHistogram(av,
                                                                                                                 "d18O-N2O_mean (per mil vs. VSMOW)")
                                                                                  ),
                                            aicv.altairviz.AltairVerticalStacking(av,
                                                                                  aicv.altairviz.AltairScatterplot(av,
                                                                                                                   "inv_N2O_mean",
                                                                                                                   "d15N-N2Oa_mean (per mil vs. atm N2)"),
                                                                                  aicv.altairviz.AltairScatterplot(av,
                                                                                                                   "inv_N2O_mean",
                                                                                                                   "d15N-N2Ob_mean (per mil vs. atm. N2)")
                                                                                  )
                                            )

av.render("My Dashboard")
