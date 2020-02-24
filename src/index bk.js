// 引入express
const express = require('express');
const url = require('url');
const bodyParser = require('body-parser');
const multer = require('multer');
const upload = multer({dest: 'tmp_uploads/'});
const fs = require('fs');
const session = require('express-session');
const moment = require('moment-timezone');
const db = require(__dirname + '/db-connect');


// 建立web serber 物件
const app = express();

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.use(session({
    saveUninitialized: false,
    resave: false,
    secret: 'ksdhkasjhfjs',
    cookie: {
        maxAge: 1200000
    }
}));


// 路由從這裡開始

//首頁
app.get('/', (req, res) => {
    res.render('chat')
});

//使用者輸入行為
app.get('/action', (req, res) => {
    res.render('chat', {
        title: 'action'
    });
});

app.post('/action', (req, res) => {
    const output = {
        success: false,   //是否成功新增
        code: 400,  // http 狀態
        results: {}, //將results丟回來 先給空物件
        errorMsg: '', //錯誤訊息
        body: req.body,  //除錯 將送過來的資料原原本本得再送給前端，讓使用者清楚看到自己哪個欄位需要修改
        
    };
    const sql1 = "INSERT INTO `user input`(`action`) VALUES (?)";
    db.query(sql1, [
        req.body.action,
    ], (error, results) => {
        output.results = results;
        if (results.affectedRows === 1) {
            output.success = true;
            output.code = 200;
        } else {
            output.code = 420;
            output.errorMsg = "資料新增失敗";
        }
        res.json(output)
    })
});


// 404 要在 routes 的最後面
app.use((req, res) => {
    res.type('text/plain');
    res.status(404);
    res.send('404 !!!!!!!!!!');
});

//偵聽server
app.listen(3002, () => {
    console.log('3002 travel server start');
});
