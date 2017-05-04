-- 公众号接口中参数accseeToken
create table accessToken(
	accessTokenID nvarchar(200) primary key comment '获取到的凭证',
	validity int comment '凭证有效时间，单位：秒',
    createTime datetime comment '创建时间'
);

-- 推送列表
create table weChatPush(
    pushedID nvarchar(100) primary key comment '推送ID',
    tenderID nvarchar(100) comment '招标公告ID',
    toUserID nvarchar(100) comment '推送到用户ID',
    createTime datetime comment '创建时间'
);


--　推送历史列表
create table weChatPushHistory(
    pushedID nvarchar(100) primary key comment '推送ID',
    tenderID nvarchar(100) comment '招标公告ID',
    toUserID nvarchar(100) comment '推送到用户ID',
    createTime datetime comment '创建时间',
    publishTime datetime comment '推送时间'
);



ALTER TABLE accessToken CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE weChatPush CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE weChatPushHistory CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;