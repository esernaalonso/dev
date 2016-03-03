"""Summary"""
#######################################
# imports

from PySide import QtCore, QtGui

import esa.common.python.lib.ui.ui as ui

reload(ui)

#######################################
# functionality


def get_streaming_widget(streaming_link):
    # streaming_widget = None
    streaming_widget = QtGui.QTextBrowser()

    text = """
        <html>
            <head>
                <script src="http://campus.insideanim.com/wp-content/plugins/jwplayer/jwplayer.js"></script>
                <script>jwplayer.key="ZcmQIvpCDXRByh3Mis42PsnX2/+2DfbhuzsFTg==";</script>
            </head>
            <body>
                <p>This is a paragraph</p>
                <div>This is inside div element</div>
                <div id="myElement">Loading the player...</div>
                <script type="text/javascript">
                    var playerInstance = jwplayer("myElement");
                    playerInstance.setup({
                        file: "http://www.db.insideanim.com/media/campus/tmp/creatures_tiger_walk_cycle_hss_001.mp4",
                        width: 640,
                        height: 360,
                        title: 'Basic Video Embed',
                        description: 'A video with a basic title and description!',
                        mediaid: '123456'
                    });
                </script>
            </body>
        </html>
    """

    streaming_widget.setHtml(text)

    return streaming_widget


#######################################
# execution

if __name__ == "__main__":
    streaming_link = "test"
    get_streaming_widget(streaming_link)
    pass
