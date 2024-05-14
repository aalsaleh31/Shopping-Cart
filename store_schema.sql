-- PRAGMA foreign_keys=off; -- dont know what this means

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	username				varchar(50) not null, --specify here or down
	name				varchar(50) not null,
	password		varchar(50) not null,
	
	PRIMARY KEY (username)
);

DROP TABLE IF EXISTS items;
CREATE TABLE items(
	item_id				varchar(50) not null,
	item_name			varchar(50) not null,
	item_price			integer not null,
	item_stock 			integer not null,
	item_type			varchar(50) not null,
	item_desc			varchar(10000) not null,
	
	PRIMARY KEY (item_id)
);

DROP TABLE IF EXISTS receipt;
CREATE TABLE receipt(
	amount				varchar(50) not null, --specify here or down
	products			VARCHAR(50) not null,
	product_id			VARCHAR(50) not null,
	quantity			VARCHAR(50) not null,
	order_date			varchar(50) not null,
	order_username		varchar(50) not null,
	order_id			varchar(50) not null,

	FOREIGN KEY (order_username) REFERENCES users(username)
	FOREIGN KEY (order_id) REFERENCES orders(my_id)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
	total_amount		varchar(50) not null, --specify here or down
	total_count			VARCHAR(50) not null,
	my_date 			varchar(50) not null,
	my_id				varchar(50) not null,
	username_id			varchar(50) not null,
	PRIMARY KEY (my_id)
	FOREIGN KEY (username_id) REFERENCES users(username)
);


--checking users might just keep one
INSERT INTO users (username, name, password) VALUES ("user", "Abdulrahman Alsaleh", "p");
INSERT INTO users (username, name, password) VALUES ("testuser", "John doe", "testpass");
INSERT INTO users (username, name, password) VALUES ("abosaleh", "d7me", "pass");
INSERT INTO users (username, name, password) VALUES ("rwrw", "wrwr", "asdffafas");

--kits (start from 0 - 99)
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("0", "Real Madrid Home Kit 01/02", 100, 9, "kit", "Real Madrid's 'Galactico' policy added Ronaldo to their star-studded lineup of Zinedine Zidane, Luis Figo, Roberto Carlos, and Raul Gonzalez, resulting in unprecedented success and numerous trophies during the 2001-2002 season.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("1", "Venezia Home kit 22/23", 60, 8, "kit", "Venezia F.C. collaborates with Bureau Borsche and Kappa for their 2022/23 Serie B season jersey, inspired by '90s shirt styles and Kappa's peak popularity, showcasing the football club's affinity for Italian finesse and luxury fashion.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("2", "AC Milan home 06/07 kit", 80, 19, "kit", "Kaka helped AC Milan win the UEFA Champions League, Serie A, and the Supercoppa Italiana during the 06/07 season, cementing his status as one of the world's best players, while wearing the AC Milan 06/07 home kit");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("3", "Man United home 07/08 kit", 50, 23, "kit", "Manchester United's 2007/08 season was historic, winning three major trophies under Sir Alex Ferguson thanks in large part to Cristiano Ronaldo's outstanding performances, scoring 42 goals and sweeping up multiple Player of the Year awards.");



--balls (start from 100 - 199)
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("100", "AL Rihla WC 2022 ball", 120, 99, "ball", "The 2022 World Cup ball, Al Rihla, took inspiration from different elements of Qatari culture such as language, architecture, boats, and the national flag. During the tournament, Argentina led by Messi emerged as the World Cup champions.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("101", "Jubalani WC 2010 ball", 200, 18, "ball", "The Adidas Jabulani was the official ball for the 2010 World Cup, but its advanced design resulted in widespread controversy, as many players found it unpredictable and difficult to control making it the most controversial ball of all time.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("102", "Brazuca WC 2014 ball", 150, 28, "ball", "The Adidas Brazuca, used in the 2014 World Cup, was inspired by Brazilian culture and colors, featuring a vibrant design and unique graphics on each of its six panels, reflecting the country's passion for football as the host nation.");


--shoes(start from 200)
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("200", "Vintage Puma King SL", 400, 1, "shoes", "The iconic Puma King soccer cleat was worn by Diego Maradona during Argentina's 1986 World Cup victory, featuring a classic design, high-quality construction, and a black and white colorway with the Puma logo.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("201", "Nike Zoom Mercurial Superfly 9", 220, 37, "shoes", "The Zoom Mercurial Superfly 9 from the Lucent Pack, featuring the new Yellow Strike colorway, offers lightning-fast speed and a bold look. Kylian Mbappe is among the top players who wear these cleats.");
INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("202", "PREDATOR ACCURACY +", 280, 140, "shoes", "The latest Predator soccer cleat boasts unbeatable accuracy for shots and passes. With its advanced design and technology, the Predator Accuracy can help players elevate their game and make precise moves on the field. ");

INSERT INTO items (item_id, item_name, item_price, item_stock, item_type, item_desc) VALUES ("203", "Invisible shoes", 280, 140, "shoes", "Whenever you wear it make you invicible");


