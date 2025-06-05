# several functions that facilitate plotting 
# well log and seismic data

import pandas as pd 

# well log data

def extract_well(df, well, well_col="WELL", 
                 depth_col="DEPTH_MD", min_depth=None):
    """
    Extracts data for a specific well from a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 
            data from multiple wells.
        well (str): The name of the well to extract.
        well_col (str): The name of the column that contains 
            well names. Defaults to "WELL".
        depth_col (str): The name of the column that contains
            depth values. Defaults to "DEPTH_MD".
        min_depth (float, optional): If specified, only rows 
            with depth >= to this value will be included.
            Defaults to None, which includes all depths.

    Returns:
        pd.DataFrame: A DataFrame containing only the rows 
            corresponding to the specified well.    Returns 
            an empty DataFrame if the well is not found.
    """
    # create an empty DataFrame
    well_df = pd.DataFrame()
    # if well is in the DataFrame column
    if well in df[well_col].values:
        # extract the well
        well_df = df[df[well_col] == well]
        # if min_depth is specified, filter the well
        if min_depth is not None:
            well_df = well_df[well_df[depth_col] >= min_depth]
    else:
        print(f"Well {well} not found in DataFrame")

    return well_df

def get_tops(df, int_col="GROUP", depth_col="DEPTH_MD"):
    """
    Identifies the top depths of intervals in a well DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame representing 
            a single well.
        int_col (str): Name of the column containing interval 
            identifiers. Defaults to "GROUP".
        depth_col (str): Name of the column containing measured 
            depths. Defaults to "DEPTH_MD".

    Returns:
        dict: A dictionary mapping each interval name 
            (from int_col) to its top depth (the first 
            occurrence in depth_col).
    """
    # find the tops or rows where a new interval starts
    
    # the comparison df[int_col] != df[int_col].shift() 
    # returns True where the current row's value is different 
    # from the previous row. mask is a boolean Series where True 
    # indicates a change in the interval column.  
    mask = df[int_col] != df[int_col].shift()
    
    # filter the DataFrame using mask to keep only those rows 
    # where the interval changes. Also, reset the index.
    m_df = df[mask].reset_index(drop=True)
    
    # create the dictionary of tops. Note that tops may be
    # repeated so we add the index to the key if the top is 
    # repeated. Also we round the depth values to 2 decimals
    tops = {}
    for i, row in m_df.iterrows():
        top = f"{row[int_col]}"
        if top not in tops:
            tops[top] = round(row[depth_col],2)
        else:
            tops[f"{top}_{i}"] = round(row[depth_col],2)

    # add the end of the log to tops
    tops["END"] = df[depth_col].max()
    
    return tops

def get_colors(df1, df2, int_col="GROUP"):
    """
    Maps intervals in a well DataFrame to their corresponding 
    RGB colors.

    Parameters:
        df1 (pd.DataFrame): DataFrame representing a well, 
            containing interval identifiers in `int_col`.
        df2 (pd.DataFrame): DataFrame defining RGB color values 
            for each interval. Must include columns:
            int_col, "RED", "GREEN", and "BLUE".
        int_col (str): Name of the column used to identify 
            intervals in both DataFrames. Defaults to "GROUP".

    Returns:
        dict: A dictionary where keys are interval names and 
            values are [R, G, B] color lists.
    """
    # find unique values in column
    intervals = df1[int_col].unique()

    # create the dictionary of colors
    colors = {}
    for interval in intervals:
        # find the row in df2 with the interval
        row = df2[df2[int_col] == interval]
        # get the RGB values
        if not row.empty:
            colors[interval] = [row["RED"].values[0],
                            row["GREEN"].values[0],
                            row["BLUE"].values[0]]
        # color values should be floats between 0 and 1
        # and the floats are rounded to 2 decimal places
        colors[interval] = [round(float(c/255), 2) for c in colors[interval]]
        # make sure the keys are strings
        colors[str(interval)] = colors.pop(interval)

    return colors

def plot_logs(df, tops, colors, axs, int_col="GROUP", 
              depth_col="DEPTH_MD"):
    """
    Plots well log data with interval shading.

    Parameters:
        df (pd.DataFrame): DataFrame containing well 
            log data.
        tops (dict): Dictionary mapping interval names 
            to their top depths.
        colors (dict): Dictionary mapping interval names 
            to RGB color lists (e.g., [R, G, B]).
        axs (list of matplotlib axes): List of subplot 
            axes on which to plot the logs.
        int_col (str): Name of the column containing interval 
            identifiers. Defaults to "GROUP".
        depth_col (str): Name of the column containing measured 
            depths. Defaults to "DEPTH_MD".

    Description:
        The function plots the well logs in the following order:
        - SP (Spontaneous Potential)
        - GR (Gamma Ray)
        - Resistivity: RMED and RDEP
        - Density: RHOB and Neutron: NPHI
        - Sonic: DTC and DTS

        It also shades the intervals defined in `tops` using 
        the corresponding colors from `colors`.

    Returns:
        None
    """
    # if not six subplots, raise an error
    if len(axs) != 6:
        print("Error: ax must have 6 subplots")
        return

    # list of logs, line colors, x limits and titles
    # for the subplots
    logs = ["SP", "GR", ["RMED","RDEP"], ["RHOB","NPHI"],
             ["DTC","DTS"], int_col]
    l_cs = ["green", "black", ["blue","red"],
                   ["red","blue"], ["red","blue"], "black"]
    x_lims = [[50, 150], [0, 300], [0.1, 100],
              [[1, 3], [0.6, 0]], [50, 200], [0, 1]]
    titles = ["SP [mV]", "GR [gAPI]", "Resistivity [ohm.m]", 
              ["RHOB [g/cm3]", "NPHI"], "Sonic [us/ft]", int_col]
    
    # iterate over subplots and plot the logs 
    for i, (log, l_c, x_lim, title) in enumerate(zip(logs, l_cs, x_lims, titles)):
        # SP and GR: i is 0 or 1, single curve each
        if i < 2: 
            # plot the log
            axs[i].plot(df[log], df[depth_col], color=l_c, lw=0.5)
            if i == 0: # on first subplot
                axs[i].invert_yaxis() # y increases down
                axs[i].set_ylabel(depth_col + " [m]") # set y label
        # Resistivity and sonic: i is 2 or 4, 2 curves each
        elif i == 2 or i == 4: 
            for j in range(2): # iterate over the two logs
                if not df[log[j]].isna().all(): # if data
                    # plot the log
                    axs[i].plot(df[log[j]], df[depth_col], 
                                color=l_c[j], lw=0.5, label=log[j])
                    axs[i].legend(loc='upper right') # add legend
            # for resistivity x axis is log scale
            if i == 2:
                axs[i].set_xscale("log") # log scale
        # RHOB and NPHI curves: i is 3
        elif i == 3: 
            ax1 = axs[i].twiny() # create a second x axis for NPHI
            ax_list = [ax1, axs[i]] # list of axes to plot on
            for j, ax in enumerate(ax_list): # iterate over axes
                # plot the log
                ax.plot(df[log[j]], df[depth_col], color=l_c[j], lw=0.5)
                # set x axis limits, labels, and colors
                ax. set_xlim(x_lim[j])
                ax.set_xlabel(title[j])
                ax.xaxis.label.set_color(l_c[j])
                ax.tick_params(axis='x', colors=l_c[j])
        # intervals: i is 6, rectangles defined by tops and colors
        elif i == 5: 
            items = list(tops.items()) # list of tops items
            for j in range(len(items) - 1): # iterate over items
                key1, val1 = items[j] # interval name and top depth
                _, val2 = items[j + 1] # next interval top depth
                color_key = key1.split("_")[0] # first part of the key
                # draw a rectangle for the interval
                axs[i].axhspan(val1, val2, facecolor = colors[color_key])
            axs[i].set_xticks([]) # no x ticks for intervals
        
        # set x_limits, title and grid
        if i != 3: # no x_limits or title for RHOB and NPHI
            axs[i].set_xlim(x_lim)
            axs[i].set_title(title)  
        if i != 5: # no grid for intervals
            axs[i].grid(axis='x', color='gray')

# seismic data

def plot_trace(trace, y, vmax, twt_pos, twt_lab, ax):
    """
    Plot trace of the seismic data. 
    
    Input:
        trace: 1D numpy array with the trace.
        y: y axis values.
        vmax: max value for the x axis.
        twt_pos: positions of the time values on the y axis.
        twt_lab: labels for the time values on the y axis.
        ax: axis of the subplot.
    """
    # plot the trace
    ax.plot(trace, y, color="black")

    # add grid
    ax.grid()
    
    # set the x limits
    ax.set_xlim(-vmax, vmax)

    # invert the y axis so that time increases downwards
    ax.invert_yaxis()
    # set the y limits
    ax.set_ylim(y[-1], y[0]) 
    # set the y ticks and labels
    ax.set_yticks(twt_pos)
    ax.set_yticklabels(twt_lab)

    # set axes labels
    ax.set_xlabel("Amplitude")
    ax.set_ylabel("Time [ms]")

def plot_slice(slice, vmax, title, sl_type, 
               ax_pos, ax_lab, fig, ax, cb=True):
    """
    Plot a slice of the seismic data. 
    
    Input:
        slice: 2D array with the seismic data.
        vmax: max value for the color scale.
        title: title of the plot.
        sl_type: slice type (inline, xline or time).
        ax_pos: positions of the axes.
        ax_lab: labels for the axes.
        fig: figure object.
        ax: axis of the subplot.
        cb: boolean for colorbar.
    """
    slice_plot = slice.copy()
    # if inline or xline slice, transpose the slice
    if sl_type == "inline" or sl_type == "xline":
        slice_plot = slice_plot.T

    # plot the slice
    sim = ax.imshow(slice_plot, cmap="RdBu", 
                    vmin=-vmax, vmax=vmax, aspect="auto")
    # colorbar
    if cb:
        fig.colorbar(sim, ax=ax)
    
    # invert axis if k slice
    if sl_type == "time":
        ax.invert_yaxis()
    
    # set title
    ax.set_title(title)
    
    # set x label    
    if sl_type == "xline":
        ax.set_xlabel("Inline")
    elif sl_type == "inline" or sl_type == "time":
        ax.set_xlabel("Xline")
    # set x ticks
    ax.set_xticks(ax_pos[0])
    ax.set_xticklabels(ax_lab[0])

    # set y label
    if sl_type == "time":
        ax.set_ylabel("Inline")
    elif sl_type == "inline" or sl_type == "xline":
        ax.set_ylabel("Time [ms]")
    # set y ticks
    ax.set_yticks(ax_pos[1])
    ax.set_yticklabels(ax_lab[1])