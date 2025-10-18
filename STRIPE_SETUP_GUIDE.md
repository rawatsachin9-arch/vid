# 🚀 Stripe Payment Integration - Setup Guide

## ✅ What's Integrated

Your VideoAI platform now includes:
- **Stripe Checkout** for subscription payments
- **Monthly & Annual billing** options
- **3 Pricing tiers**: Starter ($19/mo), Professional ($49/mo), Enterprise ($99/mo)
- **Payment success page** with confirmation
- **Webhook support** for payment events
- **Secure payment processing** (PCI compliant)

---

## 📋 Quick Setup Steps

### Step 1: Get Stripe API Keys

1. **Sign up for Stripe** (if you haven't already):
   - Go to: https://dashboard.stripe.com/register
   - Create a free account

2. **Get your API keys**:
   - Go to: https://dashboard.stripe.com/test/apikeys
   - You'll see two keys:
     - **Publishable key** (starts with `pk_test_`)
     - **Secret key** (starts with `sk_test_`) - Click "Reveal test key"

3. **Copy both keys** - you'll need them in the next step

---

### Step 2: Create Products in Stripe Dashboard

1. Go to: https://dashboard.stripe.com/test/products
2. Click **"+ Add product"**
3. Create **3 products** with the following details:

#### Product 1: VideoAI Starter
- **Name**: VideoAI Starter
- **Description**: Perfect for individuals getting started
- Click **"Add pricing"**:
  - **Monthly**: $19.00 USD, Recurring, Monthly
  - Click "Add another price"
  - **Annual**: $180.00 USD, Recurring, Yearly
- Click **"Save product"**
- **Copy the Price IDs** (starts with `price_`) for both monthly and annual

#### Product 2: VideoAI Professional  
- **Name**: VideoAI Professional
- **Description**: For content creators and marketers
- Click **"Add pricing"**:
  - **Monthly**: $49.00 USD, Recurring, Monthly
  - **Annual**: $468.00 USD, Recurring, Yearly
- Click **"Save product"**
- **Copy the Price IDs** for both

#### Product 3: VideoAI Enterprise
- **Name**: VideoAI Enterprise
- **Description**: For teams and organizations
- Click **"Add pricing"**:
  - **Monthly**: $99.00 USD, Recurring, Monthly
  - **Annual**: $948.00 USD, Recurring, Yearly
- Click **"Save product"**
- **Copy the Price IDs** for both

---

### Step 3: Update Environment Variables

#### Backend Configuration (`/app/backend/.env`):

```bash
# Replace these with your actual Stripe keys from Step 1
STRIPE_SECRET_KEY="sk_test_YOUR_ACTUAL_SECRET_KEY_HERE"
STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY_HERE"

# Replace these with your Price IDs from Step 2
STRIPE_STARTER_MONTHLY_PRICE_ID="price_YOUR_STARTER_MONTHLY_ID"
STRIPE_STARTER_ANNUAL_PRICE_ID="price_YOUR_STARTER_ANNUAL_ID"
STRIPE_PROFESSIONAL_MONTHLY_PRICE_ID="price_YOUR_PROFESSIONAL_MONTHLY_ID"
STRIPE_PROFESSIONAL_ANNUAL_PRICE_ID="price_YOUR_PROFESSIONAL_ANNUAL_ID"
STRIPE_ENTERPRISE_MONTHLY_PRICE_ID="price_YOUR_ENTERPRISE_MONTHLY_ID"
STRIPE_ENTERPRISE_ANNUAL_PRICE_ID="price_YOUR_ENTERPRISE_ANNUAL_ID"
```

#### Frontend Configuration (`/app/frontend/.env`):

```bash
# Add your Stripe publishable key
REACT_APP_STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY_HERE"
```

---

### Step 4: Restart Services

After updating the `.env` files, restart both services:

```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

---

## 🧪 Testing the Integration

### Test Card Numbers (Use in Test Mode Only)

| Card Number          | Result              |
|---------------------|---------------------|
| 4242 4242 4242 4242 | ✅ Success          |
| 4000 0000 0000 9995 | ❌ Declined         |
| 4000 0025 0000 3155 | 🔐 Requires Auth    |

**Additional Details for Test Cards:**
- **Expiry**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### Test the Payment Flow

1. **Go to your app**: http://localhost:3000 (or your domain)
2. **Scroll to Pricing section**
3. **Click any "Subscribe" button**
4. **You'll be redirected to Stripe Checkout**
5. **Enter test card**: 4242 4242 4242 4242
6. **Fill in other details** (use any future date, any CVC)
7. **Click "Subscribe"**
8. **You'll be redirected to Success page** 🎉

---

## 🎯 Features Implemented

### ✅ Subscription Payments
- Monthly and annual billing options
- Automatic recurring payments
- Stripe Checkout hosted payment page
- Secure payment processing

### ✅ Multiple Plans
- **Starter**: $19/month or $180/year
- **Professional**: $49/month or $468/year  
- **Enterprise**: $99/month or $948/year

### ✅ Payment Flow
1. User clicks "Subscribe" button
2. Backend creates Stripe Checkout session
3. User redirects to Stripe-hosted payment page
4. User enters payment details securely
5. After payment, redirects to success page
6. Webhook notifies backend of payment status

### ✅ Security
- All sensitive data handled by Stripe (PCI compliant)
- No credit card data touches your servers
- Webhook signature verification
- Test mode for development, Live mode for production

---

## 🔧 API Endpoints

### Get Stripe Config
```
GET /api/stripe/config
Response: { "publishableKey": "pk_test_...", "success": true }
```

### Create Checkout Session
```
POST /api/stripe/create-checkout-session
Body: {
  "plan": "starter" | "professional" | "enterprise",
  "billing": "monthly" | "annual",
  "email": "customer@example.com" (optional)
}
Response: { "sessionId": "cs_test_...", "url": "https://checkout.stripe.com/...", "success": true }
```

### Webhook Endpoint
```
POST /api/stripe/webhook
Headers: { "stripe-signature": "..." }
```

---

## 📊 Monitor Payments

### Stripe Dashboard Links

- **All Payments**: https://dashboard.stripe.com/test/payments
- **Subscriptions**: https://dashboard.stripe.com/test/subscriptions
- **Customers**: https://dashboard.stripe.com/test/customers
- **Products**: https://dashboard.stripe.com/test/products
- **Webhooks**: https://dashboard.stripe.com/test/webhooks

---

## 🌐 Going Live (Production)

### When Ready for Real Payments:

1. **Activate your Stripe account**:
   - Complete business verification in Stripe Dashboard
   
2. **Create Live Mode products**:
   - Switch to "Live mode" toggle in Stripe Dashboard
   - Create the same 3 products with live pricing
   - Copy the **Live Price IDs**

3. **Update environment variables**:
   - Replace `sk_test_` with `sk_live_` (Secret Key)
   - Replace `pk_test_` with `pk_live_` (Publishable Key)
   - Update all Price IDs with live versions

4. **Set up webhooks**:
   - Go to: https://dashboard.stripe.com/webhooks
   - Add endpoint: `https://yourdomain.com/api/stripe/webhook`
   - Select events: `checkout.session.completed`, `payment_intent.succeeded`, `customer.subscription.deleted`
   - Copy webhook secret and add to `.env`

5. **Restart services** and test with real cards

---

## 🚨 Troubleshooting

### Issue: "Invalid API Key"
**Solution**: 
- Check keys are correctly copied to `.env` files
- Ensure no extra spaces or quotes
- Restart backend: `sudo supervisorctl restart backend`

### Issue: "No such price"
**Solution**:
- Verify Price IDs in Stripe Dashboard
- Ensure you're using test Price IDs with test API keys
- Check for typos in `.env` file

### Issue: Button doesn't work
**Solution**:
- Check browser console for errors (F12)
- Verify frontend `.env` has correct publishable key
- Ensure backend is running: `sudo supervisorctl status backend`

### Issue: Redirect not working
**Solution**:
- Check success_url and cancel_url in checkout session
- Verify `/success` route exists in React Router

---

## 📚 Useful Resources

- **Stripe Documentation**: https://stripe.com/docs
- **Checkout Guide**: https://stripe.com/docs/payments/checkout
- **Subscriptions**: https://stripe.com/docs/billing/subscriptions/overview
- **Testing**: https://stripe.com/docs/testing
- **Webhooks**: https://stripe.com/docs/webhooks

---

## 🎉 You're All Set!

Your VideoAI platform is now ready to accept payments via Stripe. Test thoroughly in test mode before going live!

**Need help?** Check the Stripe Dashboard or contact Stripe support.
