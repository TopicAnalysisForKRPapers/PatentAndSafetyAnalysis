### aria1th@github

### visualize dmr results

from pandas import read_csv
import matplotlib.pyplot as plt
import seaborn as sns

def read_dmr(dmr_path):
    dmr = read_csv(dmr_path, index_col=0)
    return dmr

def visualize_dmr(dmr_path, topic_num: int = -1, save_path: str = None):
    topics_features = read_dmr(dmr_path)
    df1_transposed = topics_features.T.rename_axis('Date').reset_index()
    # sort by date
    df1_transposed_sorted = df1_transposed.sort_values(by='Date')
    df1_transposed_rel = df1_transposed_sorted.melt('Date', var_name='Topic', value_name='Importance Score')

    g = sns.relplot(x="Date", y="Importance Score", hue='Topic', dashes=False, markers=True,  data=df1_transposed_rel, kind='line')
    # limit xticks count to 10
    year_amount = 10
    assert year_amount > 0, 'year_amount should be positive'
    xticks = g.ax.get_xticks()
    assert len(xticks) > year_amount, f'year_amount should be less than xticks count, {len(xticks)} '
    g.ax.set_xticks(xticks[::int(len(xticks)/year_amount)])
    # reverse x axis
    #g.ax.invert_xaxis()
    g.fig.autofmt_xdate()
    g.fig.suptitle('DMR Topic Model Results')
    # select topic
    if topic_num != -1:
        g.fig.suptitle(f'Topic {topic_num} in DMR Topic Model Results')
        g.ax.set_title(f'Topic {topic_num}')
        legend = g.ax.get_legend()
        if legend is not None:
            legend.set_visible(False)
        # exclude other topics
        g:sns.FacetGrid
        for idx, line in enumerate(g.ax.lines):
            if idx != topic_num:
                line.set_visible(False)
    if save_path is not None:
        g.savefig(save_path)
    plt.show()
    return g

dmr_path = 'dmr_topic_year.csv'

visualize_dmr(dmr_path, topic_num=1, save_path='dmr_topic_all.png')

# visualize specific topic
# visualize_dmr(dmr_path, topic_num=0, save_path='dmr_topic_0.png')