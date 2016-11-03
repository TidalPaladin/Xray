#!/bin/bash
channel=2
total_steps=2220

lightOn()
{
	sudo /home/pi/kpl -r 10 etekcity 1 1
}
lightOff()
{
	sudo /home/pi/kpl -r 10 etekcity 1 0
}
beamOn()
{
	sudo /home/pi/kpl -r 5 etekcity $channel 1
}

beamOff()
{
	sudo /home/pi/kpl -r 30 etekcity $channel 0
}
setAperture()
{
	gphoto2 --set-config capture-on --set-config-index /main/capturesettings/f-number=$1
}
setIso()
{
	gphoto2 --set-config capture-on --set-config iso=$1
}
setShutter()
{
	gphoto2 --set-config capture-on --set-config shutterspeed2=$1
}
getBattery()
{
	echo $(gphoto2 --get-config=/main/status/batterylevel | grep Current: | sed 's/.* //')
}
getIso()
{
	echo $(gphoto2 --get-config=/main/imgsettings/iso | grep Current: | sed 's/.* //')
}
getAperture()
{
	echo $(gphoto2 --get-config=/main/capturesettings/f-number | grep Current: | sed 's/.* //')
}
getShutter()
{
	echo $(gphoto2 --get-config=/main/capturesettings/shutterspeed2 | grep Current: | sed 's/.* //')
}
captureToCamera()
{
	gphoto2 --trigger-capture &
}

captureToPi()
{
	gphoto2 --keep --capture-image-and-download --filename=xray-%H%M%S.nef &
}
captureVideo()
{
	gphoto2 --capture-movie=$1
}

setupStepper()
{
	echo "25" > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio25/direction
	echo "24" > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio24/direction
	echo "23" > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio23/direction
	echo "22" > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio22/direction
}

adjustAngle()
{
	for (( i=1; i<=$1; i++ ))
	do
	echo "0" > /sys/class/gpio/gpio24/value
	echo "1" > /sys/class/gpio/gpio25/value
	sleep $delay
	echo "0" > /sys/class/gpio/gpio23/value
	echo "1" > /sys/class/gpio/gpio24/value
	sleep $delay
	echo "0" > /sys/class/gpio/gpio22/value
	echo "1" > /sys/class/gpio/gpio23/value
	sleep $delay
	echo "0" > /sys/class/gpio/gpio25/value
	echo "1" > /sys/class/gpio/gpio22/value
	sleep $delay
	done
	echo "0" > /sys/class/gpio/gpio25/value
        echo "0" > /sys/class/gpio/gpio24/value
        echo "0" > /sys/class/gpio/gpio23/value
        echo "0" > /sys/class/gpio/gpio22/value
	echo "Angle adjust complete"
}

cleanupStepper()
{
	echo "0" > /sys/class/gpio/gpio25/value
	echo "0" > /sys/class/gpio/gpio24/value
	echo "0" > /sys/class/gpio/gpio23/value
	echo "0" > /sys/class/gpio/gpio22/value
	echo "25" > /sys/class/gpio/unexport
	echo "24" > /sys/class/gpio/unexport
	echo "23" > /sys/class/gpio/unexport
	echo "22" > /sys/class/gpio/unexport
}


if [ $1 == "status" ]; then
	aperture=$(getAperture)
	iso=$(getIso)
	shutter=$(getShutter)
	printf "Aperture: $aperture\nISO: $iso\nShutter: $shutter\n"

elif [ $1 == "set" ]; then
	if [ $2 == "aperture" ]; then
		setAperture $3
	elif [ $2 == "iso" ]; then
		setIso $3
	elif [ $2 == "shutter" ]; then
		setShutter $3
	else
		echo "No value to set"
	fi

elif [ $1 == "capture" ]; then
	#shutter=$(getShutter)
	shutter=3
	lightOff &
	setShutter $shutter
	setIso 3200
	gphoto2 --set-config capturetarget=0
	if [[ $shutter -le 3 ]]; then
		captureToPi &>/dev/null
		sleep 0.5
		beamOn &>/dev/null
		sleep $(awk "BEGIN {print $shutter-0.7; exit}")
		beamOff &>/dev/null
		lightOn
	else
		echo "Error: Shutter speed $shutter greater than 3"
	fi
	# Open newest file for preview
	sudo killall -9 gpicview
	sleep 5
	file=$(ls -t xray* | head -1)
	gpicview $file &>/dev/null &

elif [ $1 == "ct" ]; then
	# Set constants
	#frames=45	# 45 frames, 8 degrees each
	frames=45
	#cycles=$(awk "BEGIN {print $total_steps/$frames; exit}")
	cycles=49
	delay=0.001
	echo "Starting CT scan..."
	echo "Taking $frames frames with $cycle steps per frame"
	setupStepper

	gphoto2 --set-config capturetarget=1
	# Set camera settings
        setShutter 1
	setIso 6400

	for (( j=1; j<=$frames; j++ ))
	do
        	captureToCamera
		sleep 0.5
        	beamOn &>/dev/null
		sleep 0.1
        	beamOff &>/dev/null

		echo "Captured frame $j, adjusting angle"
		adjustAngle $cycles
		sleep 3
	done

	

elif [ $1 == "fluoroscopy" ];then
	setShutter '1/30'
	setIso 6400
	gphoto2 --set-config capturetarget=0
	delay=0.001
	cycles=512
	captureVideo 30s
	sleep 1
	if [ $2 == "rotate" ]; then
		setupStepper
		adjustAngle $cycles &
	fi
	sleep 0.5
	beamOn
	sleep 2.5
	beamOff
	sleep 8
	cleanupStepper
else
	echo "Please choose an option"
fi
