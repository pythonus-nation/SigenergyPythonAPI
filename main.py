from icecream import ic
from SigenAPI.api import SigenStorClient


"""
Small script to show api values quickly.
"""
def main():
    ip = "enter your ip address here!"
    cl = SigenStorClient(ip)

    ic(cl.get_selected_operating_mode())
    ic(cl.grid_sensor_connected())
    ic(cl.get_current_power_to_grid())
    ic(cl.get_current_power_from_grid())
    ic(cl.is_on_grid())
    ic(cl.get_battery_soc())
    ic(cl.get_current_power_to_battery())
    ic(cl.get_current_power_from_battery())
    ic(cl.get_model_type())
    ic(cl.get_current_total_pv_power())
    ic(cl.get_pv_string_1_power())
    ic(cl.get_pv_string_2_power())
    ic(cl.get_pv_string_3_power())
    ic(cl.get_pv_string_4_power())

if __name__ == '__main__':
    main()
