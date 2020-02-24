// 引入express
const express = require('express');
const url = require('url');
const bodyParser = require('body-parser');
const multer = require('multer');
const upload = multer({ dest: 'tmp_uploads/' });
const fs = require('fs');
const session = require('express-session');
const moment = require('moment-timezone');
// const db = require(__dirname + '/db-connect');


// 建立web serber 物件
const app = express();
// 引入pthon-shell套件
let { PythonShell } = require('python-shell')
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: false }));
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
    res.render('plan')
});


//使用者輸入行為
app.get('/action', (req, res) => {
    res.render('plan', {
        title: 'action'
    });
});

app.post('/action', pythonProcess)
function pythonProcess(req, res) {
    let options = {
        args:
            [
                req.body.action,
            ]
    }
    PythonShell.run('pyfile/action.py', options, (err, data) => {
        if (err) res.send(err)
        const parsedString = JSON.parse(data)
        console.log(parsedString)
        // console.log(`views: ${parsedString.views},day:${parsedString.day}`)
        console.log(`views: ${parsedString.views},day:${parsedString.day},recommend:${parsedString.recommend},url:${parsedString.url}`)
        const output ={}
        output.vie = parsedString.views
        output.day = parsedString.day
        output.recommend = parsedString.recommend
        output.url = parsedString.url
        output.gtoken =parsedString.gtoken
        res.json( output )
    })

}




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
