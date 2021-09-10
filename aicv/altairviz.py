import altair as alt

import aicv


class AltairViz(object):

    # data_frame should be an instance of aicv.core.DataFrame
    def __init__(self, data_frame, raw_features):
        self.data_frame = data_frame
        self.config = None
        self.color = None
        self.legend = None
        self.selector = None
        self.raw_features = raw_features
        self.legend_selector = None
        self.rendered_charts = alt.vconcat()

    def set_config(self, config):
        self.config = config
        self.selector = alt.selection_interval(name="interval_selector")

        # process data for feature & clustering
        # raw_features = []
        # _df = self.data_frame.get_dataframe()
        # for a in list(_df.columns): raw_features.append(a) if _df[a].dtype in ["int64", "float64"] else a

        _clusterAlg = aicv.cluster.core.BaseClusterAlg(
            self.raw_features,
            self.data_frame,
            tsne_perplexity=20)
        _clusterAlg.add_tsne_to_df()
        _clusterAlg.add_clusters_to_df()

    def build_chart(self, title, chart):
        self.rendered_charts = chart
        self._render(title)

    def _render(self, title):
        if self.config is None:
            raise RuntimeError("You need to call set_config"
                               + " to set the config!")

        if self.color is None:
            self.color = alt.condition(
                (alt.selection_interval() | alt.selection_multi(name="render_color_legends",
                                                                fields=self.config['legend_selection'])),
                'clusters', alt.value('lightgray'),
                scale=alt.Scale(scheme='category10'),
                legend=None)

        # selectable legend
        self.legend = alt.Chart(self.data_frame.get_dataframe()).mark_point().encode(
            y=alt.Y('clusters:N', axis=alt.Axis(orient='right')),
            color=self.color).add_selection(
            self.legend_selector)
        # alt.selection_multi(name="render_selectable_legends", fields=self.config['legend_selection']))

        # compose the whole layout
        _temp = self.rendered_charts
        _temp_init_chart = alt.vconcat() \
            .configure_axis(labelFontSize=self.config['fontsize'],
                            titleFontSize=self.config['fontsize']) \
            .properties(padding=0,
                        spacing=0,
                        title=title)

        self.rendered_charts = _temp_init_chart
        self.rendered_charts &= _temp
        # self.rendered_charts &= self.legend

        self.rendered_charts.configure_title(
            fontSize=30,
            fontWeight="bold",
            font='Courier',
            anchor='start',
            color='black'
        )

        self.rendered_charts.show()

    def show_legend(self):
        return self.legend


class AltairHistogram:

    def __init__(self, field, interactive=False):
        self.field = field
        self.interactive = interactive

    def __call__(self, av: AltairViz):
        column_name = av.data_frame.resolve_columnname(self.field)

        yaxis = alt.Y('count():Q', title="Count")
        xaxis = alt.X(column_name + ':Q', bin=alt.Bin(maxbins=100))

        # apparently height/width doesn't include the space for the
        # axes labels, so these need to be adjusted a bit.
        if self.interactive:
            bg_histogram = alt.Chart(av.data_frame.get_dataframe()).mark_bar().encode(
                y=yaxis,
                x=xaxis,
                color=alt.value('lightgrey')).properties(
                width=av.config['total_width'] * (1 - av.config['tsne_widthfrac']) / 4
                      - (av.config['fontsize'] + av.config['padding_guess']),
                height=av.config['total_height'] * av.config['tsne_heightfrac'] / 3
                       - (av.config['fontsize'] + av.config['padding_guess']),
                selection=av.selector)
            fg_histogram = alt.Chart(av.data_frame.get_dataframe()).mark_bar().encode(
                y=yaxis,
                x=xaxis).transform_filter(av.selector)

            return bg_histogram + fg_histogram
        else:
            return alt.Chart(av.data_frame.get_dataframe()).mark_bar().encode(
                y=yaxis,
                x=xaxis,
                color=alt.value('lightgrey')).properties(
                width=av.config['total_width'] * (1 - av.config['tsne_widthfrac']) / 4
                      - (av.config['fontsize'] + av.config['padding_guess']),
                height=av.config['total_height'] * av.config['tsne_heightfrac'] / 3
                       - (av.config['fontsize'] + av.config['padding_guess']))


class AltairScatterplot:

    def __init__(self, field1, field2, interactive=False):
        self.field1 = field1
        self.field2 = field2
        self.interactive = interactive

    def __call__(self, av: AltairViz):
        av.legend_selector = alt.selection_multi(name="scatter_legends",
                                                 fields=av.config['legend_selection'],
                                                 empty='none')

        # if self.interactive:
        # define the color property that will be shared for the scatterplots/legend
        av.color = alt.condition(
            av.selector | av.legend_selector,
            alt.Color('clusters:N', legend=None),
            alt.value('lightgray'),
            scale=alt.Scale(scheme='category10'),
            legend=None)

        # base chart for all other scatterplots
        base = alt.Chart(av.data_frame.get_dataframe()) \
            .mark_point() \
            .encode(color=av.color) \
            .properties(width=av.config['total_width'] / 4 - (av.config['fontsize'] + av.config['padding_guess']),
                        height=(av.config['total_height'] * (1 - av.config['tsne_heightfrac'])) / 2
                               - (av.config['fontsize'] + av.config['padding_guess'])) \
            .add_selection(av.selector)

        # base.add_selection(av.legend_selector)

        _chart = base.encode(x=av.data_frame.resolve_columnname(self.field1) + ":Q",
                             y=av.data_frame.resolve_columnname(self.field2) + ":Q")

        if av.legend is None:
            av.legend = alt.Chart(av.data_frame.get_dataframe()).mark_point().encode(
                y=alt.Y('clusters:N', axis=alt.Axis(orient='right')),
                color=av.color) \
                .add_selection(av.legend_selector)

        return _chart


class AltairHorizontalStacking:

    def __init__(self, av: AltairViz, *contents):
        self.contents = contents
        chart_stack = alt.hconcat()
        for chart in self.contents:
            chart_stack |= chart
        self.chart_stack = chart_stack

    def __call__(self):
        return self.chart_stack


class AltairVerticalStacking:

    def __init__(self, av: AltairViz, *contents):
        self.contents = contents
        chart_stack = alt.vconcat()
        for chart in self.contents:
            chart_stack &= chart
        self.chart_stack = chart_stack

    def __call__(self):
        return self.chart_stack
