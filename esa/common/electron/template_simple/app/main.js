//This is the main execution thread

const electron = require('electron');

// Module to control application life.
const {app} = electron;

// Module to create native browser window.
const {BrowserWindow} = electron;

// Gets the icon
//const nativeImage = require('electron').nativeImage;
//let app_icon = nativeImage.createFromPath('/app/img/icon/sound_fun.png');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

function createMainWindow() {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1024,
        height: 768,
        frame: true,
        autoHideMenuBar: true,
        resizable: true,
        icon: __dirname + '/img/icon/app_24x24.png'
    });

    // and load the index.html of the app.
    mainWindow.loadURL(`file://${__dirname}/main.html`);

    // Open the DevTools.
    //win.webContents.openDevTools();

    // Emitted when the window is closed.
    mainWindow.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createMainWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On OS X it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) {
        createMainWindow();
    }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
