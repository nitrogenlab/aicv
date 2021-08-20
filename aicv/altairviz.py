import altair as alt


class AltairViz(object):

    #data_frame should be an instance of aicv.core.DataFrame
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.config = None

    def set_config(self, config):
        self.config = config 

    def render(self):
        if (self.config is None):
            raise RuntimeError("You need to call set_config"
                               +" to set the conifg!")
        #TODO


def get_interactive_histogram(colname):
  yaxis = alt.Y('count():Q', title="Count")
  xaxis = alt.X(colname+':Q', bin=alt.Bin(maxbins=100))
  #apparently height/width doesn't include the space for the
  # axes labels, so these need to be adjusted a bit.
  bg_histogram = alt.Chart(DF_TO_USE).mark_bar().encode(
                    y=yaxis,
                    x=xaxis,
                    color=alt.value('lightgrey')).properties(
                      width=TOTAL_WIDTH*(1-TSNE_WIDTHFRAC)/4
                            - (FONTSIZE+PADDING_GUESS),
                      height=TOTAL_HEIGHT*TSNE_HEIGHTFRAC/3
                            - (FONTSIZE+PADDING_GUESS),
                      selection=INTERVAL_SELECTION)
  fg_histogram = alt.Chart(DF_TO_USE).mark_bar().encode(
                      y=yaxis,
                      color=alt.value('steelblue'),
                      x=xaxis).transform_filter(COMPOSED_SELECTION)
  return (bg_histogram+fg_histogram)



