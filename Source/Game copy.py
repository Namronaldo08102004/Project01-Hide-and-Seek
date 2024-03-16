import pygame
import sys

from Level1 import *

if len(sys.argv) != 2:
    sys.exit("Usage: python Game.py input.txt")
map = Map(sys.argv[1])

pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

image = pygame.image.load('../Image/hide-and-seek.jpg')
scaled_image = pygame.transform.scale(image, size)

seeker_image = pygame.image.load('../Image/Seeker.png')
hider_image = pygame.image.load('../Image/Hider.png')
announcement_image = pygame.image.load('../Image/Announcement.png')

level = None
game = None
startGame = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    screen.fill(LIGHTPINK)
    
    #! Let user choose a level
    if level is None:
        screen.blit(scaled_image, (0,0))
        
        #! Draw title
        title = largeFont.render("Hide and Seek", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = (935, 75)
        screen.blit(title, titleRect)

        #! Draw a frame
        Frame = pygame.Rect(725, 150, 425, 425)
        pygame.draw.rect(screen, LIGHTBLUE, Frame)
        
        #! Draw buttons
        Level_1 = pygame.Rect(725, 150, 200, 200)
        playLevel1 = mediumFont.render("Level 1", True, BLACK)
        playLevel1Rect = playLevel1.get_rect()
        playLevel1Rect.center = Level_1.center
        pygame.draw.rect(screen, WHITE, Level_1)
        screen.blit(playLevel1, playLevel1Rect)

        Level_2 = pygame.Rect(950, 150, 200, 200)
        playLevel2 = mediumFont.render("Level 2", True, BLACK)
        playLevel2Rect = playLevel2.get_rect()
        playLevel2Rect.center = Level_2.center
        pygame.draw.rect(screen, WHITE, Level_2)
        screen.blit(playLevel2, playLevel2Rect)
        
        Level_3 = pygame.Rect(725, 375, 200, 200)
        playLevel3 = mediumFont.render("Level 3", True, BLACK)
        playLevel3Rect = playLevel3.get_rect()
        playLevel3Rect.center = Level_3.center
        pygame.draw.rect(screen, WHITE, Level_3)
        screen.blit(playLevel3, playLevel3Rect)
        
        Level_4 = pygame.Rect(950, 375, 200, 200)
        playLevel4 = mediumFont.render("Level 4", True, BLACK)
        playLevel4Rect = playLevel4.get_rect()
        playLevel4Rect.center = Level_4.center
        pygame.draw.rect(screen, WHITE, Level_4)
        screen.blit(playLevel4, playLevel4Rect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if Level_1.collidepoint(mouse):
                level = 1
                game = Level1(map)
            elif Level_2.collidepoint(mouse):
                level = 2
                sys.exit()  
            elif Level_3.collidepoint(mouse):
                level = 3
                sys.exit()
            elif Level_4.collidepoint(mouse):
                level = 4
                sys.exit()
    else:
        #! Level 1
        if (level == 1):
            if (len(map.listHiderPositions) != 1):
                raise Exception("This is not a map for Level 1")
            
            cellSize = (int(height / map.numRows), int(1000 / map.numCols))
            
            #! Draw a score cell
            Score = pygame.Rect(cellSize[1] * map.numCols + (width - cellSize[1] * map.numCols) / 2 - 70, height / 3 - 25, 140, 50)
            scoreLevel = mediumFont.render(f"Score: {game.score}", True, BLACK)
            scoreLevelRect = scoreLevel.get_rect()
            scoreLevelRect.center = Score.center
            pygame.draw.rect(screen, WHITE, Score)
            screen.blit(scoreLevel, scoreLevelRect)
            
            #! Draw a frame
            Frame = pygame.Rect(0, 0, cellSize[1] * map.numCols, cellSize[0] * map.numRows)
            pygame.draw.rect(screen, WHITE, Frame)
            
            #! Draw the map
            blocks = []
            for row in range (0, map.numRows):
                temp = []
                for col in range (0, map.numCols):
                    #! Draw empty cells
                    if (map.matrix[row][col] == EMPTY):
                        rect = pygame.Rect(
                            col * cellSize[1],
                            row * cellSize[0],
                            cellSize[1], cellSize[0]
                        )
                        pygame.draw.rect(screen, BLACK, rect, 2)
                        temp.append((rect, BLACK, 2))
                    
                    #! Draw wall cells
                    elif (map.matrix[row][col] == WALL):
                        rect = pygame.Rect(
                            col * cellSize[1],
                            row * cellSize[0],
                            cellSize[1], cellSize[0]
                        )
                        
                        check = False
                        #? Check whether map.matrix[row][col] is a position of any obstacle or not
                        for k in range (0, len(map.obstacles)):
                            if (row + 1 >= map.obstacles[k][0] and row + 1 <= map.obstacles[k][2] and
                                col + 1 >= map.obstacles[k][1] and col + 1 <= map.obstacles[k][3]):
                                check = True
                                break
                            
                        if (not check):
                            pygame.draw.rect(screen, GRAY, rect)
                            temp.append((rect, GRAY, None))
                        else:
                            pygame.draw.rect(screen, SKINCOLOR, rect)
                            temp.append((rect, SKINCOLOR, None))
                        
                    #! Draw hider cell
                    elif (map.matrix[row][col] == HIDER):
                        rect = pygame.Rect(
                            col * cellSize[1],
                            row * cellSize[0],
                            cellSize[1], cellSize[0]
                        )
                        pygame.draw.rect(screen, BLACK, rect, 2)
                        scaled_hider_image = pygame.transform.scale(hider_image, (cellSize[1], cellSize[0]))
                        screen.blit(scaled_hider_image, (col * cellSize[1], row * cellSize[0]))
                        temp.append((rect, BLACK, 2))
                    
                    #! Draw seeker cell
                    elif (map.matrix[row][col] == SEEKER):
                        if ((row, col) == game.seekerPosition):
                            rect = pygame.Rect(
                                col * cellSize[1],
                                row * cellSize[0],
                                cellSize[1], cellSize[0]
                            )
                            pygame.draw.rect(screen, BLACK, rect, 2)
                            scaled_seeker_image = pygame.transform.scale(seeker_image, (cellSize[1], cellSize[0]))
                            screen.blit(scaled_seeker_image, (col * cellSize[1], row * cellSize[0]))
                            temp.append((rect, BLACK, 2))
                        
                        else:
                            rect = pygame.Rect(
                                col * cellSize[1],
                                row * cellSize[0],
                                cellSize[1], cellSize[0]
                            )
                            pygame.draw.rect(screen, BLACK, rect, 2)
                            temp.append((rect, BLACK, 2))
                            
                            row = game.seekerPosition[0]
                            col = game.seekerPosition[1]
                            scaled_seeker_image = pygame.transform.scale(seeker_image, (cellSize[1], cellSize[0]))
                            screen.blit(scaled_seeker_image, (col * cellSize[1], row * cellSize[0]))
                    
                    #! Draw announcement cell
                    elif (game.announcement is not None and (row, col) == game.announcement):
                        scaled_announcement_image = pygame.transform.scale(announcement_image, (cellSize[1], cellSize[0]))
                        screen.blit(scaled_announcement_image, (game.announcement[1] * cellSize[1], game.announcement[0] * cellSize[0]))
                        
                blocks.append(temp)
            
            Start = pygame.Rect(cellSize[1] * map.numCols + (width - cellSize[1] * map.numCols) / 2 - 50, height / 2 - 25, 100, 50)
            startLevel = mediumFont.render("Start", True, BLACK)
            startLevelRect = startLevel.get_rect()
            startLevelRect.center = Start.center
            pygame.draw.rect(screen, WHITE, Start)
            screen.blit(startLevel, startLevelRect)
            
            click1, _, _ = pygame.mouse.get_pressed()
            if click1 == 1 and startGame == False:
                mouse = pygame.mouse.get_pos()
                if Start.collidepoint(mouse):
                    startGame = True
            
            if (startGame):
                #! Hide the Start cell
                start = pygame.Rect(cellSize[1] * map.numCols + (width - cellSize[1] * map.numCols) / 2 - 50, height / 2 - 25, 100, 50)
                pygame.draw.rect(screen, LIGHTPINK, start)
                
                #! Draw observable cells
                for cell in game.listObservableCells:
                    rect = blocks[cell[0]][cell[1]][0]
                    pygame.draw.rect(screen, RED, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
                
                exitGame = False
                restartGame = False
                if (game.seekerPosition == game.hiderPosition):
                    Restart = pygame.Rect(cellSize[1] * map.numCols + (width - cellSize[1] * map.numCols) / 2 - 50, 2 * (height / 3) - 100, 100, 50)
                    restartLevel = mediumFont.render("Restart", True, BLACK)
                    restartLevelRect = restartLevel.get_rect()
                    restartLevelRect.center = Restart.center
                    pygame.draw.rect(screen, WHITE, Restart)
                    screen.blit(restartLevel, restartLevelRect)
                    
                    Exit = pygame.Rect(cellSize[1] * map.numCols + (width - cellSize[1] * map.numCols) / 2 - 50, 2 * (height / 3) - 25, 100, 50)
                    exitLevel = mediumFont.render("Exit", True, BLACK)
                    exitLevelRect = exitLevel.get_rect()
                    exitLevelRect.center = Exit.center
                    pygame.draw.rect(screen, WHITE, Exit)
                    screen.blit(exitLevel, exitLevelRect)
                    
                    pygame.display.flip()
                    
                    click2, _, _ = pygame.mouse.get_pressed()
                    if click2 == 1:
                        mouse = pygame.mouse.get_pos()
                        if Restart.collidepoint(mouse):
                            restartGame = True
                        if Exit.collidepoint(mouse):
                            exitGame = True
                            
                    if (exitGame):
                        game = None
                        level = None
                        startGame = False
                        pygame.display.flip()
                        continue
                    elif (restartGame):
                        game = Level1(map)
                        pygame.display.flip()
                        continue
                    else:
                        pygame.display.flip()
                        continue
                
                pygame.time.delay(1000)
                if (game.takeTurn == SEEKER):
                    for cell in game.listObservableCells:
                        rect = blocks[cell[0]][cell[1]][0]
                        pygame.draw.rect(screen, WHITE, rect)
                        pygame.draw.rect(screen, BLACK, rect, 2)
                    
                    game.seekerTakeTurn()
                    
                    game.takeTurn = HIDER
                    if (game.seekerPosition != game.hiderPosition):
                        game.numSeekerSteps = game.numSeekerSteps + 1
                        game.score = game.score - 1
                    else:
                        game.score = game.score + 20
                if (game.takeTurn == HIDER):
                    game.hiderTakeTurn()
                    game.takeTurn = SEEKER
                    if (game.seekerPosition != game.hiderPosition):
                        game.numHiderSteps = game.numHiderSteps + 1
                        if (game.announcementTime is not None and game.announcementTime < 2):
                            scaled_announcement_image = pygame.transform.scale(announcement_image, (cellSize[1], cellSize[0]))
                            screen.blit(scaled_announcement_image, (game.announcement[1] * cellSize[1], game.announcement[0] * cellSize[0]))
                            game.announcementTime = game.announcementTime + 1
                        else:
                            #! After 2 steps, the announcement disappears
                            if (game.announcementTime is not None):
                                rect = blocks[game.announcement[0]][game.announcement[1]][0]
                                color = blocks[game.announcement[0]][game.announcement[1]][1]
                                w = blocks[game.announcement[0]][game.announcement[1]][2]
                                
                                if (w is not None):
                                    pygame.draw.rect(screen, WHITE, rect)
                                    pygame.draw.rect(screen, color, rect, w)
                                else:
                                    pygame.draw.rect(screen, color, rect)
                            
                                game.announcement = None
                                game.announcementTime = None
                    
        #! Level 2
        elif (level == 2):
            pass
        
        #! Level 3
        elif (level == 3):
            pass
        
        #! Level 4
        else:
            pass
                
    pygame.display.flip()