# FLASK THINGS
from flask import Flask, render_template, session, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# AI THINGS
import sys
sys.path.append(r'D:\agqxyz\Documents\School\ITEP203-1 AnalysisAndDesignOfAlgo\Python\financial-adviser\ai')
from chat import *

# STRING FORMATTING THINGS
import re

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversation.db'
db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    response = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Conversation %r>' % self.id
    
with app.app_context():
    db.create_all()


# PORTFOLIO METHODS/FUNCTIONS
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import yfinance as yf
import mplfinance as mpf

import pickle
import sys
import datetime as dt

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

def savePortfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

@app.route("/chat/addPortfolio")
def addPortfolio(id, sentence, intent):
    session['id'] = id
    session['sentence'] = sentence
    session['intent'] = intent

    conversations = Conversation.query.order_by(Conversation.date_created).all()

    if id < 0:
        return render_template(
            'addPortfolio.html', 
            conversations=conversations
        )
    else:
        addPortfolioFunc()

@app.route("/chat/addPortfolioFunc", methods=['POST', 'GET'])
def addPortfolioFunc():
    id = session.get('id', None)
    sentence = session.get('sentence', None)
    intent = session.get('intent', None)

    if request.method == 'POST':
        if id < 0:
            sentence = "You: " + sentence
            tick = request.form['ticker']
            amount = request.form['amount']
            amount = int(amount)

            if tick in portfolio.keys():
                oldStock = portfolio[tick]
                stock = int(portfolio[tick])
                stock += amount

                portfolio[tick] = stock

                answer = (f"{bot_name}: Adding again to => " + 
                          tick + " with amount of " + str(amount) + " shares. Value then is " + str(oldStock) + " now " + 
                          str(stock))
                
                savePortfolio()
            else:
                portfolio[tick] = amount
        
                ## Calling the AI
                answer = (f"{bot_name}: {random.choice(intent['responses'])}")
                answer = answer + " " + tick + " with amount of " + str(amount) + " shares"

                savePortfolio()

            new_conversation = Conversation(question=sentence, response=answer)

            db.session.add(new_conversation)
            db.session.commit()

            conversations = Conversation.query.order_by(Conversation.date_created).all()

            return render_template('chat.html', conversations=conversations)
    else:
        if id > 0:
            conversation = Conversation.query.get_or_404(id)
            response = conversation.response

            try:
                tickRegex = re.split(r'\s+', re.search(r'=>.*with', response).group())
                tick = tickRegex[1]
                amountRegex = re.split(r'\s+', re.search(r'of.*shares', response).group())
                amount = amountRegex[1]
                amount = int(amount)
            except:
                tick = None
                amount = None

            if not tick is None and not amount is None:
                if tick in portfolio.keys():
                    oldStock = portfolio[tick]
                    stock = int(portfolio[tick])
                    stock += amount
                    stock = str(stock)
                    amount = str(amount)
                    oldStock = str(oldStock)

                    portfolio[tick] = stock

                    answer = (f"{bot_name}: Adding again to => " + 
                            tick + " with amount of " + amount + " shares. Value then is " + oldStock + " now " + 
                            stock)
                    
                    savePortfolio()

                    try:
                        conversation.response = answer
                        db.session.commit()
                    except:
                        return 'Something went wrong'
                else:
                    # lastID = Conversation.query.order_by(Conversation.id.desc().first())
                    # print(lastID)
                    portfolio[tick] = amount

                    answer = (f"{bot_name}: Readding " + tick + 
                            " to stocks list with amount of " + str(amount))
                    
                    savePortfolio()

                    try:
                        conversation.response = answer
                        db.session.commit()
                    except:
                        return 'Something went wrong'
            else:
                tickRegex = re.split(r'\s+', re.search(r'Readding.*to', response).group())
                tick = tickRegex[1]
                amountRegex = re.split(r'\s+', re.search(r'of.*', response).group())
                amount = amountRegex[1]
                amount = int(amount)

                if tick in portfolio.keys():
                    oldStock = portfolio[tick]
                    stock = int(portfolio[tick])
                    stock += amount
                    stock = str(stock)
                    amount = str(amount)
                    oldStock = str(oldStock)

                    portfolio[tick] = stock

                    answer = (f"{bot_name}: Adding again to => " + 
                            tick + " with amount of " + amount + " shares. Value then is " + oldStock + " now " + 
                            stock)
                    
                    savePortfolio()

                    try:
                        conversation.response = answer
                        db.session.commit()
                    except:
                        return 'Something went wrong'
                
    return redirect('/chat')


@app.route("/chat/removePortfolio")
def removePortfolio(id, sentence, intent):
    session['id'] = id
    session['sentence'] = sentence
    session['intent'] = intent

    conversations = Conversation.query.order_by(Conversation.date_created).all()

    if id < 0:
        return render_template(
            'removePortfolio.html', 
            conversations=conversations
        )
    else:
        removePortfolioFunc()

@app.route("/chat/removePortfolioFunc", methods=['POST', 'GET'])
def removePortfolioFunc():
    id = session.get('id', None)
    sentence = session.get('sentence', None)
    intent = session.get('intent', None)

    if request.method == 'POST':
        if id < 0:
            tick = request.form['ticker']
            amount = request.form['amount']
            amount = int(amount)

            if tick in portfolio.keys():
                tickCount = int(portfolio[tick])
                sentence = "You: " + sentence

                if amount <= tickCount:
                    stock = int(portfolio[tick])
                    stock -= amount
                    stock = str(stock)

                    portfolio[tick] = stock
                    savePortfolio()

                    if stock == '0':
                        with open('portfolio.pkl', 'rb') as f:
                            tempFile = pickle.load(f)
                        
                        tempDict = {}

                        for key in tempFile.keys():
                            value = tempFile[key]

                            if key == tick:
                                pass
                            elif (value == tempFile[key]):
                                tempDict[key] = value

                        with open('newfile.pkl', 'wb') as f:
                            pickle.dump(tempDict, f)

                        answer = (f"{bot_name}: " + tick + 
                                " now has amount of 0 deleting from portfolio."
                                )
                        
                        with open('newfile.pkl', 'rb') as f:
                            newFile = pickle.load(f)

                        with open('portfolio.pkl', 'wb') as f:
                            pickle.dump(newFile, f)
                    else:
                        ## Calling the AI
                        answer = (f"{bot_name}: {random.choice(intent['responses'])}")
                        
                        answer = (answer + " " + tick + " with amount of " + 
                                str(amount) + " shares. Value then is " + str(tickCount) + " now " + stock)
                        
                        savePortfolio()


                    new_conversation = Conversation(question=sentence, response=answer)

                    db.session.add(new_conversation)
                    db.session.commit()
                else:
                    flash("remove-warning", "info")
            else:
                flash("do-not-own")
    else:
        if id > 0:
            conversation = Conversation.query.get_or_404(id)
            response = conversation.response

            try:
                tickRegex = re.split(r'\s+', re.search(r'=>.*with', response).group())
                tick = tickRegex[1]
                tickCount = int(portfolio[tick])

                amountRegex = re.split(r'\s+', re.search(r'of.*shares', response).group())
                amount = amountRegex[1]
                amount = int(amount)
            except:
                tick = None
                tickCount = None
                amount = None

            if not tick is None and not tickCount is None and not amount is None:
                if tick in portfolio.keys():
                    if amount <= tickCount:
                        stock = int(portfolio[tick])
                        stock -= amount
                        stock = str(stock)

                        portfolio[tick] = stock
                        savePortfolio()

                        if int(stock) == 0:
                            with open('portfolio.pkl', 'rb') as f:
                                tempFile = pickle.load(f)
                            
                            tempDict = {}

                            for key in tempFile.keys():
                                value = tempFile[key]

                                if key == tick:
                                    pass
                                elif (value == tempFile[key]):
                                    tempDict[key] = value

                            with open('portfolio.pkl', 'wb') as f:
                                pickle.dump(tempDict, f)

                            answer = (f"{bot_name}: " + tick + 
                                    " now has amount of 0 deleting from portfolio."
                                    )
                        else:
                            answer = (f"{bot_name}: Removing again from => " + 
                                    tick + " with amount of " + str(amount) + " shares. Value then is " + str(tickCount) + " now " + stock)
                            
                        savePortfolio()

                        try:
                            conversation.response = answer
                            db.session.commit()
                        except:
                            return 'Something went wrong'
                    else:
                        flash("remove-warning", "info")
                else:
                    flash("do-not-own")  
            else:
                try:
                    tickRegex = re.split(r'\s+', re.search(r':.*now', response).group())
                    tick = tickRegex[1]
                except:
                    pass

                if tick in portfolio.keys():
                    answer = (f"{bot_name}: It appears that => " + tick +
                              " has been readded to the portfolio")
                    
                else:
                    answer = (f"{bot_name}: Stock => " + tick +
                              " has already been removed")
                
                try:
                    conversation.response = answer
                    db.session.commit()
                except:
                    return 'Something went wrong'

    return redirect('/chat')

@app.route("/chat/showPortfolio")
def showPortfolio(id, sentence, intent):
    ## Getting our list of stocks
    ownedStocks = []
    stockItem = ""
    listOfStocks = ""

    for tick, amount in portfolio.items():
        stock = f"{tick}: {amount} shares"
        ownedStocks.append(stock)

    for i in range(len(ownedStocks)):
        stockItem += "\n" + ownedStocks[i] # Concatenate items with each other
        stockItem = stockItem.split("\n", 1)[1] # Remove previous 
                                                      # concatenations
                                                      # to clean paragraph
        listOfStocks = (listOfStocks + 
                        "<br>" +
                        stockItem)                            

    ## Calling the AI 
    if id < 0:
        # Adding to our database and displaying
        sentence = "You: " + sentence

        answer = (f"{bot_name}: {random.choice(intent['responses'])}")
        answer = answer + listOfStocks
        new_conversation = Conversation(question=sentence, response=answer)

        db.session.add(new_conversation)
        db.session.commit()

        return redirect('/chat')
    elif id > 0:
        conversation = Conversation.query.get_or_404(id)

        answer = (f"{bot_name}: {random.choice(intent['responses'])}")
        answer = answer + listOfStocks

        try:
            conversation.response = answer
            db.session.commit()

            return redirect('/chat')
        except:
            return 'Something went wrong'
    else:
        return 'Something went wrong'

@app.route("/chat/worthPortfolio")
def worthPortfolio(id, sentence, intent):
    flash("worth-portfolio", "info")

    ## Getting the total price of our portfolio
    for tick in portfolio.keys():
        data = yf.download(tick)

        try:
            price = data.iat[-1, data.columns.get_loc('Close')]
            price += price
            price = str(price)
        except:
            print("Stock does not exist")

    ## Calling the AI
    if id < 0:
        # Adding to our database and displaying
        sentence = "You: " + sentence

        answer = (f"{bot_name}: {random.choice(intent['responses'])}")
        answer = answer + price + " USD"
        new_conversation = Conversation(question=sentence, response=answer)

        db.session.add(new_conversation)
        db.session.commit()

        conversations = Conversation.query.order_by(Conversation.date_created).all()

        return render_template('/chat.html', conversations=conversations)
    elif id > 0:
        conversation = Conversation.query.get_or_404(id)

        answer = (f"{bot_name}: {random.choice(intent['responses'])}")
        answer = answer + price + " USD"

        try:
            conversation.response = answer
            db.session.commit()

            return redirect('/chat')
        except:
            return 'Something went wrong'
    else:
        return 'Something went wrong'
    
@app.route("/chat/gainsPortfolio")
def gainsPortfolio(id, sentence, intent):
    session['id'] = id
    session['sentence'] = sentence
    session['intent'] = intent
    
    conversations = Conversation.query.order_by(Conversation.date_created).all()

    if id < 0:
        return render_template(
            'gainsPortfolio.html', 
            conversations=conversations
        )
    else:
        gainsPortfolioFunc()

@app.route("/chat/gainsPortfolioFunc/", methods=['POST', 'GET'])
def gainsPortfolioFunc():
    flash("gains-portfolio")
    id = session.get('id', None)
    sentence = session.get('sentence', None)
    intent = session.get('intent', None)

    sumNow = 0
    sumThen = 0
    relativeGains = 0
    gainsAbsolute = 0

    if request.method == 'POST':        
        for tick in portfolio.keys():
            data = yf.download(tick)

            try:
                priceNow = data.iat[-1, data.columns.get_loc('Close')]

                startingDate = request.form['start-date']

                priceThen = data.loc[data.index == startingDate]['Close'].values[0]

                sumNow += priceNow
                sumThen += priceThen
            except:
                pass

        relativeGains = str(((sumNow - sumThen)/sumThen) * 100)
        gainsAbsolute = str((sumNow - sumThen)/sumThen)

        endDate = dt.datetime.now().strftime("%Y-%m-%d")

        if id < 0:
            # Adding to our database and displaying
            sentence = "You: " + sentence

            answer = (f"{bot_name}: {random.choice(intent['responses'])}")
            answer = (
                answer +
                "<br>" + 
                "Relative Gains: " + 
                relativeGains + 
                " USD" +
                "<br>" +
                "Absolute Gains: " +
                gainsAbsolute +
                " USD" +
                "<br>" +
                "Starting from " +
                startingDate +
                " to " +
                endDate
            )
            
            new_conversation = Conversation(question=sentence, response=answer)

            db.session.add(new_conversation)
            db.session.commit()

            conversations = Conversation.query.order_by(Conversation.date_created).all()

            return redirect('/chat')
    else:
        conversation = Conversation.query.get_or_404(id)
        response = conversation.response

        for tick in portfolio.keys():
            data = yf.download(tick)

            try:
                priceNow = data.iat[-1, data.columns.get_loc('Close')]

                startingDateRegex = re.split(r'\s+', re.search(r'from.*to', response).group())
                startingDate = startingDateRegex[1]

                priceThen = data.loc[data.index == startingDate]['Close'].values[0]

                sumNow += priceNow
                sumThen += priceThen
            except:
                pass     

        relativeGains = str(((sumNow - sumThen)/sumThen) * 100)
        gainsAbsolute = str((sumNow - sumThen)/sumThen)

        endDate = dt.datetime.now().strftime("%Y-%m-%d")

        if id > 0:
            answer = (f"{bot_name}: {random.choice(intent['responses'])}")
            answer = (
                answer +
                "<br>" + 
                "Relative Gains: " + 
                relativeGains + 
                " USD" +
                "<br>" +
                "Absolute Gains: " +
                gainsAbsolute +
                " USD" +
                "<br>" +
                "Starting from " +
                startingDate +
                " to " +
                endDate
            )

        try:
            conversation.response = answer
            db.session.commit()

            return redirect('/chat')
        except:
            return 'Something went wrong'
        
@app.route("/chat/plotChart")
def plotChart(id, sentence, intent):
    session['id'] = id
    session['sentence'] = sentence
    session['intent'] = intent
    
    conversations = Conversation.query.order_by(Conversation.date_created).all()

    if id < 0:
        return render_template(
            'plotChart.html', 
            conversations=conversations
        )
    else:
        plotChartFunc()

@app.route("/chat/plotChartFunc", methods=['POST', 'GET'])
def plotChartFunc():
    id = session.get('id', None)
    sentence = session.get('sentence', None)
    intent = session.get('intent', None)

    if request.method == 'POST':
        if id < 0:
            ## Creating the image
            tick = request.form['ticker']

            imgName = './static/imgs/' + tick.lower() + '.png'

            startingDate = request.form['start-date']
            endDate = dt.datetime.now().strftime("%Y-%m-%d")
            dateRow = re.split('-', startingDate)

            year, month, day = dateRow[0], dateRow[1], dateRow[2]
            startFormat = dateRow[2] + "/" + dateRow[1] + "/" + dateRow[0]
            # print(startFormat)

            plt.style.use('dark_background')
            start = dt.datetime.strptime(startFormat, "%d/%m/%Y")
            end = dt.datetime.now()
            # print(start)
            # print(end)

            data = yf.download(tick, start, end)
            # print(data)

            colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
            mpfStyle = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

            mpf.plot(data, type='candle', style=mpfStyle, volume=True, savefig=imgName)

            ## Calling the AI
            sentence = "You: " + sentence

            answer = (f"{bot_name}: {random.choice(intent['responses'])}")
            answer = (
                answer +
                "<br>" +
                "<img src='" + imgName + "' alt='Stock plot'>" +
                "<br>" +
                "This is for " + tick +
                " with date " +
                startingDate + " to " +
                endDate
            )

            new_conversation = Conversation(question=sentence, response=answer)

            db.session.add(new_conversation)
            db.session.commit()

            conversations = Conversation.query.order_by(Conversation.date_created).all()

            return redirect('/chat')
    else:
        if id > 0:
            conversation = Conversation.query.get_or_404(id)
            response = conversation.response

            tickRegex = re.split(r'\s+', re.search(r'for.*with', response).group())
            tick = tickRegex[1]
            print(tickRegex)

            imgName = './static/imgs/' + tick.lower() + '.png'

            startingDateRegex = re.split(r'\s+', re.search(r'date.*to', response).group())
            startingDate = startingDateRegex[1]
            print(startingDate)
            endDate = dt.datetime.now().strftime("%Y-%m-%d")
            dateRow = re.split('-', startingDate)
            print(endDate)

            startFormat = dateRow[2] + "/" + dateRow[1] + "/" + dateRow[0]
            print(startFormat)


            plt.style.use('dark_background')
            start = dt.datetime.strptime(startFormat, "%d/%m/%Y")
            end = dt.datetime.now()

            data = yf.download(tick, start, end)

            colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume='in')
            mpfStyle = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

            mpf.plot(data, type='candle', style=mpfStyle, volume=True, savefig=imgName)
            
            answer = (f"{bot_name}: {random.choice(intent['responses'])}")
            answer = (
                answer +
                "<br>" +
                "<img src='" + imgName + "' alt='Stock plot'>" +
                "<br>" +
                "This is for " + tick +
                " with date " +
                startingDate + " to " +
                endDate
            )

            try:
                conversation.response = answer
                db.session.commit()

                return redirect('/chat')
            except:
                return 'Something went wrong'
            
    return redirect('/chat')

def openResourceSite():
    webbrowser.open('https://www.occ.gov/topics/consumers-and-communities/community-affairs/resource-directories/financial-literacy/index-financial-literacy-resource-directory.html')

method_mappings = {
    "resource": openResourceSite,
    "show": showPortfolio,
    "worth": worthPortfolio,
    "gains": gainsPortfolio,
    "plot": plotChart,
    "add": addPortfolio,
    "remove": removePortfolio
}

keys = method_mappings.keys()

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == "POST":
        # Getting our question
        sentence = request.form['sentence']

        # Getting response from AI
        sentenceTokenized = tokenize(sentence)
        x = bag_of_words(sentenceTokenized, all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x).to(device)

        output = model(x)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    if tag == "greeting" or tag == "goodbye":
                        answer = (f"{bot_name}: {random.choice(intent['responses'])}")

                        # Adding to our database and displaying
                        sentence = "You: " + sentence
                        new_conversation = Conversation(question=sentence, response=answer)

                        try:
                            db.session.add(new_conversation)
                            db.session.commit()

                            conversations = Conversation.query.order_by(Conversation.date_created).all()
                            
                            return render_template('chat.html', conversations=conversations)
                        except:
                            return 'Something went wrong'    

                    else:
                        id = -1

                        for key in keys:
                            if tag == key:
                                return method_mappings[tag](id, sentence, intent)                   
        else:
            answer = (f"{bot_name}: I do not understand...")

            # Adding to our database and displaying
            sentence = "You: " + sentence
            new_conversation = Conversation(question=sentence, response=answer)

            try:
                db.session.add(new_conversation)
                db.session.commit()

                conversations = Conversation.query.order_by(Conversation.date_created).all()

                return render_template('chat.html', conversations=conversations)
            except:
                return 'Something went wrong'
    else:
        conversations = Conversation.query.order_by(Conversation.date_created).all()

        return render_template('chat.html', conversations=conversations)

    # return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/delete/<int:id>')
def delete(id):
    conversation_to_del = Conversation.query.get_or_404(id)

    try:
        db.session.delete(conversation_to_del)
        db.session.commit()
        
        return redirect('/chat')
    except:
        return 'Something went wrong'
    
@app.route('/regenerate/<int:id>')
def regenerate(id):
    conversation  = Conversation.query.get_or_404(id)
    question = conversation.question
    sentence = conversation.response

    # Getting response from AI
    sentenceTokenized = tokenize(question)
    x = bag_of_words(sentenceTokenized, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if tag == "greeting" or tag == "goodbye":
                    answer = (f"{bot_name}: \
                              {random.choice( \
                              intent['responses'] \
                              )}")
                    
                    try:
                        conversation.response = answer
                        db.session.commit()
                    except:
                        return redirect('/chat')
                else:
                    for key in keys:
                        if tag == key:
                            method_mappings[tag](id, sentence, intent)
    else:
        answer = (f"{bot_name}: I do not understand...")

        try:
            conversation.response = answer
            db.session.commit()

            return redirect('/chat')
        except:
            return 'Something went wrong'
    
    return redirect('/chat')
    
if __name__ == "__main__":
    app.run(debug=True)
