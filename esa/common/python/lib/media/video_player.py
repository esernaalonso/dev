from PySide import QtCore, QtGui
from PySide import phonon

import os
import sys
import inspect
import urllib

import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.image.image as image
import esa.common.python.lib.ui.ui as ui

reload(theme)
reload(ui)
reload(image)


class KeyEventHandler(object):
    def __init__(self):
        super(KeyEventHandler, self).__init__()
        pass

    def get_parent_video_player(self, event_widget):
        video_player = event_widget
        while video_player.objectName() != "VideoPlayer":
            video_player = video_player.parent()
        return video_player

    def process_event(self, event_widget, event):

        # If is a mouse move.
        if (event.type() == QtCore.QEvent.Type.HoverMove):
            parent_widget = self.get_parent_video_player(event_widget)
            if parent_widget.is_full_screen:
                parent_widget.update_controls_visibility(state=True)

        # If it is a key release event.
        if (event.type() == QtCore.QEvent.KeyRelease):
            parent_widget = self.get_parent_video_player(event_widget)
            if parent_widget.is_full_screen:
                parent_widget.update_controls_visibility(state=True)

            if event.key() == QtCore.Qt.Key_Left:
                parent_widget.frame_step_prev()
                return True

            elif event.key() == QtCore.Qt.Key_Right:
                parent_widget.frame_step_next()
                return True

            elif event.key() == QtCore.Qt.Key_Up:
                parent_widget.volume_up()
                return True

            elif event.key() == QtCore.Qt.Key_Down:
                parent_widget.volume_down()
                return True

            elif event.key() == QtCore.Qt.Key_Space:
                parent_widget.toggle_play()
                return True

            elif event.key() == QtCore.Qt.Key_F and event.modifiers() == QtCore.Qt.ShiftModifier:
                parent_widget.toggle_full_screen()
                return True

            elif event.key() == QtCore.Qt.Key_Escape:
                parent_widget.exit_full_screen()
                return True

            return QtGui.QWidget.event(event_widget, event)

        # if is the mouse click
        if (event.type() == QtCore.QEvent.Type.MouseButtonRelease):
            parent_widget = self.get_parent_video_player(event_widget)
            if parent_widget.is_full_screen:
                parent_widget.update_controls_visibility(state=True)
            if isinstance(event_widget, CustomVideoPlayer):
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    parent_widget.toggle_play()
                    return True

        # if is the mouse double click
        if (event.type() == QtCore.QEvent.Type.MouseButtonDblClick):
            parent_widget = self.get_parent_video_player(event_widget)
            if parent_widget.is_full_screen:
                parent_widget.update_controls_visibility(state=True)
            if isinstance(event_widget, CustomVideoPlayer):
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    parent_widget.toggle_full_screen()
                    return True

        if (event.type() == QtCore.QEvent.Type.Wheel):
            parent_widget = self.get_parent_video_player(event_widget)
            if parent_widget.is_full_screen:
                parent_widget.update_controls_visibility(state=True)
            if isinstance(event_widget, CustomVideoPlayer) or isinstance(event_widget, CustomVolumeSlider):
                num_degrees = event.delta()/8
                num_steps = num_degrees/15
                for i in range(abs(num_steps)):
                    if num_steps > 0:
                        parent_widget.volume_up()
                    elif num_steps < 0:
                        parent_widget.volume_down()
                return True
            elif isinstance(event_widget, CustomSeekSlider):
                num_degrees = event.delta()/8
                num_steps = num_degrees/15
                for i in range(abs(num_steps)):
                    if num_steps > 0:
                        parent_widget.frame_step_next()
                    elif num_steps < 0:
                        parent_widget.frame_step_prev()
                return True

        return True

class CustomVideoPlayer(phonon.Phonon.VideoPlayer):
    def __init__(self):
        super(CustomVideoPlayer, self).__init__()
        self.event_handler = KeyEventHandler()

    def event(self, event):
        return self.event_handler.process_event(self, event)


class CustomSeekSlider(phonon.Phonon.SeekSlider):
    def __init__(self):
        super(CustomSeekSlider, self).__init__()
        self.event_handler = KeyEventHandler()

    def event(self, event):
        return self.event_handler.process_event(self, event)


class CustomVolumeSlider(phonon.Phonon.VolumeSlider):
    def __init__(self):
        super(CustomVolumeSlider, self).__init__()
        self.event_handler = KeyEventHandler()

    def event(self, event):
        return self.event_handler.process_event(self, event)


class VideoPlayerFullScreen(QtGui.QWidget):
    def __init__(self, video_player_widget=None):
        super(VideoPlayerFullScreen, self).__init__()
        self.video_player_widget = video_player_widget
        self.initUI()

    def initUI(self):
        self.setObjectName("VideoPlayerFullScreen")

        # Applies the theme for the widget
        theme.apply_style(self, "video_player.qss")

        # Allows full screen
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.setMinimumSize(500, 500)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Adds the video player to the new full screen container.
        if self.video_player_widget:
            self.layout().addWidget(self.video_player_widget)

        # Shows the full screen.
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        screen_res = QtGui.QApplication.desktop().screenGeometry(screen)
        self.move(QtCore.QPoint(screen_res.x(), screen_res.y()))
        self.showFullScreen()


class VideoPlayer(QtGui.QWidget):
    def __init__(self):
        super(VideoPlayer, self).__init__()

        self.installEventFilter(self)

        self.is_full_screen = False
        self.normal_mode_parent = None

        self.url = None
        self.mediaObject = None
        self.audio_output = None
        self.framerate = 24
        self.time_display_mode = "current"
        self.last_time = 0

        self.timer = QtCore.QTimer()
        self.timer_hide_controls = QtCore.QTimer()

        self.initUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initUI(self):
        self.setObjectName("VideoPlayer")

        # Applies the theme for the widget
        theme.apply_style(self, "video_player.qss")

        # Allows full screen
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Inserts the .ui content
        video_player_ui_file = ui.get_ui_file("video_player.ui", self.get_current_folder())
        self.ui = ui.loadUiWidget(video_player_ui_file, parent=self)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Phonon components to manage a video.

        # Video Player
        self.video_player = CustomVideoPlayer()
        self.video_player_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.video_player_size_policy.setHorizontalStretch(0)
        self.video_player_size_policy.setVerticalStretch(0)
        self.video_player_size_policy.setHeightForWidth(self.video_player.sizePolicy().hasHeightForWidth())
        self.video_player.setSizePolicy(self.video_player_size_policy)
        self.video_player.setObjectName("video_player")

        # Seek Slider - timeline
        self.seek_slider = CustomSeekSlider()
        self.seek_slider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.seek_slider.setSingleStep(0)
        self.seek_slider.setObjectName("seek_slider")

        # Volume Slider.
        self.volume_slider = CustomVolumeSlider()
        self.volume_slider.setMaximumSize(QtCore.QSize(150, 20))
        self.volume_slider.setMuteVisible(False)
        self.volume_slider.setSingleStep(0)
        self.volume_slider.setObjectName("volume_slider")

        # Inserts the phonon components in the widget containers prepared for them.
        ui.insert_widget(self, "wg_video", self.video_player, None)
        ui.insert_widget(self, "wg_seek", self.seek_slider, None)
        ui.insert_widget(self, "wg_volume", self.volume_slider, None)

        # Stores controls to use with signals and/or to get values in process.
        self.wg_controls_bar = ui.get_child(self, "wg_controls_bar")

        self.pb_time = ui.get_child(self, "pb_time")
        self.pb_time_total = ui.get_child(self, "pb_time_total")
        self.pb_time.setStyleSheet("QPushButton {text-align: left;}")
        self.pb_time_total.setStyleSheet("QPushButton {text-align: left;}")

        self.pb_refresh = ui.get_child(self, "pb_refresh")
        self.pb_play_prev = ui.get_child(self, "pb_play_prev")
        self.pb_play = ui.get_child(self, "pb_play")
        self.pb_play_next = ui.get_child(self, "pb_play_next")
        self.lb_loading = ui.get_child(self, "lb_loading")
        self.lb_state = ui.get_child(self, "lb_state")
        self.pb_volume_down = ui.get_child(self, "pb_volume_down")
        self.pb_volume_up = ui.get_child(self, "pb_volume_up")
        self.pb_volume_on = ui.get_child(self, "pb_volume_on")
        self.pb_expand = ui.get_child(self, "pb_expand")

        # Load the ui icons.
        self.refresh_icon = image.get_image_file("refresh.png", self.get_current_folder())
        self.play_prev_icon = image.get_image_file("play_prev.png", self.get_current_folder())
        self.play_icon = image.get_image_file("play.png", self.get_current_folder())
        self.pause_icon = image.get_image_file("pause.png", self.get_current_folder())
        self.play_next_icon = image.get_image_file("play_next.png", self.get_current_folder())
        self.loading_icon = image.get_image_file("squares_002.gif", self.get_current_folder())
        self.volume_up_icon = image.get_image_file("volume_up.png", self.get_current_folder())
        self.volume_down_icon = image.get_image_file("volume_down.png", self.get_current_folder())
        self.volume_on_icon = image.get_image_file("volume_on.png", self.get_current_folder())
        self.volume_off_icon = image.get_image_file("volume_off.png", self.get_current_folder())
        self.expand_icon = image.get_image_file("expand.png", self.get_current_folder())
        self.reduce_icon = image.get_image_file("reduce.png", self.get_current_folder())

        # Applies the icons.
        self.pb_refresh.setIcon(image.create_pixmap(self.refresh_icon))
        self.pb_play_prev.setIcon(image.create_pixmap(self.play_prev_icon))
        self.pb_play.setIcon(image.create_pixmap(self.play_icon))
        self.pb_play_next.setIcon(image.create_pixmap(self.play_next_icon))
        self.pb_volume_down.setIcon(image.create_pixmap(self.volume_down_icon))
        self.pb_volume_up.setIcon(image.create_pixmap(self.volume_up_icon))
        self.pb_volume_on.setIcon(image.create_pixmap(self.volume_on_icon))
        self.pb_expand.setIcon(image.create_pixmap(self.expand_icon))

        # Special config for the ui elements dedicated to show the buffering process.
        self.lb_state.setMovie(image.create_movie(self.loading_icon))
        self.lb_state.movie().setScaledSize(QtCore.QSize(18,18))
        self.lb_state.movie().start()
        self.update_buffering_ui(force=True, force_state=False)

        # Config the timer to hide the controls
        self.timer_hide_controls_ticks_count = 0
        self.timer_hide_controls.setInterval(1000)

        # Creates the signals
        self.pb_refresh.clicked.connect(self.refresh)
        self.pb_play_prev.clicked.connect(self.frame_step_prev)
        self.pb_play.clicked.connect(self.toggle_play)
        self.pb_play_next.clicked.connect(self.frame_step_next)
        self.pb_time.clicked.connect(self.toggle_time_display_mode)
        self.pb_volume_down.clicked.connect(self.volume_down)
        self.pb_volume_up.clicked.connect(self.volume_up)
        self.pb_volume_on.clicked.connect(self.toggle_volume)
        self.pb_expand.clicked.connect(self.toggle_full_screen)
        self.timer.timeout.connect(self.update_buffering_ui)
        self.timer_hide_controls.timeout.connect(self.update_controls_visibility)

    def refresh(self):
        self.pause()
        self.set_url(self.url)

    def is_ready(self):
        if self.url and self.mediaObject and self.audio_output:
            return True
        else:
            return False

    def set_url(self, url, framerate=24):
        # Clears the values.
        self.url = None
        self.mediaObject = None
        self.audio_output = None

        if url:
            self.url = url
            self.framerate = framerate

            self.video_player.play(url)
            self.video_player.pause()

            self.mediaObject = self.video_player.mediaObject()
            self.mediaObject.setTickInterval(1)
            self.timer.setInterval(1000)

            self.audio_output = self.video_player.audioOutput()

            self.seek_slider.setMediaObject(self.video_player.mediaObject())
            self.volume_slider.setAudioOutput(self.video_player.audioOutput())

            self.pb_time_total.setText(self.get_time_string(mode="total"))

            # Create the signal for the time play
            self.mediaObject.tick.connect(self.update_time_label)

    def update_controls_visibility(self, tick=0, state=False):
        self.timer_hide_controls_ticks_count += 1

        if self.timer_hide_controls_ticks_count > 5 or state:
            self.wg_controls_bar.setVisible(state)
            if state:
                self.timer_hide_controls_ticks_count = 0

    def get_time(self, mode="current"):
        time_miliseconds = 0
        if self.mediaObject:
            time_miliseconds = self.mediaObject.currentTime()
            if mode == "remaining":
                time_miliseconds = self.mediaObject.remainingTime()
            if mode == "total":
                time_miliseconds = self.mediaObject.totalTime()

        current_time_seconds = time_miliseconds/1000
        current_time_minutes = current_time_seconds/60
        current_time_hours = current_time_minutes/60

        hours = current_time_hours
        minutes = current_time_minutes - hours*60
        seconds = current_time_seconds - minutes*60 - hours*60
        miliseconds = time_miliseconds - seconds*1000 - minutes*60*1000 - hours*60*60*1000

        frames = miliseconds/(1000/self.framerate)

        return hours, minutes, seconds, miliseconds, frames

    def get_time_string(self, mode="current"):
        hours, minutes, seconds, miliseconds, frames = self.get_time(mode=mode)
        return ("%d:%02d:%02d:%02d" %(hours, minutes, seconds, frames))

    def update_time_label(self):
        self.pb_time.setText(self.get_time_string(mode=self.time_display_mode))
        self.last_time = self.mediaObject.currentTime() if self.mediaObject else 0

    def update_buffering_ui(self, tick=0, force=False, force_state=False):
        current_time = self.mediaObject.currentTime() if self.mediaObject else 0
        new_state = (self.last_time == current_time and self.video_player.isPlaying()) if not force else force_state
        self.lb_loading.setVisible(new_state)
        self.lb_state.setVisible(new_state)

    def toggle_time_display_mode(self):
        self.time_display_mode = "remaining" if self.time_display_mode == "current" else "current"
        self.pb_time.setText(self.get_time_string(mode=self.time_display_mode))
        self.seek_slider.setFocus()

    def volume_step(self, mode="up"):
        if self.audio_output:
            new_volume = self.audio_output.volume()
            new_volume += 0.05 if mode == "up" else -0.05

            new_volume = 0 if new_volume < 0 else new_volume
            new_volume = 1 if new_volume > 1 else new_volume

            self.pb_volume_on.setIcon(image.create_pixmap(self.volume_off_icon if new_volume==0 else self.volume_on_icon))
            self.audio_output.setMuted(new_volume == 0)

            self.audio_output.setVolume(new_volume)

    def volume_down(self):
        self.volume_step(mode="down")
        self.seek_slider.setFocus()

    def volume_up(self):
        self.volume_step(mode="up")
        self.seek_slider.setFocus()

    def toggle_volume(self):
        if self.audio_output:
            self.audio_output.setMuted(not self.audio_output.isMuted())
            self.pb_volume_on.setIcon(image.create_pixmap(self.volume_off_icon if self.audio_output.isMuted() else self.volume_on_icon))

    def frame_step(self, mode="next"):
        if self.mediaObject:
            if self.video_player.isPlaying():
                self.mediaObject.pause()

            total_time_miliseconds = self.mediaObject.totalTime()
            time_miliseconds = self.mediaObject.currentTime()

            frame_miliseconds = (1000/self.framerate)

            if mode == "next":
                time_miliseconds += frame_miliseconds
                if time_miliseconds > total_time_miliseconds:
                    time_miliseconds = total_time_miliseconds
            elif mode == "prev":
                time_miliseconds -= frame_miliseconds
                if time_miliseconds < 0:
                    time_miliseconds = 0

            self.video_player.seek(time_miliseconds)

    def frame_step_prev(self):
        if self.video_player.isPlaying():
            self.pause()
        self.frame_step(mode="prev")
        self.seek_slider.setFocus()

    def frame_step_next(self):
        if self.video_player.isPlaying():
            self.pause()
        self.frame_step(mode="next")
        self.seek_slider.setFocus()

    def toggle_play(self):
        if self.video_player.mediaObject():
            if self.video_player.isPlaying():
                self.pause()
            else:
                self.play()

            self.pb_time_total.setText(self.get_time_string(mode="total"))

    def play(self):
        if self.mediaObject:
            self.timer.start()
            self.video_player.play()
            self.pb_play.setIcon(image.create_pixmap(self.pause_icon))
            self.seek_slider.setFocus()

    def pause(self):
        if self.mediaObject:
            self.timer.stop()
            self.video_player.pause()
            self.pb_play.setIcon(image.create_pixmap(self.play_icon))
            # print "PAUSA"
            self.update_buffering_ui(force=True, force_state=False)
            self.seek_slider.setFocus()
            # print "AFTER PAUSA"

    def toggle_full_screen(self):
        if not self.is_full_screen:
            self.enter_full_screen()
        else:
            self.exit_full_screen()

    def enter_full_screen(self):
        if self.mediaObject:
            self.normal_mode_parent = self.parent()
            self.is_full_screen = True
            self.video_player_full_screen = VideoPlayerFullScreen(video_player_widget=self)
            self.timer_hide_controls.start()
            self.seek_slider.setFocus()

    def exit_full_screen(self):
        self.normal_mode_parent.layout().addWidget(self)
        self.is_full_screen = False
        self.video_player_full_screen.close()
        self.timer_hide_controls.stop()
        self.update_controls_visibility(state=True)
        self.seek_slider.setFocus()
