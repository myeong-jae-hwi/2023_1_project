import pygame
import sys
import random
import librosa
import time


def Rithomgame_run():

    pygame.init()

    h, w = 600, 900
    screen = pygame.display.set_mode((w, h))
    font = pygame.font.SysFont("Courier", 18, True, True)
    text_color = (255, 255, 255)

    song = "sound/gd.mp3"  # replace with your song file

    pygame.mixer.music.load(song)

    # Load the song using librosa
    y, sr = librosa.load(song, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beats_timing = librosa.frames_to_time(beat_frames, sr=sr)

    current_beat = 0
    pygame.mixer.music.play()
    clock = pygame.time.Clock()

    class Block:
        # 초기값
        def __init__(self, x, y, dx):
            self.x = x
            self.y = y
            self.dx = dx
            self.width = 50
            self.created_time = time.time()
            self.hit = False

            # 업데이트
        def update(self):
            self.y += 1
            self.x += self.dx
            self.width = int(50 + (150 - 50) * (self.y / h))  # 블록의 크기 업데이트

        def draw(self):
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, 15))

        def process_note(self, key):
            if not self.hit and 500 < self.y < 650:
                if key == 'left' and self.dx < 0:
                    self.hit = True
                    return 10
                elif key == 'mid':
                    self.hit = True
                    return 10
                elif key == 'right' and self.dx > 0:
                    self.hit = True
                    return 10

                elif not self.hit and self.y > 600:
                    self.hit = True
                    return -10
            return 0

    def lerp_color(color1, color2, factor):
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor)
        )

    blocks = []
    tracks = [(250, 0, -0.24), (300, 0, -0.08), (350, 0, 0.08)]  # 트랙별 시작 위치와 x 이동 속도
    start_time = time.time() - 1  # Add this line to initialize start_time

    # 이펙트 색
    blue_points = [(300, 600), (250, 0), (400, 0), (350, 600)]

    Right_points = [(350, 600), (400, 0), (548, 0), (400, 600)]
    Left_points = [(250, 600), (108, 0), (252, 0), (300, 600)]
    black = (0, 0, 0)
    blue = (0, 0, 255)
    purple = (255, 0, 0)
    rect_width = 2

    Left = False
    Mid = False
    Right = False

    score = 0

    running = True

    # 게임 루프
    while running:
        screen.fill((0, 0, 0))  # 화면을 검은색으로 지우기
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    Mid = True
                    for block in blocks:
                        score += block.process_note('mid')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    Mid = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Left = True
                    for block in blocks:
                        score += block.process_note('left')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Left = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Right = True
                    for block in blocks:
                        score += block.process_note('right')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    Right = False

            print("점수 : ", score)

        if Mid:
            for i in range(blue_points[1][1], blue_points[0][1], rect_width):
                progress = (i - blue_points[1][1]) / (blue_points[0][1] - blue_points[1][1])
                color = lerp_color(black, blue, progress)
                top_left_x = int(blue_points[0][0] + (blue_points[1][0] - blue_points[0][0]) * progress)
                top_right_x = int(blue_points[3][0] + (blue_points[2][0] - blue_points[3][0]) * progress)

                pygame.draw.rect(screen, color, pygame.Rect(top_left_x, i, top_right_x - top_left_x, rect_width))

        if Right:
            for i in range(Right_points[1][1], Right_points[0][1], rect_width):
                progress = (i - Right_points[1][1]) / (Right_points[0][1] - Right_points[1][1])
                color = lerp_color(black, purple, progress)
                top_left_x = int(Right_points[0][0] + (Right_points[1][0] - Right_points[0][0]) * progress)
                top_right_x = int(Right_points[3][0] + (Right_points[2][0] - Right_points[3][0]) * progress)

                pygame.draw.rect(screen, color, pygame.Rect(top_left_x, i, top_right_x - top_left_x, rect_width))

        if Left:
            for i in range(Left_points[1][1], Left_points[0][1], rect_width):
                progress = (i - Left_points[1][1]) / (Left_points[0][1] - Left_points[1][1])
                color = lerp_color(black, purple, progress)
                top_left_x = int(Left_points[0][0] + (Left_points[1][0] - Left_points[0][0]) * progress)
                top_right_x = int(Left_points[3][0] + (Left_points[2][0] - Left_points[3][0]) * progress)

                pygame.draw.rect(screen, color, pygame.Rect(top_left_x, i, top_right_x - top_left_x, rect_width))

        # 사다리꼴 라인 그리기
        pygame.draw.line(screen, (255, 0, 255), (250, 0), (100, 640), 5)
        pygame.draw.line(screen, (255, 0, 255), (400, 0), (550, 640), 5)
        pygame.draw.line(screen, (1, 85, 255), (300, 0), (250, 640), 3)
        pygame.draw.line(screen, (1, 85, 255), (350, 0), (400, 640), 3)

        for block in blocks:
            block.update()
            block.draw()

        # 스코어 생성
        score_text = font.render(f"Score: {score}", True, text_color)

        screen.blit(score_text, (600, 50))
        pygame.display.flip()

        elapsed_time = time.time() - start_time

        if current_beat < len(beats_timing) and elapsed_time >= beats_timing[current_beat]:
            block_x, _, block_dx = random.choice(tracks)
            blocks.append(Block(block_x, 0, block_dx))
            current_beat += 1

    pygame.quit()
    sys.exit()


