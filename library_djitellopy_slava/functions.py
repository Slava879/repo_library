from djitellopy import Tello
import time

def centering_the_mission_pad(tello: Tello, x: int, y: int, z: int, speed: int = 10) -> None:
    tello.go_xyz_speed(-x, -y, -z, speed)

def direction_speed(direction: str = 'forward') -> (int, int, int):
    if direction == 'forward':
        return 0, 1, 0
    elif direction == 'back':
        return 0, -1, 0
    elif direction == 'left':
        return -1, 0, 0
    elif direction == 'right':
        return 1, 0, 0
    elif direction == 'up':
        return 0, 0, 1
    elif direction == 'down':
        return 0, 0, -1

def search_for_a_mission_pad(tello: Tello, direction: str = 'forward', target_pad_id: int = 0, speed: int = 10, max_search_time: int = 10) -> int | None:

    x, y, z = direction_speed(direction)
    x, y, z = x * speed, y * speed, z * speed

    tello.enable_mission_pads()
    tello.set_mission_pad_detection_direction(0)
    print("Распознавание карточек включено")
    time.sleep(1)

    print("Начинаю движение вперёд...")
    start_time = time.monotonic()
    found_pad = -1
    try:
        while time.monotonic() - start_time < max_search_time:

            pad_id = tello.get_mission_pad_id()
            if pad_id != -1 and (target_pad_id == 0 or pad_id == target_pad_id):
                found_pad = pad_id
                tello.send_rc_control(0, 0, 0, 0)
                print(f"Найдена карточка №{found_pad}!")
                break

            tello.send_rc_control(
                x,  # Влево / вправо
                y,  # Вперёд / назад
                z,  # Вверх / вниз
                0  # Поворот
            )

            time.sleep(0.1)

        # Если карточка не найдена за отведённое время
        if found_pad == -1:
            tello.send_rc_control(0, 0, 0, 0)
            print("Время поиска закончилось!")

        # Ожидаем остановки
        time.sleep(1)
        return found_pad

    except KeyboardInterrupt:
        print("Программа остановлена пользователем")

    except Exception as error:
        print(f"Ошибка: {error}")

    finally:
        try:
            tello.send_rc_control(0, 0, 0, 0)
            tello.disable_mission_pads()

        except Exception as error:
            print(f"Ошибка завершения: {error}")
