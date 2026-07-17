---
name: wine-order-check
description: >
  Apply when investigating a customer's orders, payments, or billing issues
  for the Crested Butte Wine + Food Festival shop (shop.cbwineandfood.com).
  Triggers include: forwarded customer emails about payments, questions like
  "what did [name] pay?", "did [name] get charged?", "look up [name]'s order",
  or any order/payment triage involving CBWFF customers.
---

# CBWFF Order Investigator

You are investigating WooCommerce orders and Stripe payments for the Crested
Butte Wine + Food Festival shop at shop.cbwineandfood.com.

## Infrastructure

**Production server** (always use this for order lookups):
- SSH host: `cfta-brett@143.198.110.93`
- SSH flags: `-o StrictHostKeyChecking=no`
- MySQL: user=`nyuqcdfzjc`, password=`bfY3T7vd2Y`, db=`nyuqcdfzjc`
- WP path: `/home/nyuqcdfzjc/public_html`
- WooCommerce uses **HPOS** — orders are in `wp_wc_orders`, not `wp_posts`

**Stripe**: Use the Stripe MCP or API if available. Key order fields to
cross-reference: invoice ID, payment intent, charge amount vs WC total.

## Database schema quick reference

```sql
-- Orders
wp_wc_orders            -- id, status, billing_email, total_amount, date_created_gmt
wp_wc_orders_meta       -- order_id, meta_key, meta_value
                        --   _payment_method, _stripe_charge_id, _stripe_invoice_id
                        --   _cfta_pass_activated, customer_ip_address

-- Order items
wp_woocommerce_order_items      -- order_item_id, order_id, order_item_name, order_item_type
wp_woocommerce_order_itemmeta   -- _product_id, _qty, _line_total
```

## Investigation workflow

1. **Find the customer's orders** by billing email:
```sql
SELECT o.id, o.status, o.date_created_gmt, o.total_amount,
       oi.order_item_name, qty.meta_value AS qty,
       pm.meta_value AS payment_method
FROM wp_wc_orders o
JOIN wp_woocommerce_order_items oi ON oi.order_id = o.id AND oi.order_item_type = 'line_item'
JOIN wp_woocommerce_order_itemmeta qty ON qty.order_item_id = oi.order_item_id AND qty.meta_key = '_qty'
LEFT JOIN wp_wc_orders_meta pm ON pm.order_id = o.id AND pm.meta_key = '_payment_method'
WHERE o.billing_email IN ('email@example.com','Email@example.com')
ORDER BY o.id, oi.order_item_id;
```

2. **Check for Stripe metadata** on relevant orders:
```sql
SELECT order_id, meta_key, meta_value
FROM wp_wc_orders_meta
WHERE order_id IN (...)
  AND meta_key IN ('_payment_method','_stripe_charge_id','_stripe_invoice_id',
                   '_stripe_payment_intent_id','_cfta_pass_activated',
                   'customer_ip_address','_transaction_id')
ORDER BY order_id, meta_key;
```

3. **Cross-reference Stripe** if a charge ID or invoice ID is present. Look for:
   - Stripe Invoice vs WC total gaps (often $0.30 CC fee discrepancies)
   - Duplicate charges (two successful charges within minutes)
   - Failed charge followed by successful retry (no action needed)

## Key business rules

- **Pearl Patron Pass** (product 361): includes 2 TDF dinners per pass holder.
  If qty=2 purchased, that's 4 TDF slots total.
- **Star Patron Pass** (product 360): includes 2 TDF dinners per pass holder.
- **TDF Dinners**: Wild Dusk (281), Golden Hour (294), High Note (295),
  Annual Dinner at Campfire Ranch (290). Individual price: $450/ticket.
- **CC Processing Fee**: 3% surcharge added for credit card payments.
  Should NOT appear on orders paid via "Pay by Check" (cheque) or
  "Pay by Bank Transfer" (bacs). If it does, that's a bug.
- **Backend-created orders** (customer_ip_address is NULL or empty, customer_id=0):
  created by Natalie in WP admin — they bypass frontend checkout hooks and
  do NOT activate pass access automatically. They also don't reduce stock.
- **Pass-covered session registrations**: appear as $0 orders with
  payment_method=NULL. These are normal — the pass covers the cost.
- **`wc-processing`** = payment received, awaiting fulfillment (ticket is sold).
- **`wc-completed`** = fulfilled. **`wc-pending`** = not yet paid.

## Output format

Produce a summary table:

| Order | Item | Amount | Paid via | Status |
|-------|------|--------|----------|--------|

Then bullet-point any issues:
- Unpaid orders (pending/no payment method on completed order)
- Erroneous CC fees on check/bank orders
- Duplicate orders for the same event
- Stripe vs WC amount gaps
- Missing pass activation

End with: **Net: [one sentence on whether there's a financial issue and what action is needed]**

If the input is a forwarded email or PDF, extract the customer name/email
first, then run the lookup. Don't ask for information you can look up yourself.
