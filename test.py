from BeautifulSoup import BeautifulSoup 

html = '<html>text <b>is</b> here</html>'
soup = BeautifulSoup(html)
text = soup.getText()
print text
#print soup.b
