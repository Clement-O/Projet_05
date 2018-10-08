
DROP_TABLES = [
    "`pb_allergen`",
    "`pb_category`",
    "`pb_label`",
    "`pb_store`",
    "`pb_product`",
    "`pb_product_allergen`",
    "`pb_product_label`",
    "`pb_product_store`",
    "`pb_product_substitute`"
]

CREATE_TABLE = [
    "CREATE TABLE `pb_allergen`"
    "("
    "`id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "`allergen_name` VARCHAR(40) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE `idx_uni_allergen_name` (`allergen_name`)"
    ")"
    "ENGINE = InnoDB AUTO_INCREMENT = 1;",

    "CREATE TABLE `pb_category`"
    "("
    "`id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "`category_name` VARCHAR(250) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE `idx_uni_category_name` (`category_name`)"
    ")"
    "ENGINE = InnoDB AUTO_INCREMENT = 1;",

    "CREATE TABLE `pb_label`"
    "("
    "`id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "`label_name` VARCHAR(40) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE `idx_uni_label_name` (`label_name`)"
    ")"
    "ENGINE = InnoDB AUTO_INCREMENT = 1;",

    "CREATE TABLE `pb_store`"
    "("
    "`id` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "`store_name` VARCHAR(40) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "UNIQUE `idx_uni_store_name` (`store_name`)"
    ")"
    "ENGINE = InnoDB AUTO_INCREMENT = 1;",

    "CREATE TABLE `pb_product`"
    "("
    "`id` BIGINT UNSIGNED NOT NULL,"
    "`name` VARCHAR(250) NOT NULL,"
    "`description` TEXT NOT NULL,"
    "`main_category_id` MEDIUMINT UNSIGNED,"
    "`parent_category_id` MEDIUMINT UNSIGNED,"
    "`child_category_id` MEDIUMINT UNSIGNED,"
    "`nutrition_score` CHAR(1) NULL,"
    "`link` VARCHAR(250) NOT NULL,"
    "PRIMARY KEY (`id`),"
    "KEY `product_idx_main_category_id` (`main_category_id`),"
    "CONSTRAINT `fk_main_category` "
    "FOREIGN KEY `product_idx_main_category_id` (`main_category_id`) "
    "REFERENCES  `pb_category` (`id`),"
    "KEY `product_idx_parent_category_id` (`parent_category_id`),"
    "CONSTRAINT `fk_parent_category` "
    "FOREIGN KEY `product_idx_parent_category_id` (`parent_category_id`) "
    "REFERENCES `pb_category` (`id`),"
    "KEY `product_idx_child_category_id` (`child_category_id`),"
    "CONSTRAINT `fk_child_category` "
    "FOREIGN KEY `product_idx_child_category_id` (`child_category_id`) "
    "REFERENCES `pb_category` (`id`)"
    ")"
    "ENGINE = InnoDB;",

    "CREATE TABLE `pb_product_allergen`"
    "("
    "`product_id` BIGINT UNSIGNED NOT NULL,"
    "`allergen_id` TINYINT UNSIGNED NOT NULL,"
    "PRIMARY KEY (`product_id`, `allergen_id`),"
    "KEY `product_idx_id` (`product_id`),"
    "CONSTRAINT `pk_product_id_allergen` "
    "FOREIGN KEY `product_idx_id` (`product_id`) "
    "REFERENCES `pb_product` (`id`),"
    "KEY `allergen_idx_id` (`allergen_id`),"
    "CONSTRAINT `pk_allergen_id` "
    "FOREIGN KEY `allergen_idx_id` (`allergen_id`) "
    "REFERENCES `pb_allergen` (`id`)"
    ")"
    "ENGINE = InnoDB;",

    "CREATE TABLE `pb_product_label`"
    "("
    "`product_id` BIGINT UNSIGNED NOT NULL,"
    "`label_id` TINYINT UNSIGNED NOT NULL,"
    "PRIMARY KEY (`product_id`, `label_id`),"
    "KEY `product_idx_id` (`product_id`),"
    "CONSTRAINT `pk_product_id_label` "
    "FOREIGN KEY `product_idx_id` (`product_id`) "
    "REFERENCES `pb_product` (`id`),"
    "KEY `label_idx_id` (`label_id`),"
    "CONSTRAINT `pk_label_id` "
    "FOREIGN KEY `label_idx_id` (`label_id`) "
    "REFERENCES `pb_label` (`id`)"
    ")"
    "ENGINE = InnoDB;",

    "CREATE TABLE `pb_product_store`"
    "("
    "`product_id` BIGINT UNSIGNED NOT NULL,"
    "`store_id` TINYINT UNSIGNED NOT NULL,"
    "PRIMARY KEY (`product_id`, `store_id`),"
    "KEY `product_idx_id` (`product_id`),"
    "CONSTRAINT `pk_product_id_store` "
    "FOREIGN KEY `product_idx_id` (`product_id`) "
    "REFERENCES `pb_product` (`id`),"
    "KEY `store_idx_id` (`store_id`),"
    "CONSTRAINT `pk_store_id` "
    "FOREIGN KEY `store_idx_id` (`store_id`) "
    "REFERENCES `pb_store` (`id`)"
    ")"
    "ENGINE = InnoDB;",

    "CREATE TABLE `pb_product_substitute`"
    "("
    "`original_id` BIGINT UNSIGNED NOT NULL,"
    "`substitute_id` BIGINT UNSIGNED NOT NULL,"
    "PRIMARY KEY (`original_id`, `substitute_id`),"
    "KEY `original_idx_id` (`original_id`),"
    "CONSTRAINT `pk_original_product` "
    "FOREIGN KEY `original_idx_id` (`original_id`) "
    "REFERENCES `pb_product` (`id`),"
    "KEY `substitute_idx_id` (`substitute_id`),"
    "CONSTRAINT `pk_substitute_product` "
    "FOREIGN KEY `substitute_idx_id` (`substitute_id`) "
    "REFERENCES `pb_product` (`id`)"
    ")"
    "ENGINE = InnoDB;"
]
