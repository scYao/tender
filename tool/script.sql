CREATE DATABASE tender DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER DATABASE tender CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

use tender;

create table province(
    provinceID nvarchar(100) comment '省份ID',
	provinceName nvarchar(1000) comment '省份名称',
	primary key(provinceID)
);

create table city(
	cityID nvarchar(100) comment '城市ID',
	cityName nvarchar(1000) comment '城市名称',
	provinceID nvarchar(100) comment '省份ID',
	primary key (cityID)
);

create table tender(
    tenderID nvarchar(100) primary key comment 'id',
    title text comment '标题',
    cityID nvarchar(100) comment '城市',
    location text comment '具体地址',
    url text comment '详情链接',
    datetime datetime comment '发布时间',
    detail mediumtext comment '详情'
);

-- 关键词库
create table MerchandiseSearchKey(
    joinID nvarchar(100) primary key comment '关键词ID',
    searchKey text comment '关键词',
    merchandiseID nvarchar(100) comment '商品ID',
    createTime datetime comment '创建时间'
);

ALTER TABLE province CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE city CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tender CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE MerchandiseSearchKey CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table city add constraint city_FK_province foreign key(provinceID) references province(provinceID);
alter table tender add constraint tender_FK_city foreign key(cityID) references city(cityID);