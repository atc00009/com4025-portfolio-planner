import os
import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px

# 1. Official Task Database from COM4025 Assessment Brief
tasks_data = [
    # Section 1 - LO1 (Design Principles & Core Functions)
    {"Task #": 1, "Section": "Section 1 (LO1)", "Deliverable": "Self-Help Guide (.docx)", "Marks": 10, "Select": "Not Selected", "Description": "Network troubleshooting guide (IPConfig, screenshots) for non-technical staff."},
    {"Task #": 2, "Section": "Section 1 (LO1)", "Deliverable": "Video Analysis (.mp4)", "Marks": 20, "Select": "Selected", "Description": "Narrated Task Manager performance analysis of CPU/RAM/Disk under two workloads."},
    {"Task #": 3, "Section": "Section 1 (LO1)", "Deliverable": "Word Guide (.docx)", "Marks": 20, "Select": "Not Selected", "Description": "Word guide explaining 5 core OS design principles with Lumina Creative Windows examples."},
    {"Task #": 4, "Section": "Section 1 (LO1)", "Deliverable": "Infographic (.pptx/.docx)", "Marks": 20, "Select": "Not Selected", "Description": "Infographic explaining memory hierarchy (CPU cache, RAM, virtual memory, storage)."},
    {"Task #": 5, "Section": "Section 1 (LO1)", "Deliverable": "Video Demo (.mp4)", "Marks": 30, "Select": "Not Selected", "Description": "Video demonstrating 1GB VHD setup in Windows VM (GPT, NTFS, Student ID label)."},
    
    # Section 2 - LO2 (Enterprise Security Configuration)
    {"Task #": 6, "Section": "Section 2 (LO2)", "Deliverable": "Checklist Table (.docx)", "Marks": 10, "Select": "Not Selected", "Description": "10-item checklist table in Word explaining local admin rights & UK DPA compliance."},
    {"Task #": 7, "Section": "Section 2 (LO2)", "Deliverable": "Video Hardening (.mp4)", "Marks": 20, "Select": "Not Selected", "Description": "Video outlining desktop security hardening steps using Windows Security features."},
    {"Task #": 8, "Section": "Section 2 (LO2)", "Deliverable": "Infographic (.pptx/.docx)", "Marks": 30, "Select": "Selected", "Description": "RBAC infographic showing Windows Security Groups, NTFS, and OneDrive sharing."},
    {"Task #": 9, "Section": "Section 2 (LO2)", "Deliverable": "Technical Guide (.docx)", "Marks": 30, "Select": "Not Selected", "Description": "Technical guide showing how to add a user (Student ID) to Windows & Admin group."},
    {"Task #": 10, "Section": "Section 2 (LO2)", "Deliverable": "Video Security (.mp4)", "Marks": 30, "Select": "Not Selected", "Description": "Video identifying an open listening port, matching PID in Task Manager, & mitigations."},
    
    # Section 3 - LO3 (Monitoring OS Performance & Improvement)
    {"Task #": 11, "Section": "Section 3 (LO3)", "Deliverable": "Video Logs (.mp4)", "Marks": 20, "Select": "Selected", "Description": "Video helping 1st Line Support identify OS performance logs in Event Viewer."},
    {"Task #": 12, "Section": "Section 3 (LO3)", "Deliverable": "Video Disk Check (.mp4)", "Marks": 20, "Select": "Not Selected", "Description": "Video showing disk space checks on Windows & Ubuntu with 4 sustainable habits."},
    {"Task #": 13, "Section": "Section 3 (LO3)", "Deliverable": "Video Bash Script (.mp4)", "Marks": 30, "Select": "Not Selected", "Description": "Video testing bash CPU/RAM monitoring script on Ubuntu with Student ID output."},
    {"Task #": 14, "Section": "Section 3 (LO3)", "Deliverable": "Video ResMon (.mp4)", "Marks": 30, "Select": "Selected", "Description": "Video investigating high disk usage/performance issues using Resource Monitor."},
    {"Task #": 15, "Section": "Section 3 (LO3)", "Deliverable": "Video Performance (.mp4)", "Marks": 40, "Select": "Not Selected", "Description": "Comprehensive video on proactive OS performance management & baselines."}
]

df_init = pd.DataFrame(tasks_data)

# 2. Initialize Dash App
app = dash.Dash(__name__)
app.title = "COM4025 - Portfolio Planner"
server = app.server

# 3. Layout Design
app.layout = html.Div(style={
    'backgroundColor': '#f4f6f9',
    'padding': '30px',
    'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    'minHeight': '100vh'
}, children=[
    
    # Header Banner
    html.Div(style={
        'backgroundColor': '#1f497d',
        'padding': '25px',
        'borderRadius': '12px',
        'color': 'white',
        'textAlign': 'center',
        'marginBottom': '25px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
    }, children=[
        html.H1("🎓 COM4025 Assessment Selection Dashboard", style={'margin': '0', 'fontWeight': '700', 'fontSize': '28px'}),
        html.P("Lumina Creative IT Support Portfolio Planner | Arden University Assessment Brief", style={'fontSize': '15px', 'marginTop': '8px', 'color': '#d9e2ec'})
    ]),

    # KPI Scorecards Row
    html.Div(style={
        'display': 'flex',
        'gap': '20px',
        'flexWrap': 'wrap',
        'marginBottom': '25px'
    }, children=[
        # Marks KPI Card
        html.Div(style={
            'flex': '1',
            'minWidth': '220px',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
            'textAlign': 'center'
        }, children=[
            html.H5("Total Marks Selected", style={'color': '#6c757d', 'margin': '0', 'fontSize': '14px', 'fontWeight': '600'}),
            html.H2(id='kpi-marks', style={'color': '#1f497d', 'margin': '10px 0 5px 0', 'fontWeight': 'bold', 'fontSize': '32px'}),
            html.P("Target: Exactly 100 Marks", style={'fontSize': '12px', 'color': '#888', 'margin': '0'})
        ]),
        
        # Tasks Count KPI Card
        html.Div(style={
            'flex': '1',
            'minWidth': '220px',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
            'textAlign': 'center'
        }, children=[
            html.H5("Selected Tasks Count", style={'color': '#6c757d', 'margin': '0', 'fontSize': '14px', 'fontWeight': '600'}),
            html.H2(id='kpi-count', style={'color': '#1f497d', 'margin': '10px 0 5px 0', 'fontWeight': 'bold', 'fontSize': '32px'}),
            html.P("Allowed: 3 to 5 Tasks", style={'fontSize': '12px', 'color': '#888', 'margin': '0'})
        ]),

        # Rule Validation Status Banner
        html.Div(style={
            'flex': '1.5',
            'minWidth': '300px',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.06)',
            'textAlign': 'center',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center'
        }, children=[
            html.H5("Portfolio Validation Status", style={'color': '#6c757d', 'margin': '0 0 10px 0', 'fontSize': '14px', 'fontWeight': '600'}),
            html.Div(id='kpi-status', style={'fontSize': '15px', 'fontWeight': 'bold', 'borderRadius': '8px'})
        ])
    ]),

    # Main Interactive Row
    html.Div(style={
        'display': 'flex',
        'gap': '25px',
        'flexWrap': 'wrap'
    }, children=[
        
        # Left Panel: Data Table
        html.Div(style={
            'flex': '1.4',
            'minWidth': '450px',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.06)'
        }, children=[
            html.H4("📋 Task Selection Table (Choose 'Selected' or 'Not Selected')", style={'color': '#1f497d', 'marginBottom': '15px', 'fontSize': '18px', 'fontWeight': '600'}),
            dash_table.DataTable(
                id='task-table',
                columns=[
                    {'name': 'Task #', 'id': 'Task #', 'editable': False},
                    {'name': 'Section', 'id': 'Section', 'editable': False},
                    {'name': 'Marks', 'id': 'Marks', 'editable': False},
                    {'name': 'Selection', 'id': 'Select', 'editable': True, 'presentation': 'dropdown'},
                    {'name': 'Deliverable Format', 'id': 'Deliverable', 'editable': False},
                    {'name': 'Description', 'id': 'Description', 'editable': False}
                ],
                dropdown={
                    'Select': {
                        'options': [
                            {'label': 'Selected', 'value': 'Selected'},
                            {'label': 'Not Selected', 'value': 'Not Selected'}
                        ]
                    }
                },
                data=df_init.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': '#1f497d',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'fontSize': '13px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontSize': '12px',
                    'fontFamily': 'Segoe UI, sans-serif'
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'Select'},
                        'backgroundColor': '#e8f0fe',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    {
                        'if': {'filter_query': '{Select} = "Selected"'},
                        'backgroundColor': '#e2f0d9',
                        'color': '#006100'
                    }
                ]
            )
        ]),

        # Right Panel: Visual Chart
        html.Div(style={
            'flex': '1',
            'minWidth': '400px',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.06)'
        }, children=[
            html.H4("📊 Portfolio Learning Outcome Distribution", style={'color': '#1f497d', 'marginBottom': '15px', 'fontSize': '18px', 'fontWeight': '600'}),
            dcc.Graph(id='marks-pie-chart', config={'displayModeBar': False})
        ])
    ])
])

# 4. Reactive Callbacks Engine
@app.callback(
    [Output('kpi-marks', 'children'),
     Output('kpi-count', 'children'),
     Output('kpi-status', 'children'),
     Output('kpi-status', 'style'),
     Output('marks-pie-chart', 'figure')],
    [Input('task-table', 'data')]
)
def update_dashboard(rows):
    df = pd.DataFrame(rows)
    
    selected_df = df[df['Select'] == 'Selected'].copy()
    
    total_marks = int(selected_df['Marks'].sum()) if not selected_df.empty else 0
    total_count = int(len(selected_df))
    sections_count = selected_df['Section'].nunique() if not selected_df.empty else 0
    
    # Enforce Assessment Brief Rules
    is_marks_valid = (total_marks == 100)
    is_count_valid = (3 <= total_count <= 5)
    is_sections_valid = (sections_count == 3)
    
    if is_marks_valid and is_count_valid and is_sections_valid:
        status_text = "✅ VALID SELECTION! (100 Marks & All LOs Covered)"
        status_style = {'color': '#155724', 'backgroundColor': '#d4edda', 'padding': '12px', 'borderRadius': '8px', 'border': '1px solid #c3e6cb'}
    else:
        reasons = []
        if not is_marks_valid:
            reasons.append(f"Marks: {total_marks}/100")
        if not is_count_valid:
            reasons.append(f"Tasks: {total_count} (Need 3-5)")
        if not is_sections_valid:
            reasons.append(f"LO Sections: {sections_count}/3 covered")
        
        status_text = "❌ INVALID: " + " | ".join(reasons)
        status_style = {'color': '#721c24', 'backgroundColor': '#f8d7da', 'padding': '12px', 'borderRadius': '8px', 'border': '1px solid #f5c6cb'}
        
    # Build Horizontal Bar Chart
    if len(selected_df) > 0:
        fig = px.bar(
            selected_df, 
            y='Section', 
            x='Marks', 
            color='Deliverable',
            orientation='h',
            hover_data=['Task #', 'Description'],
            text='Marks',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=13, family='Arial')
        )
        
        fig.update_layout(
            template="plotly_white",
            barmode='stack',
            height=380,
            margin=dict(l=20, r=20, t=30, b=30),
            xaxis=dict(title="Marks", range=[0, 110], showgrid=True, gridcolor='#e9ecef'),
            yaxis=dict(title="", autorange="reversed"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title=dict(text="")
            )
        )
    else:
        fig = px.bar(title="No tasks selected. Select 'Selected' in the table.")
        fig.update_layout(template="plotly_white", height=380)

    return f"{total_marks} / 100", f"{total_count} Tasks", status_text, status_style, fig

# 5. Run Server
# 5. Run Server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port)
