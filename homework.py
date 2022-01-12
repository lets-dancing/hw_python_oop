from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        info = (f'Тип тренировки: {self.training_type}; '
        f'Длительность: {self.duration:.3f} ч.; '
        f'Дистанция: {self.distance:.3f} км; '
        f'Ср. скорость: {self.speed:.3f} км/ч; '
        f'Потрачено ккал: {self.calories:.3f}.')
        return info


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
   
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action*self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = Training.get_distance(self) / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage (type(self).__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self,
                           coeff_calorie_1 = 18, 
                           coeff_calorie_2 = 20) -> float:
        min_in_hour = self.duration * 60
        # формула расчёта (18 * средняя_скорость – 20) * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        spent_cal_run = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) * self.weight / Training.M_IN_KM * min_in_hour
        return spent_cal_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self, coeff_weight1 = 0.035, coeff_weight2 = 0.029) -> float:
        min_in_hour = self.duration * 60
        # формула расчёта (0.035 * вес + (скорость ** 2 // рост) * 0.029 * вес) * время_тренировки_в_минутах
        spent_cal_wlk = (coeff_weight1 * self.weight + (self.get_mean_speed() ** 2 // self.height) * coeff_weight2 * self.weight) * min_in_hour
        return spent_cal_wlk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    
    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool
    
    def get_mean_speed(self) -> float:
        # формула расчёта длина_бассейна * count_pool / M_IN_KM / время_тренировки
        mean_speed_swm = self.length_pool * self.count_pool / Training.M_IN_KM / self.duration
        return mean_speed_swm
    
    def get_spent_calories(self, coeff_speed = 1.1, coeff_weight = 2) -> float:
        # формула расчёта (скорость + 1.1) * 2 * вес
        spent_cal_swm = (self.get_mean_speed() + coeff_speed) * coeff_weight * self.weight
        return spent_cal_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.""" 
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print (info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

