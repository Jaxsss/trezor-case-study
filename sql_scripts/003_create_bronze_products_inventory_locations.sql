create table bronze.products_inventory_locations (
    id serial primary key,
    quantity_available varchar null,
    quantity_on_hand varchar null,
    quarantined_quantity varchar null,
    quantity_unavailable varchar null,
    warehouse_id varchar null,
    json_parent_id varchar null,
    warehouse_name varchar null,
    warehouse_identifier varchar null
);