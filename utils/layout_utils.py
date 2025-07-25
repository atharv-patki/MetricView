# utils/layout_utils.py

import plotly.graph_objs as go
import pandas as pd

def create_gauge(title, value, min_val=0, max_val=100):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [min_val, max_val]}},
    ))

def bar_chart(df: pd.DataFrame, x_col: str, y_col: str):
    df = df.groupby(x_col)[y_col].mean().reset_index()
    fig = go.Figure(data=[
        go.Bar(x=df[x_col], y=df[y_col], marker_color='skyblue')
    ])
    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col, height=400)
    return fig
