# Custom script for the M-Audio TriggerFinger (old)
# Attempt to turn the device into a guitar pedal for livelooping mainly

from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.MixerComponent import MixerComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.DrumRackComponent import DrumRackComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.MidiMap import MidiMap as MidiMapBase
from _Framework.MidiMap import make_button, make_encoder, make_slider
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE

play_flag = 0
overdub_flag = 0

class TriggerFingerMX(ControlSurface):

    def __init__(self, *a, **k):
        super(TriggerFingerMX, self).__init__(*a, **k)
        self.show_message("-----------------------= TriggerFingerMX v0.5 LOADING - maxcloutier13 says hi =----------------------------------------------------------")
        self.log_message("-----------------------= TriggerFingerMX LOADING - maxcloutier13 says hi =----------------------------------------------------------")
        with self.component_guard():
            self._init_controls()
            
    def _init_controls(self):
        #Define the controls in here for clarity
        #self.show_message("TFMX Debug: initControls")
        #Using channel 13 for some reason
        #Pads are set from C4 to D6
        self._Pad0 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 72, name='Pad0')        
        self._Pad1 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 74, name='Pad1')
        self._Pad2 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 76, name='Pad2')
        self._Pad3 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 77, name='Pad3')
        #
        self._Pad4 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 79, name='Pad4')
        self._Pad5 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 81, name='Pad5')
        self._Pad6 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 83, name='Pad6')
        self._Pad7 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 84, name='Pad7')
        #
        self._Pad8 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 86, name='Pad8')
        self._Pad9 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 88, name='Pad9')
        self._Pad10 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 89, name='Pad10')
        self._Pad11 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 91, name='Pad11')
        #
        self._Pad12 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 93, name='Pad12')      
        self._Pad13 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 95, name='Pad13')
        self._Pad14 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 96, name='Pad14')
        self._Pad15 = ButtonElement(True, MIDI_NOTE_TYPE, 12, 98, name='Pad15')
        
        #Listeners on individual pads
        self._Pad0.add_value_listener(self._trig_pad0, False)
        self._Pad1.add_value_listener(self._trig_pad1, False)
        self._Pad2.add_value_listener(self._trig_pad2, False)
        self._Pad3.add_value_listener(self._trig_pad3, False)
        #
        self._Pad4.add_value_listener(self._trig_pad4, False)
        self._Pad5.add_value_listener(self._trig_pad5, False)
        self._Pad6.add_value_listener(self._trig_pad6, False)
        self._Pad7.add_value_listener(self._trig_pad7, False)
        #
        self._Pad8.add_value_listener(self._trig_pad8, False)
        self._Pad9.add_value_listener(self._trig_pad9, False)
        self._Pad10.add_value_listener(self._trig_pad10, False)
        self._Pad11.add_value_listener(self._trig_pad11, False)
        #
        self._Pad12.add_value_listener(self._trig_pad12, False)
        self._Pad13.add_value_listener(self._trig_pad13, False)
        self._Pad14.add_value_listener(self._trig_pad14, False)
        self._Pad15.add_value_listener(self._trig_pad15, False)
        
        self._Pads = ButtonMatrixElement(rows=[[self._Pad0, self._Pad1, self._Pad2, self._Pad3],
                                               [self._Pad4, self._Pad5, self._Pad6, self._Pad7], 
                                               [self._Pad8, self._Pad9, self._Pad10, self._Pad11],
                                               [self._Pad12, self._Pad13, self._Pad14, self._Pad15]])
        #Encoders to auto-map to devices -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self._Encoder0 = EncoderElement(MIDI_CC_TYPE,12,22, Live.MidiMap.MapMode.absolute, name='Encoder0')
        self._Encoder1 = EncoderElement(MIDI_CC_TYPE,12,23, Live.MidiMap.MapMode.absolute, name='Encoder1')
        self._Encoder2 = EncoderElement(MIDI_CC_TYPE,12,24, Live.MidiMap.MapMode.absolute, name='Encoder2')
        self._Encoder3 = EncoderElement(MIDI_CC_TYPE,12,25, Live.MidiMap.MapMode.absolute, name='Encoder3')
        self._Encoder4 = EncoderElement(MIDI_CC_TYPE,12,26, Live.MidiMap.MapMode.absolute, name='Encoder4')
        self._Encoder5 = EncoderElement(MIDI_CC_TYPE,12,27, Live.MidiMap.MapMode.absolute, name='Encoder5')
        self._Encoder6 = EncoderElement(MIDI_CC_TYPE,12,28, Live.MidiMap.MapMode.absolute, name='Encoder6')
        self._Encoder7 = EncoderElement(MIDI_CC_TYPE,12,29, Live.MidiMap.MapMode.absolute, name='Encoder7')
        self._Encoders = ButtonMatrixElement(rows=[[self._Encoder0, self._Encoder1, self._Encoder2, self._Encoder3, self._Encoder4,  self._Encoder5, self._Encoder6, self._Encoder7]])
        #Device -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.log_message("Device component set")
        self._device = DeviceComponent(name='Device', is_enabled=False, layer=Layer(parameter_controls=self._Encoders), device_selection_follows_track_selection=True)
        self._device.set_enabled(True)
        self.set_device_component(self._device)
        self.show_message("TFMX Debug: initControls: Done")
        
    #--- Bottom-row
    #Record New
    def _trig_pad0(self, value):        
        if value > 0:
            self._record_new()
                
    #Play/Pause        
    def _trig_pad1(self, value):                
        if value > 0: 
            self._play_pause()
    #Stop        
    def _trig_pad2(self, value):        
        if value > 0:
            self._stop_reset()
                
    #Launch clip
    def _trig_pad3(self, value):        
        if value > 0:
            self._launch_clip()

    #-- 2nd row
    #Set new
    def _trig_pad4(self, value):        
        if value > 0:
            self._set_new()
            
    #-- Move left
    def _trig_pad5(self, value):        
        if value > 0:
            self._move_track(1)            
            
    #-- Move down        
    def _trig_pad6(self, value):        
        if value > 0:
            self._move_clipslot(0)
            
    #-- Move right
    def _trig_pad7(self, value):        
        if value > 0:
            self._move_track(0)           
            
    #-- 3rd-row
    #Stop new
    def _trig_pad8(self, value):     
        if value > 0:
            self._stop_new()            
            
    def _trig_pad9(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad9 triggered")
    
    #-- Move Up        
    def _trig_pad10(self, value):        
        if value > 0:
            self._move_clipslot(1)           

    def _trig_pad11(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad11 triggered")
    #-- Top-row
    def _trig_pad12(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad12 triggered")
            
    def _trig_pad13(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad13 triggered")
            
    def _trig_pad14(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad14 triggered")

    def _trig_pad15(self, value):        
        if value > 0:
            self.show_message("TFMX Debug: Pad15 triggered")
            
    def _stop_reset(self):
        global play_flag
        if play_flag == 0:
            #Not playing, reset playing position to start
            self.song().stop_playing()
            play_flag = 1
        else:
            #Playing, stops, but tells play button to start from position next time
            self.song().stop_playing()
            play_flag = 2
        return
            
    def _play_pause(self):
        #Play/pause functionality
        global play_flag
        if self.song().is_playing == 0:
            #Song not playing
            if play_flag == 0:
                #Song is paused: unpause
                self.song().continue_playing()
            elif play_flag == 1:
                #Song is Stopped, play from selection start
                self.song().play_selection()
                play_flag = 0 
            else:
                #Song is stopped and reset, play from start
                self.song().start_playing()
                play_flag = 0  
        else:
            #Playing: pause
            self.song().stop_playing()
    
    def _move_clipslot(self, up):
        scene = self.song().view.selected_scene
        scenes = self.song().scenes
        max_scenes = len(scenes)
        for i in range(max_scenes):
            if scene == scenes[i]:
                #Found our guy
                if up == 1:
                    self.song().view.selected_scene = scenes[i-1]
                    self.show_message("TFMX Debug: Up!")
                else:
                    if scene == scenes[max_scenes-1]:
                        self.song().view.selected_scene = scenes[0]
                    else:
                        self.song().view.selected_scene = scenes[i+1]
                    self.show_message("TFMX Debug: Down!")
             
    def _move_track(self, left):
        #Get track and tracks
        track = self.song().view.selected_track
        tracks = self.get_all_tracks(only_visible = True)
        max_tracks = len(tracks)
        #Iterate to find current track's index.
        for i in range(max_tracks):
            if track == tracks[i]:
                #Found our track
                if left == 1:
                    self.song().view.selected_track = tracks[i-1]
                else:
                    if track == tracks[max_tracks-1]:
                        self.song().view.selected_track = tracks[0]
                    else:
                        self.song().view.selected_track = tracks[i+1]
                        
    def get_all_tracks(self, only_visible = False):
        tracks = []
        for track in self.song().tracks:
            if not only_visible or track.is_visible:
                tracks.append(track)
        #Include the master track?
        #NOPE tracks.append(self.song().master_track)
        return tracks
        
    def _launch_clip(self):       
        global overdub_flag
        #self.log_message("--> Track launch! -----")
        #self.song().view.highlighted_clip_slot.set_fire_button_state(True)
        _current_slot = self.song().view.highlighted_clip_slot 
        if _current_slot.is_playing == 0 and _current_slot.is_recording == 0:            
            self.song().view.highlighted_clip_slot.set_fire_button_state(True)
        elif _current_slot.is_playing == 1 and _current_slot.is_recording == 0:
            self.song().overdub = 1
            overdub_flag = 1
        elif _current_slot.is_playing == 1 and _current_slot.is_recording == 1 and overdub_flag == 1:
            self.song().overdub = 0
            overdub_flag = 0
        else:
            self.song().view.highlighted_clip_slot.set_fire_button_state(True)
    
    #Position on next valid clipslot    
    def _set_new(self):
        self.show_message("TFMX Debug: SetNew")
        #Find the first empty available clipslot and set it as highlighed
        self._find_empty_slot()
    
    #Stop clips then Position on next valid clipslot
    def _stop_new(self):
        self.show_message("TFMX Debug: StopNew")
        self.song().view.selected_track.stop_all_clips()
        #Position on first empty cell
        self._find_empty_slot()
        
    #Stop clips, position on next valid clipslot and fire record   
    def _record_new(self):
        self.show_message("TFMX Debug: RecordNew")
        self.song().view.selected_track.stop_all_clips()
        #Position on first empty cell
        self._find_empty_slot()
        self.song().view.highlighted_clip_slot.set_fire_button_state(True)
    
    def _find_empty_slot(self):
        #Find the first empty available clipslot and set it as highlighed
        for clipslot in self.song().view.selected_track.clip_slots:
            if clipslot.has_clip == 0:
                self.song().view.highlighted_clip_slot = clipslot
                return
    
    
        
    