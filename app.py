from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def show_home():

    return render_template('survey_start.html', survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/questions/<int:q>')
def display_question(q):
    responses = session.get(RESPONSES_KEY)

    if len(responses) == len(survey.questions):
        return redirect('/thanks')

    if len(responses) != q:
        flash(f"That was not the next question")
        return redirect(f"/questions/{len(responses)}")
    
    
    # add logic for decisplaying question based off q
    # add radio choice
    # add sumbit
    # add route
    question = survey.questions[q].question
    choices = survey.questions[q].choices
    length = len(survey.questions)

    return render_template('question.html', question_num=q, question=question, choices=choices, length=length)

@app.route('/answer', methods=['POST'])
def handle_answer():
    choice = request.form['answer']
    # explore this more, had to borrow from solution to work, but don't fully understand
    responses = session.get(RESPONSES_KEY)
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    

    return redirect(f"/questions/{len(responses)}")

@app.route('/thanks')
def show_thanks():
    return render_template('thanks.html')