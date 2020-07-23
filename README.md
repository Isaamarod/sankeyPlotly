<h1> sankeyPlotly <h1>
  
  This library was developed to adapt data frames data to generate a Sankey Diagram
  
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

        


