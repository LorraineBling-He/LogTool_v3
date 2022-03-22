function get_term_size() {
        var init_width = 9;
        var init_height = 17;

        var windows_width = $(window).width();
        var windows_height = $(window).height();

        return {
            cols: Math.floor(windows_width / init_width),
            rows: Math.floor(windows_height / init_height),
        }
    }



function websocket() {
    var storage=window.sessionStorage;

    var info;
    var socketURL;
    //首先判断用户是点的下拉选项还是新建的服务器
    //如果是下拉选项，则传递给后台去查相应的服务器信息
    if (storage.length==2){
        console.log("选择的下拉选项是"+storage.getItem('name')+"//");
        // socketURL = "ws://127.0.0.1:8080/webssh/";
        info={"type":"web","name":storage.getItem('name')};
    }
    //如果是新建的服务器，则拼接地址并发送服务器信息给后端
    else{
        // socketURL = ws_scheme + '://' + window.location.host + '/webssh/' + ssh_args ;
        // socketURL = "ws://127.0.0.1:8080/webssh/";
        info=storage;
        console.log(info)
    }
    // let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws"; //获取协议
    let ws_scheme = "ws";
    let ws_port = (window.location.port) ? (':' + window.location.port) : '';  // 获取端口
    socketURL = ws_scheme + '://' + window.location.host + '/webssh/' ;
    document.getElementById('name').innerText=info.name
    //建立连接，并发送服务器信息或者下拉选项的id号给后端
    try{
        sock = new WebSocket(socketURL);
    }
    catch ( e) {
        console.log("连接websocket时异常："+e);
    }
    // sock.send(info);  这里不能直接发送，因为连接websocket需要时间，直接发送会导致在连接成功前就执行此条，就会报错，所以要用onopen函数，确保连接成功后再发送
    //客户端和服务商创建连接成功后自动触发（服务端执行self.accept()）
    sock.onopen =function (event) {
        console.log("websocket连接成功")
        console.log(typeof(JSON.stringify(info)))
        sock.send(JSON.stringify(info));
    }

    var term = new Terminal(
    {
        cols: get_term_size().cols,
        rows: get_term_size().rows,
        useStyle: true,
        cursorBlink: true
    }
    );


    // 打开 websocket 连接, 打开 web 终端
    sock.addEventListener('open', function () {
        // $('#form').addClass('hide');
        // $('#django-webssh-terminal').removeClass('hide');
        term.open(document.getElementById('terminal'));
    });

    // 读取服务器端发送的数据并写入 web 终端
    sock.addEventListener('message', function (recv) {
        var data = JSON.parse(recv.data);
        var message = data.message;
        var status = data.status;
        if (status === 0) {
            term.write(message)
        } else {
            window.location.reload()
        }
    });

    /*
    * status 为 0 时, 将用户输入的数据通过 websocket 传递给后台, data 为传递的数据, 忽略 cols 和 rows 参数
    * status 为 1 时, resize pty ssh 终端大小, cols 为每行显示的最大字数, rows 为每列显示的最大字数, 忽略 data 参数
    */
    var message = {'status': 0, 'data': null, 'cols': null, 'rows': null};

    // 向服务器端发送数据
    term.on('data', function (data) {
        message['status'] = 0;
        message['data'] = data;
        var send_data = JSON.stringify(message);
        sock.send(send_data)
    });



    // 监听浏览器窗口, 根据浏览器窗口大小修改终端大小
    $(window).resize(function () {
        var cols = get_term_size().cols;
        var rows = get_term_size().rows;
        message['status'] = 1;
        message['cols'] = cols;
        message['rows'] = rows;
        var send_data = JSON.stringify(message);
        sock.send(send_data);
        term.resize(cols, rows);
    })
}




window.onload=websocket()