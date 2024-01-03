from pyecharts.charts import Line, Bar, Scatter
import pyecharts.options as opts


selected_color = ['#6A5ACD','#5F9EA0',"#3CB371","#FF7F50"]
def draw_line(x_data,y_data:dict,file_name):
    """Use Echarts to draw Line plot.
    And output to output_file.
    Keyword arguments:
    data: dict that contains data. Stored in format:
    {
    "TypeA":[y_data],
    "TypeB":[y_data],
    ...
    }
    Return: map
    """

    c = Line(
        init_opts=opts.InitOpts(width="1280px",height="720px")
             ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            # min_=0,
            # max_=600,
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        title_opts=opts.TitleOpts(file_name)
    ).add_xaxis(xaxis_data=x_data)

    class_name = list(y_data.keys())
    for _ in range(len(class_name)):
        c.add_yaxis(
        color=selected_color[_],
        series_name=class_name[_],
        y_axis=y_data[class_name[_]],
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
    c.render(f"{file_name}.html")
    return c

if __name__ == "__main__":
    import numpy as np
    data = np.load(r"process-new\1\down\amp.npy")
    print(data.shape)
    sample = data[0]
    print(sample.shape)
    x_data = [_ for _ in range(1,625)]
    y_data = sample.tolist()
    y_data_1 = [y_data[i][0][0] for i in range(len(x_data))]
    y_data_2 = [y_data[i][0][1] for i in range(len(x_data))]

    y_ = {
        "gNB_TX_1":y_data_1,
        "gNB_TX_2":y_data_2,
    }
    c = draw_line(x_data,y_,"Origin Data")