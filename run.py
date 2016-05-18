from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])

def response():
    """Respond to incoming calls with a simple text message."""

    print("***TEXT RECEIVED!!!***")
    resp = twilio.twiml.Response()
    resp.message("Hello, Linda! Test Test Test.")
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)