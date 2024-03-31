from UI.App.App import App
import pygame


app = App()
try:
    app.run()
except Exception as e:
    print(e)
    pygame.quit()
    quit()
