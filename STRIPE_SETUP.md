# Stripe Payment Integration Setup Guide

## 🚀 Quick Start

Your VideoAI platform now has Stripe payment integration with both **one-time payments** and **subscription billing**!

## 📋 Setup Steps

### 1. Get Stripe API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/register)
2. Sign up or log in to your account
3. Navigate to **Developers → API keys**
4. Copy your keys:
   - **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - **Secret key** (starts with `sk_test_` or `sk_live_`)

### 2. Create Products and Prices in Stripe

1. Go to [Products](https://dashboard.stripe.com/test/products) in Stripe Dashboard
2. Click **+ Add product**
3. Create 3 products:

#### Product 1: Starter Plan
- **Name**: VideoAI Starter
- **Description**: Perfect for individuals getting started
- **Pricing**:
  - Monthly: $19/month (Recurring)
  - Annual: $180/year (Recurring, billed yearly)
- Copy the Price IDs for later

#### Product 2: Professional Plan
- **Name**: VideoAI Professional
- **Description**: For content creators and marketers
- **Pricing**:
  - Monthly: $49/month (Recurring)
  - Annual: $468/year (Recurring, billed yearly)
- Copy the Price IDs for later

#### Product 3: Enterprise Plan
- **Name**: VideoAI Enterprise
- **Description**: For teams and organizations
- **Pricing**:
  - Monthly: $99/month (Recurring)
  - Annual: $948/year (Recurring, billed yearly)
- Copy the Price IDs for later

### 3. Configure Environment Variables

#### Backend (.env file at `/app/backend/.env`):

```bash
# Replace with your actual Stripe keys
STRIPE_SECRET_KEY="sk_test_YOUR_ACTUAL_SECRET_KEY"
STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY"
STRIPE_WEBHOOK_SECRET="whsec_YOUR_WEBHOOK_SECRET"  # From webhook setup

# Replace with your actual Price IDs from Stripe Dashboard
STRIPE_STARTER_MONTHLY_PRICE_ID="price_xxxxxxxxxxxxx"
STRIPE_STARTER_ANNUAL_PRICE_ID="price_xxxxxxxxxxxxx"
STRIPE_PROFESSIONAL_MONTHLY_PRICE_ID="price_xxxxxxxxxxxxx"
STRIPE_PROFESSIONAL_ANNUAL_PRICE_ID="price_xxxxxxxxxxxxx"
STRIPE_ENTERPRISE_MONTHLY_PRICE_ID="price_xxxxxxxxxxxxx"
STRIPE_ENTERPRISE_ANNUAL_PRICE_ID="price_xxxxxxxxxxxxx"
```

#### Frontend (.env file at `/app/frontend/.env`):

```bash
# Add this line with your publishable key
REACT_APP_STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY"
```

### 4. Set Up Webhooks (Optional but Recommended)

1. Go to [Webhooks](https://dashboard.stripe.com/test/webhooks) in Stripe Dashboard
2. Click **+ Add endpoint**
3. Enter your endpoint URL:
   ```
   https://your-domain.com/api/stripe/webhook
   ```
4. Select events to listen to:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. Copy the **Signing secret** (starts with `whsec_`)
6. Add it to your backend `.env` file as `STRIPE_WEBHOOK_SECRET`

### 5. Restart Services

After updating the `.env` files:

```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

## 🎯 Features Implemented

### ✅ Subscription Payments
- Monthly and annual billing options
- Automatic recurring payments
- Stripe Checkout hosted payment page
- Subscription management

### ✅ One-Time Payments
- Single purchase option (if needed)
- PaymentIntent API integration

### ✅ Payment Flow
1. User clicks "Subscribe" button on pricing page
2. Redirects to Stripe Checkout
3. User enters payment details securely on Stripe
4. After payment, redirects to success page
5. Webhook notifies your backend of payment status

### ✅ Security
- PCI-compliant (Stripe handles all card data)
- No sensitive data stored on your server
- Webhook signature verification
- Test mode for development

## 🧪 Testing

### Test Card Numbers

Use these test cards in **test mode**:

| Card Number | Description |
|-------------|-------------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 9995` | Declined payment |
| `4000 0025 0000 3155` | Requires authentication |

- **Expiry**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### Test the Integration

1. Start your servers
2. Go to pricing page
3. Click any "Subscribe" button
4. You'll be redirected to Stripe Checkout
5. Use test card `4242 4242 4242 4242`
6. Complete the payment
7. You'll be redirected to success page

## 📊 Monitoring

### Stripe Dashboard
- View all payments: [Payments](https://dashboard.stripe.com/test/payments)
- View subscriptions: [Subscriptions](https://dashboard.stripe.com/test/subscriptions)
- View customers: [Customers](https://dashboard.stripe.com/test/customers)

### Backend Logs
```bash
sudo supervisorctl tail -f backend
```

## 🚨 Important Notes

1. **Test Mode vs Live Mode**
   - Use test keys (`sk_test_` and `pk_test_`) for development
   - Switch to live keys (`sk_live_` and `pk_live_`) for production

2. **Never Commit API Keys**
   - Keys are in `.env` files (gitignored)
   - Never hardcode keys in source code

3. **Webhook Secret**
   - Required for production to verify webhook authenticity
   - Different secret for test and live mode

## 🆘 Troubleshooting

### Issue: "Invalid API Key"
- Check that keys are correctly copied to `.env` files
- Ensure no extra spaces or quotes
- Restart backend after updating `.env`

### Issue: "No such price"
- Verify Price IDs in Stripe Dashboard
- Ensure Price IDs are copied correctly to `.env`
- Check that you're using test mode Price IDs with test API keys

### Issue: Payment button not working
- Check browser console for errors
- Verify `REACT_APP_STRIPE_PUBLISHABLE_KEY` in frontend `.env`
- Ensure backend is running and accessible

## 📚 API Endpoints

### Get Stripe Config
```
GET /api/stripe/config
```

### Create Checkout Session
```
POST /api/stripe/create-checkout-session
Body: {
  "plan": "starter" | "professional" | "enterprise",
  "billing": "monthly" | "annual",
  "email": "customer@example.com"
}
```

### Create Payment Intent (One-time)
```
POST /api/stripe/create-payment-intent
Body: {
  "plan": "starter" | "professional" | "enterprise",
  "billing": "monthly" | "annual"
}
```

### Webhook Endpoint
```
POST /api/stripe/webhook
```

## 🎓 Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [Stripe Subscriptions](https://stripe.com/docs/billing/subscriptions/overview)
- [Stripe Testing](https://stripe.com/docs/testing)

## ✨ Next Steps

1. Add user authentication
2. Store subscription data in MongoDB
3. Create user dashboard to manage subscriptions
4. Add email notifications for payment events
5. Implement trial periods
6. Add promo codes/coupons

---

**Need Help?** Check the Stripe Dashboard or contact support!