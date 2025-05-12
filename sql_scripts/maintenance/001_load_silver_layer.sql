truncate table silver.products;
insert into silver.products (product_inventory_id,
product_weight,
weight_unit,
product_length,
product_width,
product_height,
dimension_unit,
product_sku,
product_name,
is_product_active,
product_type,
dw_date_loaded)
select
	inventory_locations as product_inventory_id,
	weight_value::float as product_weight,
	weight_unit as weight_unit,
	dimensions_length::float as product_length,
	dimensions_width::float as product_width,
	dimensions_height::float as product_height,
	dimensions_unit as dimension_unit,
	sku as product_sku,
	name as product_name,
	case
		when is_active is null then false
		when is_active::numeric != 0 then true
		else false
	end as is_product_active,
	product_type,
	dw_date_loaded
from bronze.products p;

truncate table silver.products_inventory_locations;
insert into silver.products_inventory_locations (
product_quantity_available,
product_quantity_on_hand,
product_quarantined_quantity,
product_quantity_unavailable,
warehouse_id,
product_inventory_id,
warehouse_name,
warehouse_identifier
)
select
	quantity_available::integer as product_quantity_available,
	case
		when quantity_available < quantity_on_hand then quantity_available::integer
		else quantity_on_hand::integer
	end as product_quantity_on_hand,
	quarantined_quantity::integer as product_quarantined_quantity,
	quantity_unavailable::integer as product_quantity_unavailable,
	warehouse_id::integer,
	json_parentid as product_inventory_id,
	warehouse_name,
	warehouse_identifier
from bronze.products_inventory_locations;