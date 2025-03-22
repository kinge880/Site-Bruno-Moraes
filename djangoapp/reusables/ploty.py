import plotly.express as px
import pandas as pd
from plotly.offline import plot

def reusablePloty(data, columns, xvalue, yvalue, title, plot_type, label_format=None):
    try:
        # Colocando os dados em um DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Restante do código para criação do gráfico...
        if plot_type == 'pie':
            fig = px.pie(df, values=yvalue, names=xvalue, title=title)
        elif plot_type == 'bar':
            df_sorted = df.sort_values(by=yvalue, ascending=True)
            print(df_sorted)
            fig = px.bar(df_sorted, x=xvalue, y=yvalue, color=xvalue, title=title)
        else:
            return "<p>Erro: Tipo de gráfico não suportado.</p>"

        # Centralizando o título
        fig.update_layout(title=dict(text=title, x=0.5, y=0.95, xanchor='center', yanchor='top'), autosize=True)
        
        # Exibir o gráfico
        return plot({'data': fig}, output_type='div')
    except Exception as e:
        return f"<p>Erro: {e}</p>"