from flask import Blueprint, render_template, request
from app.services.chatgpt import generate_commands
import subprocess

main = Blueprint('main', __name__)

def command_run(commands):
    result = subprocess.run(
        commands,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    return result.stdout + result.stderr

@main.route("/", methods=['GET', 'POST'])
def index():
    user_answer = None
    commands = None
    commands_output = None
    commands_output_without_exec = None
    user_answer_number_of_commands = None
    user_answer_os_type = None
    if request.method == 'POST':
        user_answer = request.form.get('scenario')
        user_answer_number_of_commands = request.form.get('number_of_commands')
        user_answer_os_type = request.form.get('os_type')
        commands = generate_commands(user_answer, user_answer_os_type, user_answer_number_of_commands)
        user_approval = request.form.get('user_approval')
        if user_approval == "yes":
            commands_output = command_run(commands)
        else :
            commands_output = "User did not approve the commands"
            commands_output_without_exec = commands
    return render_template('index.html', user_answer=user_answer,user_answer_number_of_commands=user_answer_number_of_commands ,user_answer_os_type=user_answer_os_type ,commands=commands ,commands_output=commands_output)


