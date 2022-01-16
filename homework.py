from typing import List, ClassVar
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    INFO: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )
    training_type: str
    duration: int
    distance: int
    speed: int
    calories: int

    def get_message(self) -> str:
        return self.INFO.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action_step = action
        self.duration_m = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_step * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_m

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__, self.duration_m,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )

    def convert_hour_in_min(self) -> int:
        """Конвертировать время тренировки из часов в минуты"""
        return self.duration_m * self.MIN_IN_HOUR


class Running(Training):
    """Тренировка: бег.
    Формула расчёта потраченных калорий: (18 * средняя_скорость – 20)
    * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах"""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_CALORIE_1
             * self.get_mean_speed() - self.COEFF_CALORIE_2) * self.weight_kg
            / self.M_IN_KM * self.convert_hour_in_min()
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Формула расчёта потраченных калорий: (0.035 * вес + (скорость ** 2 // рост)
    * 0.029 * вес) * время_тренировки_в_минутах"""

    COEFF_WEIGHT_1: float = 0.035
    COEFF_WEIGHT_2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_WEIGHT_1 * self.weight_kg
             + (self.get_mean_speed() ** 2 // self.height_cm)
             * self.COEFF_WEIGHT_2 * self.weight_kg)
            * self.convert_hour_in_min()
        )


class Swimming(Training):
    """Тренировка: плавание.
    Формула расчета средней скорости: длина_бассейна * count_pool / M_IN_KM
    / время_тренировки
    Формула расчета потраченных калорий: (средняя скорость + 1.1) * 2 * вес"""

    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool_m = length_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool_m * self.count_pool
            / self.M_IN_KM / self.duration_m
        )

    def get_spent_calories(self, coeff_speed=1.1, coeff_weight=2) -> float:
        return (
            (self.get_mean_speed() + coeff_speed)
            * coeff_weight * self.weight_kg
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for key in training_type:
        if key in training_type:
            return training_type[workout_type](*data)
        else:
            return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
