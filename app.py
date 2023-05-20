from flask import Flask, request, render_template, redirect, flash, session
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "Im-A-Baddy"

responses = []

@app.route('/')
def default():
    global satisfaction_survey
    return render_template('intro.html', surveyName = satisfaction_survey.title, surveyInstructions = satisfaction_survey.instructions)


@app.route('/questions/<questInt>')
def showQuestion(questInt):
    if int(questInt) != session['numOn']:
        flash("Trying to access Invalid Question!")
        return redirect(f'/questions/{session["numOn"]}')
    global satisfaction_survey
    if int(questInt) > len(satisfaction_survey.questions):
        return redirect('/finished')
    return render_template('question.html',num = int(questInt)+1, surveyQuestion = satisfaction_survey.questions[int(questInt)-1].question, surveyChoice1 = satisfaction_survey.questions[int(questInt)-1].choices[0], surveyChoice2 = satisfaction_survey.questions[int(questInt)-1].choices[1])

@app.route('/submitted/<questInt>', methods=["POST"])
def answer(questInt):
    global satisfaction_survey
    global numOn
    session['numOn'] = session['numOn']+1
    newR = session['responses']
    newR.append(request.form["answer"])
    session['responses'] = newR
    return redirect(f"/questions/{int(questInt)}")

@app.route('/finished')
def finish():
    global satisfaction_survey
    return render_template('Final.html', answers = session['responses'])

@app.route('/start')
def start():
    session['responses'] = []
    session['numOn'] = 1
    global satisfaction_survey
    return redirect(f'/questions/{session["numOn"]}')