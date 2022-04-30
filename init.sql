create table file
(
    id              bigint unsigned auto_increment
        primary key,
    folder_location varchar(255) null,
    file_path       varchar(255) null,
    constraint id
        unique (id)
);

create table page
(
    id          int auto_increment
        primary key,
    file_id     int           null,
    file_path   varchar(255)  null,
    page        int           null,
    orientation int           null,
    score       int default 0 null,
    sheet       varchar(255)  null,
    done_by     varchar(255)  null,
    status      varchar(255)  null
);

