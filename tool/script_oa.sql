-- 招标信息推送流
-- 经办人 : operation
-- 负责人 : responsiblePerson
-- 审核人: auditor
-- 审定人 : boss
-- 
create table pushedTenderInfo(
	pushedID nvarchar(100) primary key comment '推送ID',
	userID nvarchar(100) comment '推送人',
	createTime datetime comment '推送时间',
	responsiblePersonPushedTime datetime comment '负责人推送时间',
	auditorPushedTime datetime comment '审核人',
	state int comment 'boss决定是否投标, 0 未确定, 1 投, 2 放弃',
	step int comment '0表示未开始，１表示正在进行中，２表示已经完成，３表示历史记录',
	tenderID nvarchar(100) comment '哪一个标, 不设外键',
	projectManagerName nvarchar(100) comment '项目经理姓名',
	openedDate date comment '开标时间',
	openedLocation text comment '开标地点',
	ceilPrice float comment '最高限价',
	tenderInfoDescription text comment '项目信息备注',
	quotedPrice float comment '报价',
	quotedDate date comment '报价时间',
	quotedDescription text comment '报价备注'
);

-- 领导批注
create table tenderComment(
	commentID nvarchar(100) primary key comment '领导批注ID',
	userID nvarchar(100) comment '批注人ID',
    createTime datetime comment '批注时间',
    description text comment '批注内容'
);

-- 经办人表
create table operator(
	operatorID nvarchar(100) primary key comment '经办人ID, 每个项目一个经办人, 一个用户可以充当多个经办人',
	userID nvarchar(100) comment '用户', 
	tenderID nvarchar(100) comment '经办的项目, 不设外键',
	state int comment '负责人分配好经办人, 老板是否同意 0 未操作, 1 同意, 2 驳回'
);

-- 报名  1
-- 打保证金 2
-- 制作标书 3
-- 现场投标 4
create table operation(
	operationID nvarchar(100) primary key comment '业务ID',
	tag int comment '业务类型',
	operatorID nvarchar(100) comment '经办人ID, 不是用户ID, 需要通过经办人ID知道哪个项目',
	state int comment '1 成功, 2 失败',
	description text comment '备注',
	createTime datetime comment '创建时间'
);

-- 标书推送流
create table biddingDocPushInfo(
	pushedID nvarchar(100) primary key comment '推送ID',
	userID nvarchar(100) comment '推送人',
	createTime datetime comment '推送时间',
	responsiblePersonPushedTime datetime comment '负责人推送时间',
	auditorPushedTime datetime comment '审核人',
	state int comment 'boss决定是否投标, 0 未确定, 1 投, 2 放弃',
	tenderID nvarchar(100) comment '哪一个标, 不设外键'
);

-- 用户自定义的招标信息表
-- 文件上传，保存到imgPath 表
create table customizedTender(
	tenderID nvarchar(100) primary key comment '招标信息ID',
	title text comment '标题',
	createTime datetime comment '创建时间',
	userID nvarchar(100) comment '用户', 
	url text comment '链接'
);

-- 未读消息
create table message(
    messageID nvarchar(100) primary key comment '消息ID',
    foreignID nvarchar(100) comment '外键ID',
    fromUserID nvarchar(100) comment '主动回复人ID',
    toUserID nvarchar(100) comment '被动回复人ID',
    description text comment '回复的文本内容',
    createTime datetime comment '回复时间',
    tag int comment '消息类型, 1 推送消息'
);

ALTER TABLE pushedTenderInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE operator CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE operation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE biddingDocPushInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE customizedTender CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tenderComment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table pushedTenderInfo add constraint push_FK_user foreign key(userID) references UserInfo(userID);
alter table operation add constraint operation_FK_operator foreign key(operatorID) references operator(operatorID);
alter table customizedTender add constraint customized_T_FK_operator foreign key(userID) references UserInfo(userID);
alter table message add constraint message_FK_T_user foreign key(toUserID) references userInfo(userID);
alter table message add constraint message_FK_F_user foreign key(fromUserID) references userInfo(userID);
alter table tenderComment add constraint comment_FK_F_user foreign key(userID) references userInfo(userID);