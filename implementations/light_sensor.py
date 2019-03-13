from flask import jsonify
import grovepi

print('light_sensor imported')

def get_light_intensity(a=1):
    light_sensor = 2
    threshold = 10
    sum = 0
    cnt = 0
    min = 9999
    max = 0

    # while(cnt<50):
    #     sensor_value = grovepi.analogRead(light_sensor)
    #     sum += sensor_value
    #     if (sensor_value > max):
    #         max = sensor_value
    #     if (sensor_value < min):
    #         min = sensor_value
    #     cnt += 1


    sensor_value = grovepi.analogRead(light_sensor)

    resistance = (float)(1023 - sensor_value) * 10 / sensor_value
    #Send HIGH to switch on LED
    if resistance > threshold:
       return jsonify({'resistance':'HIGH', 'light-value':sensor_value, 'resistance-value':resistance})
    else:
       return jsonify({'resistance':'LOW', 'light-value':sensor_value, 'resistance-value':resistance})
    #return jsonify({'light-value':sum/cnt})

