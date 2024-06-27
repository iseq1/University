import numpy as np
import plotly.graph_objects as go

N = 100000
fig = go.Figure(data=go.Scattergl(
    x = np.random.randn(N),
    y = np.random.randn(N),
    mode = 'markers',
    marker=dict(
        color=np.random.randn(N),
    #     colorscale ='Viridis',
    #     colorscale = 'Reds',
        colorscale = 'peach',
        line_width = 1
    )
))

fig.show()