<h1> sankeyPlotly <h1>
  
  Library developed to adapt data frames data to generate a Sankey Diagram
  
  <h2>Creación de función para preparar un Data Frame y printear un diagrama Sankey </h2>

<div class="alert alert-block alert-info">

* NECESIDADES DE SANKEY: 
    - NODOS : Lista de listas con nombres de todas las clases dentro de las columnas que se vayan a relacionar y un número asignado a cada una, por ejemplo:    
    
   <b> '[[coche,0],[moto,1],[avion,2],[viaje negocios,3], [viaje recreativo,4]] </b>

    - LINKS: Lista de listas que relaciona los nombres y la frecuencia por ejemplo:     
    
     <b> [[coche, viaje recretivo, 100], [coche, viaje negocios, 200], [avion, viaje negocios, 3], [moto, viaje recreativo, 5]]</b>
     
    'Realmente se representa con los números que sería para el caso anterior:    
     <b>[[0,4, 100], [0,3, 200], [2, 3,3], [1, 4,5]]</b>
</div>

Pasos: 

* Importación de librerias
* Importar csv como Data Frame
    
* Operaciones sobre el Data Frame original:

    - GROUP BY:  Hacer group by sum con las  columnas que se vayan a relacionar y crear columna 'sum' 
    df_grouped
    
* CODIFICADORA : Nos ayudará a asignar un número a cada valor distinto en las columnas que queramos relacionar
    - COLUMNA 'todos': 
    
    
<b> df_codificadora['todos']= df_grouped['col1'].tolist()+...+df_grouped['colN'].tolist()</b>
    
    - COLUMNA 'todosCode': 
           - Pasamos todos los valores de 'todos' a categoricos 
<b>df_codificadora.todos = pd.Categorical(df_codificadora.todos)</b>
 
           - Creamos una columna 'todosCode' con un número asignado a cada valor
df_codificadora_numbers=    df_codificadora       
           
<b> df_codificadora_numbers['todosCode'] = df_codificadora.todos.cat.codes </b>



* Creación NODOS: 

     - Eliminacion de los duplicados en df_codificadora
           
<b>   df_codificadora_uniq= df_codificadora.drop_duplicates()</b>

     - Ordenamiento de valores por todosCode: 
     
<b> df_codificadora_sorted=df_codificadora_uniq.sort_values('todosCode')</b>

    - Transformación a tipo List
<b> 
nodes = df_codificadora_sorted.values.tolist()
</b>
    - Etiquetar las filas
    
<b> 
nodes.insert(0,['Label', 'ID'])
</b>


* Creación LINKS: 

     - MERGE BY: df_codificadora_uniq , COLUMNAS para añadir cols con los numeros.
        Hacemos 1 merge por cada columna que metimos en la codificadora
<b> 
links = df_grouped.merge(df_codificadora_uniq, left_on='COLUMNA', right_on='todos')
links = links.drop('todos',axis=1)
 </b>
        
        
La columna todos se va borrando para no quedar repeticiones y quede el vestigio de df_codificadora_uniq.


        - Convertimos a tipo List
        links = links.values.tolist()
        - Etiquetar las filas
        links.insert(0,['Target', 'Source','Value'])

        


<h3> Import Libraries </h3>


```python
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# Comment this if the data visualisations doesn't work on your side
%matplotlib inline

plt.style.use('bmh')
```


```python
import plotly.graph_objects as go
import plotly.express as pex
```


```python
# imports
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# settings
init_notebook_mode(connected=True)
```


<script type="text/javascript">
window.PlotlyConfig = {MathJaxConfig: 'local'};
if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}
if (typeof require !== 'undefined') {
require.undef("plotly");
requirejs.config({
    paths: {
        'plotly': ['https://cdn.plot.ly/plotly-latest.min']
    }
});
require(['plotly'], function(Plotly) {
    window._Plotly = Plotly;
});
}
</script>



<h3> Import CSV </h3>


```python
df = pd.read_csv ('/home/VICOMTECH/iamaya/Documents/hm_gydra_cleaned/visualizations/csv1_clean3.csv',encoding = "ISO-8859-1",sep = ';',error_bad_lines=False)
```


```python
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PATIENT ID</th>
      <th>EDAD/AGE</th>
      <th>SEXO/SEX</th>
      <th>DIAG ING/INPAT</th>
      <th>F_INGRESO/ADMISSION_D_ING/INPAT</th>
      <th>F_ENTRADA_UC/ICU_DATE_IN</th>
      <th>F_SALIDA_UCI/ICU_DATE_OUT</th>
      <th>UCI_DIAS/ICU_DAYS</th>
      <th>F_ALTA/DISCHARGE_DATE_ING</th>
      <th>MOTIVO_ALTA/DESTINY_DISCHARGE_ING</th>
      <th>...</th>
      <th>AgeRangeMore</th>
      <th>AgeRangePed</th>
      <th>uci</th>
      <th>fiebrePrimTempUrg</th>
      <th>fiebreUltTempUrg</th>
      <th>ingreso_urgencias</th>
      <th>prim_const_urgencias</th>
      <th>ult_const_urgencias</th>
      <th>diasHospTotal</th>
      <th>diasHospTotalName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>577</td>
      <td>78</td>
      <td>MALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2019-12-26 00:00:00</td>
      <td>26/12/2019 17:12</td>
      <td>27/12/2019 12:22</td>
      <td>1.0</td>
      <td>2020-02-04 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Vejez</td>
      <td>Vejez</td>
      <td>Si</td>
      <td>sinDatos</td>
      <td>sinDatos</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>40</td>
      <td>Mes+</td>
    </tr>
    <tr>
      <th>1</th>
      <td>44</td>
      <td>75</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-01-28 00:00:00</td>
      <td>30/01/2020 13:03</td>
      <td>31/01/2020 17:08</td>
      <td>1.0</td>
      <td>2020-04-04 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Vejez</td>
      <td>Vejez</td>
      <td>Si</td>
      <td>sinDatos</td>
      <td>sinDatos</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>67</td>
      <td>Mes+</td>
    </tr>
    <tr>
      <th>2</th>
      <td>585</td>
      <td>62</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-02-05 00:00:00</td>
      <td>10/03/2020 14:20</td>
      <td>20/03/2020 14:11</td>
      <td>10.0</td>
      <td>2020-03-26 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto mayor</td>
      <td>Adulto mayor</td>
      <td>Si</td>
      <td>sinDatos</td>
      <td>sinDatos</td>
      <td>2020-05-02 18:21:00</td>
      <td>2020-05-02 18:27:00</td>
      <td>2020-05-02 18:34:00</td>
      <td>50</td>
      <td>Mes+</td>
    </tr>
    <tr>
      <th>3</th>
      <td>587</td>
      <td>69</td>
      <td>MALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-02-06 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-03-24 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Vejez</td>
      <td>Vejez</td>
      <td>No</td>
      <td>Febricula</td>
      <td>Febricula</td>
      <td>2020-06-02 15:27:00</td>
      <td>2020-06-02 15:35:00</td>
      <td>2020-06-02 18:54:00</td>
      <td>47</td>
      <td>Mes+</td>
    </tr>
    <tr>
      <th>4</th>
      <td>586</td>
      <td>67</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-02-06 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-03-28 00:00:00</td>
      <td>Fallecimiento</td>
      <td>...</td>
      <td>Vejez</td>
      <td>Vejez</td>
      <td>No</td>
      <td>Normal</td>
      <td>Normal</td>
      <td>2020-06-02 00:34:00</td>
      <td>2020-06-02 00:41:00</td>
      <td>2020-06-02 00:55:00</td>
      <td>51</td>
      <td>Mes+</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2084</th>
      <td>2320</td>
      <td>49</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-04-19 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-04-20 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto mayor</td>
      <td>Adulto mayor</td>
      <td>No</td>
      <td>Normal</td>
      <td>Normal</td>
      <td>2020-04-19 03:57:00</td>
      <td>2020-04-19 04:02:00</td>
      <td>2020-04-19 04:03:00</td>
      <td>1</td>
      <td>Dias</td>
    </tr>
    <tr>
      <th>2085</th>
      <td>275</td>
      <td>32</td>
      <td>MALE</td>
      <td>COVID19 - PENDIENTE</td>
      <td>2020-04-19 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-04-21 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto joven</td>
      <td>Adulto joven</td>
      <td>No</td>
      <td>Normal</td>
      <td>Normal</td>
      <td>2020-04-19 11:44:00</td>
      <td>2020-04-19 11:46:00</td>
      <td>2020-04-19 11:48:00</td>
      <td>2</td>
      <td>Dias</td>
    </tr>
    <tr>
      <th>2086</th>
      <td>273</td>
      <td>52</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-04-19 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-04-21 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto mayor</td>
      <td>Adulto mayor</td>
      <td>No</td>
      <td>Normal</td>
      <td>Normal</td>
      <td>2020-04-19 11:34:00</td>
      <td>2020-04-19 11:37:00</td>
      <td>2020-04-19 15:11:00</td>
      <td>2</td>
      <td>Dias</td>
    </tr>
    <tr>
      <th>2087</th>
      <td>287</td>
      <td>35</td>
      <td>FEMALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-04-20 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-04-21 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto joven</td>
      <td>Adulto joven</td>
      <td>No</td>
      <td>sinDatos</td>
      <td>Normal</td>
      <td>2020-04-20 07:19:00</td>
      <td>NaN</td>
      <td>2020-04-20 07:39:00</td>
      <td>1</td>
      <td>Dias</td>
    </tr>
    <tr>
      <th>2088</th>
      <td>284</td>
      <td>26</td>
      <td>MALE</td>
      <td>COVID19 - POSITIVO</td>
      <td>2020-04-20 00:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2020-04-20 00:00:00</td>
      <td>Domicilio</td>
      <td>...</td>
      <td>Adulto joven</td>
      <td>Adulto joven</td>
      <td>No</td>
      <td>Febricula</td>
      <td>Febricula</td>
      <td>2020-04-19 23:44:00</td>
      <td>2020-04-19 00:26:00</td>
      <td>2020-04-19 23:50:00</td>
      <td>0</td>
      <td>Dias</td>
    </tr>
  </tbody>
</table>
<p>2089 rows × 37 columns</p>
</div>



<h3>FUNCION: Group by LIST OF COLUMNS</h3>


```python
list_cols= ['DIAG_URG/EMERG','MOTIVO_ALTA/DESTINY_DISCHARGE_ING']

```


```python
holi = df['MOTIVO_ALTA/DESTINY_DISCHARGE_ING'].unique()
```


```python
df['motivoAlta']=df['MOTIVO_ALTA/DESTINY_DISCHARGE_ING']
df['motivoAlta']=df['motivoAlta'].astype(str)
#print(df['motivoAlta'].unique())
df_nonnan=df.loc[df['motivoAlta']!='nan']
#print(df_nonnan['motivoAlta'].unique())
motivoAlta_u=df_nonnan['motivoAlta'].unique()

```


```python
motivoAlta_u=np.sort(motivoAlta_u)
```


```python
motivoAlta_u
```




    array(['Alta Voluntaria', 'Domicilio', 'Fallecimiento',
           'Traslado a un Centro Sociosanitario', 'Traslado al Hospital'],
          dtype=object)




```python
#recibe list con las columnas por las que se va a agrupar y el data frame
def groupbyfunc (df, list_cols_input):
    list_aux=[]
    df_grouped = df.groupby(list_cols).size().reset_index(name="sum") 
    df_grouped = df_grouped[df_grouped['sum'] > 0]    
    
    list_aux.extend(list_cols)        
    list_aux.append('sum')   
        
    df_grouped =df_grouped[list_aux]
    
   
    return df_grouped
```


```python
df_grouped = groupbyfunc (df, list_cols)
```


```python
df_grouped
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DIAG_URG/EMERG</th>
      <th>MOTIVO_ALTA/DESTINY_DISCHARGE_ING</th>
      <th>sum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ALTERACIÃ N DEL NIVEL DE CONCIENCIA</td>
      <td>Domicilio</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ANSIEDAD</td>
      <td>Domicilio</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ASTENIA</td>
      <td>Domicilio</td>
      <td>6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ASTENIA</td>
      <td>Fallecimiento</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>COMPLICACIÃ N HERIDA QUIRÃ©RGICA</td>
      <td>Domicilio</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>82</th>
      <td>TRAUMATISMO CRANEAL</td>
      <td>Domicilio</td>
      <td>3</td>
    </tr>
    <tr>
      <th>83</th>
      <td>TRAUMATISMO CRANEAL</td>
      <td>Traslado a un Centro Sociosanitario</td>
      <td>1</td>
    </tr>
    <tr>
      <th>84</th>
      <td>TRAUMATISMO FACIAL</td>
      <td>Domicilio</td>
      <td>1</td>
    </tr>
    <tr>
      <th>85</th>
      <td>TRAUMATISMO MMII</td>
      <td>Fallecimiento</td>
      <td>1</td>
    </tr>
    <tr>
      <th>86</th>
      <td>TUMORACIÃ N (SIN ESPECIFICAR)</td>
      <td>Domicilio</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>87 rows × 3 columns</p>
</div>



<h3>Codificadora</h3>

<h4> FUNCION: Creación lista con las columnas a representar </h4>


```python
list_cols= ['DIAG_URG/EMERG','MOTIVO_ALTA/DESTINY_DISCHARGE_ING']
new_col_name='todos'
```


```python
list_cols = ['DIAG_URG/EMERG', 'MOTIVO_ALTA/DESTINY_DISCHARGE_ING']
```


```python
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
```


```python
df_codificadora=column2list(list_cols, df_grouped, new_col_name )
```


```python
df_codificadora
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>todos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ALTERACIÃ N DEL NIVEL DE CONCIENCIA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ANSIEDAD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ASTENIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ASTENIA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>COMPLICACIÃ N HERIDA QUIRÃ©RGICA</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>169</th>
      <td>Domicilio</td>
    </tr>
    <tr>
      <th>170</th>
      <td>Traslado a un Centro Sociosanitario</td>
    </tr>
    <tr>
      <th>171</th>
      <td>Domicilio</td>
    </tr>
    <tr>
      <th>172</th>
      <td>Fallecimiento</td>
    </tr>
    <tr>
      <th>173</th>
      <td>Domicilio</td>
    </tr>
  </tbody>
</table>
<p>174 rows × 1 columns</p>
</div>



<h4> Asignación de un nº a cada variable distinta </h3>


```python
#recibe df , columna a categorizar en la que se basa la conversion, nombre columna nueva
#devuelve frame con columna nueva añadida que contiene el numero asignado a cada uno
def number2column (df_codificadora,column_input,column_output_name):
    df_codificadora[column_input]=pd.Categorical(df_codificadora[column_input])
    df_codificadora[column_output_name] = df_codificadora[column_input].cat.codes
    df_codificadora_numbers = df_codificadora.drop_duplicates()
    #df_codificadora_numbers=df_codificadora
    return df_codificadora_numbers
```


```python
df_codificadora_numbers=number2column(df_codificadora,'todos','todosCode')
```

<h4> FUNCION: codificadora completa</h4> Union column2list y number2column.

Recibe una lista con las columnas que se van a relacionar 
Las columnas agrupadas



```python
def codificadora (df_grouped,list_cols,column_input,column_output_name):
    df_codificadora=column2list(list_cols, df_grouped, column_input )
#     print(df_codificadora)
    df_codificadora_numbers=number2column(df_codificadora,column_input,column_output_name)
#     print(df_codificadora_numbers)
    df_codificadora_numbers=df_codificadora_numbers.sort_values(column_output_name)
#     print(df_codificadora_numbers)
    return df_codificadora_numbers
```


```python
list_cols= ['DIAG_URG/EMERG','MOTIVO_ALTA/DESTINY_DISCHARGE_ING']

```


```python
df_codificadora_numbers=  codificadora (df_grouped,list_cols,'todos','todosCode')
```

<h3> NODOS </h3>


```python
def nodesfunc (df_codificadora_numbers, input_colname):
    nodes_list=df_codificadora_numbers.values.tolist()
    nodes_list.insert(0,['Label', 'ID'])    
    return nodes_list
```


```python
nodes= nodesfunc (df_codificadora_numbers,'todosCode' )
```


<h3>LINKS</h3>

Hay que relacionar mediante merges los números de las codificadoras con las columnas que queremos representar


```python
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
```


```python
links = linksfunc (df_codificadora_numbers, df_grouped,list_cols, 'todos','todosCode')
```

    /home/VICOMTECH/iamaya/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:11: SettingWithCopyWarning:
    
    
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    


<h3>prueba SANKEY </h3>


```python
# # # Retrieve headers and build dataframes
# nodes_aux=nodes

# links_aux=links
# nodes_headers = nodes_aux.pop(0)
# links_headers = links_aux.pop(0)
# df_nodes = pd.DataFrame(nodes_aux, columns = nodes_headers)
# df_links = pd.DataFrame(links_aux, columns = links_headers)

# # Sankey plot setup
# data_trace = dict(
#     type='sankey',
#     domain = dict(
#       x =  [0,1],
#       y =  [0,1]
#     ),
#     orientation = "h",
#     valueformat = ".0f",
#     node = dict(
#       pad = 10,
#     # thickness = 30,
#       line = dict(
#         color = "black",
#         width = 0
#       ),
#       label =  df_nodes['Label'].dropna(axis=0, how='any'),
      
#     ),
#     link = dict(
#       source = df_links['Source'].dropna(axis=0, how='any'),
#       target = df_links['Target'].dropna(axis=0, how='any'),
#       value = df_links['Value'].dropna(axis=0, how='any'),
      
#   )
# )

# layout = dict(
#         title = "Sankey Test",
#     height = 772,
#     font = dict(
#       size = 10),)

# fig = dict(data=[data_trace], layout=layout)
# iplot(fig, validate=False)
```


```python
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

    layout = dict(
            title = "Sankey Test",
        height = 772,
        font = dict(
          size = 10),)

    fig = dict(data=[data_trace], layout=layout)
    

    return iplot(fig, validate=False)
    
```


```python
sankey (nodes,links)
```


<div>


            <div id="05fd8f7e-bfd0-49c3-a3ba-a5eaec66a7dd" class="plotly-graph-div" style="height:772px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("05fd8f7e-bfd0-49c3-a3ba-a5eaec66a7dd")) {
                    Plotly.newPlot(
                        '05fd8f7e-bfd0-49c3-a3ba-a5eaec66a7dd',
                        [{"domain": {"x": [0, 1], "y": [0, 1]}, "link": {"source": [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 50, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 3, 3], "target": [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 2, 6, 7, 8, 9, 10, 11, 12, 13, 15, 19, 21, 24, 30, 31, 32, 33, 34, 35, 37, 44, 45, 48, 6, 8, 12, 13, 24, 27, 33, 44, 46, 6, 7, 9, 12, 15, 16, 24, 33, 35, 37, 44, 12, 44], "value": [1, 1, 6, 1, 1, 194, 6, 20, 13, 2, 1, 838, 6, 2, 12, 5, 3, 3, 1, 3, 1, 214, 1, 1, 1, 1, 1, 29, 58, 3, 1, 3, 2, 1, 1, 1, 1, 3, 130, 3, 1, 1, 3, 27, 2, 16, 1, 1, 1, 185, 5, 1, 1, 3, 26, 1, 1, 2, 16, 2, 1, 3, 13, 1, 1, 2, 2, 22, 1, 1, 1, 1, 1, 1, 9, 1, 1, 23, 1, 2, 15, 3, 1, 1, 2, 2, 1]}, "node": {"label": ["ALTERACI\u00c3\u00a0N DEL NIVEL DE CONCIENCIA", "ANSIEDAD", "ASTENIA", "Alta Voluntaria", "COMPLICACI\u00c3\u00a0N HERIDA QUIR\u00c3\u00a9RGICA", "COMPLICACI\u00c3\u00a0N POSTQUIR\u00c3\u00a9RGICA", "CUADRO CATARRAL", "DESORIENTACI\u00c3\u00a0N", "DETERIORO PACIENTE ONCOL\u00c3\u00a0GICO", "DIARREA", "DIFICULTAD EN DIURESIS", "DIFICULTAD PARA HABLAR", "DIFICULTAD RESPIRATORIA", "DISURIA", "DOLOR (SIN ESPECIFICAR)", "DOLOR ABDOMINAL", "DOLOR AL TRAGAR", "DOLOR COSTAL", "DOLOR EN EL PECHO", "DOLOR LUMBAR", "DOLOR MMII", "DOLOR TOR\u00c2\u00b5CICO", "Domicilio", "ESTRE\u00c2\u00a5IMIENTO", "FIEBRE", "Fallecimiento", "HEMORRAGIA DIGESTIVA", "HERIDA CABEZA/CARA", "HINCHAZ\u00c3\u00a0N MMII", "HIPERGLUCEMIA", "HIPERTENSI\u00c3\u00a0N ARTERIAL", "INTOXICACI\u00c3\u00a0N MEDICAMENTOSA", "MALESTAR", "MALESTAR GENERAL", "MAREO", "MELENAS", "METRORRAGIA 3\u00c2\u00a7 TRIMESTRE", "N\u00c2\u00b5USEAS/V\u00c3\u00a0MITOS", "PALPITACIONES (ARRITMIA)", "PARESIA MMSS", "REACCI\u00c3\u00a0N AL\u00c2\u0090RGICA", "SOSPECHA C\u00c3\u00a0LICO NEFRITICO", "SOSPECHA RPM", "S\u00c3\u0096NCOPE", "TOS", "TRAUMATISMO COSTAL", "TRAUMATISMO CRANEAL", "TRAUMATISMO FACIAL", "TRAUMATISMO MMII", "TUMORACI\u00c3\u00a0N (SIN ESPECIFICAR)", "Traslado a un Centro Sociosanitario", "Traslado al Hospital"], "line": {"color": "black", "width": 0}, "pad": 10}, "orientation": "h", "type": "sankey", "valueformat": ".0f"}],
                        {"font": {"size": 10}, "height": 772, "title": "Sankey Test"},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('05fd8f7e-bfd0-49c3-a3ba-a5eaec66a7dd');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>


<h3>Pipeline Completo </h3>

<h4> Recibe el dataframe y una lista con el nombre de las dos columnas a representar </h4>

##TODO: QUE RECIBA + DE DOS COLUMNAS Y FUNCIONE


```python
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
    print(nodes)
    #links
    
    links = linksfunc(df_codificadora_numbers, df_grouped,list_cols,col_todosCodif_name,col_todosCodif_cod)
    print(links)
    #sankey 
    
    
     
    return sankey (nodes,links)
```


```python
list_cols= ['DIAG_URG/EMERG','MOTIVO_ALTA/DESTINY_DISCHARGE_ING']
df = pd.read_csv ('/home/VICOMTECH/iamaya/Documents/hm_gydra_cleaned/visualizations/csv1_clean3.csv',encoding = "ISO-8859-1",sep = ';',error_bad_lines=False)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
```


```python
list_cols
```




    ['DIAG_URG/EMERG', 'MOTIVO_ALTA/DESTINY_DISCHARGE_ING']




```python
pipelineSankey (df,list_cols)
```

    [['Label', 'ID'], ['ALTERACIÃ\xa0N DEL NIVEL DE CONCIENCIA', 0], ['ANSIEDAD', 1], ['ASTENIA', 2], ['Alta Voluntaria', 3], ['COMPLICACIÃ\xa0N HERIDA QUIRÃ©RGICA', 4], ['COMPLICACIÃ\xa0N POSTQUIRÃ©RGICA', 5], ['CUADRO CATARRAL', 6], ['DESORIENTACIÃ\xa0N', 7], ['DETERIORO PACIENTE ONCOLÃ\xa0GICO', 8], ['DIARREA', 9], ['DIFICULTAD EN DIURESIS', 10], ['DIFICULTAD PARA HABLAR', 11], ['DIFICULTAD RESPIRATORIA', 12], ['DISURIA', 13], ['DOLOR (SIN ESPECIFICAR)', 14], ['DOLOR ABDOMINAL', 15], ['DOLOR AL TRAGAR', 16], ['DOLOR COSTAL', 17], ['DOLOR EN EL PECHO', 18], ['DOLOR LUMBAR', 19], ['DOLOR MMII', 20], ['DOLOR TORÂµCICO', 21], ['Domicilio', 22], ['ESTREÂ¥IMIENTO', 23], ['FIEBRE', 24], ['Fallecimiento', 25], ['HEMORRAGIA DIGESTIVA', 26], ['HERIDA CABEZA/CARA', 27], ['HINCHAZÃ\xa0N MMII', 28], ['HIPERGLUCEMIA', 29], ['HIPERTENSIÃ\xa0N ARTERIAL', 30], ['INTOXICACIÃ\xa0N MEDICAMENTOSA', 31], ['MALESTAR', 32], ['MALESTAR GENERAL', 33], ['MAREO', 34], ['MELENAS', 35], ['METRORRAGIA 3Â§ TRIMESTRE', 36], ['NÂµUSEAS/VÃ\xa0MITOS', 37], ['PALPITACIONES (ARRITMIA)', 38], ['PARESIA MMSS', 39], ['REACCIÃ\xa0N ALÂ\x90RGICA', 40], ['SOSPECHA CÃ\xa0LICO NEFRITICO', 41], ['SOSPECHA RPM', 42], ['SÃ\x96NCOPE', 43], ['TOS', 44], ['TRAUMATISMO COSTAL', 45], ['TRAUMATISMO CRANEAL', 46], ['TRAUMATISMO FACIAL', 47], ['TRAUMATISMO MMII', 48], ['TUMORACIÃ\xa0N (SIN ESPECIFICAR)', 49], ['Traslado a un Centro Sociosanitario', 50], ['Traslado al Hospital', 51]]
    [['Target', 'Source', 'Value'], [0, 22, 1], [1, 22, 1], [2, 22, 6], [4, 22, 1], [5, 22, 1], [6, 22, 194], [7, 22, 6], [8, 22, 20], [9, 22, 13], [10, 22, 2], [11, 22, 1], [12, 22, 838], [13, 22, 6], [14, 22, 2], [15, 22, 12], [17, 22, 5], [18, 22, 3], [19, 22, 3], [20, 22, 1], [21, 22, 3], [23, 22, 1], [24, 22, 214], [26, 22, 1], [27, 22, 1], [28, 22, 1], [29, 22, 1], [30, 22, 1], [32, 22, 29], [33, 22, 58], [34, 22, 3], [36, 22, 1], [37, 22, 3], [38, 22, 2], [39, 22, 1], [40, 22, 1], [41, 22, 1], [42, 22, 1], [43, 22, 3], [44, 22, 130], [46, 22, 3], [47, 22, 1], [49, 22, 1], [2, 25, 3], [6, 25, 27], [7, 25, 2], [8, 25, 16], [9, 25, 1], [10, 25, 1], [11, 25, 1], [12, 25, 185], [13, 25, 5], [15, 25, 1], [19, 25, 1], [21, 25, 3], [24, 25, 26], [30, 25, 1], [31, 25, 1], [32, 25, 2], [33, 25, 16], [34, 25, 2], [35, 25, 1], [37, 25, 3], [44, 25, 13], [45, 25, 1], [48, 25, 1], [6, 50, 2], [8, 50, 2], [12, 50, 22], [13, 50, 1], [24, 50, 1], [27, 50, 1], [33, 50, 1], [44, 50, 1], [46, 50, 1], [6, 51, 9], [7, 51, 1], [9, 51, 1], [12, 51, 23], [15, 51, 1], [16, 51, 2], [24, 51, 15], [33, 51, 3], [35, 51, 1], [37, 51, 1], [44, 51, 2], [12, 3, 2], [44, 3, 1]]


    /home/VICOMTECH/iamaya/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:11: SettingWithCopyWarning:
    
    
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    



<div>


            <div id="f0b9d28c-c5d8-425b-817b-e08de52b91f0" class="plotly-graph-div" style="height:772px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("f0b9d28c-c5d8-425b-817b-e08de52b91f0")) {
                    Plotly.newPlot(
                        'f0b9d28c-c5d8-425b-817b-e08de52b91f0',
                        [{"domain": {"x": [0, 1], "y": [0, 1]}, "link": {"source": [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 50, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 3, 3], "target": [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 2, 6, 7, 8, 9, 10, 11, 12, 13, 15, 19, 21, 24, 30, 31, 32, 33, 34, 35, 37, 44, 45, 48, 6, 8, 12, 13, 24, 27, 33, 44, 46, 6, 7, 9, 12, 15, 16, 24, 33, 35, 37, 44, 12, 44], "value": [1, 1, 6, 1, 1, 194, 6, 20, 13, 2, 1, 838, 6, 2, 12, 5, 3, 3, 1, 3, 1, 214, 1, 1, 1, 1, 1, 29, 58, 3, 1, 3, 2, 1, 1, 1, 1, 3, 130, 3, 1, 1, 3, 27, 2, 16, 1, 1, 1, 185, 5, 1, 1, 3, 26, 1, 1, 2, 16, 2, 1, 3, 13, 1, 1, 2, 2, 22, 1, 1, 1, 1, 1, 1, 9, 1, 1, 23, 1, 2, 15, 3, 1, 1, 2, 2, 1]}, "node": {"label": ["ALTERACI\u00c3\u00a0N DEL NIVEL DE CONCIENCIA", "ANSIEDAD", "ASTENIA", "Alta Voluntaria", "COMPLICACI\u00c3\u00a0N HERIDA QUIR\u00c3\u00a9RGICA", "COMPLICACI\u00c3\u00a0N POSTQUIR\u00c3\u00a9RGICA", "CUADRO CATARRAL", "DESORIENTACI\u00c3\u00a0N", "DETERIORO PACIENTE ONCOL\u00c3\u00a0GICO", "DIARREA", "DIFICULTAD EN DIURESIS", "DIFICULTAD PARA HABLAR", "DIFICULTAD RESPIRATORIA", "DISURIA", "DOLOR (SIN ESPECIFICAR)", "DOLOR ABDOMINAL", "DOLOR AL TRAGAR", "DOLOR COSTAL", "DOLOR EN EL PECHO", "DOLOR LUMBAR", "DOLOR MMII", "DOLOR TOR\u00c2\u00b5CICO", "Domicilio", "ESTRE\u00c2\u00a5IMIENTO", "FIEBRE", "Fallecimiento", "HEMORRAGIA DIGESTIVA", "HERIDA CABEZA/CARA", "HINCHAZ\u00c3\u00a0N MMII", "HIPERGLUCEMIA", "HIPERTENSI\u00c3\u00a0N ARTERIAL", "INTOXICACI\u00c3\u00a0N MEDICAMENTOSA", "MALESTAR", "MALESTAR GENERAL", "MAREO", "MELENAS", "METRORRAGIA 3\u00c2\u00a7 TRIMESTRE", "N\u00c2\u00b5USEAS/V\u00c3\u00a0MITOS", "PALPITACIONES (ARRITMIA)", "PARESIA MMSS", "REACCI\u00c3\u00a0N AL\u00c2\u0090RGICA", "SOSPECHA C\u00c3\u00a0LICO NEFRITICO", "SOSPECHA RPM", "S\u00c3\u0096NCOPE", "TOS", "TRAUMATISMO COSTAL", "TRAUMATISMO CRANEAL", "TRAUMATISMO FACIAL", "TRAUMATISMO MMII", "TUMORACI\u00c3\u00a0N (SIN ESPECIFICAR)", "Traslado a un Centro Sociosanitario", "Traslado al Hospital"], "line": {"color": "black", "width": 0}, "pad": 10}, "orientation": "h", "type": "sankey", "valueformat": ".0f"}],
                        {"font": {"size": 10}, "height": 772, "title": "Sankey Test"},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('f0b9d28c-c5d8-425b-817b-e08de52b91f0');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



```python
import plotly.graph_objects as go
import urllib, json

url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
response = urllib.request.urlopen(url)
data = json.loads(response.read())

# override gray link colors with 'source' colors
opacity = 0.4
# change 'magenta' to its 'rgba' value to add opacity
data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in data['data'][0]['node']['color']]
data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity))
                                    for src in data['data'][0]['link']['source']]

fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    valuesuffix = "TWh",
    # Define nodes
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  data['data'][0]['node']['label'],
      color =  data['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source =  data['data'][0]['link']['source'],
      target =  data['data'][0]['link']['target'],
      value =  data['data'][0]['link']['value'],
      label =  data['data'][0]['link']['label'],
      color =  data['data'][0]['link']['color']
))])

fig.update_layout(title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
                  font_size=10)
fig.show()

```


<div>


            <div id="395397cb-b875-4752-a1ec-25478409474c" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("395397cb-b875-4752-a1ec-25478409474c")) {
                    Plotly.newPlot(
                        '395397cb-b875-4752-a1ec-25478409474c',
                        [{"link": {"color": ["rgba(31, 119, 180, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(188, 189, 34, 0.4)", "rgba(31, 119, 180, 0.4)", "rgba(23, 190, 207, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(214, 39, 40, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(188, 189, 34, 0.4)", "rgba(23, 190, 207, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(255,0,255, 0.4)", "rgba(255,0,255, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(188, 189, 34, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(23, 190, 207, 0.4)", "rgba(23, 190, 207, 0.4)", "rgba(31, 119, 180, 0.4)", "rgba(31, 119, 180, 0.4)", "rgba(255, 127, 14, 0.4)", "rgba(44, 160, 44, 0.4)", "rgba(214, 39, 40, 0.4)", "rgba(214, 39, 40, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(148, 103, 189, 0.4)", "rgba(140, 86, 75, 0.4)", "rgba(227, 119, 194, 0.4)", "rgba(127, 127, 127, 0.4)", "rgba(255,0,255, 0.4)", "rgba(255,0,255, 0.4)"], "label": ["stream 1", "", "", "", "stream 1", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "stream 1", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "Old generation plant (made-up)", "New generation plant (made-up)", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""], "source": [0, 1, 1, 1, 1, 6, 7, 8, 10, 9, 11, 11, 11, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 23, 25, 5, 5, 5, 5, 5, 27, 17, 17, 28, 29, 2, 2, 2, 2, 2, 2, 2, 2, 34, 24, 35, 35, 36, 38, 37, 39, 39, 40, 40, 41, 42, 43, 43, 4, 4, 4, 26, 26, 26, 44, 45, 46, 47, 35, 35], "target": [1, 2, 3, 4, 5, 2, 4, 9, 9, 4, 12, 13, 14, 16, 14, 17, 12, 18, 19, 13, 3, 20, 21, 22, 24, 24, 13, 3, 26, 19, 12, 15, 28, 3, 18, 15, 12, 30, 18, 31, 32, 19, 33, 20, 1, 5, 26, 26, 37, 37, 2, 4, 1, 14, 13, 15, 14, 42, 41, 19, 26, 12, 15, 3, 11, 15, 1, 15, 15, 26, 26], "value": [124.729, 0.597, 26.862, 280.322, 81.144, 35, 35, 11.606, 63.965, 75.571, 10.639, 22.505, 46.184, 104.453, 113.726, 27.14, 342.165, 37.797, 4.412, 40.858, 56.691, 7.863, 90.008, 93.494, 40.719, 82.233, 0.129, 1.401, 151.891, 2.096, 48.58, 7.013, 20.897, 6.242, 20.897, 6.995, 121.066, 128.69, 135.835, 14.458, 206.267, 3.64, 33.218, 4.413, 14.375, 122.952, 500, 139.978, 504.287, 107.703, 611.99, 56.587, 77.81, 193.026, 70.672, 59.901, 19.263, 19.263, 59.901, 0.882, 400.12, 46.477, 525.531, 787.129, 79.329, 9.452, 182.01, 19.013, 289.366, 100, 100]}, "node": {"color": ["rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(255,0,255, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)", "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)"], "label": ["Agricultural 'waste'", "Bio-conversion", "Liquid", "Losses", "Solid", "Gas", "Biofuel imports", "Biomass imports", "Coal imports", "Coal", "Coal reserves", "District heating", "Industry", "Heating and cooling - commercial", "Heating and cooling - homes", "Electricity grid", "Over generation / exports", "H2 conversion", "Road transport", "Agriculture", "Rail transport", "Lighting & appliances - commercial", "Lighting & appliances - homes", "Gas imports", "Ngas", "Gas reserves", "Thermal generation", "Geothermal", "H2", "Hydro", "International shipping", "Domestic aviation", "International aviation", "National navigation", "Marine algae", "Nuclear", "Oil imports", "Oil", "Oil reserves", "Other waste", "Pumped heat", "Solar PV", "Solar Thermal", "Solar", "Tidal", "UK land based bioenergy", "Wave", "Wind"], "line": {"color": "black", "width": 0.5}, "pad": 15, "thickness": 15}, "type": "sankey", "valueformat": ".0f", "valuesuffix": "TWh"}],
                        {"font": {"size": 10}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('395397cb-b875-4752-a1ec-25478409474c');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



```python
print (data)
```

    {'data': [{'type': 'sankey', 'domain': {'x': [0, 1], 'y': [0, 1]}, 'orientation': 'h', 'valueformat': '.0f', 'valuesuffix': 'TWh', 'node': {'pad': 15, 'thickness': 15, 'line': {'color': 'black', 'width': 0.5}, 'label': ["Agricultural 'waste'", 'Bio-conversion', 'Liquid', 'Losses', 'Solid', 'Gas', 'Biofuel imports', 'Biomass imports', 'Coal imports', 'Coal', 'Coal reserves', 'District heating', 'Industry', 'Heating and cooling - commercial', 'Heating and cooling - homes', 'Electricity grid', 'Over generation / exports', 'H2 conversion', 'Road transport', 'Agriculture', 'Rail transport', 'Lighting & appliances - commercial', 'Lighting & appliances - homes', 'Gas imports', 'Ngas', 'Gas reserves', 'Thermal generation', 'Geothermal', 'H2', 'Hydro', 'International shipping', 'Domestic aviation', 'International aviation', 'National navigation', 'Marine algae', 'Nuclear', 'Oil imports', 'Oil', 'Oil reserves', 'Other waste', 'Pumped heat', 'Solar PV', 'Solar Thermal', 'Solar', 'Tidal', 'UK land based bioenergy', 'Wave', 'Wind'], 'color': ['rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(140, 86, 75, 0.8)', 'rgba(227, 119, 194, 0.8)', 'rgba(127, 127, 127, 0.8)', 'rgba(188, 189, 34, 0.8)', 'rgba(23, 190, 207, 0.8)', 'rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(140, 86, 75, 0.8)', 'rgba(227, 119, 194, 0.8)', 'rgba(127, 127, 127, 0.8)', 'rgba(188, 189, 34, 0.8)', 'rgba(23, 190, 207, 0.8)', 'rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(140, 86, 75, 0.8)', 'rgba(227, 119, 194, 0.8)', 'rgba(127, 127, 127, 0.8)', 'rgba(188, 189, 34, 0.8)', 'rgba(23, 190, 207, 0.8)', 'rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(255,0,255, 0.8)', 'rgba(227, 119, 194, 0.8)', 'rgba(127, 127, 127, 0.8)', 'rgba(188, 189, 34, 0.8)', 'rgba(23, 190, 207, 0.8)', 'rgba(31, 119, 180, 0.8)', 'rgba(255, 127, 14, 0.8)', 'rgba(44, 160, 44, 0.8)', 'rgba(214, 39, 40, 0.8)', 'rgba(148, 103, 189, 0.8)', 'rgba(140, 86, 75, 0.8)', 'rgba(227, 119, 194, 0.8)', 'rgba(127, 127, 127, 0.8)']}, 'link': {'source': [0, 1, 1, 1, 1, 6, 7, 8, 10, 9, 11, 11, 11, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 23, 25, 5, 5, 5, 5, 5, 27, 17, 17, 28, 29, 2, 2, 2, 2, 2, 2, 2, 2, 34, 24, 35, 35, 36, 38, 37, 39, 39, 40, 40, 41, 42, 43, 43, 4, 4, 4, 26, 26, 26, 44, 45, 46, 47, 35, 35], 'target': [1, 2, 3, 4, 5, 2, 4, 9, 9, 4, 12, 13, 14, 16, 14, 17, 12, 18, 19, 13, 3, 20, 21, 22, 24, 24, 13, 3, 26, 19, 12, 15, 28, 3, 18, 15, 12, 30, 18, 31, 32, 19, 33, 20, 1, 5, 26, 26, 37, 37, 2, 4, 1, 14, 13, 15, 14, 42, 41, 19, 26, 12, 15, 3, 11, 15, 1, 15, 15, 26, 26], 'value': [124.729, 0.597, 26.862, 280.322, 81.144, 35, 35, 11.606, 63.965, 75.571, 10.639, 22.505, 46.184, 104.453, 113.726, 27.14, 342.165, 37.797, 4.412, 40.858, 56.691, 7.863, 90.008, 93.494, 40.719, 82.233, 0.129, 1.401, 151.891, 2.096, 48.58, 7.013, 20.897, 6.242, 20.897, 6.995, 121.066, 128.69, 135.835, 14.458, 206.267, 3.64, 33.218, 4.413, 14.375, 122.952, 500, 139.978, 504.287, 107.703, 611.99, 56.587, 77.81, 193.026, 70.672, 59.901, 19.263, 19.263, 59.901, 0.882, 400.12, 46.477, 525.531, 787.129, 79.329, 9.452, 182.01, 19.013, 289.366, 100, 100], 'color': ['rgba(31, 119, 180, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(188, 189, 34, 0.4)', 'rgba(31, 119, 180, 0.4)', 'rgba(23, 190, 207, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(214, 39, 40, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(188, 189, 34, 0.4)', 'rgba(23, 190, 207, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(255,0,255, 0.4)', 'rgba(255,0,255, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(188, 189, 34, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(23, 190, 207, 0.4)', 'rgba(23, 190, 207, 0.4)', 'rgba(31, 119, 180, 0.4)', 'rgba(31, 119, 180, 0.4)', 'rgba(255, 127, 14, 0.4)', 'rgba(44, 160, 44, 0.4)', 'rgba(214, 39, 40, 0.4)', 'rgba(214, 39, 40, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(148, 103, 189, 0.4)', 'rgba(140, 86, 75, 0.4)', 'rgba(227, 119, 194, 0.4)', 'rgba(127, 127, 127, 0.4)', 'rgba(255,0,255, 0.4)', 'rgba(255,0,255, 0.4)'], 'label': ['stream 1', '', '', '', 'stream 1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'stream 1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Old generation plant (made-up)', 'New generation plant (made-up)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}}], 'layout': {'title': {'text': "Energy forecast for 2050, UK — Department of Energy & Climate Change<br>Imperfect copy of <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock's example</a><br>with numerous <a href='https://plotly.com/javascript/'>Plotly</a> features"}, 'width': 1118, 'height': 772, 'font': {'size': 10}, 'updatemenus': [{'y': 1, 'buttons': [{'label': 'Light', 'method': 'relayout', 'args': ['paper_bgcolor', 'white']}, {'label': 'Dark', 'method': 'relayout', 'args': ['paper_bgcolor', 'black']}]}, {'y': 0.9, 'buttons': [{'label': 'Thick', 'method': 'restyle', 'args': ['node.thickness', 15]}, {'label': 'Thin', 'method': 'restyle', 'args': ['node.thickness', 8]}]}, {'y': 0.8, 'buttons': [{'label': 'Small gap', 'method': 'restyle', 'args': ['node.pad', 15]}, {'label': 'Large gap', 'method': 'restyle', 'args': ['node.pad', 20]}]}, {'y': 0.7, 'buttons': [{'label': 'Snap', 'method': 'restyle', 'args': ['arrangement', 'snap']}, {'label': 'Perpendicular', 'method': 'restyle', 'args': ['arrangement', 'perpendicular']}, {'label': 'Freeform', 'method': 'restyle', 'args': ['arrangement', 'freeform']}, {'label': 'Fixed', 'method': 'restyle', 'args': ['arrangement', 'fixed']}]}, {'y': 0.6, 'buttons': [{'label': 'Horizontal', 'method': 'restyle', 'args': ['orientation', 'h']}, {'label': 'Vertical', 'method': 'restyle', 'args': ['orientation', 'v']}]}]}}



```python
datatype = df.dtypes
```


```python
datatype
```




    PATIENT ID                              int64
    EDAD/AGE                                int64
    SEXO/SEX                               object
    DIAG ING/INPAT                         object
    F_INGRESO/ADMISSION_D_ING/INPAT        object
    F_ENTRADA_UC/ICU_DATE_IN               object
    F_SALIDA_UCI/ICU_DATE_OUT              object
    UCI_DIAS/ICU_DAYS                     float64
    F_ALTA/DISCHARGE_DATE_ING              object
    MOTIVO_ALTA/DESTINY_DISCHARGE_ING      object
    F_INGRESO/ADMISSION_DATE_URG/EMERG     object
    ESPECIALIDAD/DEPARTMENT_URG/EMERG      object
    DIAG_URG/EMERG                         object
    DESTINO/DESTINY_URG/EMERG              object
    TEMP_PRIMERA/FIRST_URG/EMERG          float64
    FC/HR_PRIMERA/FIRST_URG/EMERG           int64
    GLU_PRIMERA/FIRST_URG/EMERG             int64
    SAT_02_PRIMERA/FIRST_URG/EMERG          int64
    TA_MAX_PRIMERA/FIRST/EMERG_URG          int64
    TA_MIN_PRIMERA/FIRST_URG/EMERG          int64
    FC/HR_ULTIMA/LAST_URG/EMERG             int64
    TEMP_ULTIMA/LAST_URG/EMERG            float64
    GLU_ULTIMA/LAST_URG/EMERG               int64
    SAT_02_ULTIMA/LAST_URG/EMERG            int64
    TA_MAX_ULTIMA/LAST_URGEMERG             int64
    TA_MIN_ULTIMA/LAST_URG/EMERG            int64
    AgeRange                               object
    AgeRangeMore                           object
    AgeRangePed                            object
    uci                                    object
    fiebrePrimTempUrg                      object
    fiebreUltTempUrg                       object
    ingreso_urgencias                      object
    prim_const_urgencias                   object
    ult_const_urgencias                    object
    diasHospTotal                           int64
    diasHospTotalName                      object
    dtype: object




```python
tmp3 = datatype[(datatype == 'object') | (datatype == 'category')].index.tolist()
```


```python
tmp3
```




    ['SEXO/SEX',
     'DIAG ING/INPAT',
     'F_INGRESO/ADMISSION_D_ING/INPAT',
     'F_ENTRADA_UC/ICU_DATE_IN',
     'F_SALIDA_UCI/ICU_DATE_OUT',
     'F_ALTA/DISCHARGE_DATE_ING',
     'MOTIVO_ALTA/DESTINY_DISCHARGE_ING',
     'F_INGRESO/ADMISSION_DATE_URG/EMERG',
     'ESPECIALIDAD/DEPARTMENT_URG/EMERG',
     'DIAG_URG/EMERG',
     'DESTINO/DESTINY_URG/EMERG',
     'AgeRange',
     'AgeRangeMore',
     'AgeRangePed',
     'uci',
     'fiebrePrimTempUrg',
     'fiebreUltTempUrg',
     'ingreso_urgencias',
     'prim_const_urgencias',
     'ult_const_urgencias',
     'diasHospTotalName']




```python

```
