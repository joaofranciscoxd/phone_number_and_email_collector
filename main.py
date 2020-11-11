import re
import requests
from collections import deque
from selenium import webdriver

def main():
    f = open('links_to_search.txt', 'r')
    lines = f.readlines()
    links = list()
    for a in lines:
        a = a.replace('\n', '')
        links.append(a)
        print(a)
    f.close()
    print("Quantity of links: " + str(len(links)))

    def checa_link(site):
        original_url = site
        unscraped = deque([original_url])
        while len(unscraped):
            url = unscraped.popleft()
            print("Crawling URL %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as erro_louco:
                print("{}!Trying in another way...".format(erro_louco))
                driver = webdriver.Chrome(r".\Chromedriver\chromedriver.exe")
                driver.set_window_size(width=0, height=0)
                driver.get(original_url)
                element = driver.find_element_by_xpath("//body")
                driver.quit()
                html_content = element.get_attribute('outerHTML')
                texto = html_content
                remove_trash = re.sub(r"<[^<>]+?>", "", texto)
                regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$", flags=re.MULTILINE | re.I)
                texto = list(regex.findall(remove_trash))
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{5}-[\d]{4}", texto))
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{4}-[\d]{4}", texto))
                for lista in telefone:
                    for num in lista:
                        if (len(num)) < 14 and (len(num) > 13):
                            telefone.remove(lista)
                new_emails = re.findall(r"[\w\.-]+@[\w\.-]+", texto, re.I)
            texto = response.text
            remove_trash = re.sub(r"<[^<>]+?>", "", texto)
            regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$", flags=re.MULTILINE | re.I)
            texto = str(regex.findall(remove_trash))
            telefone = list()
            if "Not Acceptable!" in (texto):
                print("Not Acceptable!Trying in another way...")
                driver = webdriver.Chrome(r".\Chromedriver\chromedriver.exe")
                driver.set_window_size(width=0, height=0)
                driver.get(original_url)
                element = driver.find_element_by_xpath("//body")
                driver.quit()
                html_content = element.get_attribute('outerHTML')
                texto = html_content
                remove_trash = re.sub(r"<[^<>]+?>", "", texto)
                regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$", flags=re.MULTILINE | re.I)
                texto = list(regex.findall(remove_trash))
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{5}-[\d]{4}", texto))
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{4}-[\d]{4}", texto))
                for lista in telefone:
                    for num in lista:
                        if (len(num)) < 14 and (len(num) > 13):
                            telefone.remove(lista)
                new_emails = re.findall(r"[\w\.-]+@[\w\.-]+", texto, re.I)
            elif "Not Acceptable!" not in (texto):
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{5}-[\d]{4}", texto))
                telefone.append(re.findall(r"[(][\d]{2}[)][ ]?[\d]{4}-[\d]{4}", texto))
                for lista in telefone:
                    for num in lista:
                        if (len(num)) < 14 and (len(num) > 13):
                            telefone.remove(lista)
                new_emails = re.findall(r"[\w\.-]+@[\w\.-]+", texto, re.I)
            for analise1 in telefone:
                if len(analise1) == 0:
                    telefone.remove(analise1)
            for analise2 in new_emails:
                if len(analise2) == 0:
                    new_emails.remove(analise2)
            telefones = list(set(list(telefone[0])))
            if len(telefones) > 0:
                print(telefones)
                f_telefone = open("txts/links_phone_numbers.txt", "a")
                f_telefone.write("LINK: {} \nPHONE NUMBERS: {}\n".format(site, telefones))
                f_telefone.close()
            else:
                print("No phone numbers or blocked!")
                sem_telefones = open("txts/no_phone_numbers.txt", "a")
                sem_telefones.write("LINK: {}\n".format(original_url))
                sem_telefones.close()
            if len(new_emails) > 0:
                emails_validos = list()
                for email in new_emails:
                    if ".com" in email:
                        emails_validos.append(email)
                        print("Valid email!: {}".format(email))
                    else:
                        print("Invalid email: {}".format(email))
                f_email = open("txts/links_email.txt", "a")
                f_email.write("LINK: {} \nEMAIL: {} \n".format(site, emails_validos))
                f_email.close()
                print(emails_validos)
            else:
                print("No emails or blocked!")
                sem_email = open("txts/no_email.txt", "a")
                sem_email.write("LINK: {}\n".format(original_url))
                sem_email.close()
    erros_links = 0
    for num_site in range(0, (len(links))):
        try:
            print("LINK N° {}°".format(num_site + 1))
            checa_link(links[num_site])
        except Exception as e:
            erros_links = erros_links + 1
            print("TYPE OF ERROR: {}".format(e))
            ("Quantity of erros: {}".format(erros_links))
            print("Link with error: {}".format(links[num_site]))
            erro = open("txts/links_error.txt", "a")
            erro.write("TYPE OF ERROR: {}\n".format(e))
            erro.write("Quantity of erros: {}\n".format(erros_links))
            erro.write("Link with error: {}\n".format(links[num_site]))
            erro.close()
if __name__ == '__main__':
    main()
