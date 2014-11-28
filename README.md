Visualize Daily Arbtt Statistics
================================

Daily usage statistics straight from my laptop. Stolen a few things from [@karpathy's](https://github.com/karpathy/) [ulogme](https://github.com/karpathy/ulogme). Only I am not that comfortable sharing my entire usage history like him. Might be possible to do so for a work computer, certainly not for a personal laptop.

I like [arbtt](http://arbtt.nomeata.de/#what). The logs are a little safer and it's easy to find usage stats using `arbtt-stats`. But an ascii table is not as visually striking as a colored donut chart.

There a few issues remaining that need to be resolved, otherwise this works fine. I guess the code can be simplified.  Any pull requests is welcome of course.

**Requires yet unreleased `arbtt-stats` version 0.9. Since it now has `for-each=minute` for the barcode chart to work.**

How to use?
-----------

1. Install [`arbtt`](http://arbtt.nomeata.de/#install). Run `arbtt-capture` at startup.
2. Fork this project.
3. Clone the project to your machine.
4. Modify `categorize.cfg` as per your need.
4. `make` should do I guess. Please let me know if you have any problems.

TODO
----

- Handle categories maybe?
- Find why some are greater than 100. (For now we've hacked around it.)
