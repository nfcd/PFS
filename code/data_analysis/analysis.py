# several functions that facilitate the analysis
# of well log data

import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def property_table(df, class_col, prop_col):
    """
    For a given DataFrame df with well logs, this function 
    creates a table with the statistics of a property prop_col
    for each class in class_col.
    
    Input:
    df: DataFrame with the well logs
    class_col: string with the name of the column with the
        classes (e.g., "LITH" for lithology)
    prop_col: string with the name of the column with the
        property to analyze (e.g., "GR" for gamma ray)
    
    Output:
    table: DataFrame with the statistics of the property
        for each class
    """
    # get the classes
    classes = df[class_col].unique()
    # create a table
    table = pd.DataFrame(index=["count", "min", 
                                "max", "mean", "std", 
                                "25%", "50%", "75%"])
    for clas in classes:
        # get the porosity for the flow unit
        prop = df[df[class_col] == clas][prop_col]
        # add statistics to the table
        table[clas] = [prop.count(), prop.min(), prop.max(), 
                       prop.mean(), prop.std(), 
                       prop.quantile(0.25), prop.median(), 
                       prop.quantile(0.75)]
    
    return table

def property_plot(df, class_col, colors, prop_col, 
                  type="boxplot"):
    """
    For a given DataFrame df with well logs, this function
    plots the property prop_col for each class in class_col.
    
    Input:
    df: DataFrame with the well logs
    class_col: string with the name of the column with the
        classes (e.g., "LITH" for lithology)
    colors: dictionary with the class names as the keys
        and the colors as [red, green, blue] values
    prop_col: string with the name of the column with the
        property to analyze (e.g., "GR" for gamma ray)
    type: string with the type of plot to create.
        Options are "boxplot" and "violin"
    
    Output:
        returns the figure 
    """
    # create a figure
    fig, ax = plt.subplots(figsize=(10, 6))
    # create the plot
    if type == "boxplot":
        # create a boxplot
        sns.boxplot(x=class_col, y=prop_col, data=df, 
                    hue=class_col, palette=colors, ax=ax)
    elif type == "violin":
        # create a violin plot
        sns.violinplot(x=class_col, y=prop_col, data=df, 
                       hue=class_col, palette=colors, ax=ax)
    else:
        raise ValueError("type must be 'box' or 'violin'")
    
    # set the x-axis label
    ax.set_xlabel(class_col)
    # set the y-axis label
    ax.set_ylabel(prop_col)
    # show the plot
    plt.show()

    return fig

def cross_plot(df, col_1, col_2, class_col, colors, ax):
    """
    Cross plots two columns of the DataFrame df, and color the
    points by the classes in class_col.
    
    Input:
    df: DataFrame with the well logs
    col_1 and col_2: columns to cross plot
    class_col: string with the name of the column with the
        classes (e.g., "LITH" for lithology)
    cols: dictionary with the class names as the keys
        and the colors as [red, green, blue] values
    ax: axis to plot on
    
    Output:
    returns the slope, intercept and R² of the line
    fit to the data    
    """
    
    # create a scatter plot of the two columns
    sns.scatterplot(x=col_1, y=col_2, data=df, 
                       hue=class_col, palette=colors, ax=ax)
    
    # create a dataframe with the two columns and drop NaNs
    df_s = df[[col_1, col_2]].dropna()
    # get the x and y data
    x, y = df_s[col_1], df_s[col_2]
    
    # fit a line to the data
    m, b, r, _, _ = linregress(x, y)
    # plot the line
    ax.plot(x, m * x + b, color="red", linestyle="--")
    
    ax.legend()
    
    return m, b, r**2

def optimal_clusters(data, max_k):
    """
    chooses the optimal number of clusters
    using the elbow and silhouette methods
    
    Input:
    data: DataFrame with the data to cluster
    max_k: maximum number of clusters to test
    
    Output:
    returns the figure
    """ 
    means_e = []
    means_s = []
    inertias = []
    scores = []

    for k in range(1,max_k+1):
        means_e.append(k)
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
        if k > 1:
            means_s.append(k)
            score = silhouette_score(data, kmeans.labels_)
            scores.append(score)
        
    fig, axs = plt.subplots(1,2,figsize=(10, 5))
    axs[0].plot(means_e, inertias, 'o-')
    axs[1].plot(means_s, scores, 'o-')

    y_labels = ["Inertia", "Silhouette Score"]
    titles = ["Elbow Curve", "Silhouette Curve"]
    for i, ax in enumerate(axs):
        ax.set_ylabel(y_labels[i])
        ax.set_title(titles[i])
        ax.set_xlabel("Number of Clusters")
        ax.grid()
    
    fig.tight_layout()
    plt.show()

    return fig  

def cluster_data(data, k):
    """
    Performs KMeans clustering 
    
    Input:
    data: DataFrame (e.g., well logs) to cluster
    k: number of clusters to create
    
    Output:
    returns the KMeans object and the labels
    """
    # create the KMeans object
    kmeans = KMeans(n_clusters=k, random_state=42)
    # fit the model
    kmeans.fit(data)
    
    return kmeans, kmeans.labels_