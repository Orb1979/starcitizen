import gremlin
from gremlin.spline import CubicSpline

# This script copies front part of the Joysitck y-axis values, to the slider
# advanteges:
# - Dont need any form of a split axis, to throttle forward and strafe back
# - you can see scm speed, (because y-axis forward is copied to slider, which is bind to throttle)
# - can use your slider as sort of a trim or base speed
# - helps with the throttle stuck at 100% issue when going out of decoupled mode (just move your y-axis a bit)

# bind "strafe forward / back" to your Y-axis stick
# bind "throttle up / down" to your slider

# joystick axis range    = [-1 .. +1] = 0 is no throttle (stick is centered)
# slider range           = [-1 .. +1] = 0 is throttle 50% (slider in the center)

# Joystick decorator
t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=(72331530,1), #1 = system id of left joystick, remove if only using 1 joystick
    mode="Default"
)

# set correct axis for joysticks and vjoy output
inputY          = 2      # joystick axis "Axis 2"
inputSlider     = 4      # joystick axis "Axis 4"
slider          = 7      # vjoy axis"7ax"

# set your curve values (curve values can be read from profile xml)
curve = CubicSpline([
    (-1.0, -1.0),
    ( 1.0, 1.0),
    ( 0.0, 0.0),
    ( 0.1, 0.05),
])
inversionY      = -1     # -1 if Y axis is inverted, else 1
inversionSlider = -1     # -1 if Y axis is inverted, else 1
sliderValue     = -1     # intial value of slider is all the way down

@t16000m.axis(inputY)
def setSliderValue(event, vjoy):
    # reading input of y (so need to adjust with curve)
    y = curve(event.value * inversionY)
    vjoy[1].axis(slider).value = sliderValue + (y*2)

@t16000m.axis(inputSlider)
def getSliderValue(event, vjoy):
    global sliderValue
    sliderValue = event.value * inversionSlider
