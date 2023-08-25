# Render Output Workflow

1. run the mainPatch_outputRender.toe
   1. choose Realime OFF + 48fps
   2. click the button Start Recording
   3. redering video only into the folder /Render/ as HAP
   4. a txt fil is being generated that holds all OSC commands being generated during render process
2. run MaxMSP Render-DirectRouting patch
   1. load the sound files as usual
3. run the AudioRenderer.toe TD patch
   1. load the TXT file with the OSC commands into the table
   2. choose Realtime ON!! and 24 fps
   3. click the button Start Recording
   4. the audio is being triggered through the osc commands and then recorded into the Render folder
   5. there is one audio track for each video screen and an additional track for the intermission
4. mix/mux video and audio tracks
   1. A+V have to be aligned, (normally delay the video +9 frames )
   2. mix audio tracks for the desired routing to the files