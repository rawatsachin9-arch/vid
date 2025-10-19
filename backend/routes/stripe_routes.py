from fastapi import APIRouter, HTTPException, Request
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Pricing configuration
PRICING_PLANS = {
    'starter': {
        'monthly': {'price': 1900, 'price_id': os.getenv('STRIPE_STARTER_MONTHLY_PRICE_ID')},
        'annual': {'price': 15000, 'price_id': os.getenv('STRIPE_STARTER_ANNUAL_PRICE_ID')}
    },
    'professional': {
        'monthly': {'price': 4900, 'price_id': os.getenv('STRIPE_PROFESSIONAL_MONTHLY_PRICE_ID')},
        'annual': {'price': 39000, 'price_id': os.getenv('STRIPE_PROFESSIONAL_ANNUAL_PRICE_ID')}
    },
    'enterprise': {
        'monthly': {'price': 9900, 'price_id': os.getenv('STRIPE_ENTERPRISE_MONTHLY_PRICE_ID')},
        'annual': {'price': 79000, 'price_id': os.getenv('STRIPE_ENTERPRISE_ANNUAL_PRICE_ID')}
    }
}

@router.get('/config')
async def get_stripe_config():
    """Return Stripe publishable key"""
    return {
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
        'success': True
    }

@router.post('/create-checkout-session')
async def create_checkout_session(request: Request):
    """Create a Stripe Checkout session for subscription payments"""
    try:
        data = await request.json()
        plan_type = data.get('plan')  # starter, professional, enterprise
        billing_period = data.get('billing')  # monthly, annual
        
        if plan_type not in PRICING_PLANS:
            raise HTTPException(status_code=400, detail='Invalid plan type')
        
        if billing_period not in ['monthly', 'annual']:
            raise HTTPException(status_code=400, detail='Invalid billing period')
        
        plan_config = PRICING_PLANS[plan_type][billing_period]
        price_id = plan_config['price_id']
        
        # Get frontend URL from environment
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        
        # Create Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=data.get('success_url', f'{frontend_url}/success?session_id={{CHECKOUT_SESSION_ID}}'),
            cancel_url=data.get('cancel_url', f'{frontend_url}/'),
            customer_email=data.get('email'),
            metadata={
                'plan': plan_type,
                'billing': billing_period
            }
        )
        
        return {
            'sessionId': checkout_session.id,
            'url': checkout_session.url,
            'success': True
        }
    
    except Exception as e:
        print(f"Stripe Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/create-payment-intent')
async def create_payment_intent(request: Request):
    """Create a PaymentIntent for one-time payments"""
    try:
        data = await request.json()
        plan_type = data.get('plan')
        billing_period = data.get('billing', 'monthly')
        
        if plan_type not in PRICING_PLANS:
            raise HTTPException(status_code=400, detail='Invalid plan type')
        
        plan_config = PRICING_PLANS[plan_type][billing_period]
        amount = plan_config['price']
        
        # Create PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            metadata={
                'plan': plan_type,
                'billing': billing_period
            },
            automatic_payment_methods={
                'enabled': True,
            },
        )
        
        return {
            'clientSecret': intent.client_secret,
            'success': True
        }
    
    except Exception as e:
        print(f"Stripe Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/webhook')
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail='Invalid payload')
    except Exception as e:
        raise HTTPException(status_code=400, detail='Invalid signature')
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle successful subscription
        print(f"Subscription successful for session: {session['id']}")
        # TODO: Update user subscription status in database
        
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(f"PaymentIntent successful: {payment_intent['id']}")
        # TODO: Handle one-time payment success
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        print(f"Subscription cancelled: {subscription['id']}")
        # TODO: Update user subscription status
    
    return {'success': True}

@router.get('/subscription/{subscription_id}')
async def get_subscription(subscription_id: str):
    """Get subscription details"""
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        return {
            'subscription': subscription,
            'success': True
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/cancel-subscription')
async def cancel_subscription(request: Request):
    """Cancel a subscription"""
    try:
        data = await request.json()
        subscription_id = data.get('subscription_id')
        
        subscription = stripe.Subscription.delete(subscription_id)
        
        return {
            'subscription': subscription,
            'success': True
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))