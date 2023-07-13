create table locations (
	id_stove integer primary key,
	country varchar not null,
	province varchar not null
);

create table raw_temperature (
	id_record serial primary key,
	id_stove integer not null references locations(id_stove),
	"date" timestamp not null,
	temperature numeric(4, 1) not null
);

create table temperature (
	"date" date primary key,
	stoves_num integer not null,
	work_num integer not null,
	work_time numeric(8,2) not null
);