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
    
    if request.method == 'POST':
        user_answer = request.form.get('scenario')
        user_answer_number_of_commands = request.form.get('number_of_commands')
        user_answer_os_type = request.form.get('os_type')
        commands = generate_commands(user_answer, user_answer_os_type, user_answer_number_of_commands)
        
        user_approval = request.form.get('user_approval')
        analyze_approval = request.form.get('analyze_approval')
        
        if user_approval == "yes":
            commands_output = command_run(commands)
            
            if analyze_approval == "yes" and commands_output:
                analysis_output = generate_analyze(commands_output, user_answer)
        else:
            commands_output = "User did not approve the commands"

    return render_template(
        'index.html', 
        user_answer=user_answer,
        user_answer_number_of_commands=user_answer_number_of_commands,
        user_answer_os_type=user_answer_os_type,
        commands=commands,
        commands_output=commands_output,
        analysis_output=analysis_output,
            )
