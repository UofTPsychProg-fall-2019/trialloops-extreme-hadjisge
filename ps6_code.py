#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

each cell in this script contains a different experiment ingredient.
it's not meant to be run from beginning to end but istead is a resource
that you can use to grab code snippets when building your own experiment

@author: katherineduncan
"""

# %% Required: import packages
"""
just like any python script, you'll want to import all your required packages
at the top of the script
this list isn't exhaustive, but contains many of the packages that you'll
likely need for an experiment
"""
import numpy as np
import pandas as pd
import os
import sys
from psychopy import visual, core, event, gui, logging
# visual is needed to open a window and present visual stim
# core is needed for basic timing functions
# event is needed to get keypresses and mouse clicks
# gui lets you use a gui to collect info from experimenter


event.globalKeys.add(key='q', func=core.quit)
# %% Optional: collect info about session
"""
the built-in gui is a simple way to collect session information
you can include whatever fields you like!
some experiments may not require this, but usually you'll want
subject info to save your data
"""
# create a gui object
subgui = gui.Dlg()

# add fields. the strings become the labels in the gui
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

# %% Optional: prepare output
"""
once you have subject info, it's a good idea to make sure that you haven't
already run the subject! you can include a check up front
"""
outputFileName = 'data' + os.sep + 'sub' + subjID + '_sess' + sessNum + '.csv'
if os.path.isfile(outputFileName):
    sys.exit("data for this session already exists")

outVars = ['subj', 'trial', 'response', 'rt',
           'stimOn', 'stimDur', 'correct_letter']
out = pd.DataFrame(columns=outVars)

# experiment parameters
stimDur = 1
respDur = 2
isiDur = 1

stims = ['T.png', 'L.png', 'E.png', 'L.png', 'T.png',
         'E.png', 'A.png', 'T.png', 'B.png', 'B.png']
corr_responses = ['f', 'j', 'f', 'j', 'j', 'j', 'j', 'j', 'j', 'j']

# record output
out['subj'] = subjID  # record subject
out['correct_letter'] = corr_responses

# %% Required: set up your window
"""
your window is a box in which all stimuli are presented
it can be full screen (recomended for when your run a real experiment)
or it can be any size you like (can help when building an experiment)

see http://www.psychopy.org/api/visual/window.html for all options
"""

win = visual.Window(size=[800, 800], fullscr=True,
                    allowGUI=False, color=('black'), units='height')
# lots of optional parameters; these are just a few handy ones:
# size specifies how big the window is in pixels
# fullscr will override size if used
# allowGui determines whether a box with controls surrounds the screen
# color is in rgb from -1 to 1
# units will set default for how stimulus size is detfined
#    'height' will maintain aspect ratio while normalizing stim to screen size

# you can also include quality checks
# here to make sure that your screen refresh
# rate is what it should be. this is optional
win.recordFrameIntervals = True
win.refreshThreshold = 1 / 60 + 0.005
logging.console.setLevel(logging.WARNING)


# %% presenting an image
"""
here's how you draw an image from a file to your window
"""

# Instructions
instr = visual.ImageStim(win, image="instructions1.png",
                         size=1, interpolate=False)
# be sure to use the full/relative path to the image location on your computer
# if you set your window units to "height" size=1 means full screen height
# setting interpolate to True will make images look nicer but could add time

# draw image to window buffer
instr.draw()
# flip window to reveal image
win.flip()
keys = event.waitKeys()

instr2 = visual.ImageStim(
    win, image="instructions2.png", size=1, interpolate=False)
# draw image to window buffer
instr2.draw()
# flip window to reveal image
win.flip()
keys = event.waitKeys()

instr_keys = visual.ImageStim(
    win, image="instructions_keypress.png", size=1, interpolate=False)
# draw image to window buffer
instr_keys.draw()
# flip window to reveal image
win.flip()
keys = event.waitKeys()

get_ready = visual.ImageStim(
    win, image="Get_Ready.png", size=1, interpolate=False)
# draw image to window buffer
get_ready.draw()
# flip window to reveal image
win.flip()
keys = event.waitKeys(maxWait=1)

"""Start Experiment!"""

corText = visual.TextStim(win, text='correct', pos=(0, 0), height=0.05)
incText = visual.TextStim(win, text='incorrect', pos=(0, 0), height=0.05)
fixationText = visual.TextStim(win, text="+", color='white', pos=(0, 0),
                               height=0.05)

expClock = core.Clock()  # won't reset
trialClock = core.Clock()  # will reset at the beginning of each trial
stimClock = core.Clock()
respClock = core.Clock()

for i, stim in enumerate(stims):
    trialClock.reset()

    thisStim = visual.ImageStim(win, image=stim, pos=(0, 0))

    thisStim.draw()

    while trialClock.getTime() < isiDur:
        core.wait(.001)

    win.flip()
    stimClock.reset()
    respClock.reset()

    out.loc[i, 'stimOn'] = expClock.getTime()

    trialResp = 0
    trialRT = 0
    event.clearEvents()
    while respClock.getTime() < respDur:
        # check if show stimulus
        if stimClock.getTime() < stimDur:
            thisStim.draw()
            win.flip()
        else:
            win.flip()
            if np.isnan(out.loc[i, 'stimDur']):  # record when stimulus removed
                out.loc[i, 'stimDur'] = expClock.getTime() - out.loc[i, 'stimOn']

        # check for a key response
        keys = event.getKeys(keyList=['f', 'j'], timeStamped=respClock)
        if len(keys) > 0:  # if response made, collect response information
            trialResp, trialRT = keys[-1]

    if trialResp == out.loc[i, 'correct_letter']:
        # save for summary at end: np.mean(out.correct)
        out.loc[i, 'correct'] = 1
        corText.draw()
    else:
        out.loc[i, 'correct'] = 0
        incText.draw()
    rt = visual.TextStim(
        win, text=f"rt: {trialRT:.3f} [s]", color='white', pos=(0, -.1),
        height=0.05)
    rt.draw()
    win.flip()
    core.wait(1)
    fixationText.draw()
    win.flip()
    # record trial parameters
    out.loc[i, 'trial'] = i + 1
    out.loc[i, 'stimDur'] = expClock.getTime() - out.loc[i, 'stimOn']
    # save responses if made
    if trialResp is not None:
        out.loc[i, 'response'] = trialResp
        out.loc[i, 'rt'] = trialRT
    else:
        out.loc[i, 'response'] = None
        out.loc[i, 'rt'] = None

# summary
avg_accuracy = (np.mean(out.loc[:,'correct']))*100
avg_rt = np.mean(out.loc[:,'rt'])
avg_accuracy_text = visual.TextStim(win, text=f"Average Accuracy: {avg_accuracy:.0f} [%]", color='white', pos=(0, 0), height=0.05)
avg_rt_text = visual.TextStim(win, text=f"Average RT: {avg_rt:.3f} [s]", color='white', pos=(0, -.1), height=0.05)
avg_accuracy_text.draw()
avg_rt_text.draw()
win.flip()
core.wait(3)

# manage output
out.to_csv(outputFileName, index=False)

win.close()
core.quit()
