-- 
-- 资质证书编号，资质证书图片，类型号 1
-- 营业执照，注册号 图片      类型号 2
-- 安全生产许可证 图片       类型号 3
-- 信用手册       图片       类型号 4
create table company(
	companyID nvarchar(100) primary key comment '公司ID',
	companyName nvarchar(100) comment '公司名称，单位名称',
	newArchiveID nvarchar(100) comment '新档案号',
	registerArea nvarchar(100) comment '注册地区',
	companyAreaType nvarchar(100) comment '企业地点类别',
	certificateID nvarchar(100) comment '证书编号',
	certificationAuthority nvarchar(100) comment '资质证书, 发证机关',
	legalRepresentative nvarchar(100) comment '法定代表人',
	enterprisePrincipal nvarchar(100) comment '企业负责人',
	technologyDirector nvarchar(100) comment '技术负责人',
	remarks nvarchar(100) comment '备注',
	licenseID nvarchar(100) comment '营业执照, 注册号',
	registeredCapital float comment '注册资本',
	companyType nvarchar(100) comment '公司类型',
	foundingTime date comment '公司成立时间',
	businessTermFrom date comment '营业期限从',
	businessTermEnd date comment '营业期限到',
	safetyProductionPermitID nvarchar(100) comment '安全生产许可证ID',
	safePrincipal nvarchar(100) comment '主要负责人',
	businessScope nvarchar(100) comment '许可范围',
	safeAuthority nvarchar(100) comment '安全生产许可证, 发证机关',
	safeFromDate date comment '安全生产许可证, 发证时间',
	safeEndDate date comment '有效期',
	creditBookID nvarchar(100) comment '信用手册ID',
	creditScore1 float comment '信用分，最近半年',
	creditScore2 float comment '信用分，前一个半年',
	creditEndDate date comment '信用手册，有效期',
	creditAuthority nvarchar(100) comment '信用手册, 发证单位',
	creditAddress nvarchar(100) comment '信用手册， 详细地址',
	creditWebSet nvarchar(500) comment '信用手册, 企业网址',
	creditContact nvarchar(100) comment '信用手册, 联系人',
	creditNjAddress nvarchar(100) comment '信用手册, 驻宁地址',
	creditNjPrincipal nvarchar(100) comment '信用手册, 驻宁负责人',
	creditNjTech nvarchar(100) comment '信用手册, 驻宁技术负责人',
	creditFinancialStaff nvarchar(100) comment '信用手册, 驻宁财务负责人',
	companyBrief text comment '公司简介'
);

-- 资质等级表
create table qualificationGrade(
	qualificationID nvarchar(100) primary key comment '资质ID',
	qualificationName nvarchar(100)
);

create table companyQualification(
	joinID nvarchar(100) primary key comment '组合ID',
	companyID nvarchar(100) comment '公司ID',
	qualificationID nvarchar(100) comment '资质ID' 
);

create table imgPath
(
    imgPathID nvarchar(100) primary key comment '图片主键',
    path text comment '照片的路径',
    foreignID nvarchar(100) comment '照片对应的商品',
    tag int comment '区别同一张表中不同的图片，比如公司表中，证书图片N张，信用手册图片N张等等'
);

-- 项目经理表
create table projectManager(
	managerID nvarchar(100) primary key comment '项目经理ID',
	managerName nvarchar(100) comment '项目经理姓名',
	gender smallint comment '0 female, 1 male',
	positionalTitles nvarchar(100) comment '职称',
	post nvarchar(100) comment '职务',
	safetyAssessment nvarchar(100) comment '安全生产考核证号',
	safeEndDate date comment '有效期',
	safeAuthority nvarchar(100) comment '安全生产考核证号, 发证机关',
	safeFromDate date comment '发证时间',
	companyID nvarchar(100) comment '企业ID'
);

-- 项目经理证
create table managerLicense(
	licenseID nvarchar(100) primary key comment '项目经理证ID',
	licenseName nvarchar(100) comment '证书名称',
	licenseNum nvarchar(100) comment '证件号',
	grade nvarchar(100) comment '专业等级',
	authority nvarchar(100) comment '发证机关',
	licenseDate date comment '发证日期',
	licenseEndDate date comment '有效期',
	managerID nvarchar(100) comment '项目经理ID',
	tag smallint comment '0 项目经理证, 1 注册建造师证件'
);

-- 项目经理业绩
create table managerAchievement(
	achievementID nvarchar(100) primary key comment '项目ID',
	projectName nvarchar(100) comment '项目名称',
	companyName nvarchar(100) comment '建设单位, 即甲方',
	winBiddingDate date comment '中标时间',
	price float comment '中标金额(万元)',
	projectManagerName nvarchar(100) comment '项目经理',
	managerID nvarchar(100) comment '项目经理ID',
	tag smallint comment '0 招标网提供的信息，1 自己填写的信息'
);

-- 企业业绩
create table companyAchievement(
	achievementID nvarchar(100) primary key comment '项目ID',
	projectName nvarchar(100) comment '项目名称',
	companyName nvarchar(100) comment '建设单位, 即甲方',
	winBiddingDate date comment '中标时间',
	price float comment '中标金额(万元)',
	projectManagerName nvarchar(100) comment '项目经理',
	managerID nvarchar(100) comment '项目经理ID, 此字段不设外键, 防止有项目经理不在表中',
	companyID nvarchar(100) comment '企业ID',
	tag smallint comment '0 场内项目业绩, 1 自己填写的信息' 
);

-- 不良行为
create table delinquenentConduct(
	conductID nvarchar(100) primary key comment '不良行为ID',
	conductName nvarchar(100) comment '不良行为',
	consequence nvarchar(100) comment '情节后果',
	penaltyType nvarchar(100) comment '处罚种类',
	penaltyAuthority nvarchar(100) comment '处罚机关',
	penaltyDate date comment '处理时间',
	publicDateFrom date comment '公示期限始',
	publicDateEnd date comment '公示期限止',
	companyID nvarchar(100) comment '企业ID'
);

-- 资质等级第一级
create table certificationGrade1(
	gradeID nvarchar(100) primary key comment '资质等级ID',
	gradeName nvarchar(100) comment '资质等级名称'
);

-- 资质等级第二级
create table certificationGrade2(
	gradeID nvarchar(100) primary key comment '资质等级ID',
	gradeName nvarchar(100) comment '资质等级名称',
	superiorID nvarchar(100) comment '上一级ID'
);

-- 资质等级第三级
create table certificationGrade3(
	gradeID nvarchar(100) primary key comment '资质等级ID',
	gradeName nvarchar(100) comment '资质等级名称',
	superiorID nvarchar(100) comment '上一级ID'
);

-- 资质等级第四级
create table certificationGrade4(
	gradeID nvarchar(100) primary key comment '资质等级ID',
	gradeName nvarchar(100) comment '资质等级名称',
	superiorID nvarchar(100) comment '上一级ID'
);


-- 中标公示
create table winBiddingPub(
	biddingID nvarchar(100) primary key comment '中标公示ID',
	title nvarchar(100) comment '标题',
	publicDate date comment '发布时间',
	biddingNum nvarchar(100) comment '标段编号'
);

-- 候选人表
-- 其中候选人ID非companyID, 因为同一个公司可能出现在多个项目候选人里面
-- 候选公司ID, 数据爬取完后, 会进行一遍搜索, 查看是否在企业数据库中有记录, 没有记录为-1
create table candidate(
	candidateID nvarchar(100) primary key comment '候选人ID',
	candidateName nvarchar(100) comment '候选人名称',
	companyID nvarchar(100) default '-1' comment '候选人公司ID, 不设外键',
	price float comment '报价',
	ranking int comment '排名',
	managerName nvarchar(100) comment '项目负责人',
	managerID nvarchar(100) comment '项目负责人ID',
	biddingID nvarchar(100) comment '中部公示ID'
);


ALTER TABLE company CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE qualificationGrade CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE companyQualification CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE projectManager CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE managerLicense CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE managerAchievement CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE companyAchievement CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE delinquenentConduct CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE certificationGrade1 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE certificationGrade2 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE certificationGrade3 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE certificationGrade4 CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE winBiddingPub CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE candidate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table companyQualification add constraint company_q_FK_company foreign key(companyID) references company(companyID);
alter table companyQualification add constraint company_q_FK_qualification foreign key(qualificationID) references qualificationGrade(qualificationID);
alter table managerLicense add constraint manager_l_FK_manager foreign key(managerID) references projectManager(managerID);
alter table managerAchievement add constraint manager_a_FK_manager foreign key(managerID) references projectManager(managerID);
alter table certificationGrade2 add constraint grade_2_FK_1 foreign key(superiorID) references certificationGrade1(gradeID);
alter table certificationGrade3 add constraint grade_3_FK_2 foreign key(superiorID) references certificationGrade2(gradeID);
alter table certificationGrade4 add constraint grade_4_FK_3 foreign key(superiorID) references certificationGrade3(gradeID);
alter table projectManager add constraint manager_FK_company foreign key(companyID) references company(companyID);
alter table companyAchievement add constraint company_a_FK_company foreign key(companyID) references company(companyID);
alter table delinquenentConduct add constraint delinquenent_FK_company foreign key(companyID) references company(companyID);
alter table candidate add constraint candidate_FK_win foreign key(biddingID) references winBiddingPub(biddingID);
