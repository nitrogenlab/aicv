import sys
import aicv
import aicv.altairviz as altviz

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

raw_features = [
    'd15N_N2Oa_mean', 'd15N_N2Ob_mean', 'd18O_N2O_mean',
    'N2O_mean', 'd18O_NO3_mean', 'd15N_NO3_mean',
    'd15N_NO2', 'd18O_NO2', 'Nitrite',
    'Oxygen', 'NO3_mean', 'Depth']

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
}

av = altviz.AltairViz(df, raw_features)
av.set_config(av_config)

av.build_chart("My Dashboard",
               altviz.AltairVerticalStacking(
                   av,
                   altviz.AltairHorizontalStacking(
                       av,
                       altviz.AltairScatterplot(
                           "tsne_ax1",
                           "tsne_ax2")(av),
                       altviz.AltairVerticalStacking(
                           av,
                           altviz.AltairHistogram(
                               "Target Depth [m]",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "Seabird Oxygen [umol/L]",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "inv_N2O_mean",
                               interactive=True)(av))(),
                       altviz.AltairVerticalStacking(
                           av,
                           altviz.AltairHistogram(
                               "d15N-N2Oa_mean (per mil vs. atm N2)",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d15N-N2Ob_mean (per mil vs. atm. N2)",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d18O-N2O_mean (per mil vs. VSMOW)",
                               interactive=True)(av))(),
                       altviz.AltairVerticalStacking(
                           av,
                           altviz.AltairHistogram(
                               "NO3_mean (uM)",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d15N-NO3 avg (per mil vs. atm. N2)",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d18O-NO3 avg (per mil vs. VSMOW)",
                               interactive=True)(av))(),
                       altviz.AltairVerticalStacking(
                           av,
                           altviz.AltairHistogram(
                               "Nitrite [uM]",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d15N-NO2 (per mil vs. atm N2)",
                               interactive=True)(av),
                           altviz.AltairHistogram(
                               "d18O-NO2 (per mil vs. VSMOW)",
                               interactive=True)(av))()
                       , av.show_legend()
                   )()  # Row #1
                   , altviz.AltairHorizontalStacking(
                       av,
                       altviz.AltairScatterplot(
                           "inv_N2O_mean",
                           "d15N-N2Oa_mean (per mil vs. atm N2)")(av),
                       altviz.AltairScatterplot(
                           "inv_N2O_mean",
                           "d15N-N2Ob_mean (per mil vs. atm. N2)")(av),
                       altviz.AltairScatterplot(
                           "inv_N2O_mean",
                           "d18O-N2O_mean (per mil vs. VSMOW)")(av),
                       altviz.AltairScatterplot(
                           "d15N-N2Oa_mean (per mil vs. atm N2)",
                           "d18O-N2O_mean (per mil vs. VSMOW)")(av))()
                   , altviz.AltairHorizontalStacking(
                       av,
                       altviz.AltairScatterplot(
                           "d15N-NO2 (per mil vs. atm N2)",
                           "Nitrite [uM]")(av),
                       altviz.AltairScatterplot(
                           "d15N-NO2 (per mil vs. atm N2)",
                           "d18O-NO2 (per mil vs. VSMOW)")(av),
                       altviz.AltairScatterplot(
                           "Seabird Oxygen [umol/L]",
                           "NO3_mean (uM)")(av),
                       altviz.AltairScatterplot(
                           "d15N-NO3 avg (per mil vs. atm. N2)",
                           "d18O-NO3 avg (per mil vs. VSMOW)")(av))()
               )()

               )
