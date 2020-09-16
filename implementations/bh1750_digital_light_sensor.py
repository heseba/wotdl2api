from flask import jsonify
import smbus

print('light_sensor imported')

DEVICE = 0x23
ONE_TIME_HIGH_RES_MODE_2 = 0x21


def get_light_intensity_bh1750():
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_2)
    light_level = convertToNumber(data)
    return jsonify({'light-value': light_level})


def convertToNumber(data):
    # convert 2 bytes of data into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)
