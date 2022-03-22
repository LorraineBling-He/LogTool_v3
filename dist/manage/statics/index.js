

function get_connect_info() {
    var name = $.trim($('#name').val());
    var host = $.trim($('#host').val());
    var port = $.trim($('#port').val());
    var user = $.trim($('#user').val());
    var auth = $("input[name='auth']:checked").val();
    var pwd = $.trim($('#password').val());
    var password = window.btoa(pwd); //加密密码传输
    var dockerName = $.trim($('#dockerName').val());
    var ssh_key = null;
    let sshkey_filename = '';
    if (auth === 'key') {
        var pkey = $('#pkey')[0].files[0];
        var csrf = $("[name='csrfmiddlewaretoken']").val();
        var formData = new FormData();

        formData.append('pkey', pkey);
        formData.append('csrfmiddlewaretoken', csrf);

        $.ajax({
            url: '/upload_ssh_key/',
            type: 'post',
            data: formData,
            async: false,
            processData: false,
            contentType: false,
            mimeType: 'multipart/form-data',
            success: function (data) {
                ssh_key = data;
            }
        });
    }

    var connect_info1 = 'host=' + host + '&port=' + port + '&user=' + user + '&auth=' + auth;
    var connect_info2 = '&password=' + password + '&ssh_key=' + ssh_key;
    // var connect_info = connect_info1 + connect_info2;
    //组装为ssh连接参数
    // var ssh_args = `host=${host}`;
    var conn_info={"type":"web","name":name,"host":host,"port":port,"user":user,"pwd":pwd,"docker_name":dockerName}
    return conn_info

}

var storage=window.sessionStorage
storage.clear()
function connect(self) {
    var info;
    // window.location.replace('webssh')
    //首先判断用户是点的下拉选项还是新建的服务器
    //如果是下拉选项，则传递给后台去查相应的服务器信息
    if (self.id=="button1"){
        var index=document.getElementById("txt").selectedIndex;
        var tag=document.getElementById("txt").options[index].text;
        console.log("选择的下拉选项是"+tag+"//");
        info={"type":"web","name":tag};
        storage.setItem("type",info.type);
        storage.setItem("name",info.name)
        console.log(info)
    }
    //如果是新建的服务器，则拼接地址并发送服务器信息给后端
    else{
        var info = get_connect_info();
        console.log(info);
        // let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws"; //获取协议
        let ws_scheme = "ws";
        let ws_port = (window.location.port) ? (':' + window.location.port) : '';  // 获取端口
        // socketURL = ws_scheme + '://' + window.location.host + '/webssh/' + ssh_args ;
        console.log(info)
        for(key in info){
            storage.setItem(key,info[key])
        }
    }

    window.open('webssh')
    setTimeout(function(){
        location.reload();
    },1000
    );
}

function dele(self) {
    var xmlHttp=new createXMLRequest();
    var index=document.getElementById("txt").selectedIndex;
    var tag=document.getElementById("txt").options[index].text;
    xmlHttp.onreadystatechange=function () {
        if(xmlHttp.readyState==4&& xmlHttp.status==200){
            if (xmlHttp.responseText==1){
                alert('删除成功')
            }
            else{
                alert('删除失败')
            }
        }
    }
    xmlHttp.open("POST","/django_webssh/dele",true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded")
    xmlHttp.send("name="+tag);
    console.log(tag)
    setTimeout(function(){
        location.reload();
    },1000
    );
}
function is_login(self) {
    var xmlHttp=new createXMLRequest();
    var name=self.value;
    xmlHttp.onreadystatechange=function () {
        if(xmlHttp.readyState==4&& xmlHttp.status==200){
            if (xmlHttp.responseText==1){
                document.getElementById("error").innerText="该名称已使用过！！！"
            }
            else{
                document.getElementById("error").innerText="该名称可以使用~"
            }
        }
    }
    xmlHttp.open("POST","/django_webssh/is_login",true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded")
    xmlHttp.send("name="+name);

}
function createXMLRequest() {
        var xmlHttp;
        //适用于大多数浏览器，以及IE7和IE更改版本
        try{
            xmlHttp=new XMLHttpRequest()
        }catch (e) {
            //适用于IE6
            try{
                xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
            }catch (e) {
                //适用于IE5.5，以及IE更早版本
                try {
                    xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
                }catch (e) {

                }
            }
        }
        return xmlHttp;
    }

