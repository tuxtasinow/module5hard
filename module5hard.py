import hashlib
import time


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __eq__(self, other):
        return self.nickname == other.nickname and self.password == other.password

    def __str__(self):
        return f'{self.nickname}, {self.age}'


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __str__(self):
        return f'{self.title}, {self.duration} сек.'


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        hashed_password = self._hash_password(password)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                print(f'{nickname} успешно вошёл в систему')
                return
        print('Неверный логин или пароль')

    def register(self, nickname, password, age):
        if any(user.nickname == nickname for user in self.users):
            print(f'Пользователь {nickname} уже существует')
        else:
            new_user = User(nickname, password, age)
            self.users.append(new_user)
            self.current_user = new_user
            print(f'Пользователь {nickname} успешно зарегистрирован')

    def log_out(self):
        if self.current_user:
            print(f'{self.current_user.nickname} вышел из системы')
            self.current_user = None
        else:
            print('Никто не вошел в систему')

    def add(self, *videos):
        for video in videos:
            if any(v.title == video.title for v in self.videos):
                print(f'Видео "{video.title}" уже существует на платформе')
            else:
                self.videos.append(video)
                print(f'Видео "{video.title}" добавлено на платформу')

    def get_videos(self, search_word):
        search_word_lower = search_word.lower()
        result = [video.title for video in self.videos if search_word_lower in video.title.lower()]
        return result

    def watch_video(self, title):
        if not self.current_user:
            print('Войдите в аккаунт, чтобы смотреть видео')
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print('Вам нет 18 лет, пожалуйста покиньте страницу')
                    return
                self._play_video(video)
                return
        print(f'Видео "{title}" не найдено')

    def _play_video(self, video):
        for i in range(video.time_now + 1, video.duration + 1):
            print(i, end=' ')
            video.time_now = i
            time.sleep(1)  # Имитация воспроизведения
        print('Конец видео')
        video.time_now = 0

    def _hash_password(self, password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')