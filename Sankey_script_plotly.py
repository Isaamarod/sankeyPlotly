import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt



plt.style.use('bmh')

import plotly.graph_objects as go
import plotly.express as pex

# imports
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

 ##TODO: RECIEVE MORE THAN ONE COLUMN


#recibe list con las columnas por las que se va a agrupar y el data frame
def groupbyfunc (df, list_cols_input):
    list_aux=[]
    df_grouped = df.groupby(list_cols_input).size().reset_index(name="sum") 
    df_grouped = df_grouped[df_grouped['sum'] > 0]    
    
    list_aux.extend(list_cols_input)        
    list_aux.append('sum')   
        
    df_grouped =df_grouped[list_aux]
    df_grouped = df_grouped.nlargest(10, columns=['sum'])
   
    return df_grouped

def column2list (list_cols, df_grouped, new_col_name ):
    list_of_lists=[]
    df_codificadora=pd.DataFrame()
    for i in list_cols:
        #print(i)
        list_of_lists+= df_grouped[i].tolist()
        
        
    df_codificadora[new_col_name]=list_of_lists
    #print(df_codificadora[new_col_name])
    #print("HASTA AQUI COLUMN2LIST")
    return df_codificadora



#recibe df , columna a categorizar en la que se basa la conversion, nombre columna nueva
#devuelve frame con columna nueva añadida que contiene el numero asignado a cada uno
def number2column (df_codificadora,column_input,column_output_name):
    df_codificadora[column_input]=pd.Categorical(df_codificadora[column_input])
    df_codificadora[column_output_name] = df_codificadora[column_input].cat.codes
    df_codificadora_numbers = df_codificadora.drop_duplicates()
    
    return df_codificadora_numbers



def codificadora (df_grouped,list_cols,column_input,column_output_name):
    df_codificadora=column2list(list_cols, df_grouped, column_input )
#     print(df_codificadora)
    df_codificadora_numbers=number2column(df_codificadora,column_input,column_output_name)
#     print(df_codificadora_numbers)
    df_codificadora_numbers=df_codificadora_numbers.sort_values(column_output_name)
#     print(df_codificadora_numbers)
    return df_codificadora_numbers



def nodesfunc (df_codificadora_numbers, input_colname):
    nodes_list=df_codificadora_numbers.values.tolist()
    nodes_list.insert(0,['Label', 'ID'])    
    return nodes_list


def linksfunc (df_codificadora_numbers, df_grouped,list_cols, input_col_name_codif,input_col_code_codif):
    for i in range(len(list_cols)):        
        
        
        df_grouped= df_grouped.merge(df_codificadora_numbers, left_on=list_cols[i], right_on=input_col_name_codif)
        df_grouped = df_grouped.rename(columns={input_col_code_codif: 'link'+str(i)})
        df_grouped = df_grouped.drop(input_col_name_codif,axis=1)
        
                          
    df_links= df_grouped.loc[:, df_grouped.columns.str.startswith('link')]
    df_links['sum']=df_grouped['sum']
    links_list = df_links.values.tolist()
    links_list.insert(0,['Target', 'Source','Value'])

    return links_list




# Retrieve headers and build dataframes
def sankey (nodes,links):
    nodes_headers = nodes.pop(0)
    links_headers = links.pop(0)
    df_nodes = pd.DataFrame(nodes, columns = nodes_headers)
    df_links = pd.DataFrame(links, columns = links_headers)

    # Sankey plot setup
    data_trace = dict(
        type='sankey',
        domain = dict(
          x =  [0,1],
          y =  [0,1]
        ),
        orientation = "h",
        valueformat = ".0f",
        node = dict(
          pad = 10,
        # thickness = 30,
          line = dict(
            color = "black",
            width = 0
          ),
          label =  df_nodes['Label'].dropna(axis=0, how='any'),

        ),
        link = dict(
          source = df_links['Source'].dropna(axis=0, how='any'),
          target = df_links['Target'].dropna(axis=0, how='any'),
          value = df_links['Value'].dropna(axis=0, how='any'),

      )
    )
    layout = go.Layout(
            title = "Sankey Test",
        height = 772,
        font = dict(
          size = 10),)



    fig = go.Figure(data=[data_trace], layout=layout)
    

    return fig
    


def pipelineSankey (df,list_cols):
    col_todosCodif_name='todos'
    col_todosCodif_cod='todosCode'
    
    #group by
    df_grouped = groupbyfunc(df,list_cols)
    
    
    #codificadora
    
    df_codificadora_numbers=codificadora (df_grouped,list_cols,col_todosCodif_name,col_todosCodif_cod)
#     print(df_codificadora_numbers)
    #nodes
    
    nodes= nodesfunc(df_codificadora_numbers,col_todosCodif_cod)
    #print(nodes)
    #links
    
    links = linksfunc(df_codificadora_numbers, df_grouped,list_cols,col_todosCodif_name,col_todosCodif_cod)
    print(links)
    #sankey 
    
    
     
    return sankey (nodes,links)




