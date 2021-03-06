CREATE TABLE "cart" (
	"id"	SERIAL PRIMARY KEY
);

CREATE TABLE "cart_item" (
	"id"		SERIAL 	PRIMARY KEY,
	"product"	TEXT 	NOT NULL,
	"quantity"	INTEGER	CHECK ("quantity" > 0),
	"cart_id"	INTEGER NOT NULL REFERENCES "cart"	ON UPDATE CASCADE ON DELETE RESTRICT
);
