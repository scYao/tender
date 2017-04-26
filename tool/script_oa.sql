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
	operatorPersonPushedTime datetime comment '经办人推送时间',
	responsiblePersonPushedTime datetime comment '负责人推送时间',
	auditorPushedTime datetime comment '审核人',
	state int comment 'boss决定是否投标, 0 未确定, 1 投, 2 放弃',
	step int comment '0表示未开始，１表示正在进行中，２表示已经完成，３表示历史记录',
	tag int default 0 comment '0 tender表中的数据, 1 自定义标数据',
	tenderID nvarchar(100) comment '哪一个标, 不设外键',
	-- 经办人填写的 在投标中详情中的字段
	projectManagerName nvarchar(100) comment '项目经理姓名',
	openedDate date comment '开标时间',
	openedLocation text comment '开标地点',
	ceilPrice double comment 'B 最高限价',
	tenderInfoDescription text comment '项目信息备注',
	-- 老板填写的报价字段
	quotedPrice double comment '报价,定价',
	quotedDate date comment '报价时间',
	quotedDescription text comment '报价备注',
	-- 投标已完成详情字段
	averagePrice double comment 'A 平均价',
	benchmarkPrice double comment 'C(评标基准价)',
	K1 double comment 'K1 值',
	K2 double comment 'K2 值',
	Q1 double comment 'Q1 值',
	Q2 double comment 'Q2 值',
	deductedRate1 double comment '啟勋下浮率',
	deductedRate2 double comment '下浮率',
	workerName nvarchar(100) comment '开标人',
	candidateName1 nvarchar(100) comment '候选人1',
	candidatePrice1 double comment '候选人1报价',
	candidateName2 nvarchar(100) comment '候选人2',
	candidatePrice2 double comment '候选人2报价',
	candidateName3 nvarchar(100) comment '候选人3',
	candidatePrice3 double comment '候选人3报价'
	-- 新增的进行中的详情
	tenderCompanyName nvarchar(100) comment '投标单位',
	projectType nvarchar(100) comment '项目类型',
	workContent nvarchar(100) comment '工作内容',
	deposit double comment '投标保证金',
	planScore double comment '方案评分',
	tenderType nvarchar(100) comment '评标方法',
	-- 新增报名截止时间
	deadline date comment '报名截止日期',
	winbidding boolean default 0 comment '是否中标',
	-- 新增13项
	tenderee text comment '招标人',
	tenderProxy text comment '招标代理',
	tenderer text comment '投标人',
	constructionLocation text comment '建设地点',
	plannedProjectDuration text comment '计划工期',
	answerDeadline date comment '答疑截止日期',
	tenderDeadline date comment '投标截止日期',
	attender text comment '开标人',
	companyAchievement text comment '企业业绩要求',
	pmAchievement text comment '项目经理业绩要求'
);

create table quotedPrice(
	quotedID nvarchar(100) primary key comment '报价ID',
	tenderID nvarchar(100) comment '标段ID',
	userID nvarchar(100) comment '用户ID',
	quotedPrice double comment '预估价',
	-- 定价 变为报价
	price double comment '报价',
	costPrice double comment '成本价',
	createTime datetime comment '创建时间',
	description text comment '备注',
	-- 增加最高限价，定额价
	ceilingPrice double comment '最高限价',
	fixedPrice double comment '定额价'
);

-- 领导批注
create table tenderComment(
	commentID nvarchar(100) primary key comment '领导批注ID',
	userID nvarchar(100) comment '批注人ID',
    createTime datetime comment '批注时间',
    description text comment '批注内容',
    tenderID nvarchar(100) comment 'tenderID'
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
	createTime datetime comment '创建时间',
	typeID int default 0 comment '只有标书涉及此字段, 1 商务标,  2 技术标',
	userName nvarchar(100) comment '只有标书涉及此字段, 开标人',
	userType int comment '只有标书涉及此字段, 上传人的类型'
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
    tag int comment '消息类型, 1 推送消息',
    state int comment '是否已读，0未读, 1已读'
);


-- 招标资讯
create table news(
	newsID nvarchar(100) primary key comment '资讯ID',
	title nvarchar(100) comment '标题',
	content text comment '正文内容',
	createTime datetime comment '创建时间'
);

-- 订阅
create table subscribedKey(
	subscribedID nvarchar(100) primary key comment '订阅ID',
	userID nvarchar(100) comment '用户ID',
	keywords nvarchar(100) comment '关键字',
	createTime datetime comment '创建时间',
	frequency int comment '推送频率',
	pushType int comment '推送方式'
);

ALTER TABLE pushedTenderInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE operator CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE operation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE biddingDocPushInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE customizedTender CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE tenderComment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE quotedPrice CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE news CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE subscribedKey CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table pushedTenderInfo add constraint push_FK_user foreign key(userID) references UserInfo(userID);
alter table operation add constraint operation_FK_operator foreign key(operatorID) references operator(operatorID);
alter table customizedTender add constraint customized_T_FK_operator foreign key(userID) references UserInfo(userID);
alter table message add constraint message_FK_T_user foreign key(toUserID) references userInfo(userID);
alter table message add constraint message_FK_F_user foreign key(fromUserID) references userInfo(userID);
alter table tenderComment add constraint comment_FK_F_user foreign key(userID) references userInfo(userID);
alter table quotedPrice add constraint quote_FK_F_user foreign key(userID) references userInfo(userID);
alter table quotedPrice add constraint quote_FK_tender foreign key(tenderID) references tender(tenderID);
alter table tenderComment add constraint comment_FK_user foreign key(userID) references userInfo(userID);
alter table subscribedKey add constraint subscribed_FK_user foreign key(userID) references userInfo(userID);