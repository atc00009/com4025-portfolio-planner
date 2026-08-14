import os
from dash import Dash, dcc, html, Input, Output, State, dash_table
import pandas as pd
from google import genai

# Initialize Dash App
app = Dash(__name__)
server = app.server  # Required for Gunicorn / Render deployment

# Initialize Gemini Client (uses GEMINI_API_KEY from Render environment variables)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# -------------------------------------------------------------------
# Task Data Structure based on COM4025 Brief
# -------------------------------------------------------------------
tasks_data = [
    # Section 1
    {"Task": "Task 1", "Section": "Section 1 (LO1)", "Marks": 10, "Description": "1-page Self-Help Guide: Network Troubleshooting (IPConfig)"},
    {"Task": "Task 2", "Section": "Section 1 (LO1)", "Marks": 20, "Description": "2-3 min Video: Performance Analysis under Workloads (Task Manager)"},
    {"Task": "Task 3", "Section": "Section 1 (LO1)", "Marks": 20, "Description": "1-page Training Guide: 5 Core OS Design Principles"},
    {"Task": "Task 4", "Section": "Section 1 (LO1)", "Marks": 20, "Description": "Infographic: Memory Hierarchy (Cache, RAM, Virtual, Storage)"},
    {"Task": "Task 5", "Section": "Section 1 (LO1)", "Marks": 30, "Description": "Video Demo: VHD Initialization, GPT Partitioning, NTFS & Compression"},
    
    # Section 2
    {"Task": "Task 6", "Section": "Section 2 (LO2)", "Marks": 10, "Description": "Word Table Checklist: Local Admin Rights & DPA Compliance"},
    {"Task": "Task 7", "Section": "Section 2 (LO2)", "Marks": 20, "Description": "2-3 min Video: Windows Security Desktop Hardening"},
    {"Task": "Task 8", "Section": "Section 2 (LO2)", "Marks": 30, "Description": "Infographic: Role-Based Access Control (RBAC), NTFS & OneDrive"},
    {"Task": "Task 9", "Section": "Section 2 (LO2)", "Marks": 30, "Description": "Technical Guide: Adding New User & Administrator Rights"},
    {"Task": "Task 10", "Section": "Section 2 (LO2)", "Marks": 30, "Description": "2-3 min Video: Open Listening Port Security Risk Identification"},
    
    # Section 3
    {"Task": "Task 11", "Section": "Section 3 (LO3)", "Marks": 20, "Description": "2-3 min Video: Identifying Performance Logs (Event Viewer)"},
    {"Task": "Task 12", "Section": "Section 3 (LO3)", "Marks": 20, "Description": "Video Guide: Disk Space Cleanup (Windows & Ubuntu Baobab)"},
    {"Task": "Task 13", "Section": "Section 3 (LO3)", "Marks": 30, "Description": "3-4 min Video: Ubuntu Bash Script for CPU/RAM Monitoring"},
    {"Task": "Task 14", "Section": "Section 3 (LO3)", "Marks": 30, "Description": "3-4 min Video: Disk Usage Investigation using Resource Monitor"},
    {"Task": "Task 15", "Section": "Section 3 (LO3)", "Marks": 40, "Description": "6-8 min Video: Proactive OS Performance Management & Health Checks"},
]

df = pd.DataFrame(tasks_data)

# -------------------------------------------------------------------
# APP LAYOUT
# -------------------------------------------------------------------
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "maxWidth": "1200px",
        "margin": "0 auto",
        "backgroundColor": "#f4f6f9"
    },
    children=[
        # Title Header
        html.Div(
            style={
                "textAlign": "center",
                "backgroundColor": "#003366",
                "color": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "marginBottom": "20px"
            },
            children=[
                html.H1("COM4025 Assessment Portfolio Planner", style={"margin": "0"}),
                html.P("Select 3 to 5 tasks across all 3 sections totaling exactly 100 marks.", style={"marginTop": "5px"})
            ]
        ),
        
        # --- PORTFOLIO PLANNER SECTION ---
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "marginBottom": "25px"
            },
            children=[
                html.H2("1. Task Selection Table"),
                dash_table.DataTable(
                    id="task-table",
                    columns=[
                        {"name": "Select", "id": "Select", "presentation": "dropdown"},
                        {"name": "Task", "id": "Task"},
                        {"name": "Section", "id": "Section"},
                        {"name": "Marks", "id": "Marks"},
                        {"name": "Description", "id": "Description"}
                    ],
                    data=[{**row, "Select": "No"} for row in df.to_dict("records")],
                    editable=True,
                    dropdown={
                        "Select": {
                            "options": [
                                {"label": "Yes", "value": "Yes"},
                                {"label": "No", "value": "No"}
                            ]
                        }
                    },
                    style_cell={"textAlign": "left", "padding": "10px", "fontSize": "14px"},
                    style_header={"backgroundColor": "#003366", "color": "white", "fontWeight": "bold"},
                    style_data_conditional=[
                        {
                            "if": {"column_id": "Select", "value": "Yes"},
                            "backgroundColor": "#e6f3ff",
                            "fontWeight": "bold"
                        }
                    ]
                ),
                
                # Validation Feedback Box
                html.Div(
                    id="validation-summary",
                    style={"marginTop": "20px", "padding": "15px", "borderRadius": "5px"}
                )
            ]
        ),
        
        # --- AI TUTOR SECTION ---
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
            },
            children=[
                html.H2("2. 💬 COM4025 Assessment AI Tutor"),
                html.P("Have questions on how to complete Tasks 1 to 15? Ask the AI Tutor below:"),
                
                html.Div(
                    style={"display": "flex", "gap": "10px", "marginBottom": "15px"},
                    children=[
                        dcc.Input(
                            id="user-question",
                            type="text",
                            placeholder="e.g., How do I format the VHD in Task 5?",
                            style={
                                "flex": "1",
                                "padding": "12px",
                                "borderRadius": "5px",
                                "border": "1px solid #ccc",
                                "fontSize": "15px"
                            }
                        ),
                        html.Button(
                            "Ask Tutor",
                            id="ask-btn",
                            n_clicks=0,
                            style={
                                "padding": "12px 25px",
                                "backgroundColor": "#003366",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "5px",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "fontSize": "15px"
                            }
                        )
                    ]
                ),
                
                dcc.Loading(
                    id="loading-tutor",
                    type="default",
                    children=html.Div(
                        id="tutor-output",
                        style={
                            "padding": "15px",
                            "backgroundColor": "#f9f9f9",
                            "borderLeft": "5px solid #003366",
                            "borderRadius": "4px",
                            "minHeight": "50px"
                        }
                    )
                )
            ]
        )
    ]
)

# -------------------------------------------------------------------
# CALLBACK 1: PORTFOLIO PLANNER VALIDATION
# -------------------------------------------------------------------
@app.callback(
    Output("validation-summary", "children"),
    Output("validation-summary", "style"),
    Input("task-table", "data")
)
def validate_portfolio(rows):
    selected_tasks = [row for row in rows if row.get("Select") == "Yes"]
    
    total_tasks = len(selected_tasks)
    total_marks = sum(int(row["Marks"]) for row in selected_tasks)
    sections_covered = set(row["Section"] for row in selected_tasks)
    
    # Check compliance rules
    valid_count = 3 <= total_tasks <= 5
    valid_marks = total_marks == 100
    valid_sections = len(sections_covered) == 3
    
    is_valid = valid_count and valid_marks and valid_sections
    
    bg_color = "#d4edda" if is_valid else "#f8d7da"
    text_color = "#155724" if is_valid else "#721c24"
    border_color = "#c3e6cb" if is_valid else "#f5c6cb"
    
    style = {
        "backgroundColor": bg_color,
        "color": text_color,
        "border": f"1px solid {border_color}",
        "borderRadius": "5px",
        "padding": "15px",
        "marginTop": "20px"
    }
    
    summary = html.Div([
        html.H3("Allocation Status Summary:", style={"marginTop": "0"}),
        html.Ul([
            html.Li(f"Total Selected Tasks: {total_tasks} / (Required: 3 to 5) {'✅' if valid_count else '❌'}"),
            html.Li(f"Total Marks: {total_marks} / 100 {'✅' if valid_marks else '❌'}"),
            html.Li(f"Sections Covered: {len(sections_covered)} / 3 {'✅' if valid_sections else '❌'}"),
        ]),
        html.P(
            "🎉 Perfect! Your selected portfolio combination meets all assessment rules!" 
            if is_valid else 
            "⚠️ Please adjust your selections to ensure you have 3–5 tasks, covering all 3 sections, totaling 100 marks."
        )
    ])
    
    return summary, style

# -------------------------------------------------------------------
# CALLBACK 2: FULL DYNAMIC RUNTIME MODEL DISCOVERY
# -------------------------------------------------------------------
@app.callback(
    Output("tutor-output", "children"),
    Input("ask-btn", "n_clicks"),
    State("user-question", "value"),
    prevent_initial_call=True
)
def answer_student_question(n_clicks, question):
    if not question or question.strip() == "":
        return "Please enter a question about your COM4025 task!"
    
    prompt = f"""
    You are an expert AI tutor for the COM4025 module (Introduction to Operating Systems and Security).
    Provide clear, step-by-step guidance for the student based on the official task brief rules:
    - Must choose 3-5 tasks totaling 100 marks.
    - Must select from all 3 sections (LO1: OS Design, LO2: OS Security, LO3: Performance Monitoring).
    
    Student Question: {question}
    """
    
    try:
        # Ask Google API directly what models this key has access to
        available = []
        for model in client.models.list():
            # Check if model supports text generation
            actions = getattr(model, "supported_actions", []) or getattr(model, "supported_generation_methods", [])
            if not actions or "generateContent" in actions:
                name = getattr(model, "name", str(model))
                clean_name = name.replace("models/", "")
                available.append(clean_name)
        
        if not available:
            return "Error: Your API key returned zero supported models. Please generate a key at aistudio.google.com."

        # Pick the first active available model from Google's runtime response
        chosen_model = available[0]
        
        # Prefer a flash model if present in the list
        for m in available:
            if "flash" in m.lower():
                chosen_model = m
                break

        response = client.models.generate_content(
            model=chosen_model,
            contents=prompt,
        )
        return dcc.Markdown(response.text)
        
    except Exception as e:
        return f"Error connecting to AI Tutor: {str(e)}"

# -------------------------------------------------------------------
# SERVER RUNNER
# -------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port)
