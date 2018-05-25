# UTB-tf-py-module
uptobox python3.6 module to transfer files from url while watching the progress


### Python version
I developed/have tested this script
with the following python versions installed: 3.6.2 & 3.6.4

I know for a fact that it does not work without modification with a version earlier than 3.6 (due to the print statement switching to a command)


## Usage

Usage is very simple:

    from utb_rm_s import toUTB
    links = ['http://example.com/pdf1.pdf','http://example.com/pdf2.pdf']
    for idx,link in links:
      toUTB(link, idx = idx, max = len(links))
  
 Or techincally if you only want 1 URL transferred:

    from utb_rm_s import toUTB
    link = http://example.com/pdf.pdf
    toUTB(link)
    
    
 
 ## Don't forget!
Don't forget to modify the `$SESSION_ID` in the module accordingly!
    
### May be weired...  
The way it currently displays the filenames may seem a bit weired at first but this is on purpose. 
It's so that it can be fairly easily adapted to accept (in a 2nd edition) a list to handle...
### Please use english!
For any questions feel free to open a issue but please use proper english if you do so.
