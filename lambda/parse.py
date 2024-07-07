import urllib.request
import pypdf
import io
import luapatt
import datetime

class cMeal:
    def __init__(self, menu_url):
        self.page   = self.getMenu(menu_url)
        self.at_mon = self.getMeal('Montag', 'Dienst')
        self.at_tue = self.getMeal('Dienst', 'Mittw')
        self.at_wed = self.getMeal('Mittwo', 'Donner')
        self.at_thu = self.getMeal('Donner', '\n\n')

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

    def getMeal(self, day_token, next_day_token):
        start = self.page.find(day_token)
        ende  = self.page.find(next_day_token, start)
        meal  = self.page[start:ende]
        if not meal.find(day_token):
            meal  = self.correct_space_dot(meal)
            meal  = self.correct_mittwoch(meal)
            meal  = self.correct_space_comma(meal)
            meal  = self.correct_comma_space_space(meal)
            meal  = self.correct_space_space(meal)
            meal  = self.add_sentence_end(meal)
            meal  = self.remove_additives(meal)
            meal  = self.remove_allergy_triggers(meal)
            meal  = self.correct_space_dot(meal)
            meal  = self.add_final_dot(meal)
            meal  = self.correct_space_dot(meal)
            meal  = self.correct_space_comma(meal)
        else:
            meal = 'Sorry, nix aufm Plan.'
        return meal
    
    def correct_space_dot(self, meal):
        return meal.replace(' .', '.')
    
    def correct_mittwoch(self, meal):
        return meal.replace('Mittwo ch', 'Mittwoch')
    
    def correct_space_comma(self, meal):
        return meal.replace(' ,', ',')
    
    def correct_comma_space_space(self, meal):
        return meal.replace(',  ', ', ')
    
    def correct_space_space(self, meal):
        return meal.replace('  ', ' ')
    
    def add_sentence_end(self, meal):
        return meal.replace('\n', '.\n')
    
    def remove_additives(self, meal):
        meal = luapatt.gsub(meal, '%b()', '')
        return meal
    
    def remove_allergy_triggers(self, meal):
        return meal
    
    def add_final_dot(self, meal):
        return meal + '.'
    
    def get_todays_meal(self):
        today = datetime.datetime.today()
        if today.weekday() == 0:
            retval = self.at_mon
        elif today.weekday() == 1:
            retval = self.at_tue
        elif today.weekday() == 2:
            retval = self.at_wed
        elif today.weekday() == 3:
            retval = self.at_thu
        else:
            retval = "... hmm.. für heute steht ja gar nichts auf dem Plan."
        return retval

