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
    publishDate date comment '发布时间',
    detail mediumtext comment '详情',
    typeID nvarchar(100) comment '招标类型, type3类型',
    -- 新增字段
    biddingNum nvarchar(100) comment '标段编号',
    reviewType nvarchar(100) comment "评审方式"
);

-- 关键词库
create table searchKey(
    joinID nvarchar(100) primary key comment '关键词ID',
    searchKey text comment '关键词',
    foreignID nvarchar(100) comment '外键ID',
    createTime datetime comment '创建时间',
    tag int comment '用户1, 招标 2, 中标 3, 企业数据库 4, 项目经理 5'
);

-- 招标公告关键词库
-- create table tenderSearchKey(
--     joinID nvarchar(100) primary key comment '关键词ID',
--     searchKey text comment '关键词',
--     tenderID nvarchar(100) comment '商品ID',
--     createTime datetime comment '创建时间',
--     tag int comment '招标1, 中标 2, 企业数据库 3'
-- );

-- 一级分类
create table Type1(
    typeID nvarchar(100) primary key comment '类型ID',
    typeName nvarchar(100) comment '类型名称'
);

-- 二级分类
create table Type2(
    typeID nvarchar(100) primary key comment '类型ID',
    typeName nvarchar(100) comment '类型名称',
    superTypeID nvarchar(100) comment '上级类型名称'
);

-- 三级分类
create table Type3(
    typeID nvarchar(100) primary key comment '类型ID',
    typeName nvarchar(100) comment '类型名称',
    superTypeID nvarchar(100) comment '上级类型名称'
);

-- userInfo
create table userInfo
(
    userID nvarchar(100) primary key comment '主键',
    userName nvarchar(100) comment '用户名，昵称',
    companyName nvarchar(100) comment '公司名称',
    jobPosition nvarchar(100) comment '职位',
    password nvarchar(100) comment '密码',
    info text comment '个人简介，个性签名等',
    portraitPath text comment '头像路径',
    account float default 0 comment '账户',
    tel nvarchar(20) comment '手机号码',
    email nvarchar(100) comment '电子邮箱',
    gender smallint comment '性别',
    createTime datetime comment '创建时间',
    deviceID nvarchar(100) comment '设备号',
    code nvarchar(100) comment '邀请码',
    provinceID nvarchar(100) default '-1' comment '省份ID',
    cityID nvarchar(100) default '-1' comment '城市ID'
);

-- 管理员信息
create table adminInfo(
    adminID nvarchar(100) primary key comment '管理员ID',
    adminName nvarchar(100) comment '管理员用户名',
    tel nvarchar(100) comment '手机号',
	adminPW nvarchar(100) comment '管理员密码'
);

-- token
create table token
(
    tokenID nvarchar(100) primary key comment '根据用户ID和时间生成的token',
    userID nvarchar(100) comment '用户ID',
    createtime datetime comment 'token被创建的时间',
    validity long comment 'token的有效时长'
);

-- 收藏表
create table Favorite
(
	favoriteID nvarchar(100) primary key comment '收藏的ID',
    tenderID nvarchar(100) comment '收藏商品的ID',
    userID nvarchar(100) comment '收藏者的ID',
    createTime datetime comment '收藏的时间',
    tag nvarchar(100) comment '收藏标志,为中标还是招标, 1 招标, 2 中标',
);

-- sms code
create table SmsCode(
    codeID nvarchar(100) primary key comment '短信验证码ID',
    tel nvarchar(20) comment '手机号',
    code nvarchar(100) comment '验证码',
    createTime datetime comment '创建时间'
);

--用户注册IP地址
create table UserIP(
    joinID nvarchar(100) primary key comment '注册ID',
    userID nvarchar(100) comment '用户ID',
    ipAddress nvarchar(100) comment 'ip地址',
    createTime datetime comment '注册时间'
);

ALTER TABLE province CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE city CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tender CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE searchKey CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- ALTER TABLE TenderSearchKey CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Type1 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Type2 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Type3 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Favorite CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE UserIP CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE UserInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE Token CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE SmsCode CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE adminInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table city add constraint city_FK_province foreign key(provinceID) references province(provinceID);
alter table tender add constraint tender_FK_city foreign key(cityID) references city(cityID);
alter table Type2 add constraint type2_FK_type1 foreign key(superTypeID) references Type1(typeID);
alter table Type3 add constraint type3_FK_type2 foreign key(superTypeID) references Type2(typeID);
alter table UserIP add constraint ip_FK_user foreign key(userID) references UserInfo(userID);
-- alter table tenderSearchKey add constraint tenderSearchKey_FK_tender foreign key(tenderID) references tender(tenderID);