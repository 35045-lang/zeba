import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table # Import the DataTable component
import plotly.express as px
from dash.dependencies import Input, Output

# --- 1. Data Loading and Preparation ---
try:
    df = pd.read_csv('exam_data.csv')
except FileNotFoundError:
    print("Error: 'exam_data.csv' not found. Please create the file.")
    exit()

# Get a unique list of subjects for the dropdown options
subject_options = [{'label': i, 'value': i} for i in df['Subject'].unique()]
default_subject = df['Subject'].unique()[0]

# --- 2. Initialize the Dash Application ---
app = dash.Dash(__name__)

# --- 3. Define the Dashboard Layout (HTML Structure) ---
app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    
    # Title
    html.H1(
        children='📊 Exam Results and Trends Dashboard',
        style={'textAlign': 'center', 'color': '#0A1931', 'marginBottom': '30px'}
    ),

    # Dropdown Component for Subject Selection
    html.Div(
        children=[
            html.Label('Select Subject:', style={'fontSize': '18px', 'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='subject-dropdown',
                options=subject_options,
                value=default_subject, # Set the default selected value
                clearable=False,
                style={'width': '300px', 'display': 'inline-block'}
            )
        ], 
        style={'textAlign': 'center', 'marginBottom': '40px'}
    ),

    # --- NEW: Side-by-Side Content Container ---
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, children=[
        
        # COLUMN 1: Bar Graph (65% width)
        html.Div(style={'flex': '65%'}, children=[
            dcc.Graph(
                id='score-trend-graph',
                style={'height': '600px'}
            )
        ]),
        
        # COLUMN 2: Data Table (35% width)
        html.Div(style={'flex': '35%', 'paddingTop': '40px'}, children=[
            html.H3("Selected Exam Mark List", style={'textAlign': 'center', 'color': '#0A1931'}),
            dash_table.DataTable(
                id='mark-list-table',
                columns=[{"name": i, "id": i} for i in df.columns], # Define columns
                data=df.to_dict('records'), # Initial data (will be updated by callback)
                style_table={'overflowX': 'auto', 'height': 550, 'overflowY': 'auto'},
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold'
                }
            )
        ])
    ])
    # --- END Side-by-Side Content Container ---
])


# --- 4. Define Interactivity (The Callback) ---
@app.callback(
    [Output(component_id='score-trend-graph', component_property='figure'),
     Output(component_id='mark-list-table', component_property='data')], # ADDED TABLE OUTPUT
    Input(component_id='subject-dropdown', component_property='value')
)
def update_content(selected_subject):
    """Updates the graph AND the data table based on the selected subject."""
    
    # Filter data for the selected subject
    filtered_df = df[df['Subject'] == selected_subject]

    # --- 1. Update Graph (Same as before) ---
    fig = px.bar(
        filtered_df,
        x='Semester',
        y='Score',
        color='Student_Name', 
        title=f'Individual Student Scores in {selected_subject} by Semester',
        barmode='group', 
        height=550,
        color_discrete_sequence=px.colors.qualitative.Safe 
    )
    
    fig.update_layout(
        transition_duration=500,
        xaxis_title="Semester",
        yaxis_title="Score Achieved (%)"
    )

    # --- 2. Update Data Table ---
    # Convert the filtered DataFrame to a list of dictionaries for the DataTable
    table_data = filtered_df.to_dict('records')
    
    return fig, table_data # Return both the figure and the table data


# --- 5. Run the Application ---
if __name__ == '__main__':
    app.run(debug=True)