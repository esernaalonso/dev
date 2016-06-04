module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        'create-windows-installer': {
            x64: {
                appDirectory: './app',
                outputDirectory: './dist/installer64',
                authors: 'Eduardo Serna Alonso',
                exe: 'templateApp.exe'
            }
        }
    });

    grunt.loadNpmTasks('grunt-electron-installer-windows');
    grunt.registerTask('default', ['create-windows-installer']);

};
