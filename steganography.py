from PIL import Image


class Steganography:
    def __init__(self):
        self.src_path = None
        self.dest_path = None
        self.size = None
        self.breakpoint = '0' * 7

    def __img2binary(self, img_path):
        img = Image.open(img_path)
        self.src_path = img_path
        self.size = img.size

        if img.mode != 'RGB':
            print("Image is not in RGB mode!")
            return

        binary_data = []
        for r, g, b in img.getdata():
            binary_data.append((bin(r), bin(g), bin(b)))

        return binary_data

    def __binary2img(self, binary_data):
        image_data = []
        for r, g, b in binary_data:
            image_data.append((int(r, 2), int(g, 2), int(b, 2)))

        img = Image.new(mode="RGB", size=self.size)
        img.putdata(image_data)
        img.save(self.dest_path)

    def __text2binary(self, text):
        binary_data = ""

        byte_obj = text.encode('ascii')
        for b in byte_obj:
            temp = bin(b)[2:]
            temp = '0' * (7 - len(temp)) + temp
            binary_data += temp

        # Add breakpoint
        binary_data += self.breakpoint

        return binary_data

    def __binary2text(self, binary_text):
        text = ""
        for i in range(0, len(binary_text), 7):
            text += chr(int(binary_text[i:i+7], 2))
        return text

    def __return_secret_text_binary(self, binary_image):
        binary_text = ""
        for r, b, g in binary_image:
            binary_text += r[-1]
            if binary_text[-7:] == self.breakpoint:
                return binary_text[:-7]
        return None

    def hide(self, text, img_src, img_dest):
        self.src_path = img_src
        self.dest_path = img_dest
        binary_image = self.__img2binary(self.src_path)
        binary_text = self.__text2binary(text)
        binary_image_new = []

        if len(binary_image) < len(binary_text) / 7:
            raise Exception("Image is too small to hide a text inside!")

        for i, bin_value in enumerate(binary_text):
            r, g, b = binary_image[i]
            r = r[:-1] + bin_value
            binary_image_new.append((r, g, b))

        for i in range(len(binary_text), len(binary_image)):
            binary_image_new.append(binary_image[i])

        self.__binary2img(binary_image_new)

    def reveal(self, img_path):
        binary_image = self.__img2binary(img_path)
        binary_text = self.__return_secret_text_binary(binary_image)
        if binary_text is not None:
            text = self.__binary2text(binary_text)
            return text


if __name__ == '__main__':
    try:
        s = Steganography()
        # s.hide("Agram Uber Alles", "leclerc.png", "secret_leclerc.png")
        s.reveal("secret_leclerc.png")
    except Exception as e:
        print(e)
