create table raw_temperature (
	id_record serial primary key,
	id_stove integer not null,
	"date" timestamp not null,
	temperature numeric(4, 1) not null
)
