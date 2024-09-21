from pyModbusTCP.client import ModbusClient

EMS_MODES = {"0": "Max Self Consumption", "1": "AI Mode", "2": "TOU", "7": "Remote EMS Mode"}


class SigenStorClient:
    def __init__(self, ip, port=502):
        self.client_1 = ModbusClient(host=ip, port=port, unit_id=1, auto_open=True, auto_close=True)
        self.client_247 = ModbusClient(host=ip, port=port, unit_id=247, auto_open=True, auto_close=True)

    # Chapter 5.1 Modbus Doc (read only)

    def get_selected_operating_mode(self):
        """
        Get the selected operating mode of the SigenStor EMS.
        :return: Short Description of the selected operating mode.
        """
        result = self.client_247.read_holding_registers(30003, 1)[0]
        return EMS_MODES.get(str(result), "Unknown")

    def grid_sensor_connected(self):
        """
        Check grid sensor status.
        :return: True if grid sensor is connected, False otherwise.
        """
        return self.client_247.read_holding_registers(30004, 1)[0] == 1

    def get_current_power_to_grid(self):
        """
        Get the current power selling to grid.
        :return: Current power to grid in kW.
        """
        reading = self.client_247.read_holding_registers(30005, 2)
        result = reading[0] - reading[1]
        return result / 1000 if result > 0 else 0

    def get_current_power_from_grid(self):
        """
        Get the current power buying from grid.
        :return: Current power from grid in kW.
        """
        reading = self.client_247.read_holding_registers(30005, 2)
        result = reading[0] - reading[1]
        return result / 1000 if result < 0 else 0

    def is_on_grid(self):
        """
        Check if the system is connected to grid.
        :return: True if the system is on grid, False otherwise.
        """
        return self.client_247.read_holding_registers(30009, 1)[0] == 0

    def get_current_power_to_battery(self):
        """
        Get the current power charging the battery.
        :return: Current power to battery in kW.
        """
        reading = self.client_247.read_holding_registers(30037, 2)
        result = reading[0] - reading[1]
        return round(result / 1000, 2) if result > 0 else 0

    def get_current_power_from_battery(self):
        """
        Get the current power discharging the battery.
        :return: Current power from the battery in kW.
        """
        reading = self.client_247.read_holding_registers(30037, 2)
        result = reading[0] - reading[1]
        return round(result / 1000, 2) if result < 0 else 0

    def enable_remote_ems_mode(self):
        """
        Enables remote EMS mode.
        """
        self.client_247.write_single_register(40029, 1)

    # Chapter 5.2 Modbus Doc (read/write)

    def disable_remote_ems_mode(self):
        """
        Disabled remote EMS mode.
        """
        self.client_247.write_single_register(40029, 0)

    def set_remote_ems_control_mode(self, mode):
        """
        Sets the remote EMS mode.
        :param mode: Number for the mode.
            0: PCS Remote control.
            1: Standby
            2: Max self consumption
            3: Command Charging (prioritize grid power)
            4: Command Charging (prioritize PV power)
            5: Command Discharging (Output PV first)
            6: Command Discharging (Output battery first)
        """
        self.client_247.write_single_register(40031, mode)

    def get_model_type(self):
        """
        Get the model type of the inverter.
        :return: The model type.
        """
        return self.client_1.read_holding_registers(30500, 15)[0]

    # Chapter 5.3 Modbus Doc (read only)

    def get_current_total_pv_power(self):
        """
        Get the current total PV power.
        :return: The current total PV power in kW.
        """
        return round(self.get_pv_string_1_power() + self.get_pv_string_2_power() +
                     self.get_pv_string_3_power() + self.get_pv_string_4_power(), 2)

    def get_battery_soc(self):
        """
        Get the current battery state of charge.
        :return: Current battery state of charge in %.
        """
        return self.client_1.read_holding_registers(30601, 1)[0] / 10

    def get_pv_string_1_power(self):
        """
        Get the current power of PV String 1 in kW.
        :return: Current power of String 1 in kW.
        """
        result = (self.client_1.read_holding_registers(31027,1)[0] *
                self.client_1.read_holding_registers(31028, 1)[0] / 1000000)

        return round(result, 2) if result < 50 else 0
        # validation with 50 because getting strange values if String is not connected


    def get_pv_string_2_power(self):
        """
        Get the current power of PV String 2 in kW.
        :return: Current power of String 2 in kW.
        """
        result = (self.client_1.read_holding_registers(31029,1)[0] *
                self.client_1.read_holding_registers(31030, 1)[0] / 1000000)

        return round(result, 2) if result < 50 else 0
        # validation with 50 because getting strange values if String is not connected

    def get_pv_string_3_power(self):
        """
        Get the current power of PV String 3 in kW.
        :return: Current power of String 3 in kW.
        """
        result = (self.client_1.read_holding_registers(31031,1)[0] *
                self.client_1.read_holding_registers(31032, 1)[0] / 1000000)

        return round(result, 2) if result < 50 else 0
        # validation with 50 because getting strange values if String is not connected

    def get_pv_string_4_power(self):
        """
        Get the current power of PV String 4 in kW.
        :return: Current power of String 4 in kW.
        """
        result = (self.client_1.read_holding_registers(31033,1)[0] *
                self.client_1.read_holding_registers(31034, 1)[0] / 1000000)

        return round(result, 2) if result < 50 else 0
        # validation with 50 because getting strange values if String is not connected
