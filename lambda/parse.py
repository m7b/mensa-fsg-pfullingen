import urllib.request
import pypdf
import io

class cMeal:
    def __init__(self, menu_url):
        self.page   = self.getMenu(menu_url)
        self.at_mon = self.getMeal('Montag')
        self.at_tue = self.getMeal('Dienst')
        self.at_wed = self.getMeal('Mittwo')
        self.at_thu = self.getMeal('Donner')

    def getMenu(self, menu_url):
        remote_file = urllib.request.urlopen(menu_url)
        memory_file = io.BytesIO(remote_file.read())
        read_pdf = pypdf.PdfReader(memory_file)
        number_of_pages = read_pdf.get_num_pages()
        #print(number_of_pages)

        pageObj = read_pdf.get_page(0)
        page = pageObj.extract_text()
        #print (page)
        return page

    def getMeal(self, day_token):
        start = self.page.find(day_token)
        ende  = self.page.find('\n \n', start)
        meal  = self.page[start:ende]
        meal  = self.correct_date(meal)
        meal  = self.correct_mittwoch(meal)
        meal  = self.correct_space_comma(meal)
        meal  = self.correct_comma_space_space(meal)
        meal  = self.correct_space_space(meal)
        meal  = self.remove_additives(meal)
        meal  = self.remove_allergy_triggers(meal)
        return meal
    
    def correct_date(self, meal):
        return meal.replace(' .', '.')
    
    def correct_mittwoch(self, meal):
        return meal.replace('Mittwo ch', 'Mittwoch')
    
    def correct_space_comma(self, meal):
        return meal.replace(' ,', ',')
    
    def correct_comma_space_space(self, meal):
        return meal.replace(',  ', ', ')
    
    def correct_space_space(self, meal):
        return meal.replace('  ', ' ')
    
    def remove_additives(self, meal):
        return meal
    
    def remove_allergy_triggers(self, meal):
        return meal

