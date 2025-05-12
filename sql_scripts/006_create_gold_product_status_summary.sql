create or replace view gold.products_stat_summary as
SELECT
  p.product_sku,
  p.product_name,
  SUM(pil.product_quantity_available - pil.product_quarantined_quantity - pil.product_quantity_unavailable) AS total_product_stock_available,
  CASE
    WHEN SUM(pil.product_quantity_available) = 0 THEN 'Out of Stock'
    WHEN SUM(pil.product_quantity_available) <= 5 THEN 'Low Stock'
    ELSE 'In Stock'
  END AS product_stock_status,
  CASE
    WHEN p.product_length IS NOT NULL
      AND p.product_width IS NOT NULL
      AND p.product_height IS NOT NULL
    THEN ROUND(((p.product_length * p.product_width * p.product_height) * 2.54)::numeric, 2)
    ELSE NULL
  END AS product_volume,
  CASE
    WHEN p.product_length IS NOT NULL
      AND p.product_width IS NOT NULL
      AND p.product_height IS NOT NULL
    THEN ROUND((p.product_length * p.product_width * p.product_height * SUM(pil.product_quantity_available))::numeric, 2)
    ELSE NULL
  END AS total_warehouse_space_taken_by_product,
  'cm²' as product_volume_unit
FROM
  silver.products_inventory_locations pil
JOIN
  silver.products p ON p.product_inventory_id = pil.product_inventory_id
where p.is_product_active = True
GROUP BY
  p.product_sku, p.product_name, p.product_length, p.product_width, p.product_height;