CREATE DATABASE OpenFoodFact CHARACTER SET 'utf8';

USE OpenFoodFact

CREATE TABLE Categories(
	id INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(40),
	url VARCHAR(255),

	PRIMARY KEY(id)
)
ENGINE=INNODB;
CREATE INDEX index_name ON Categories(name); 


CREATE TABLE Store(
	id INTEGER NOT NULL AUTO_INCREMENT,
	name VARCHAR(40),
	localisation VARCHAR(40),

	PRIMARY KEY(id)
)
ENGINE=INNODB;
CREATE INDEX index_name ON Store(localisation); 


CREATE TABLE Product(
	id INTEGER NOT NULL AUTO_INCREMENT,
	url VARCHAR(255),
	name VARCHAR(255),
	brand VARCHAR(40),
	ingredients TEXT,
	labels TEXT,
	saturated_fat VARCHAR(40),
	fat VARCHAR(40),
	salt VARCHAR(40),
	sugar VARCHAR(40),
	allergens TEXT,
	nutriscore INTEGER,

	PRIMARY KEY(id)
)
ENGINE=INNODB;
CREATE INDEX index_name ON Product(name);
CREATE INDEX index_url ON Product(url);


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
	id INTEGER NOT NULL AUTO_INCREMENT,

	pfk_product_id INTEGER,
	pfk_substitute_id INTEGER,

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
ADD FOREIGN KEY (pfk_product_id) REFERENCES Product(id),
ADD FOREIGN KEY (pfk_substitute_id) REFERENCES Product(id);
