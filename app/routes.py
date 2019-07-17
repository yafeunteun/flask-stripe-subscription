import os
import stripe

from app import app
from flask import render_template

stripe_public_key = os.environ.get("STRIPE_PUBLIC_KEY")
stripe.api_key =  os.environ.get("STRIPE_SECRET_KEY")

@app.route('/')
@app.route('/index')
def index():
    return render_template('order.html')

@app.route('/success')
def success():
        return "Success!"


@app.route('/cancel')
def cancel():
        return "CANCELED!"


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        subscription_data={
            'items': [{
                'plan': os.environ.get("STRIPE_PLAN_ID"), 
            }],
        },
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )
    
    print(session)
    print("+" * 42)
    _id = session.get("id")
    print(_id)
    
    return render_template('checkout.html', _id=_id, stripe_public_key=stripe_public_key)
