# SIMPLE IMAGE FILTER
This python program performs various image manipulation techniques using OpenCV to apply photoshop or instagram-like filters.
Please be aware that some of the results may differ depending on the input image used, even if the same filter is applied.

## Dependencies:
* Python - 3.10.5
* OpenCV - 4.6.0
* Numpy - 1.22.4
* Streamlit - 1.10.0 (Only required to run the streamlit app version)

## How to use:
Once all dependencies have been installed, run the program contained in the 'src' folder with:

```console
    $ python ImageFilter.py
```
As expected, you'll be asked to enter the input image path.
After that, a new window will pop up showing the result of applying each filter available. Just choose which one you'd like to save.

![alt text](https://github.com/Josgonmar/Simple-image-filters/blob/master/visuals/interface.jpg?raw=false)

*Note that the selected images are remarked with a red rectangle. Select or deselect using the mouse click.*

Inside the *visuals* folder you'll find several demo images to try the code.

### Streamlit:
To run the Streamlit app locally, just go to the folder where *ImageFilterApp.py* is contained and type:

```console
    $ streamlit run ImageFilterApp.py
```
A new window will be opened in your favourite web browser where you can preform the exact same thing as in the python program, but in a much more user-friendly way!

## License:
Feel free to use this program however you like!
