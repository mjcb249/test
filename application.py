from dash import Dash, html, dash_table, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# Incorporate data
x = pd.read_csv('DiagnosisRegistryReport.csv')
# Remove Duplicated rows:
x = x.drop_duplicates()
# Change ,MD to DM in PROVIDER column
mask = x['PROVIDER'].str.contains(', MD')
x.loc[mask, 'PROVIDER'] = 'Elizabeth BenstockDM' 
# Remove empty last column
x = x.iloc[:, :-1]
# Random Age column - Delete later
x['Age'] = np.random.randint(low = 1, high = 100, size = len(x))



########################################

# Initialize the app
app = Dash()

# Get min and max age for slider range
min_age = x['Age'].min()
max_age = x['Age'].max()

# Provider Options
provider_options = [{'label': 'All Providers', 'value': 'all'}] + [
    {'label': provider, 'value': provider} for provider in sorted(x['PROVIDER'].unique())
]

# App layout
app.layout = html.Div([
    html.H1("Histogram of Age", style = {'textAlign': 'center'}),
    dcc.Graph(
        id='age-histogram',
    ),
    dcc.RangeSlider(
      id = 'age-slider',
      min = min_age,
      max = max_age,
      step = 1,
      value = [min_age, max_age],
      marks={int(age): str(int(age)) for age in range(int(min_age), int(max_age)+1, max(1, (max_age-min_age)//10))},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Dropdown(
        id='provider-dropdown',
        options=provider_options,
        value='all',  # Default to first provider
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    )
])

@app.callback(
  Output('age-histogram', 'figure'),
  Input('age-slider', 'value'),
  Input('provider-dropdown', 'value')
)

def update_histogram(selected_range, selected_provider):
  filtered_df = x[(x['Age'] >= selected_range[0]) & (x['Age'] <= selected_range[1])]
  if selected_provider != 'all':
    filtered_df = x[x['PROVIDER'] == selected_provider]
  figure=px.histogram(filtered_df, x='Age', nbins = 10, title="Distribution of Age")
  return figure

# Run the app
application = app.server

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8050, debug=True)

########################################

