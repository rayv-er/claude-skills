---
name: wine-stock-audit
description: >
  Apply when auditing or fixing ticket/stock counts for the Crested Butte
  Wine + Food Festival shop (shop.cbwineandfood.com). Triggers include:
  "are the ticket counts right?", "stock looks off", "how many tickets are
  left for [event]?", "fix the ticket counts", or any question about
  available capacity vs actual sales.
---

# CBWFF Festival Stock Auditor

You audit and optionally correct WooCommerce stock levels for all festival
products at shop.cbwineandfood.com. Stock levels must match actual orders —
the `_stock` meta field is the source of truth for what customers see as
available, but it can drift from reality due to manual resets, backend-created
orders, or cancelled orders that didn't restock.

## Infrastructure

**Production server**:
- SSH: `cfta-brett@143.198.110.93` (flags: `-o StrictHostKeyChecking=no`)
- MySQL: user=`nyuqcdfzjc`, password=`bfY3T7vd2Y`, db=`nyuqcdfzjc`
- WP path: `/home/nyuqcdfzjc/public_html`
- WooCommerce HPOS: orders in `wp_wc_orders`, products still in `wp_posts`/`wp_postmeta`

## Key product meta fields

| Meta key | Meaning |
|---|---|
| `_stock` | Current available stock (what customers see) |
| `_manage_stock` | `yes` = stock tracking enabled |
| `_cfta_max_capacity` | Hard capacity ceiling set by staff |
| `total_sales` | WC internal counter (increments on completion) |

## Audit query — run this first

```sql
SELECT
  po.ID AS product_id,
  po.post_title,
  cap.meta_value AS capacity,
  stk.meta_value AS wc_stock,
  CAST(cap.meta_value AS SIGNED) - CAST(stk.meta_value AS SIGNED) AS wc_thinks_sold,
  COALESCE(ord.completed, 0)  AS completed_orders,
  COALESCE(ord.processing, 0) AS processing_orders,
  COALESCE(ord.completed, 0) + COALESCE(ord.processing, 0) AS true_sold,
  CAST(cap.meta_value AS SIGNED)
    - (COALESCE(ord.completed, 0) + COALESCE(ord.processing, 0)) AS true_remaining,
  CAST(stk.meta_value AS SIGNED)
    - (CAST(cap.meta_value AS SIGNED)
    - (COALESCE(ord.completed, 0) + COALESCE(ord.processing, 0))) AS stock_error
FROM wp_posts po
LEFT JOIN wp_postmeta cap ON cap.post_id = po.ID AND cap.meta_key = '_cfta_max_capacity'
LEFT JOIN wp_postmeta stk ON stk.post_id = po.ID AND stk.meta_key = '_stock'
LEFT JOIN (
  SELECT
    im.meta_value AS product_id,
    SUM(CASE WHEN o.status = 'wc-completed'  THEN qty.meta_value ELSE 0 END) AS completed,
    SUM(CASE WHEN o.status = 'wc-processing' THEN qty.meta_value ELSE 0 END) AS processing
  FROM wp_woocommerce_order_items oi
  JOIN wp_woocommerce_order_itemmeta im  ON im.order_item_id = oi.order_item_id AND im.meta_key = '_product_id'
  JOIN wp_woocommerce_order_itemmeta qty ON qty.order_item_id = oi.order_item_id AND qty.meta_key = '_qty'
  JOIN wp_wc_orders o ON o.id = oi.order_id
  WHERE oi.order_item_type = 'line_item'
  GROUP BY im.meta_value
) ord ON ord.product_id = po.ID
WHERE po.post_type = 'product'
  AND po.post_status = 'publish'
  AND cap.meta_value IS NOT NULL
  AND stk.meta_value IS NOT NULL
ORDER BY ABS(
  CAST(stk.meta_value AS SIGNED)
  - (CAST(cap.meta_value AS SIGNED)
  - (COALESCE(ord.completed, 0) + COALESCE(ord.processing, 0)))
) DESC;
```

## Reading the results

- **`stock_error = 0`**: Perfect — no action needed.
- **`stock_error > 0` (positive)**: WC is showing MORE tickets available than
  reality. Customers could oversell these events. Urgent fix.
  _Cause_: stock was manually reset to capacity after sales started, or
  stock management was enabled after orders were already placed.
- **`stock_error < 0` (negative)**: WC is showing FEWER tickets available than
  reality. Events look more sold-out than they are. Less urgent but worth fixing.
  _Cause_: cancelled orders didn't restock (admin clicked "No" on restock prompt,
  or order was backend-created and cancellation didn't trigger hook).

## Pending orders — important caveat

Backend-created orders (created by staff in WP admin) with `wc-pending` status
do NOT reduce stock. Do not include `wc-pending` in the "true sold" count unless
you've verified those orders went through frontend checkout.

Check pending orders before correcting:
```sql
SELECT o.id, o.status, o.billing_email, o.total_amount,
       oi.order_item_name, qty.meta_value AS qty
FROM wp_wc_orders o
JOIN wp_woocommerce_order_items oi ON oi.order_id = o.id AND oi.order_item_type = 'line_item'
JOIN wp_woocommerce_order_itemmeta qty ON qty.order_item_id = oi.order_item_id AND qty.meta_key = '_qty'
WHERE o.status = 'wc-pending'
ORDER BY o.id;
```

## Applying corrections

Only apply corrections after showing the user the audit table and getting
explicit approval. The correction is a direct SQL UPDATE — not a WC hook,
so cancellations after the fact won't corrupt the corrected values:

```sql
-- Example corrections (confirm values from audit first):
UPDATE wp_postmeta SET meta_value = <true_remaining>
  WHERE post_id = <product_id> AND meta_key = '_stock';
```

After all UPDATEs, always flush cache:
```bash
cd /home/nyuqcdfzjc/public_html && wp cache flush --allow-root
wp transient delete --all --allow-root
```

## Output format

Present the audit as a table with columns:
**Event | Capacity | WC Shows Available | Actually Available | Error | Action**

Then group into:
- 🔴 **Needs immediate fix** (stock_error > 5 — potential oversell)
- 🟡 **Minor correction** (stock_error 1–5 or negative)
- ✅ **Accurate** (stock_error = 0)

Ask for approval before running any SQL corrections.
After corrections, run a verification query to confirm values landed correctly.
