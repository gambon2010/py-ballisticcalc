class VelocityUnits:

    _unit_type = 'velocity'

    # the value indicating that weight value is expressed in some unit
    VelocityMPS = 70
    VelocityKMH = 71
    VelocityFPS = 72
    VelocityMPH = 73
    VelocityKT = 74

    _units = {
        VelocityMPS: {'multiplier': 1 / 1, 'name': 'm/s', 'accuracy': 0},
        VelocityKMH: {'multiplier': 1 / 3.6, 'name': 'km/h', 'accuracy': 1},
        VelocityFPS: {'multiplier': 1 / 3.2808399, 'name': 'ft/s', 'accuracy': 1},
        VelocityMPH: {'multiplier': 1 / 2.23693629, 'name': 'mph', 'accuracy': 1},
        VelocityKT: {'multiplier': 1 / 1.94384449, 'name': 'kt', 'accuracy': 1},
    }

    # return the units in which the value is measured
    def __call__(self, units):
        return self._units[units]

    @staticmethod
    def to_default(value: float, units: int) -> [float, Exception]:
        try:
            multiplier = VelocityUnits()(units)['multiplier']
            return value * multiplier, None
        except KeyError as error:
            return 0, f'KeyError: {VelocityUnits._unit_type}: unit {error} is not supported'

    @staticmethod
    def from_default(value: float, units: int) -> [float, Exception]:
        try:
            multiplier = VelocityUnits()(units)['multiplier']
            return value / multiplier, None
        except KeyError as error:
            return 0, f'KeyError: {VelocityUnits()._unit_type}: unit {error} is not supported'


class Velocity(object):
    """ Velocity object keeps velocity or speed values """

    def __init__(self, value: float, units: int):
        f"""
        Creates a velocity value
        :param value: velocity value
        :param units: TemperatureUnits.consts
        """
        v, err = VelocityUnits.to_default(value, units)
        if err:
            self._value = None
            self._defaultUnits = None
        else:
            self._value = v
            self._default_units = units
        self.error = err

    def __str__(self):
        v, err = VelocityUnits.from_default(self.v, self.default_units)
        if err:
            return f'Velocity: unit {self.default_units} is not supported'
        multiplier, name, accuracy = VelocityUnits()(self.default_units)
        return f'{round(v, accuracy)} {name}'

    @staticmethod
    def must_create(value: float, units: int) -> float:
        """
        Returns the velocity value but panics instead of return error
        :param value: velocity value
        :param units: TemperatureUnits.consts
        :return: None
        """
        v, err = VelocityUnits.to_default(value, units)
        if err:
            raise ValueError(f'Velocity: unit {units} is not supported')
        else:
            return v

    @staticmethod
    def value(velocity: 'Velocity', units: int) -> [float, Exception]:
        """
        :param velocity: Velocity
        :param units: TemperatureUnits.consts
        :return: Value of the velocity in the specified units
        """
        return VelocityUnits.from_default(velocity.v, units)

    @staticmethod
    def convert(velocity: 'Velocity', units: int) -> 'Velocity':
        """
        Returns the value into the specified units
        :param velocity: Velocity
        :param units: TemperatureUnits.consts
        :return: Velocity object in the specified units
        """
        return Velocity(velocity.v, units)

    @staticmethod
    def convert_in(velocity: 'Velocity', units: int) -> [float, Exception]:
        """
        Converts the value in the specified units.
        Returns 0 if unit conversion is not possible.
        :param velocity: Velocity
        :param units: TemperatureUnits.consts
        :return: float
        """
        v, err = VelocityUnits.from_default(velocity.v, units)
        if err:
            return 0
        return v

    @property
    def v(self):
        return self._value

    @property
    def default_units(self):
        return self._default_units


if __name__ == '__main__':
    pass