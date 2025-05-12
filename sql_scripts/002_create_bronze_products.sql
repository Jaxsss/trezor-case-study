create table bronze.products (
    id serial primary key,
    inventory_locations varchar null,
    weight_value varchar null,
    weight_unit varchar null,
    dimensions_length varchar null,
    dimensions_width varchar null,
    dimensions_height varchar null,
    dimensions_unit varchar null,
    sku varchar null,
    name varchar null,
    is_active varchar null,
    product_type varchar null
);