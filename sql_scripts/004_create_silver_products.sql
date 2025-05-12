create table silver.products (
	id serial primary key,
	inventory_location_id varchar(60) null,
	product_weight float null,
	weight_unit varchar(2) null,
	product_length float null,
	product_width float null,
	product_height float null,
	dimension_unit varchar(2) null,
	product_sku varchar(50) null,
	product_name varchar(100) null,
	is_product_active bool default false null,
	product_type varchar(10) null
);