# SIMPLE IMAGE FILTER
This python program performs various image manipulation techniques using OpenCV to apply photoshop or instagram-like filters.
Please be aware that some of the results may differ depending on the input image used, even if the same filter is applied.

## Dependencies:
* [Python](https://www.python.org/doc/) - 3.10.5
* [OpenCV](https://docs.opencv.org/4.6.0/) - 4.6.0
* [Numpy](https://numpy.org/doc/stable/) - 1.22.4
* [Streamlit](https://docs.streamlit.io/library/get-started) - 1.10.0 (Only required to run the streamlit app version)

## How to use:
Once all dependencies have been installed, not before having placed the original image inside the */visuals* folder, run the program contained in the 'src' folder with:

```console
    $ python ImageFilter.py
```

After that, a new window will pop up showing the result of applying each filter available. Just choose which one you'd like to save and close the window.

![alt text](https://github.com/Josgonmar/Simple-image-filters/blob/master/docs/interface.jpg?raw=true)

*Note that the selected images are remarked with a red rectangle. Select or deselect using the mouse click.*

Inside the */visuals* folder you'll find several demo images to try the code.

### Streamlit:
To run the Streamlit app locally, just go to the folder where `ImageFilterApp.py` is contained and type:

```console
    $ streamlit run ImageFilterApp.py
```
A new window will be opened in your favourite web browser where you can perform the exact same thing as in the python program, but in a much more user-friendly way!

## License:
Feel free to use this program whatever you like!
