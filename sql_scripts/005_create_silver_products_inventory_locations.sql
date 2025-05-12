create table silver.products_inventory_locations (
	id serial primary key,
	product_quantity_available int4 null,
	product_quantity_on_hand int4 null,
	product_quarantined_quantity int4 null,
	product_quantity_unavailable int4 null,
	warehouse_id int4 null,
	product_inventory_id varchar(60) null,
	warehouse_name varchar(20) null,
	warehouse_identifier varchar(20) null
)