import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px


def scatterer(dataset,title,x_column,x_title,y_column,y_title,color_column,legend_title):

    """
    helper function to generate scatter plots.
    takes datasets, columns for x,y and desired title names for them,
    column which is use as color map and desired name for legend title -> plotly scatter plot
    """
    fig = px.scatter(dataset, x=x_column, y=y_column, color=color_column)
    fig.update_layout(
    title=title,
    xaxis_title=x_title,
    yaxis_title=y_title,
    legend_title=legend_title,
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    ) )
    fig.update_layout(
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend={
        'yanchor': 'top'})
    return fig

def pies(dataset,title,legend):
    """
    helper function to generate pie charts. 
    Takes dataset, desirable title and legend names -> plotly pie charts
    """
    #adding column to count 
    dataset['count'] =1
    fig = px.pie(dataset,values='count',names='rating_range')
    fig.update_layout(
    title=title,
    legend_title=legend,
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    ) )
    fig.update_layout(
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend={
        'yanchor': 'top'})
    return fig

def scatter_3d(dataset,title,x_col,x_title,y_col,y_title,z_col,z_title,color,legend_title):

    """
    helper function to generate 3d scatter plots.
    Takes dataset, title , columns for x,y,z, title for x,y,z axes,
    legend titile , column to use as colormap, legend title -> plotly scatter 3d
    """

    fig = px.scatter_3d(dataset,x=x_col,y=y_col,z=z_col,color=color)
    fig.update_layout(
    title=title,
    legend_title=legend_title,
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    ) )
    fig.update_layout(
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        legend={
        'yanchor': 'top'})
        
    fig.update_layout(scene = dict(
                    xaxis_title=x_title,
                    yaxis_title=y_title,
                    zaxis_title=z_title))
    return fig

def heatmap(df,title,legend_title):
    fig = px.imshow(df.corr(),title=title,
                labels=dict(color=legend_title),
                x=df.corr().columns,
                y=df.corr().columns
               )
    fig.update_layout(font=dict(
            family="Courier New, monospace",
            size=10,
            color="RebeccaPurple"
        ) )
    fig.update_layout(
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            legend={
            'yanchor': 'top'})
    return fig

def barchart(df,min,max):
    df = df.groupby(['first_published']).count().sort_values(by='titles')
    fig = px.bar(df[(df['first_published']>=min)&(df['first_published']<=max)],x=df.index,y='count')
    return fig