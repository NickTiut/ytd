import pygame

class GUI():
    
    def __init__(self):
        pygame.init()

        self.custom_font = pygame.font.SysFont('Helvetica', 15)
        self.custom_font_1 = pygame.font.SysFont('Helvetica', 12)

        self.settings_image = pygame.image.load('settings.png')
        self.play_image = pygame.image.load('play.png')
        self.icon = pygame.image.load('youtube_icon.png')

        self.w_main = 500
        self.h_main = 500
        self.w_start = 500
        self.h_start = 500

        pygame.display.set_caption('YouTube Downloader')
        pygame.display.set_icon(self.icon)

        self.running()

    def running(self):
        configured_id = False
        running = True
        while running:
            if configured_id:
                screen = pygame.display.set_mode((self.w_main, self.h_main), 0, 32)

                while configured_id:
                    screen.fill((0, 0, 0))
                    text = self.custom_font.render('Playlist:', True, (255, 255, 255))
                    screen.blit(text, (150, 20))
                    text = self.custom_font_1.render('...here will be inserted the name of the pl...', True, (255, 255, 255))
                    screen.blit(text, (100, 40))
                    output = '...this will be the output...'
                    text = self.custom_font_1.render(str(output), True, (255, 255, 255))
                    screen.blit(text, (100, 100))
                    screen.blit(self.settings_image, (400, 400))
                    settings_rect = pygame.Rect(400, 400, self.settings_image.get_width(), self.settings_image.get_height())
                    screen.blit(self.play_image, (100, 400))
                    play_rect = pygame.Rect(100, 400, self.play_image.get_width(), self.play_image.get_height())
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.display.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = pygame.mouse.get_pos()
                                if settings_rect.collidepoint(x, y):
                                    print 'settings'
                                elif play_rect.collidepoint(x, y):
                                    print 'play'

            else:
                left_click = False
                right_click = False
                copied = False

                screen = pygame.display.set_mode((self.w_start, self.h_start), 0, 32)
                while not configured_id:
                    
                    screen.fill((0, 0, 0))
                    text_1 = self.custom_font.render('Enter playlist ID or YouTube link', True, (255, 255, 255))
                    screen.blit(text_1, (50, 50))
                    rect = pygame.Rect(50, 200, 400, 100)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                    if copied:
                        text_2 = self.custom_font.render(str(text[:-1]), True, (255, 255, 255))
                        screen.blit(text_2, (75, 250))
                    if right_click:
                        right_click_rect = pygame.Rect(x, y, 50, 20)
                        pygame.draw.rect(screen, (170, 170, 170), right_click_rect, 0)
                        text_3 = self.custom_font.render('Paste', True, (255, 255, 255))
                        screen.blit(text_3, (x + 10, y))
                        
                    pygame.display.update()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.display.quit()        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = pygame.mouse.get_pos()
                            if rect.collidepoint(x, y):
                                if event.button == 1:                                
                                    left_click = True
                                if event.button == 3:
                                    right_click = True
                            elif right_click and right_click_rect.collidepoint(x, y):
                                pygame.scrap.init()
                                try:
                                    text = pygame.scrap.get('text/plain')
                                    copied = True
                                except TypeError:
                                    pass
                                                              
                                
                                    
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                if copied and click:
                                    configured_id = True

                    if left_click:
                        key = pygame.key.get_pressed()
                        if key[pygame.K_LCTRL] and key[pygame.K_v]:
                            pygame.scrap.init()
                            try:
                                text = pygame.scrap.get('text/plain')
                                copied = True
                            except TypeError:
                                pass
                            pygame.time.wait(250)


                        
GUI()
















        
