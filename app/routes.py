from flask import Blueprint, render_template, request
from app.services.chatgpt import generate_commands
from app.utils import command_run
from app.services.chatgpt import generate_analyze

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def index():
    user_answer = None
    commands = None
    commands_output = None
    analysis_output = None
    user_answer_number_of_commands = None
    user_answer_os_type = None
    step = "initial"  # Track which step of the process we're in
    
    if request.method == 'POST':
        # Always get the scenario and settings when they're present
        if 'scenario' in request.form:
            user_answer = request.form.get('scenario')
            user_answer_number_of_commands = request.form.get('number_of_commands')
            user_answer_os_type = request.form.get('os_type')
        else:
            # Retrieve these from hidden fields if we're in a later step
            user_answer = request.form.get('hidden_scenario')
            user_answer_number_of_commands = request.form.get('hidden_number_of_commands')
            user_answer_os_type = request.form.get('hidden_os_type')
            
        # Determine which step we're in
        if 'generate_commands' in request.form or 'scenario' in request.form:
            # First step - generate commands
            commands = generate_commands(user_answer, user_answer_os_type, user_answer_number_of_commands)
            step = "commands_generated"
            
        elif 'run_commands' in request.form:
            # Second step - run the commands
            commands = request.form.get('hidden_commands')
            commands_output = command_run(commands)
            step = "commands_executed"
            
        elif 'analyze_output' in request.form:
            # Third step - analyze the output
            commands = request.form.get('hidden_commands')
            commands_output = request.form.get('hidden_output')
            analysis_output = generate_analyze(commands_output, user_answer)
            step = "analysis_complete"
    
    return render_template(
        'index.html', 
        user_answer=user_answer,
        user_answer_number_of_commands=user_answer_number_of_commands,
        user_answer_os_type=user_answer_os_type,
        commands=commands,
        commands_output=commands_output,
        analysis_output=analysis_output,
        step=step
    )