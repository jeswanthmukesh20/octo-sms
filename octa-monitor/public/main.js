const electron = require('electron');
const url = require('url');
const path = require('path');
require('@electron/remote/main').initialize();

const {app, BrowserWindow, Menu, ipcMain} = electron;

let mainWindow;

app.on('ready', function(){
    mainWindow = new BrowserWindow({
        webPreferences:{
            enableRemoteModule: true
        }
    });
    // mainWindow.loadFile(url.format({
    //     pathname: path.join(__dirname, 'mainWindow.html'),
    //     protocol: 'file:'
    // }))
    mainWindow.loadURL('http://localhost:3000');
});
