CREATE DATABASE OpenFoodFact CHARACTER SET 'utf8';

USE OpenFoodFact

CREATE TABLE Categories(
	id INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(40),
	url VARCHAR(255),

	PRIMARY KEY(id)
)
ENGINE=INNODB;


CREATE TABLE Store(
	id INTEGER NOT NULL AUTO_INCREMENT,
	localisation VARCHAR(40),
	name VARCHAR(40),

	PRIMARY KEY(id)
)
ENGINE=INNODB;


CREATE TABLE Product(
	id INTEGER NOT NULL AUTO_INCREMENT,
	url VARCHAR(255),
	name VARCHAR(40),
	brand VARCHAR(40),
	ingredients TEXT,
	labels TEXT,
	saturated_fat VARCHAR(40),
	fat VARCHAR(40),
	salt VARCHAR(40),
	sugar VARCHAR(40),
	allergens TEXT,
	nutricore INTEGER,

	PRIMARY KEY(id)
)
ENGINE=INNODB;


CREATE TABLE Association_product_category(
	pfk_category_id INTEGER,
	pfk_product_id INTEGER,

	PRIMARY KEY(pfk_category_id, pfk_product_id)
)
ENGINE=INNODB;


CREATE TABLE Association_product_store(
	pfk_product_id INTEGER,
	pfk_store_id INTEGER,

	PRIMARY KEY(pfk_product_id, pfk_store_id)
)
ENGINE=INNODB;


CREATE TABLE Favorites(
	id INTEGER NOT NULL,

	fk_product_id INTEGER,
	fk_surrogate_id INTEGER,

	PRIMARY KEY(id)
)
ENGINE=INNODB;

ALTER TABLE Association_product_category
ADD FOREIGN KEY (pfk_category_id) REFERENCES Categories(id),
ADD FOREIGN KEY (pfk_product_id) REFERENCES Product(id);

ALTER TABLE Association_product_store
ADD FOREIGN KEY (pfk_product_id) REFERENCES Product(id),
ADD FOREIGN KEY (pfk_store_id) REFERENCES Store(id);

ALTER TABLE Favorites
ADD FOREIGN KEY (fk_product_id) REFERENCES Product(id),
ADD FOREIGN KEY (fk_surrogate_id) REFERENCES Product(id);
