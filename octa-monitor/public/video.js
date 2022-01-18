const {ipcRenderer} = require('electron');
let model;
const student_id = 232321;
const class_id = 322;
let video=document.getElementById("video");
const SetupCamera = () => {
    navigator.mediaDevices
        .getUserMedia({
            video: {width:1080, height: 720},
            audio:false
        })
        .then((stream)=>{
            video.srcObject=stream;
        });
}
let face_state = false;
let tab_data;
const detectFace = async () => {
    const predction = await model.estimateFaces(video, false);
    // console.log(predction);
    if(predction.length !== 0 ){
        if (face_state === false){
            console.log("Face detected");
            face_state = true;
        }
    }else {
        if (face_state === true){
            console.log("Face not detected");
            face_state = false;
        }
    }
    ipcRenderer.send('face_state', {
        faceState: face_state,
        faces: predction.length,
        studentId: student_id,
        classId: class_id
    });
}

SetupCamera();

video.addEventListener('loadeddata', async () => {
    model = await blazeface.load();
    setInterval(detectFace, 1000)
});
