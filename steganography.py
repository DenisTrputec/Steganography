import os
from PIL import Image


class Steganography:
    def __init__(self):
        self.__size = None
        self.breakpoint = '0' * 7


    def __img2binary(self, img_path):

        # Provjeri ispravnost slike
        if not os.path.exists(img_path):
            raise Exception("Ne postoji putanja izvorne slike!")
        elif not img_path.endswith(".png"):
            raise Exception("Izvorna slika mora biti .png ekstenzije!")


        # Otvori sliku i saznaj njenu veličinu
        img = Image.open(img_path)
        self.__size = img.size


        # Provjeri je li slika RGB
        if img.mode != 'RGB':
            raise Exception("Izvorna slika nije u RGB formata!")


        # Pretvori RGB (dekadske vrijednosti) u binarni zapis i dodaj u listu kao tuple-ove
        binary_data = []
        for r, g, b in img.getdata():
            binary_data.append((bin(r), bin(g), bin(b)))

        return binary_data


    def __binary2img(self, binary_data, img_path):

        # Provjeri ispravnost odredišne putanje
        if not os.path.exists(os.path.dirname(img_path)) and os.path.dirname(img_path) != "":
            raise Exception("Ne postoji putanja odredišne slike!")
        elif not img_path.endswith(".png"):
            raise Exception("Odredišna slika mora biti .png ekstenzije!")


        # Pretvori binarne vrijedosti tuple-ova u dekadski sustav
        image_data = []
        for r, g, b in binary_data:
            image_data.append((int(r, 2), int(g, 2), int(b, 2)))


        # Stvori novu sliku koja sadrži skriveni tekst
        img = Image.new(mode="RGB", size=self.__size)
        img.putdata(image_data)
        img.save(img_path)


    def __text2binary(self, text):

        # Provjeri je li upisan tekst
        if text == "":
            raise Exception("Nije upisan tekst za skrivanje!")


        # Kodiraj zadani tekst u ASCII
        byte_obj = text.encode('ascii')


        # Čitaj znak po znak u binarnom zapisu
        # Ignoriraj '0b' na početku zapisa
        # Ako znak koristi manje od 7 (toliko ih može biti maksimalno) nadopuni prazna mjesta s nulama
        # Svaki uređeni zapis znaka nadodaj na string varijablu 'binary_data'
        binary_data = ""
        for b in byte_obj:
            temp = bin(b)[2:]
            temp = '0' * (7 - len(temp)) + temp
            binary_data += temp

        # Dodaj točku završetka na kraj kako bi znali prilikom čitanja slike gdje skrivena poruka završava
        binary_data += self.breakpoint

        return binary_data


    @staticmethod
    def __binary2text(binary_text):
        # Grupiraj bitove po 7 i konvertiraj ih u dekadsku vrijednost koju se zatim konvertira u ASCII znak
        # Svi konvertirani znakovi se vraćaju kao jedan string
        text = ""
        for i in range(0, len(binary_text), 7):
            text += chr(int(binary_text[i:i+7], 2))
        return text


    def __return_secret_text_binary(self, binary_image):
        # Dohvaćaj zadnji bit crvene boje sve dok zadnjih sedam znamenki ne bude jednaka točki završetka
        # Vrati sve dohvaćene bitove kao string bez zadnjih sedam (oni su točka završetka koja se odbacuje)
        binary_text = ""
        for r, b, g in binary_image:
            binary_text += r[-1]
            if binary_text[-7:] == self.breakpoint:
                return binary_text[:-7]

        # Vrati 'None' ako nije pronađen uzorak jednak točki završetka (znači da nema skrivene poruke u slici)
        return None


    def hide(self, text, img_src, img_dest):
        """
        Metoda kao argumente prima tekst koji će se sakriti, putanju slike u koju će se sakriti
        te putanju na koju će biti pohranjena nova slika sa skrivenim tekstom.
        Metoda vraća None vrijednost
        """
        binary_image = self.__img2binary(img_src)
        binary_text = self.__text2binary(text)


        # Provjeri ima li slika manje binarnih tuple-ova nego tekst binarnih znamenki
        if len(binary_image) < len(binary_text):
            raise Exception("Slika je premala da mi se u nju sakrio zadani tekst")


        # Svaki bit teksta zapiši na mjesto bita najmanje značajnosti (LSB algoritam) crvene boje
        binary_image_new = []
        for i, bin_value in enumerate(binary_text):
            r, g, b = binary_image[i]
            r = r[:-1] + bin_value
            binary_image_new.append((r, g, b))

        # Ostatak tuple-ova (nepromjenjenih) dodaj u novi binarni zapis slike
        for i in range(len(binary_text), len(binary_image)):
            binary_image_new.append(binary_image[i])

        self.__binary2img(binary_image_new, img_dest)


    def reveal(self, img_path):
        """
        Metoda kao argument prima putanju slike i vraća string ako se u njoj nalazi skriveni tekst
        ili None ako ga nema skrivenog teksta
        """
        binary_image = self.__img2binary(img_path)
        binary_text = self.__return_secret_text_binary(binary_image)
        return self.__binary2text(binary_text)


if __name__ == '__main__':
    try:
        s = Steganography()
        # s.hide("Neki tekst", "src_image.png", "dest_image.png")
        s.reveal("dest_image.png")
    except Exception as e:
        print(e)
