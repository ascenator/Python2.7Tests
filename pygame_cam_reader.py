import pygame
import pygame.camera

pygame.camera.init()

cam = pygame.camera.Camera("/dev/video1",(640,480))

cam.start()

img = cam.get_image()

pygame.image.save(img,"filename.jpg")