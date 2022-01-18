const electron = require('electron');
const url = require('url');
const path = require('path');
require('@electron/remote/main').initialize();
const axios = require('axios');
const {app, BrowserWindow, Menu, ipcMain} = electron;

let mainWindow;

app.on('ready', function(){
    mainWindow = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });
    // mainWindow.loadFile(url.format({
    //     pathname: path.join(__dirname, 'mainWindow.html'),
    //     protocol: 'file:'
    // }))
    mainWindow.loadURL('http://localhost:3000');
});

let tab_status = null;
app.on('browser-window-focus', () => {
    tab_status = true;
    console.log('online', tab_status);
});
app.on('browser-window-blur', () => {
    tab_status = false;
    console.log('offline', tab_status);
});

console.log("tab_status: ", tab_status);
ipcMain.on('face_state', (event, arg) => {
    console.log('online');
    const headers = {"accept": "application/json", "Content-Type": "application/json"};
    arg = Object.assign({tabStatus: tab_status}, arg);
    let data = JSON.stringify(arg);
    console.log(data);
    resp =  axios.post("http://localhost:5000/api/live", data, {headers: headers})
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.log(error);
    });
});
    // console.log(resp);