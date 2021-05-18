# Zeitkippen
This implements the procedure "Zeitkippen" on videos as described by Werner Grosse in his [2006 paper](https://core.ac.uk/download/pdf/14510663.pdf).

* [Basketball](https://zeitkippen.qvwx.de/index.html?q=_Basketball)
* [Abstract](https://zeitkippen.qvwx.de/index.html?q=_Abstract)

Zeitkippen explores the notion of looking at video as a 3D dataset with two spatial and one temporal coordinates and then asking the question: How would this look if viewed along a different axis.

Jan-Eric Harting implemented this in C++ and produced videos accompanying the paper. The film can be watched here:

https://av.tib.eu/media/21945

I have taken the basic idea, implemented it in Python and created a visualization that emphasizes the 3D aspect of it by displaying the frames in a 3D scene in the browser and allowing the user to view it from all sides.

DONE:

* Basic Zeitkippen around two axes by 90. Effectively swapping the temporal coordinate for one of the spatial ones.
* Visualization of the result in a webbrower in 3D.

TODO:

* Uploading and processing of user-submitted videos.
* Produce views along arbitrary non-orthogonal directions.
