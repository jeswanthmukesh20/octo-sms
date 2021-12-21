const electron = require('electron');
const url = require('url');
const path = require('path');

const {app, BrowserWindow, Menu, ipcMain} = electron;

let mainWindow;

app.on('ready', function(){
    mainWindow = new BrowserWindow({});
    // mainWindow.loadFile(url.format({
    //     pathname: path.join(__dirname, 'mainWindow.html'),
    //     protocol: 'file:'
    // }))
    mainWindow.loadURL('http://localhost:3000');
});
