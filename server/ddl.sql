create table raw_temperature (
	id_record serial primary key,
	id_stove integer not null,
	"date" timestamp not null,
	temperature numeric(4, 1) not null
);

create table temperature (
	"date" date primary key,
	stoves_num integer not null,
	work_num integer not null,
	work_time numeric(8,2) not null
);
