

import wget

url = "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"

filename = wget.download(url)