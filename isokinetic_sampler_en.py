# -*- coding: utf-8 -*-

from guizero import App, Box, Text, ButtonGroup, TextBox, Combo, PushButton, info
from math import pi, sqrt

def update_txt_value():
    if btn_duct_type.value == "round":
        txt_size_value.value = "Diameter:"
    else:
        txt_size_value.value = "Side length:"

flow_units = ["m³/h", "m³/min", "m³/s", "L/h", "L/min", "L/s"]
speed_units = ["m/s", "cm/s"]

def update_duct_type():
    if btn_input_type.value == "flow rate":
        box_duct_type.enabled = True
        txt_input_unit.clear()
        for i in range(len(flow_units)):
            txt_input_unit.insert(i, flow_units[i])
    else:
        box_duct_type.enabled = False
        txt_input_unit.clear()
        for i in range(len(speed_units)):
            txt_input_unit.insert(i, speed_units[i])

def is_float(to_check):
    values = to_check.split(".")
    if len(values) not in [1, 2]:
        return False
    for value in values:
        if value.isdigit() != True:
            return False
    return True

def check_values():
    correct = True
    correct *= is_float(tbox_input_value.value)
    if tbox_size_value.enabled:
        correct *= is_float(tbox_size_value.value)
    correct *= is_float(tbox_probe_flow_value.value)
    if correct:
        calculate_probe()
    else:
        txt_probe_diameter_value.value = ""
        info("Error", "An invalid value was entered.\nRemember to use a period in fractions.")

def calculate_probe():
    if btn_input_type.value == "velocity":
        duct_speed = float(tbox_input_value.value)
        if txt_input_unit.value == "cm/s":
            duct_speed = duct_speed / 100    # in m/s
    else:
        duct_flow = float(tbox_input_value.value)
        if txt_input_unit.value == "m³/h":
            duct_flow = duct_flow / 3600    # in m^3/s
        elif txt_input_unit.value == "m³/min":
            duct_flow = duct_flow / 60    # in m^3/s
        elif txt_input_unit.value == "L/h":
            duct_flow = duct_flow / 1000 / 3600    # in m^3/s
        elif txt_input_unit.value == "L/min":
            duct_flow = duct_flow / 1000 / 60    # in m^3/s
        elif txt_input_unit.value == "L/s":
            duct_flow = duct_flow / 1000    # in m^3/s
        duct_size = float(tbox_size_value.value) / 1000    # in m
        if btn_duct_type.value == "okrągły":
            duct_cross_area = pi * (duct_size)**2 / 4
        else:
            duct_cross_area = (duct_size)**2
        duct_speed = duct_flow / duct_cross_area
    probe_flow = float(tbox_probe_flow_value.value)
    if txt_probe_flow_unit.value == "L/h":
        probe_flow = probe_flow / 1000 / 3600    # in m^3/s
    elif txt_probe_flow_unit.value == "L/min":
        probe_flow = probe_flow / 1000 / 60    # in m^3/s
    elif txt_probe_flow_unit.value == "L/s":
        probe_flow = probe_flow / 1000    # in m^3/s
    isokinetic_area = probe_flow / duct_speed
    probe_diameter = sqrt(4 * isokinetic_area / pi)
    probe_diameter *= 1000    # in mm
    probe_diameter = round(probe_diameter, 1)
    txt_probe_diameter_value.value = str(probe_diameter) + " mm"

app = App(title="Isokinetic probe", width=500, height=320)

txt_header = Text(app, text="Selection of isokinetic probe")

box_top_row = Box(app, align="top")

box_input_type = Box(box_top_row, align="left", width=250, height=150)
txt_choose_input = Text(box_input_type, text="Known air flow parameter:")
btn_input_type = ButtonGroup(box_input_type, options=["flow rate", "velocity"], selected="flow rate", command=update_duct_type)
text_input_value = Text(box_input_type, text="Value:")
box_input_value = Box(box_input_type)
tbox_input_value = TextBox(box_input_value, align="left")
txt_input_unit = Combo(box_input_value, options=flow_units, selected="m³/h", align="left")

box_duct_type = Box(box_top_row, align="right", width=250, height=150, enabled=True)
txt_duct_type = Text(box_duct_type, text="Channel cross-section:")
btn_duct_type = ButtonGroup(box_duct_type, options=["round", "square"], selected="round", command=update_txt_value)
txt_size_value = Text(box_duct_type, text="Diameter:")
box_size_value = Box(box_duct_type)
tbox_size_value = TextBox(box_size_value, align="left")
txt_size_unit = Text(box_size_value, text=" mm", align="left")

box_probe_flow = Box(app, width=500, height=80)
txt_probe_flow = Text(box_probe_flow, text="Probe flow rate:")
box_probe_flow_value = Box(box_probe_flow)
tbox_probe_flow_value = TextBox(box_probe_flow_value, align="left")
txt_probe_flow_unit = Combo(box_probe_flow_value, options=["L/h", "L/min", "L/s"], enabled="L/h", align="left")

box_calculate = Box(app)
box_btn_calculate = Box(box_calculate, width=200, height=150, align="left")
btn_calculate = PushButton(box_btn_calculate, text="Oblicz", command=check_values)
box_probe_diameter = Box(box_calculate, width=200, height=150, align="right")
txt_probe_diameter = Text(box_probe_diameter, text="Probe diameter:")
txt_probe_diameter_value = Text(box_probe_diameter, text="")

app.display()
