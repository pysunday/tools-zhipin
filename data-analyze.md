# 开启日志打印

链接加上`&debug=true`

# 数据结构

```javascript
{
    type: number,               // 数据类别
    message: array[message],    // 未读消息列表
    iqResponse: 作用未知        // type为4时
}
```

type | 关联字段 | 说明
---- | -------- | ----
6 | messageRead | 消息被查看
1 | messages | 消息
4 | iqResponse | -
5 | messageSync | -

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

### message.type与message.body.type

作用：标记信息类型

message.type | message.body.type | 关联字段 | 说明
------------ | ----------------- | -------- | ----
1 | 1 | message.body.text | 用户发送信息(实时)
1 | 4 | message.body.action.aid == 32 | 交换微信
1 | 7 | message.body.dialog | 是否发简历
1 | 20 | message.body.sticker.image | 表情
4 | 7 | message.body.dialog | 设置boss优先提醒
4 | 16 | message.body.articles | 个人竞争力分析
4 | 17 | message.body.templateId == 3 | 该BOSS招聘过程中若向你收费，请举报。
3 | 1 | message.body.text | 用户发送信息(历史)
3 | 4 | message.body.action.aid == 51 | -
3 | 8 | message.body.jobDesc | 系统打招呼
3 | 15 | message.body.articles | 系统通知
3 | 16 | message.body.templateId == 201 | 满意Ta的职位推荐吗？
3 | 25 | message.body.starRate | 系统让vip评分

