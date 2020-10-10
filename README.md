# TriggerFinger_AbletonLive_MIDIRemoteScript

Custom midi remote script for using the TriggerFinger in Ableton Live 10.x <br/>
Removes all controls on program 13 and turns the device into a Guitar live-looping pedal-board<br/>
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How to Install<br/>
1: Find the "MIDI Remote Scripts" folder for your installation of Ableton (Usually: C:\Program Files\Ableton\Resources\MIDI Remote Scripts)<br/>
2: Copy the TriggerFingerMX folder there<br/>
3: Open Ableton and got to Option/Preferences .. Then the Link MIDI tab. Select the desired script in the Control Surface selector. Set Input/Output as your TriggerFinger<br/>

Setting on the TriggerFinger<br/>
1: Select the program you want to use. I use 13<br/>
2: Set global channel to 13<br/>
3: Set every pad to channel 13<br/>
4: Set the pad note so they look like this:<br/>
--  A5-B5-C6-B6<br/>
--  D5-E5-F5-G5<br/>
--  G4-A4-B4-C5<br/>
--  C4-D4-E4-F4<br/>
5: Save your preset<br/>

<b>Current layout</b><br/>
| Column | Row 1 | Row 2 | Row 3 | Row 4 |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 | StopNew |  | Up |  |
| 3 | SetNew | Left | Down | right |
| 4 | RecordNew | Play/Pause | Stop | Record |
<br/>
StopNew: Stop playing clip in selected track and selects the first available slot. Useful to stop a loop and start playing instead to look for something that fits, ready to hit record manually.<br/>
SetNew: Selects the first available slot. Ready to hit record manually.<br/>
RecordNew: Selects the first available slots and starts recording. Useful when there is a clip playing already and you are ready to replace without warmup.<br/>
Play/Pause: Plays from current position when unpaused. If Stop was pressed before it will start from selection position.<br/>
Stop: Pressed once: pause and makes the play button start from selection position. Twice: sets selection position to start of song.<br/>
------------------------------------------------------------------------------------------------------------------------------------------------------

Some links on how to mess with MIDI remote scripts:<br/>
https://djtechtools.com/2014/07/06/the-basics-of-ableton-live-midi-controller-scripts-auto-mapping/<br/>
Max 8 Documentation (translates a lot to what you can do in the scripts: https://docs.cycling74.com/max8<br/>
http://remotescripts.blogspot.com/2010_03_01_archive.html<br/>
Good view of the live object model and its definitions<br/>
https://docs.cycling74.com/max5/refpages/m4l-ref/m4l_live_object_model.html<br/>

