
// Borrowed minimalistic Streamlit API from Thiago
// https://discuss.streamlit.io/t/code-snippet-create-components-without-any-frontend-tooling-no-react-babel-webpack-etc/13064
function sendMessageToStreamlitClient(type, data) {
    // console.log(type, data)
    const outData = Object.assign({
        isStreamlitMessage: true,
        type: type,
    }, data);
    window.parent.postMessage(outData, "*");
  }

let is_restart;

const Streamlit = {
    setComponentReady: function() {
        sendMessageToStreamlitClient("streamlit:componentReady", {apiVersion: 1});
    },
    setFrameHeight: function(height) {
        sendMessageToStreamlitClient("streamlit:setFrameHeight", {height: height});
    },
    setComponentValue: function(value) {
        sendMessageToStreamlitClient("streamlit:setComponentValue", {value: value});
    },
    RENDER_EVENT: "streamlit:render",
    events: {
        addEventListener: function(type, callback) {
            window.addEventListener("message", function(event) {
                if (event.data.type === type) {
                    console.log(event.data.args.data)
                    is_restart = event.data.args.data
                    callback(event);
                }
            });
        }
    }
}

function sendValue(value) {
    Streamlit.setComponentValue(value);
  }



function onRender(event) {
    if (!window.rendered) {
        let video = document.getElementById('video');
        let captureButton = document.getElementById('capture');
        let inputText = document.getElementById('inputText');
        let restartButton = document.getElementById('restart');
        
        const constraints =  { facingMode: 'environment', advanced : [{focusMode: "continuous"}],width: { ideal: 1920 },
        height: { ideal: 1440 }};
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: constraints, audio: false})
                .then(function(stream) {
                    // video.src = window.webkitURL.createObjectURL(stream);  
                    video.srcObject = stream;
                    video.play();
                })
                .catch(function(err) {
                    console.log("An error occurred: " + err);
            });
        }
        captureButton.addEventListener('click', function() {
            const canvas = document.createElement('canvas');
            // 设置画布宽度和高度
            const targetWidth = 960;
            const targetHeight = 960;

            // 获取视频宽高，并保持纵横比缩放到目标宽高
            const aspectRatio = video.videoWidth / video.videoHeight;
            if (aspectRatio > 1) {
                // 视频宽度大于高度，按照宽度调整
                canvas.width = targetWidth;
                canvas.height = targetWidth / aspectRatio;
            } else {
                // 视频高度大于或等于宽度，按照高度调整
                canvas.height = targetHeight;
                canvas.width = targetHeight * aspectRatio;
            }

            const context = canvas.getContext('2d');

            // 将视频绘制到画布上
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // 将画布转换为 base64 string
            const base64Image = canvas.toDataURL('image/jpeg');
            // // video.pause();
            const dataToSend = {
                text: inputText.value,
                image: base64Image
            };
            sendValue(dataToSend);
        });
        video.addEventListener('click', function(){this.focus();});


        document.getElementById('upload').addEventListener('click', function() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = e => {
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = function(event) {
                    const dataToSend = {
                        text: inputText.value,
                        image: event.target.result
                    };
                    console.log(dataToSend)
                    sendValue(dataToSend);
                }
                reader.readAsDataURL(file);
            }
            input.click();
        });

        // https://lismin.online:10003/component/streamlit_camera.streamlit_camera/index.html?streamlitUrl=https%3A%2F%2Flismin.online%3A10003%2F

        // 获取当前URL
        const currentUrl = window.parent.location.href;;
        console.log(currentUrl); // 输出: 123
        // 获取查询字符串部分
        const queryStringIndex = currentUrl.indexOf('?');
        if (queryStringIndex !== -1){
            const queryString = currentUrl.split('?')[1];
            const params = queryString.split('&');
            // 初始化一个对象来存储参数
            const queryParams = {};
            // 遍历键值对并存储到对象中
            params.forEach(param => {
                const [key, value] = param.split('=');
                queryParams[key] = decodeURIComponent(value);
            });
    
            // 获取code参数
            const code = queryParams['code'];
            inputText.value = code
        } else {
            inputText.value = ""
        }
        


    window.rendered = true
  }
}
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

Streamlit.setComponentReady();
Streamlit.setFrameHeight(700);

// 🐑老板请我吃烤鸡了，我要加倍努力工作