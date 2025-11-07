from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import hashlib
import os
from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# PayU Configuration
PAYU_MERCHANT_KEY = os.getenv('PAYU_MERCHANT_KEY')
PAYU_MERCHANT_SALT = os.getenv('PAYU_MERCHANT_SALT')
PAYU_MODE = os.getenv('PAYU_MODE', 'live')

# PayU URLs
PAYU_BASE_URL = "https://secure.payu.in/_payment" if PAYU_MODE == 'live' else "https://test.payu.in/_payment"

# Pricing in INR
PRICING_PLANS = {
    'starter': {
        'monthly': 100,
        'annual': 1000
    },
    'professional': {
        'monthly': 1000,
        'annual': 10000
    },
    'enterprise': {
        'monthly': 1500,
        'annual': 15000
    }
}

def generate_hash(data):
    """Generate PayU hash for transaction"""
    hash_string = f"{PAYU_MERCHANT_KEY}|{data['txnid']}|{data['amount']}|{data['productinfo']}|{data['firstname']}|{data['email']}|||||||||||{PAYU_MERCHANT_SALT}"
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

@router.post('/create-payment')
async def create_payu_payment(request: Request):
    """Create PayU payment request"""
    try:
        data = await request.json()
        plan = data.get('plan')  # starter, professional, enterprise
        billing = data.get('billing')  # monthly, annual
        email = data.get('email')
        name = data.get('name')
        phone = data.get('phone', '9999999999')
        
        if plan not in PRICING_PLANS:
            raise HTTPException(status_code=400, detail='Invalid plan')
        
        if billing not in ['monthly', 'annual']:
            raise HTTPException(status_code=400, detail='Invalid billing period')
        
        # Get amount in INR
        amount = PRICING_PLANS[plan][billing]
        
        # Generate unique transaction ID
        import time
        txnid = f"VM{int(time.time())}"
        
        # Prepare PayU data
        payu_data = {
            'key': PAYU_MERCHANT_KEY,
            'txnid': txnid,
            'amount': str(amount),
            'productinfo': f'VideoMaker {plan.title()} - {billing.title()}',
            'firstname': name,
            'email': email,
            'phone': phone,
            'surl': data.get('success_url', 'http://localhost:3000/success'),
            'furl': data.get('failure_url', 'http://localhost:3000/'),
        }
        
        # Generate hash
        payu_data['hash'] = generate_hash(payu_data)
        
        return {
            'success': True,
            'payment_url': PAYU_BASE_URL,
            'payment_data': payu_data,
            'txnid': txnid
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/verify-payment')
async def verify_payu_payment(request: Request):
    """Verify PayU payment response"""
    try:
        data = await request.json()
        
        # Verify hash
        status = data.get('status')
        txnid = data.get('txnid')
        amount = data.get('amount')
        productinfo = data.get('productinfo')
        firstname = data.get('firstname')
        email = data.get('email')
        
        # Generate reverse hash for verification
        hash_string = f"{PAYU_MERCHANT_SALT}|{status}|||||||||||{email}|{firstname}|{productinfo}|{amount}|{txnid}|{PAYU_MERCHANT_KEY}"
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
        
        received_hash = data.get('hash')
        
        if generated_hash == received_hash and status == 'success':
            # Update user's subscription plan
            plan_name = productinfo.split('-')[0].lower()  # Extract plan from productinfo
            
            # Update user in database
            result = await db.users.update_one(
                {'email': email},
                {
                    '$set': {
                        'subscription_plan': plan_name,
                        'subscription_status': 'active',
                        'subscription_updated_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            return {
                'success': True,
                'verified': True,
                'status': status,
                'txnid': txnid,
                'subscription_updated': result.modified_count > 0
            }
        elif generated_hash == received_hash:
            return {
                'success': True,
                'verified': True,
                'status': status,
                'txnid': txnid
            }
        else:
            return {
                'success': False,
                'verified': False,
                'message': 'Hash verification failed'
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/config')
async def get_payu_config():
    """Get PayU configuration"""
    return {
        'merchant_key': PAYU_MERCHANT_KEY,
        'payment_url': PAYU_BASE_URL,
        'success': True
    }
