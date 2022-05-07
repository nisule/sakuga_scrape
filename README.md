# sakugabooru_download
Downloads and renames video clips from sakugabooru.com

Clips are saved locally with the file name renamed to be the source plus a list of all the tags

For example, using https://www.sakugabooru.com/post/show/167485 will download the video on this URL and save the video as:

**artist unknown naruto naruto (2002) naruto movie 3 guardians of the crescent moon animated character acting.mp4**

the script removes invalid windows file name characters.

You may need to enable long file name support, link to instructions: https://www.itprotoday.com/windows-10/enable-long-file-name-support-windows-10 as some clips have very long tags

## Usage
-Change the file path in the main method to be where your local urls.txt file is

-fill the urls.txt file with a list of urls you want to download files from. 1 url per line e.g.
> https://www.sakugabooru.com/post/show/167485
> 
> https://www.sakugabooru.com/post/show/167596
>
> https://www.sakugabooru.com/post/show/164555
