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
	responsiblePersonID nvarchar(100) comment '负责人ID',
	auditorPushedTime datetime comment '审核人推送时间',
	auditorID nvarchar(100) comment '审核人ID',
	bossPushedTime datetime comment '审定人推送时间',
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

create table fileInfo(
	fileID nvarchar(100) primary key comment '文件ID',
	fileName nvarchar(100) comment '文件名',
	userID nvarchar(100) comment '创建者',
	createTime datetime comment '创建时间',
	superID nvarchar(100) default '-1' comment '上级ID',
	isDirectory boolean default false comment '是否是文件夹',
	privateLevel int default 0 comment '私密等级, 0 代表public',
	filePath nvarchar(1000) comment '在OSS 上的名称',
	areaID nvarchar(100) comment '区域ID',
	tag int comment '合同类型'
);

-- 部门表
create table department(
	departmentID nvarchar(100) primary key comment '主键',
	departmentName nvarchar(100) comment '部门名称',
	createTime datetime comment '创建时间'
);
-- 部门下的区域
create table departmentArea(
	areaID nvarchar(100) primary key comment '主键',
	areaName nvarchar(100) comment '区域名称',
	createTime datetime comment '创建时间',
	departmentID nvarchar(100) comment '部门ID'
);

-- 权限表
create table departmentRight(
	rightID nvarchar(100) primary key comment '权限ID',
	areaID nvarchar(100) comment '区域ID',
	userID nvarchar(100) comment '用户ID',
	tag int default 0 comment '0 代表department,  1 代表areaID'
);

-- 合同管理相关表
-- 项目类型表
create table projectType(
	projectTypeID int primary key comment '项目类型ID',
	projectTypeName nvarchar(100) comment '项目类型名称'
);

-- 承接方式表
create table projectOperationType(
	operationTypeID int primary key comment '承接方式ID',
	operationTypeName nvarchar(100) comment '承接方式'
);

-- 合同
create table contract(
	contractID nvarchar(100) primary key comment '合同ID',
	title nvarchar(1000) comment '工程名称',
	serialNumber nvarchar(100) comment '流水号',
	createTime datetime comment '合同签订日期',
	projectTypeName nvarchar(100) comment '项目类型',
	operationTypeName nvarchar(100) comment '承接方式',
	contractPrice double comment '合同金额（万元）',
	contractWorkContent nvarchar(1000) comment '合同工作内容（工程量）',
	contractor nvarchar(1000) comment '承包单位',
	responsiblePerson nvarchar(1000) comment '项目负责人',
	biddingDate datetime comment '中标通知书日期',
	contractRecordDate datetime comment '合同备案日期',
	contractKeepingDeprt nvarchar(1000) comment '合同保管部门',
	archiveInfo nvarchar(1000) comment '合同归档情况',
	contractDuration nvarchar(1000) comment '合同工期（开竣工日期）'
);

-- 合同进度表
create table contractProjectProcess(
	processID nvarchar(100) primary key comment '合同进度ID',
	createTime datetime comment '时间',
	processRate int comment '进度值',
	description text comment '描述',
	userName nvarchar(100) comment '汇报人',
	contractID nvarchar(100) comment '合同ID',
	resultSubmissionDate nvarchar(100) comment '提交成果日期',
	resultReviewDate nvarchar(100) comment '成果审查合格日期'
);

-- 决算进度
create table contractFinalAccounts(
	accountID nvarchar(100) primary key comment '进度ID',
	submittalDate nvarchar(100) comment '送审日期',
	submittalPrice double comment '送审金额（万元）',
	authorizedDate datetime comment '审定日期',
	authorizedPrice double comment '审定金额（万元）',
	cumulativeInvoicePrice double comment '累计开票金额（万元）',
	cumulativePayPrice double comment '累计付款金额（万元）',
	balance double comment '余款（万元）',
	unPaidBalance double comment '未结算金额',
	contractID nvarchar(100) comment '合同ID'
);

-- 突发事件
create table contractEmergency(
	emergencyID nvarchar(100) primary key comment '突发事件ID',
	createTime datetime comment '创建时间',
	description text comment '描述',
	resolvent text comment '解决方法',
	contractID nvarchar(100) comment '合同ID'
);

create table operationRight(
	rightID nvarchar(100) primary key comment '',
	userID nvarchar(100) comment '',
	operatorTag int comment '',

);

-- 权限类型
create table rightType(
	rightTypeID nvarchar(100) primary key comment '权限类型ID',
	rightTypeName nvarchar(100) comment '权限类型名称',
	createTime datetime comment '创建时间'
);

-- 用户权限表
create table userRight(
	rightID nvarchar(100) primary key comment '权限ID',
	rightTypeID nvarchar(100) comment '区域ID',
	userID nvarchar(100) comment '用户ID',
	createTime datetime comment '创建时间'
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
ALTER TABLE fileInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE department CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE departmentArea CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE departmentRight CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE contract CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE projectType CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE projectOperationType CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE contractProjectProcess CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE contractFinalAccounts CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE contractEmergency CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE rightType CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE userRight CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


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
alter table departmentArea add constraint area_FK_department foreign key(departmentID) references department(departmentID);
-- alter table contract add constraint contract_FK_type foreign key(projectTypeID) references projectType(projectTypeID);
-- alter table contract add constraint contract_FK_o_type foreign key(operationTypeID) references projectOperationType(operationTypeID);
alter table contractProjectProcess add constraint process_FK_contract foreign key(contractID) references contract(contractID);
alter table contractFinalAccounts add constraint account_FK_contract foreign key(contractID) references contract(contractID);
alter table contractEmergency add constraint emergency_FK_contract foreign key(contractID) references contract(contractID);