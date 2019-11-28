import logging


class FakeEpd:

    def init(self):
        logging.info('INIT')

    def Clear(self):
        logging.info('CLEAR')

    def sleep(self):
        logging.info('SLEEP')

    def display(self, img):
        logging.info('DISPLAY')

    def getbuffer(self, image):
        self.height = 384
        self.width = 640

        buf = [0x00] * int(self.width * self.height / 4)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        logging.debug('imwidth = %d  imheight =  %d ',imwidth, imheight)
        if(imwidth == self.width and imheight == self.height):
            print('A')
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] < 64:           # black
                        buf[int((x + y * self.width) / 4)] &= ~(0xC0 >> (x % 4 * 2))
                    # elif pixels[x, y] < 192:     # convert gray to red
                    #     buf[int((x + y * self.width) / 4)] &= ~(0xC0 >> (x % 4 * 2))
                    #     buf[int((x + y * self.width) / 4)] |= 0x40 >> (x % 4 * 2)
                    else:                           # white
                        buf[int((x + y * self.width) / 4)] |= 0xC0 >> (x % 4 * 2)
        elif(imwidth == self.height and imheight == self.width):
            print('AB')
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] < 64:           # black
                        buf[int((newx + newy*self.width) / 4)] &= ~(0xC0 >> (y % 4 * 2))
                    # elif pixels[x, y] < 192:     # convert gray to red
                    #     buf[int((newx + newy*self.width) / 4)] &= ~(0xC0 >> (y % 4 * 2))
                    #     buf[int((newx + newy*self.width) / 4)] |= 0x40 >> (y % 4 * 2)
                    else:                           # white
                        buf[int((newx + newy*self.width) / 4)] |= 0xC0 >> (y % 4 * 2)
        return buf