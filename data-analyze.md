# 数据结构

```javascript
{
    type: number,               // 数据类别
    message: array[message],    // 未读消息列表
    iqResponse: 作用未知        // type为4时
}
```

# 初始化数据

```javascript
message = [{
    "from": {                  // 信息来源
        "uid": number,         // 用户编号uid: 9位整数
        "name": "姓名",
        "avatar": "头像",      // https://img.bosszhipin.com/beijin/upload/avatar/20210724/*.png
        "company": "公司名称",
        "headImg": 0,
        "certification": 3,
        "source": 0
    },
    "to": {
        "uid": number,
        "name": "用户姓名",
        "avatar": "头像",
        "company": "",
        "headImg": 0,
        "certification": 0,
        "source": 0
    },
    "type": 3,                 // 数据类型, 1为用户发送
    "mid": number,             // 12位整数，作用未知
    "time": number,            // 13位时间戳
    "body": {                  // 消息内容
        "type": 8,             // 消息类型
        "templateId": 1,
        "headTitle": "消息文本",
        "text": null,
        "sound": null,
        "image": null,
        "action": null,
        "articles": [],        // type为16时，文章列表，跳外链
        "notify": null,
        "dialog": null,
        "jobDesc": {
            "title": "jD名称",
            "company": "公司",
            "salary": "薪酬",
            "url": "",
            "jobId": number,
            "positionCategory": "工作性质/类型",
            "experience": "要求年限",
            "education": "要求学历",
            "city": "工作地点",
            "bossTitle": "招聘者类型",
            "boss": { },    // 招聘人员信息
            "lid": "",
            "stage": "融资情况",
            "bottomText": "底部文案",
            "jobLabel": "",
            "iconFlag": 0,
            "content": "员工要求",
            "labels": [ ],   // 标签列表
            "expectId": 0,
            "expectPosition": "",
            "expectSalary": "",
            "partTimeDesc": "",
            "geek": { },     // 未知人员信息
            "latlon": "",
            "distance": ""
        },
        "resume": null,
        "redEnvelope": null,
        "orderDetail": null,
        "hyperLink": null,
        "video": null,
        "interview": null,
        "jobShare": null,
        "resumeShare": null,
        "atInfo": null,
        "sticker": null,
        "chatShare": null,
        "interviewShare": null,
        "listCard": null,
        "starRate": null,
        "frame": null,
        "multiImage": null,
        "extend": null
    },
    "offline": boolean,              // 是否在线
    "received": boolean,
    "pushText": null,              // 如果非系统信息则为消息内容
    "taskId": 0,
    "cmid": 0,
    "status": 1,
    "uncount": 1,
    "pushSound": 0,
    "flag": 0,
    "encryptedBody": null,
    "bizId": null,
    "bizType": null,
    "securityId": "",
    "isSelf": boolean
}]
```

## 字段说明

### message.body.type: number

作用：标记信息类型

值 | 描述 | 是否用户发送 | headText | text | 其他
-- | ---- | ------------ | -------- | ---- | ----
8 |  | - | Boss[xxx]希望就如下职位与您沟通 | - | jobDesc字段值为JD描述
4 | 未知 | - | - | - | -
1 | 聊天信息 | 是 | - | 用户发送的信息 | 与message.pushText值一致
17 | 举报提示 | - | - | 该BOSS招聘过程中若向你收费，请举报。| -
16 | 跳转入口 | - | - | - | articles存在值，跳外链, 如：竞争力分析

message.type | message.body.type | 关联字段 | 说明
------------ | ----------------- | -------- | ----
4 | 16 | message.body.articles | 个人竞争力分析
3 | 1 | message.body.text | 用户发送信息
3 | 4 | message.body.action | -
3 | 8 | message.body.jobDesc | 系统打招呼
3 | 25 | message.body.starRate | 系统让vip评分

