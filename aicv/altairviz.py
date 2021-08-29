import altair as alt

import aicv


class AltairViz(object):

    # data_frame should be an instance of aicv.core.DataFrame
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.config = None
        self.color = None
        self.legend = None
        self.rendered_charts = alt.vconcat()

    def set_config(self, config):
        self.config = config

    def _set_config(self, name):
        if name in self.config.keys():
            return True
        return False

    def render(self, title):
        if self.config is None:
            raise RuntimeError("You need to call set_config"
                               + " to set the config!")

        # Process data
        BaseClusterAlg(self.data_frame, )


        # define the color property that will be shared for the scatterplots/legend
        self.color = alt.condition(
            (alt.selection_interval() | alt.selection_multi(fields=self.config['legend_selection'])),
            'clusters', alt.value('lightgray'),
            scale=alt.Scale(scheme='category10'),
            legend=None)

        # # base chart for all other scatterplots
        # base = alt.Chart(self.data_frame).mark_point().encode(
        #     color=self.color).properties(width=self.config['total_width'] / 4 - (
        #         self.config['fontsize'] + self.config['padding_guess']),
        #                                  height=(self.config['total_height'] * (
        #                                          1 - self.config['tsne_heightfrac'])) / 2
        #                                         - (
        #                                                 self.config['fontsize'] + self.config[
        #                                             'padding_guess'])).add_selection(
        #     alt.selection_interval())

        # selectable legend
        self.legend = legend = alt.Chart(self.data_frame).mark_point().encode(
            y=alt.Y('clusters:N', axis=alt.Axis(orient='right')),
            color=self.color).add_selection(alt.selection_multi(fields=self.config['legend_selection']))

        # compose the whole layout
        self.rendered_charts = alt.vconcat() \
            .configure_axis(labelFontSize=self.config['fontsize'],
                            titleFontSize=self.config['fontsize']) \
            .properties(padding=0,
                        spacing=0,
                        title=title)
        # the padding/spacing doesn't propagate to subcharts propertly

        self.rendered_charts.configure_title(
            fontSize=30,
            fontWeight="bold",
            font='Courier',
            anchor='start',
            color='black'
        )

        self.rendered_charts.show()


class AltairHistogram:

    def __init__(self, av: AltairViz, field):
        self.field = field
        self.altair_viz = av

    def __call__(self):
        column_name = self.altair_viz.data_frame.resolve_columnname(self.field)


        yaxis = alt.Y('count():Q', title="Count")
        xaxis = alt.X(column_name + ':Q', bin=alt.Bin(maxbins=100))
        # apparently height/width doesn't include the space for the
        # axes labels, so these need to be adjusted a bit.
        bg_histogram = alt.Chart(self.altair_viz.data_frame).mark_bar().encode(
            y=yaxis,
            x=xaxis,
            color=alt.value('lightgrey')).properties(
            width=self.altair_viz.config['total_width'] * (1 - self.altair_viz.config['tsne_widthfrac']) / 4
                  - (self.altair_viz.config['fontsize'] + self.altair_viz.config['padding_guess']),
            height=self.altair_viz.config['total_height'] * self.altair_viz.config['tsne_heightfrac'] / 3
                   - (self.altair_viz.config['fontsize'] + self.altair_viz.config['padding_guess']),
            selection=alt.selection_interval())
        fg_histogram = alt.Chart(self.altair_viz.data_frame).mark_bar().encode(
            y=yaxis,
            color=alt.value('steelblue'),
            x=xaxis).transform_filter(
            (alt.selection_interval() | alt.selection_multi(fields=self.altair_viz.config['legend_selection'])))
        return bg_histogram + fg_histogram


class AltairScatterplot:

    def __init__(self, av: AltairViz, field1, field2):
        self.field1 = field1
        self.field2 = field2
        self.altair_viz = av

    def __call__(self):
        # base chart for all other scatterplots
        base = alt.Chart(self.altair_viz.data_frame).mark_point().encode(
            color=self.altair_viz.color).properties(width=self.altair_viz.config['total_width'] / 4 - (
                self.altair_viz.config['fontsize'] + self.altair_viz.config['padding_guess']),
                                                    height=(self.altair_viz.config['total_height'] * (
                                                            1 - self.altair_viz.config['tsne_heightfrac'])) / 2
                                                           - (
                                                                   self.altair_viz.config['fontsize'] +
                                                                   self.altair_viz.config[
                                                                       'padding_guess'])).add_selection(
            alt.selection_interval())

        return base.encode(x=self.altair_viz.data_frame.resolve_columnname(self.field1),
                           y=self.altair_viz.data_frame.resolve_columnname(self.field2))


class AltairHorizontalStacking:

    def __init__(self, av: AltairViz, *contents):
        self.contents = contents
        chart_stack = alt.hconcat()
        for chart in self.contents:
            chart_stack |= chart
        self.chart_stack = chart_stack
        av.rendered_charts |= chart_stack

    def __call__(self):
        return self.chart_stack


class AltairVerticalStacking:

    def __init__(self, av: AltairViz, *contents):
        self.contents = contents
        chart_stack = alt.vconcat()
        for chart in self.contents:
            chart_stack &= chart
        self.chart_stack = chart_stack
        av.rendered_charts &= chart_stack

    def __call__(self):
        return self.chart_stack
