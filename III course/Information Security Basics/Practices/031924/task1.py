import plotly.graph_objects as go

def layout(x,y):
    fig = go.Figure(go.Scattermapbox(
        fill="toself",
        lon=[40, 36, 36, 40], lat=[57,57,55, 55],
        marker={'size': 10, 'color': "orange"}))
    fig1 = go.Figure(go.Scattermapbox(
        fill="toself",
        lon=[50, 46, 46, 50], lat=[57, 57, 55, 55],
        marker={'size': 10, 'color': "orange"}))
    fig2 = go.Figure(go.Scattermapbox(
        fill="toself",
        lon=[200, 30, 30, 200], lat=[40,40,100, 100],
        marker={'size': 10, 'color': "orange"}))
    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'center': {'lon': 40, 'lat': 50},
            'zoom': 5},
        showlegend=False
    )
    fig1.update_layout(
        mapbox={
            'style': "open-street-map",
            'center': {'lon': 40, 'lat': 50},
            'zoom': 5},
        showlegend=False
    )
    fig2.update_layout(
        mapbox={
            'style': "open-street-map",
            'center': {'lon': 40, 'lat': 50},
            'zoom': 5},
        showlegend=False
    )
    fig.show()
    fig1.show()
    fig2.show()


layout([74, 70, 70, 74],[47, 47, 45, 45])