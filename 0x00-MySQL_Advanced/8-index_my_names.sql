-- create an index 'idx_name_first' on table names and the first letter of 'name'
alter TABLE names ADD INDEX idx_name_first ON names (name(1));
