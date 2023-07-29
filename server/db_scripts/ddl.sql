create table districts (
	id_district integer primary key,
	district varchar not null,
	country varchar not null
);

create table raw_temperature (
	id_stove integer not null,
	"date" timestamp not null,
	temperature numeric(4, 1) not null,
	primary key (id_stove, "date")
);

create table temperature (
	"date" date not null,
	stoves_num integer not null,
	work_num integer not null,
	work_time numeric(8,2) not null,
	id_district integer references districts(id_district),
	primary key (id_district, "date")
);

create table locations (
	id_stove integer primary key,
	id_district integer references districts(id_district)
);